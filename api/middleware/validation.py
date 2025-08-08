"""
Input Validation middleware и утилиты для AI SEO Architects API
Расширенная валидация запросов с защитой от атак
"""

import json
import re
from typing import Dict, Any, List, Optional, Union
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError, validator
import bleach

from ..monitoring.logger import get_logger

logger = get_logger(__name__)


class ValidationConfig:
    """Конфигурация валидации"""
    
    # Максимальные размеры
    MAX_REQUEST_SIZE = 20 * 1024 * 1024  # 20MB
    MAX_JSON_DEPTH = 10
    MAX_ARRAY_LENGTH = 1000
    MAX_STRING_LENGTH = 10000
    
    # Разрешенные HTML теги для контента
    ALLOWED_HTML_TAGS = ['b', 'i', 'u', 'strong', 'em', 'p', 'br', 'ul', 'ol', 'li']
    
    # Паттерны для валидации
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    URL_PATTERN = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    PHONE_PATTERN = r'^\+?1?\d{9,15}$'
    
    # Опасные паттерны (потенциальные атаки)
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # XSS
        r'javascript:',  # JavaScript injection
        r'on\w+\s*=',  # HTML event handlers
        r'eval\s*\(',  # Code evaluation
        r'exec\s*\(',  # Code execution
        r'system\s*\(',  # System calls
        r'\$\{.*?\}',  # Template injection
        r'#{.*?}',  # Expression language injection
    ]


class RequestValidator:
    """Валидатор HTTP запросов"""
    
    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()
    
    async def validate_request(self, request: Request) -> Dict[str, Any]:
        """
        Полная валидация HTTP запроса
        
        Returns:
            Dict с результатами валидации
        """
        errors = []
        warnings = []
        
        # Проверка размера запроса
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.config.MAX_REQUEST_SIZE:
            errors.append(f"Request size {content_length} exceeds maximum {self.config.MAX_REQUEST_SIZE}")
        
        # Проверка Content-Type для POST/PUT запросов
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not content_type:
                warnings.append("Missing Content-Type header")
            elif "application/json" in content_type:
                try:
                    body = await request.body()
                    if body:
                        json_data = json.loads(body.decode())
                        json_errors = self._validate_json_structure(json_data)
                        errors.extend(json_errors)
                except json.JSONDecodeError as e:
                    errors.append(f"Invalid JSON: {str(e)}")
                except Exception as e:
                    errors.append(f"JSON processing error: {str(e)}")
        
        # Проверка заголовков на потенциальные атаки
        header_errors = self._validate_headers(request.headers)
        errors.extend(header_errors)
        
        # Проверка query parameters
        query_errors = self._validate_query_params(dict(request.query_params))
        errors.extend(query_errors)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _validate_json_structure(self, data: Any, depth: int = 0) -> List[str]:
        """Валидация структуры JSON"""
        errors = []
        
        if depth > self.config.MAX_JSON_DEPTH:
            errors.append(f"JSON nesting depth {depth} exceeds maximum {self.config.MAX_JSON_DEPTH}")
            return errors
        
        if isinstance(data, dict):
            for key, value in data.items():
                # Проверяем ключи
                if not isinstance(key, str):
                    errors.append(f"Non-string key found: {type(key)}")
                elif len(key) > 100:
                    errors.append(f"Key too long: {len(key)} characters")
                
                # Рекурсивная проверка значений
                errors.extend(self._validate_json_structure(value, depth + 1))
        
        elif isinstance(data, list):
            if len(data) > self.config.MAX_ARRAY_LENGTH:
                errors.append(f"Array length {len(data)} exceeds maximum {self.config.MAX_ARRAY_LENGTH}")
            
            for item in data:
                errors.extend(self._validate_json_structure(item, depth + 1))
        
        elif isinstance(data, str):
            if len(data) > self.config.MAX_STRING_LENGTH:
                errors.append(f"String length {len(data)} exceeds maximum {self.config.MAX_STRING_LENGTH}")
            
            # Проверка на опасные паттерны
            dangerous = self._check_dangerous_patterns(data)
            if dangerous:
                errors.append(f"Potentially dangerous content detected: {dangerous}")
        
        return errors
    
    def _validate_headers(self, headers: Dict[str, str]) -> List[str]:
        """Валидация HTTP заголовков"""
        errors = []
        
        for name, value in headers.items():
            # Проверка на потенциальные header injection атаки
            if '\n' in value or '\r' in value:
                errors.append(f"Header injection attempt in {name}")
            
            # Проверка User-Agent на подозрительные паттерны
            if name.lower() == "user-agent":
                if len(value) > 500:
                    errors.append("Suspiciously long User-Agent header")
                
                suspicious_agents = ['sqlmap', 'nikto', 'nmap', 'masscan']
                if any(agent in value.lower() for agent in suspicious_agents):
                    errors.append("Suspicious User-Agent detected")
        
        return errors
    
    def _validate_query_params(self, params: Dict[str, str]) -> List[str]:
        """Валидация query parameters"""
        errors = []
        
        for key, value in params.items():
            # Проверка на SQL injection паттерны
            sql_patterns = [
                r'\b(union|select|insert|update|delete|drop|create|alter)\b',
                r'(\"|\'|\`).*(or|and).*(\"|\'|\`)',
                r';\s*(select|insert|update|delete|drop)',
            ]
            
            for pattern in sql_patterns:
                if re.search(pattern, value.lower()):
                    errors.append(f"Potential SQL injection in parameter {key}")
                    break
            
            # Проверка на XSS
            dangerous = self._check_dangerous_patterns(value)
            if dangerous:
                errors.append(f"Potentially dangerous content in parameter {key}: {dangerous}")
        
        return errors
    
    def _check_dangerous_patterns(self, text: str) -> Optional[str]:
        """Проверка текста на опасные паттерны"""
        for pattern in self.config.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return pattern
        return None


