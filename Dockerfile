# AI SEO Architects API Server Dockerfile
FROM python:3.11-slim

# Метаданные
LABEL maintainer="Andrew Popov <a.popov.gv@gmail.com>"
LABEL version="1.0.0"
LABEL description="AI SEO Architects - Enterprise-ready мультиагентная система для автоматизации SEO-агентства"

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    API_PORT=8000

# Создаем пользователя для безопасности
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Обновляем систему и устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем необходимые директории
RUN mkdir -p logs exports && \
    chown -R appuser:appuser /app

# Переключаемся на непривилегированного пользователя
USER appuser

# Указываем порт
EXPOSE $API_PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$API_PORT/health || exit 1

# Команда запуска
CMD ["python", "run_api.py"]