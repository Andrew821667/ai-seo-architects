# 🚀 VDS/VPS Deployment Guide - AI SEO Architects

> **Полное руководство по развертыванию AI SEO Architects на VDS/VPS**  
> Ubuntu 20.04+ / CentOS 8+ / Debian 11+ совместимость

## 📋 Системные требования

### **Минимальные требования:**
- **CPU:** 2 cores (4 рекомендуется)
- **RAM:** 4GB (8GB рекомендуется)
- **Storage:** 20GB SSD (50GB+ рекомендуется)
- **Network:** 100 Mbps
- **OS:** Ubuntu 20.04+, CentOS 8+, Debian 11+

### **Рекомендуемые требования:**
- **CPU:** 4+ cores
- **RAM:** 8GB+
- **Storage:** 50GB+ SSD
- **Network:** 1 Gbps
- **Firewall:** Настроен (порты 80, 443, 22)

## 🔧 Подготовка сервера

### **1. Обновление системы**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git htop nginx certbot

# CentOS/RHEL
sudo yum update -y
sudo yum install -y curl wget git htop nginx certbot
```

### **2. Установка Docker и Docker Compose**
```bash
# Установка Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker --version
docker-compose --version
```

### **3. Создание пользователя приложения**
```bash
sudo useradd -m -s /bin/bash aiseo
sudo usermod -aG docker aiseo
sudo mkdir -p /opt/ai-seo-architects
sudo chown -R aiseo:aiseo /opt/ai-seo-architects
```

## 📦 Развертывание приложения

### **1. Клонирование репозитория**
```bash
cd /opt/ai-seo-architects
git clone https://github.com/Andrew821667/ai-seo-architects.git .
```

### **2. Настройка переменных окружения**
```bash
# Копируем example конфиг
cp .env .env.production

# Редактируем production конфиг
nano .env.production
```

**Важные переменные для production:**
```bash
# Production режим
ENVIRONMENT=production

# Безопасные пароли (ОБЯЗАТЕЛЬНО ИЗМЕНИТЬ!)
POSTGRES_PASSWORD=your_secure_database_password_here
JWT_SECRET_KEY=your_super_secure_jwt_secret_key_here
GRAFANA_PASSWORD=your_grafana_admin_password

# Ваш OpenAI API ключ
OPENAI_API_KEY=sk-...

# SQL отладка (отключить в production)
SQL_ECHO=false
LOG_LEVEL=WARNING
```

### **3. Настройка SSL сертификата (Let's Encrypt)**
```bash
# Замените your-domain.com на ваш домен
sudo certbot certonly --nginx -d your-domain.com

# Сертификаты сохранятся в:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem
```

### **4. Обновление Nginx конфигурации**
```bash
# Редактируем nginx.conf
nano nginx/nginx.conf
```

**Раскомментируйте HTTPS секцию и обновите:**
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;  # ВАШ ДОМЕН
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    # ... остальные настройки
}

# HTTP -> HTTPS редирект
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### **5. Обновление Docker Compose для production**
```bash
nano docker-compose.yml
```

**Добавьте SSL volume bindings:**
```yaml
nginx:
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - /etc/letsencrypt:/etc/letsencrypt:ro  # SSL сертификаты
    - ./logs/nginx:/var/log/nginx
```

## 🚀 Запуск системы

### **1. Первый запуск с инициализацией**
```bash
# Переключаемся на пользователя приложения
sudo su - aiseo
cd /opt/ai-seo-architects

# Устанавливаем переменные окружения для production
export $(cat .env.production | xargs)

# Запуск полной инфраструктуры
docker-compose up -d

# Проверяем логи запуска
docker-compose logs -f ai-seo-api
```

### **2. Проверка работоспособности**
```bash
# Проверяем все контейнеры
docker-compose ps

# Тестируем инфраструктуру
python test_docker_infrastructure.py

# Проверяем доступность сервисов:
curl -I https://your-domain.com/health
curl -I https://your-domain.com/api/docs
curl -I https://your-domain.com/dashboard
```

### **3. Ожидаемые сервисы:**
- **AI SEO API:** https://your-domain.com
- **Dashboard:** https://your-domain.com/dashboard
- **API Docs:** https://your-domain.com/api/docs
- **Grafana:** https://your-domain.com:3000 (admin/ваш_пароль)
- **Prometheus:** https://your-domain.com:9090

## 🔒 Настройка безопасности

### **1. Firewall (UFW)**
```bash
sudo ufw enable
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS
sudo ufw allow 3000/tcp   # Grafana
sudo ufw allow 9090/tcp   # Prometheus
sudo ufw status
```

### **2. Автоматическое обновление SSL**
```bash
# Добавляем в crontab
sudo crontab -e

# Добавить строку:
0 12 * * * /usr/bin/certbot renew --quiet --reload-hook "docker-compose -f /opt/ai-seo-architects/docker-compose.yml restart nginx"
```

### **3. Регулярные бэкапы**
```bash
# Создаем скрипт бэкапа
sudo nano /opt/ai-seo-architects/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/ai-seo-$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Бэкап PostgreSQL
docker-compose exec postgres pg_dump -U ai_seo_user ai_seo_architects > $BACKUP_DIR/database.sql

