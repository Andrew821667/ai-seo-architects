# 🚀 AI SEO Architects - Deployment Guide

Полное руководство по развертыванию AI SEO Architects API с Dashboard, мониторингом и production инфраструктурой.

## 📋 Содержание

1. [Быстрый старт](#быстрый-старт)
2. [Development режим](#development-режим)  
3. [Production развертывание](#production-развертывание)
4. [Docker Compose](#docker-compose)
5. [Мониторинг и логирование](#мониторинг-и-логирование)
6. [Безопасность](#безопасность)
7. [Troubleshooting](#troubleshooting)

## 🚀 Быстрый старт

### Предварительные требования

```bash
# Системные требования
- Python 3.11+
- Docker & Docker Compose (опционально)
- 4GB RAM (минимум)
- 10GB свободного места

# Проверка версий
python --version    # >= 3.11
docker --version    # >= 20.10
docker-compose --version  # >= 2.0
```

### Установка зависимостей

```bash
# 1. Клонирование репозитория
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# 2. Создание виртуального окружения
python -m venv venv

# Активация (Linux/macOS)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Проверка установки
python -c "import fastapi, uvicorn; print('✅ FastAPI готов к работе')"
```

### Первый запуск

```bash
# Запуск API сервера
python run_api.py

# Проверка работоспособности
curl http://localhost:8000/health
```

**🎉 Готово! Переходите к интерфейсам:**
- 🎛️ **Dashboard**: http://localhost:8000/dashboard
- 📚 **API Docs**: http://localhost:8000/api/docs  
- 🔍 **Health Check**: http://localhost:8000/health

## 🛠️ Development режим

### Конфигурация для разработки

```bash
# .env файл для development
cat > .env << EOF
ENVIRONMENT=development
API_PORT=8000
LOG_LEVEL=DEBUG

# MCP настройки
MCP_ENABLED=true
MCP_CACHE_TTL=5
MCP_ENABLE_FALLBACK=true

# Для разработки можно оставить пустыми
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
EOF
```

### Запуск с hot-reload

```bash
# Автоматическая перезагрузка при изменениях
python run_api.py

# Или напрямую через uvicorn
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Тестирование

```bash
# Интеграционные тесты агентов
python test_agents_integration.py

# MCP интеграционные тесты
python test_mcp_integration.py

# Comprehensive тесты
python comprehensive_agent_test.py

# Проверка API endpoints
curl -X GET "http://localhost:8000/api/agents/" \
  -H "accept: application/json"
```

### Development workflow

```bash
# 1. Внесите изменения в код
# 2. API автоматически перезагрузится
# 3. Проверьте в браузере: http://localhost:8000/dashboard
# 4. Запустите тесты
python test_mcp_integration.py
```

## 🏭 Production развертывание

### Подготовка production окружения

```bash
# 1. Обновление системы
sudo apt update && sudo apt upgrade -y

# 2. Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Проверка
docker version
docker-compose version
```

### Production конфигурация

```bash
# .env.production файл
cat > .env.production << EOF
ENVIRONMENT=production
API_PORT=8000

# Безопасность
SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -hex 16)
GRAFANA_PASSWORD=$(openssl rand -hex 12)

# MCP настройки для production
MCP_ENABLED=true
MCP_CACHE_TTL=30
MCP_MAX_CONCURRENT=20
MCP_TIMEOUT=60

# API ключи (добавьте свои)
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# Мониторинг
PROMETHEUS_RETENTION=15d
GRAFANA_ALLOW_SIGN_UP=false

# SSL (если используете)
SSL_CERT_PATH=/etc/ssl/certs/ai-seo-architects.crt
SSL_KEY_PATH=/etc/ssl/private/ai-seo-architects.key
EOF
```

### Настройка SSL сертификатов

```bash
# Создание самоподписанного сертификата (для тестирования)
sudo mkdir -p /etc/ssl/certs /etc/ssl/private

sudo openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -subj "/C=RU/ST=Moscow/L=Moscow/O=AI SEO Architects/OU=IT/CN=localhost" \
  -keyout /etc/ssl/private/ai-seo-architects.key \
  -out /etc/ssl/certs/ai-seo-architects.crt

# Для production используйте Let's Encrypt
# sudo certbot certonly --standalone -d your-domain.com
```

## 🐳 Docker Compose

### Полное развертывание инфраструктуры

```bash
# 1. Загрузка переменных окружения
cp .env.production .env

# 2. Сборка и запуск всех сервисов
docker-compose up -d

# 3. Проверка статуса
docker-compose ps

# 4. Просмотр логов
docker-compose logs -f ai-seo-api
```

### Структура сервисов

```yaml
Сервисы в docker-compose.yml:

📊 ai-seo-api (порт 8000)     # Основной API сервер
🗄️  postgres (порт 5432)      # База данных
🔄 redis (порт 6379)          # Кэширование
🌐 nginx (порт 80/443)        # Reverse proxy
📈 prometheus (порт 9090)     # Метрики  
📊 grafana (порт 3000)        # Дашборды
🧠 chroma (порт 8001)         # Vector DB
```

### Управление сервисами

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose stop

# Перезапуск конкретного сервиса
docker-compose restart ai-seo-api

# Обновление образов
docker-compose pull
docker-compose up -d

# Очистка
docker-compose down -v  # Удаляет volumes!
```

### Масштабирование API

```bash
# Запуск нескольких экземпляров API
docker-compose up -d --scale ai-seo-api=3

# Nginx автоматически настроит load balancing
```

## 📊 Мониторинг и логирование

### Grafana дашборды

1. Откройте http://localhost:3000
2. Войдите (admin / пароль из .env)
3. Импортируйте готовые дашборды:
   - AI SEO Architects System Metrics
   - Agent Performance Metrics  
   - Business Intelligence Dashboard

### Prometheus метрики

Доступ к метрикам: http://localhost:9090

**Основные метрики:**
```promql
# CPU usage
ai_seo_cpu_percent

# Memory usage  
ai_seo_memory_percent

# HTTP requests
ai_seo_http_requests_total

# Agent performance
ai_seo_agent_success_rate
ai_seo_agent_processing_time
```

### Логирование

```bash
# Просмотр логов API
docker-compose logs -f ai-seo-api

# Логи конкретного агента
docker-compose exec ai-seo-api tail -f /app/logs/api.log | jq

# Поиск ошибок за последний час
docker-compose exec ai-seo-api grep "ERROR" /app/logs/errors.log | tail -20
```

### Structured logging запросы

```bash
# Фильтр по correlation_id
docker-compose exec ai-seo-api grep "req_12345" /app/logs/api.log | jq

# Медленные запросы (>5s)
docker-compose exec ai-seo-api grep '"processing_time_seconds"' /app/logs/api.log | jq 'select(.processing_time_seconds > 5)'

# Агенты с низким success rate
docker-compose exec ai-seo-api grep '"success_rate"' /app/logs/api.log | jq 'select(.success_rate < 0.8)'
```

## 🔒 Безопасность

### Базовая безопасность

```bash
# 1. Обновление паролей по умолчанию
# Измените все пароли в .env файле

# 2. Настройка брандмауэра
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS  
sudo ufw deny 8000/tcp    # API только через nginx
sudo ufw enable

# 3. Настройка fail2ban для SSH
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

### JWT токены

```bash
# Генерация secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Добавьте в .env:
# JWT_SECRET_KEY=your_generated_secret_key
```

### HTTPS настройка

```bash
# nginx/ssl.conf
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/ai-seo-architects.crt;
    ssl_certificate_key /etc/ssl/private/ai-seo-architects.key;
    
    # Современная SSL конфигурация
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    location / {
        proxy_pass http://ai-seo-api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔧 Troubleshooting

### Частые проблемы

#### 1. API не запускается

```bash
# Проверка логов
docker-compose logs ai-seo-api

# Проверка портов
netstat -tlnp | grep 8000

# Проверка зависимостей
pip check

# Проверка Python версии
python --version  # Должна быть 3.11+
```

#### 2. Агенты не инициализируются

```bash
# Проверка MCP статуса
curl http://localhost:8000/api/agents/health/all

# Проверка логов агентов
docker-compose logs ai-seo-api | grep "agent"

# Ручное тестирование MCP
python test_mcp_integration.py
```

#### 3. WebSocket подключение не работает

```bash
# Проверка WebSocket endpoint
curl --include \
     --no-buffer \
     --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     --header "Sec-WebSocket-Version: 13" \
     http://localhost:8000/ws/dashboard

# Проверка в браузере
# F12 -> Console:
# new WebSocket('ws://localhost:8000/ws/dashboard')
```

#### 4. База данных недоступна

```bash
# Проверка статуса PostgreSQL
docker-compose exec postgres pg_isready -U ai_seo_user

# Подключение к базе
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects

# Проверка таблиц
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "\dt"
```

#### 5. Высокое потребление памяти

```bash
# Мониторинг ресурсов
docker stats

# Ограничение памяти в docker-compose.yml
services:
  ai-seo-api:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Диагностика производительности

```bash
# 1. Проверка системных метрик
curl http://localhost:8000/api/analytics/system

# 2. Производительность агентов
curl http://localhost:8000/api/analytics/agents

# 3. HTTP метрики
curl http://localhost:8000/health | jq '.metrics'

# 4. Профилирование медленных запросов
docker-compose logs ai-seo-api | grep "processing_time_seconds" | jq 'select(.processing_time_seconds > 5)'
```

### Восстановление после сбоя

```bash
# 1. Остановка всех сервисов
docker-compose down

# 2. Проверка целостности данных
docker volume ls | grep ai-seo
docker volume inspect ai-seo_postgres_data

# 3. Backup базы данных (если нужно)
docker-compose exec postgres pg_dump -U ai_seo_user ai_seo_architects > backup.sql

# 4. Полный перезапуск
docker-compose up -d

# 5. Проверка здоровья всех сервисов
docker-compose ps
curl http://localhost:8000/health
```

## 📋 Checklist для production

### Перед развертыванием

- [ ] Все пароли изменены с дефолтных
- [ ] SSL сертификаты настроены
- [ ] Firewall настроен (только необходимые порты)
- [ ] Backup стратегия определена
- [ ] Monitoring dashboard настроен
- [ ] API ключи для MCP добавлены
- [ ] Логирование настроено
- [ ] Health checks работают

### После развертывания

- [ ] Smoke tests пройдены
- [ ] Dashboard доступен и показывает данные
- [ ] Все 14 агентов активны
- [ ] WebSocket подключение работает
- [ ] Metrics собираются в Prometheus
- [ ] SSL сертификат валиден
- [ ] Backup процедура протестирована

### Еженедельное обслуживание

- [ ] Проверка логов на ошибки
- [ ] Обновление зависимостей
- [ ] Ротация логов
- [ ] Проверка размера базы данных
- [ ] Мониторинг производительности

## 📞 Поддержка

### Каналы поддержки

- 🐛 **GitHub Issues**: https://github.com/Andrew821667/ai-seo-architects/issues
- 📧 **Email**: a.popov.gv@gmail.com  
- 📚 **Документация**: API_DOCUMENTATION.md

### При создании issue указывайте:

1. Версию AI SEO Architects
2. Операционную систему
3. Версию Docker/Python
4. Логи ошибок
5. Шаги воспроизведения

### Сбор диагностической информации

```bash
# Скрипт для сбора информации о системе
cat > collect_diagnostics.sh << 'EOF'
#!/bin/bash
echo "=== AI SEO Architects Diagnostics ==="
echo "Date: $(date)"
echo "OS: $(uname -a)"
echo "Docker: $(docker --version)"
echo "Docker Compose: $(docker-compose --version)"
echo "Python: $(python --version)"

echo -e "\n=== Service Status ==="
docker-compose ps

echo -e "\n=== Resource Usage ==="
docker stats --no-stream

echo -e "\n=== Recent Logs (last 50 lines) ==="
docker-compose logs --tail=50 ai-seo-api

echo -e "\n=== Health Check ==="
curl -s http://localhost:8000/health | jq .
EOF

chmod +x collect_diagnostics.sh
./collect_diagnostics.sh > diagnostics.txt
```

---

**🚀 Готово! AI SEO Architects развернут и готов к работе**

**Автор**: Andrew Popov (a.popov.gv@gmail.com)  
**Версия**: 1.0.0  
**Последнее обновление**: 2025-08-06