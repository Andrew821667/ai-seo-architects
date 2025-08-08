# 🐳 Docker Deployment Guide - AI SEO Architects

Полное руководство по развертыванию AI SEO Architects в Docker на production сервере.

## 📋 Предварительные требования

### Системные требования:
- **RAM**: минимум 4GB, рекомендуется 8GB+
- **CPU**: минимум 2 cores, рекомендуется 4+ cores  
- **Диск**: минимум 20GB свободного места
- **OS**: Linux (Ubuntu 20.04+, CentOS 8+, Debian 11+)

### Установленное ПО:
- Docker 20.10+
- Docker Compose 2.0+
- Git

## 🚀 Быстрый запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects
```

### 2. Создание .env файла
```bash
cp .env.example .env
nano .env  # Отредактируйте переменные
```

### 3. Настройка environment variables
```env
# Обязательные переменные:
DATABASE_PASSWORD=ваш-супер-секретный-пароль
JWT_SECRET_KEY=ваш-jwt-ключ-минимум-32-символа
OPENAI_API_KEY=ваш-openai-api-ключ

# Опционально:
ANTHROPIC_API_KEY=ваш-anthropic-ключ-для-mcp
```

### 4. Запуск всего стека
```bash
docker-compose up -d
```

### 5. Проверка статуса
```bash
docker-compose ps
docker-compose logs -f ai-seo-api
```

## 🌐 Доступ к сервисам

После успешного запуска доступны:

- **🎛️ AI SEO API**: http://your-server:8000
- **📊 Dashboard**: http://your-server:8000/dashboard  
- **📚 API Docs**: http://your-server:8000/api/docs
- **❤️ Health Check**: http://your-server:8000/health
- **📈 Prometheus**: http://your-server:9090
- **📊 Grafana**: http://your-server:3000 (admin/admin)
- **🗄️ PostgreSQL**: your-server:5432
- **⚡ Redis**: your-server:6379

## 🔐 Первый запуск и настройка

### Аутентификация
По умолчанию создается admin пользователь:
- **Логин**: `admin`
- **Пароль**: `secret`

⚠️ **ВАЖНО**: Смените пароль после первого входа!

### Проверка здоровья системы
```bash
# Проверка API
curl http://your-server:8000/health

# Проверка агентов
curl http://your-server:8000/api/agents/health

# Проверка метрик
curl http://your-server:8000/metrics
```

## 📊 Мониторинг и метрики

### Prometheus метрики
Доступны на `/metrics`:
- Системные метрики (CPU, память, диск)
- HTTP метрики (запросы, ошибки, время отклика)
- Метрики агентов (задачи, успешность, производительность)

### Grafana дашборды
1. Откройте http://your-server:3000
2. Логин: `admin`, пароль: `admin`
3. Импортируйте готовые дашборды из `monitoring/grafana/dashboards/`

## 🛠️ Управление сервисами

### Основные команды
```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск конкретного сервиса
docker-compose restart ai-seo-api

# Просмотр логов
docker-compose logs -f ai-seo-api

# Масштабирование API (если нужно)
docker-compose up -d --scale ai-seo-api=3
```

### Обновление
```bash
# Получение обновлений
git pull origin main

# Пересборка и перезапуск
docker-compose build --no-cache
docker-compose down
docker-compose up -d
```

## 🔧 Конфигурация production

### SSL/HTTPS настройка
1. Получите SSL сертификаты (Let's Encrypt рекомендуется)
2. Поместите в `nginx/ssl/`
3. Обновите `nginx/nginx.conf`
4. Перезапустите Nginx:
```bash
docker-compose restart nginx
```

### Резервное копирование
```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U ai_seo_user ai_seo_architects > backup_$(date +%Y%m%d).sql

# Backup volumes
docker run --rm -v ai-seo-architects_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data_$(date +%Y%m%d).tar.gz /data
```

### Настройка firewall
```bash
# Откройте необходимые порты
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 8000  # API (если нужен прямой доступ)
ufw allow 9090  # Prometheus (для мониторинга)
ufw allow 3000  # Grafana (для визуализации)
```

## 🐛 Troubleshooting

### Проблемы с запуском

**База данных не подключается:**
```bash
# Проверьте логи PostgreSQL
docker-compose logs postgres

# Проверьте переменные окружения
docker-compose config
```

**API не стартует:**
```bash
# Проверьте логи API
docker-compose logs ai-seo-api

# Проверьте зависимости
docker-compose exec ai-seo-api pip list
```

**Нет места на диске:**
```bash
# Очистка неиспользуемых образов
docker system prune -a

# Очистка volumes (ОСТОРОЖНО!)
docker volume prune
```

### Проблемы с производительностью

**Высокое потребление памяти:**
```bash
# Проверьте потребление ресурсов
docker stats

# Настройте лимиты в docker-compose.yml
services:
  ai-seo-api:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

**Медленные запросы:**
```bash
# Проверьте метрики
curl http://your-server:8000/api/metrics/detailed

# Мониторинг в реальном времени
docker-compose logs -f ai-seo-api | grep "duration"
```

## 🔄 Обновления и миграции

### Обновление версии
```bash
# Сохраните данные
docker-compose exec postgres pg_dump -U ai_seo_user ai_seo_architects > backup_before_update.sql

# Получите обновления
git pull origin main

# Остановите сервисы
docker-compose down

# Обновите образы
docker-compose pull
docker-compose build --no-cache

# Запустите обновленную версию
docker-compose up -d

# Проверьте health check
curl http://your-server:8000/health
```

### Миграция базы данных
```bash
# Запустите миграции (если есть)
docker-compose exec ai-seo-api alembic upgrade head
```

## 📞 Поддержка

При возникновении проблем:

1. **Проверьте логи**: `docker-compose logs -f`
2. **Health check**: `curl http://your-server:8000/health`
3. **Создайте issue**: https://github.com/Andrew821667/ai-seo-architects/issues

### Полезные команды для диагностики
```bash
# Статус всех сервисов
docker-compose ps

# Использование ресурсов
docker stats

# Сетевая конфигурация
docker network ls
docker network inspect ai-seo-network

# Информация о volumes
docker volume ls
docker volume inspect ai-seo-architects_postgres_data
```

---

## ✅ Чеклист готовности к production

- [ ] ✅ Настроены все environment variables
- [ ] ✅ Изменены дефолтные пароли
- [ ] ✅ Настроен SSL/HTTPS
- [ ] ✅ Настроен firewall
- [ ] ✅ Настроено резервное копирование
- [ ] ✅ Протестирован health check
- [ ] ✅ Настроен мониторинг (Prometheus/Grafana)
- [ ] ✅ Проверена производительность под нагрузкой

**🎉 Готово к production! Система полностью функциональна.**