# Бэкап конфигураций
tar -czf $BACKUP_DIR/configs.tar.gz .env.production nginx/ monitoring/

# Бэкап знаний агентов
tar -czf $BACKUP_DIR/knowledge.tar.gz knowledge/ data/vector_stores/

# Очистка старых бэкапов (старше 30 дней)
find /opt/backups -name "ai-seo-*" -mtime +30 -exec rm -rf {} \;
```

```bash
chmod +x /opt/ai-seo-architects/backup.sh

# Добавляем в crontab (каждый день в 2:00)
0 2 * * * /opt/ai-seo-architects/backup.sh
```

## 📊 Мониторинг и логи

### **1. Просмотр логов**
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f ai-seo-api
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f nginx
```

### **2. Мониторинг ресурсов**
```bash
# Использование ресурсов контейнерами
docker stats

# Общие системные ресурсы
htop
df -h
free -h
```

### **3. Health checks**
```bash
# Комплексная проверка
python test_docker_infrastructure.py

# Быстрая проверка API
curl -s https://your-domain.com/health | jq .

# Проверка базы данных
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "SELECT COUNT(*) FROM ai_seo.agents;"
```

## 🔧 Обновление системы

### **1. Обновление кода**
```bash
cd /opt/ai-seo-architects

# Бэкап перед обновлением
./backup.sh

# Получаем последние изменения
git pull origin main

# Перезапуск сервисов
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Проверяем после обновления
python test_docker_infrastructure.py
```

### **2. Обновление конфигураций**
```bash
# При изменении Nginx конфига
docker-compose restart nginx

# При изменении переменных окружения
docker-compose down
docker-compose up -d

# Проверка применения изменений
docker-compose logs -f ai-seo-api
```

## 🚨 Устранение проблем

### **Частые проблемы:**

#### **1. Контейнер не запускается**
```bash
# Проверяем логи
docker-compose logs ai-seo-api

# Проверяем переменные окружения
docker-compose exec ai-seo-api env | grep POSTGRES

# Перезапуск с пересборкой
docker-compose down
docker-compose build --no-cache ai-seo-api
docker-compose up -d
```

#### **2. База данных недоступна**
```bash
# Проверяем статус PostgreSQL
docker-compose exec postgres pg_isready -U ai_seo_user

# Проверяем подключение
docker-compose exec ai-seo-api python -c "
import asyncio
from api.database.connection import db_manager
async def test():
    await db_manager.initialize()
    print('DB OK:', await db_manager.health_check())
asyncio.run(test())
"
```

#### **3. SSL сертификат не работает**
```bash
# Проверяем сертификат
sudo certbot certificates

# Обновляем сертификат
sudo certbot renew --force-renewal

# Перезапуск Nginx
docker-compose restart nginx
```

#### **4. Высокое использование ресурсов**
```bash
# Анализ использования
docker stats
htop

# Оптимизация PostgreSQL connection pool
# В .env.production:
# POSTGRES_POOL_SIZE=10
# POSTGRES_MAX_OVERFLOW=20

# Перезапуск с новыми настройками
docker-compose down && docker-compose up -d
```

## 📈 Производительность

### **Оптимизация для production:**

#### **1. PostgreSQL**
```sql
-- Подключаемся к базе данных
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects

-- Оптимизация настроек
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET work_mem = '4MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;

-- Перезапуск для применения настроек
```

#### **2. Redis**
```bash
# Настройка Redis в docker-compose.yml
redis:
  command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
```

#### **3. Nginx кэширование**
```nginx
# В nginx.conf добавить:
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m inactive=60m;

# В location блоки:
proxy_cache api_cache;
proxy_cache_valid 200 5m;
proxy_cache_key $scheme$proxy_host$uri$is_args$args;
```

## ✅ Чеклист готовности к production

### **Безопасность:**
- [ ] SSL сертификат настроен и работает
- [ ] Firewall настроен правильно
- [ ] Пароли базы данных изменены
- [ ] JWT secret key уникальный
- [ ] Логи не содержат sensitive данные

### **Производительность:**
- [ ] Connection pooling настроен
- [ ] Nginx кэширование включено
- [ ] Database индексы созданы
- [ ] Мониторинг настроен

### **Надежность:**
- [ ] Автоматические бэкапы работают
- [ ] Health checks проходят
- [ ] Логирование настроено
- [ ] Автоперезапуск контейнеров включен

### **Мониторинг:**
- [ ] Grafana дашборды настроены
- [ ] Prometheus метрики собираются
- [ ] Алерты настроены
- [ ] Log rotation настроен

---

## 🚀 Quick Start для VDS

```bash
# 1. Подготовка сервера
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 2. Клонирование
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# 3. Настройка переменных
cp .env .env.production
nano .env.production  # Изменить пароли и ключи!

# 4. SSL сертификат
sudo certbot certonly --nginx -d your-domain.com

# 5. Запуск
docker-compose up -d

# 6. Проверка
python test_docker_infrastructure.py
```

**🎉 Система готова к работе!**

---

**Поддержка:** Если возникают проблемы, создайте issue в GitHub репозитории.