class InputSanitizer:
    """Санитизация входных данных"""
    
    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()
    
    def sanitize_html(self, html_content: str) -> str:
        """Безопасная очистка HTML контента"""
        return bleach.clean(
            html_content,
            tags=self.config.ALLOWED_HTML_TAGS,
            strip=True
        )
    
    def sanitize_string(self, text: str, max_length: Optional[int] = None) -> str:
        """Общая санитизация строки"""
        if not isinstance(text, str):
            return str(text)
        
        # Удаляем опасные символы
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Ограничиваем длину
        if max_length:
            text = text[:max_length]
        elif len(text) > self.config.MAX_STRING_LENGTH:
            text = text[:self.config.MAX_STRING_LENGTH]
        
        return text.strip()
    
    def sanitize_email(self, email: str) -> str:
        """Валидация и санитизация email"""
        email = self.sanitize_string(email, 254)  # RFC 5321 limit
        
        if not re.match(self.config.EMAIL_PATTERN, email):
            raise ValueError(f"Invalid email format: {email}")
        
        return email.lower()
    
    def sanitize_url(self, url: str) -> str:
        """Валидация и санитизация URL"""
        url = self.sanitize_string(url, 2048)  # Common URL length limit
        
        if not re.match(self.config.URL_PATTERN, url):
            raise ValueError(f"Invalid URL format: {url}")
        
        return url
    
    def sanitize_phone(self, phone: str) -> str:
        """Валидация и санитизация номера телефона"""
        # Удаляем все кроме цифр, + и пробелов
        phone = re.sub(r'[^\d\+\s\-\(\)]', '', phone)
        phone = re.sub(r'\s+', '', phone)  # Убираем пробелы
        
        if not re.match(self.config.PHONE_PATTERN, phone):
            raise ValueError(f"Invalid phone format: {phone}")
        
        return phone


class ValidationMiddleware:
    """FastAPI middleware для валидации входящих запросов"""
    
    def __init__(self, app, strict_mode: bool = False):
        self.app = app
        self.strict_mode = strict_mode
        self.validator = RequestValidator()
        self.sanitizer = InputSanitizer()
        
        # Endpoints которые нужно пропускать без строгой валидации
        self.skip_validation = [
            "/health",
            "/metrics", 
            "/static/",
            "/api/docs",
            "/redoc"
        ]
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        # Пропускаем некоторые endpoints
        if any(request.url.path.startswith(skip) for skip in self.skip_validation):
            await self.app(scope, receive, send)
            return
        
        try:
            # Выполняем валидацию
            validation_result = await self.validator.validate_request(request)
            
            if not validation_result["valid"]:
                # Логируем ошибки валидации
                logger.warning(
                    f"Request validation failed for {request.method} {request.url.path}",
                    extra={
                        "errors": validation_result["errors"],
                        "client_ip": self._get_client_ip(request),
                        "user_agent": request.headers.get("user-agent", "")
                    }
                )
                
                if self.strict_mode:
                    # В строгом режиме блокируем запрос
                    response = JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                            "error": "Request validation failed",
                            "details": validation_result["errors"][:5],  # Показываем только первые 5 ошибок
                            "message": "Request contains invalid or potentially dangerous content"
                        }
                    )
                    await response(scope, receive, send)
                    return
                else:
                    # В мягком режиме только предупреждаем
                    logger.info("Continuing with warning due to non-strict mode")
            
            # Логируем предупреждения
            if validation_result["warnings"]:
                logger.info(
                    f"Request validation warnings for {request.method} {request.url.path}",
                    extra={"warnings": validation_result["warnings"]}
                )
            
        except Exception as e:
            logger.error(f"Validation middleware error: {e}")
            # В случае ошибки middleware, продолжаем без блокировки
        
        # Продолжаем обработку запроса
        await self.app(scope, receive, send)
    
    def _get_client_ip(self, request: Request) -> str:
        """Получение IP адреса клиента"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        if request.client:
            return request.client.host
        
        return "unknown"


# Pydantic модели для строгой валидации
class StrictEmailStr(str):
    """Строгая валидация email"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        sanitizer = InputSanitizer()
        try:
            return sanitizer.sanitize_email(v)
        except ValueError as e:
            raise ValidationError(str(e), cls)


class StrictUrlStr(str):
    """Строгая валидация URL"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        sanitizer = InputSanitizer()
        try:
            return sanitizer.sanitize_url(v)
        except ValueError as e:
            raise ValidationError(str(e), cls)


class SafeStr(str):
    """Безопасная строка без опасных символов"""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        sanitizer = InputSanitizer()
        return sanitizer.sanitize_string(v)


# Декораторы для endpoint валидации
def validate_json_size(max_size: int = 1024 * 1024):  # 1MB по умолчанию
    """Декоратор для валидации размера JSON"""
    def decorator(func):
        func._max_json_size = max_size
        return func
    return decorator


def sanitize_input(fields: List[str] = None):
    """Декоратор для автоматической санитизации полей"""
    def decorator(func):
        func._sanitize_fields = fields or []
        return func
    return decorator