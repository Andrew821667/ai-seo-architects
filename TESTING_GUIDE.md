# 🧪 Полное руководство по тестированию AI SEO Architects

> **Комплексная инструкция для демонстрации всех возможностей проекта**  
> Включает Real-time Dashboard, API endpoints, агенты и production infrastructure

## 📋 Оглавление

1. [🚀 Быстрый старт](#-быстрый-старт)
2. [🎛️ Real-time Dashboard](#️-real-time-dashboard)
3. [🔌 API Endpoints тестирование](#-api-endpoints-тестирование)
4. [🤖 Тестирование агентов](#-тестирование-агентов)
5. [🐳 Production infrastructure](#-production-infrastructure)
6. [🔧 Troubleshooting](#-troubleshooting)

---

## 🚀 Быстрый старт

### Системные требования
- **Python 3.11+** 
- **4GB RAM** (минимум)
- **Интернет соединение** (для AI моделей)
- **Docker** (опционально для production тестирования)

### Подготовка окружения
```bash
# 1. Клонируем репозиторий (если еще не сделано)
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# 2. Устанавливаем зависимости
pip install -r requirements.txt

# 3. Проверяем что все установлено
python -c "import fastapi, uvicorn, websockets; print('✅ Все зависимости установлены')"
```

### Запуск API сервера
```bash
# Основной способ - через run_api.py
python run_api.py

# Ожидаемый вывод:
# 🚀 Запуск AI SEO Architects API Server...
# ✅ MCP Agent Manager инициализирован
# ✅ Создано 14 агентов для API
# ✅ Система метрик запущена
# 🎉 API Server готов к работе!
# INFO: Uvicorn running on http://0.0.0.0:8000
```

**🎯 Основные URL после запуска:**
- 🎛️ **Dashboard:** http://localhost:8000/dashboard
- 📚 **API Docs:** http://localhost:8000/api/docs
- 🔍 **Health Check:** http://localhost:8000/health
- 🔌 **WebSocket:** ws://localhost:8000/ws/dashboard

---

## 🎛️ Real-time Dashboard

> **Главная фишка проекта - живой мониторинг всех 14 агентов в реальном времени!**

### Пошаговое тестирование Dashboard

#### Шаг 1: Откройте Dashboard
```bash
# После запуска API сервера откройте в браузере:
http://localhost:8000/dashboard
```

**🎯 Что вы должны увидеть:**
- ✅ Заголовок "AI SEO Architects - Real-time Dashboard"
- ✅ System Health секцию с live метриками CPU/Memory
- ✅ Agents Status grid с 14 агентами
- ✅ Performance charts (пустые пока, будут заполняться)
- ✅ Activity Feed с начальными событиями

#### Шаг 2: Проверьте WebSocket соединение
**Индикаторы работы WebSocket:**
- 🟢 **Connection Status: Connected** в правом верхнем углу
- 🔄 **Live updates** метрик каждые 5 секунд
- 📊 **Charts updating** в реальном времени

**Если WebSocket не работает:**
```bash
# Проверьте в браузерной консоли (F12):
# Должны быть сообщения типа:
# WebSocket connection established
# Received metrics update
```

#### Шаг 3: Изучите секции Dashboard

##### 🖥️ System Health
```
✅ Status: Healthy
📊 CPU Usage: ~15-25% (во время работы)
💾 Memory Usage: ~30-40%  
⚡ Uptime: увеличивается каждую секунду
```

##### 🤖 Agents Status (14 агентов)
```
Executive Level (2/2):
├─ Chief SEO Strategist: 🟢 Active
└─ Business Development Director: 🟢 Active

Management Level (4/4):
├─ Task Coordinator: 🟢 Active
├─ Sales Operations Manager: 🟢 Active
├─ Technical SEO Operations Manager: 🟢 Active
└─ Client Success Manager: 🟢 Active

Operational Level (8/8):
├─ Lead Qualification: 🟢 Active
├─ Sales Conversation: 🟢 Active
├─ Proposal Generation: 🟢 Active
├─ Technical SEO Auditor: 🟢 Active
├─ Content Strategy: 🟢 Active
├─ Link Building: 🟢 Active
├─ Competitive Analysis: 🟢 Active
└─ Reporting: 🟢 Active
```

##### 📈 Performance Charts
- **Request Latency** - время ответа API
- **Agent Tasks** - количество выполненных задач
- **System Resources** - CPU/Memory trends

##### 📋 Activity Feed
Показывает real-time события:
```
[12:34:56] ✅ API Server started
[12:34:57] 🤖 14 agents initialized
[12:34:58] 📊 Metrics collection started
[12:35:00] 🔄 WebSocket client connected
```

#### Шаг 4: Генерируйте активность для мониторинга

**Откройте второй терминал** и выполните тестирование API:
```bash
# В новом терминале (оставьте API сервер работать):
python test_api_endpoints.py
```

**🎯 Наблюдайте на Dashboard:**
- 📈 **Charts updating** с новыми метриками
- 📋 **Activity Feed** показывает новые события
- 🤖 **Agent status** обновления
- 📊 **Performance metrics** изменения

---

## 🔌 API Endpoints тестирование

### Автоматическое тестирование
```bash
# Запустите полное API тестирование:
python test_api_endpoints.py
```

**🎯 Ожидаемые результаты:**
```
🧪 AI SEO Architects API Testing Suite
==================================================
Base URL: http://localhost:8000
Timestamp: 2025-08-06T15:30:00
==================================================

🔍 Тестирование health endpoint...
✅ Health check: healthy
   Версия: 1.0.0
   Uptime: 120s

🔐 Тестирование аутентификации...
✅ Авторизация успешна
   Token type: bearer
   Expires in: 3600s

🏗️ Тестирование создания агентов...
✅ Создано агентов: 14
   MCP enabled: true

🤖 Тестирование списка агентов...
✅ Получено агентов: 14
   Активные: 14
   MCP включен: 14

⚡ Тестирование выполнения задачи агентом...
✅ Задача выполнена: success
   Processing time: 2.34s
   Task ID: task_1725634200
   Lead Score: 85/100

📊 Тестирование данных дашборда...
✅ Dashboard data получены:
   System: healthy
   CPU: 23.5%
   Memory: 42.1%
   Agents: 14/14
   Success rate: 100.0%

🔗 Тестирование WebSocket подключения...
✅ WebSocket подключение установлено
   Received: heartbeat_response
✅ WebSocket работает корректно

==================================================
🎉 Тестирование завершено!
💡 Откройте http://localhost:8000/dashboard для просмотра UI
📚 API Docs: http://localhost:8000/api/docs
```

### Ручное тестирование через API Documentation

#### Откройте Swagger UI:
```bash
http://localhost:8000/api/docs
```

#### Пошаговое тестирование:

##### 1. **Authentication** (обязательно первым):
```json
POST /auth/login
{
  "username": "admin",
  "password": "secret"
}
```
**Скопируйте** `access_token` из ответа.

##### 2. **Авторизуйтесь в Swagger:**
- Нажмите кнопку 🔒 **"Authorize"** вверху справа
- Введите: `Bearer YOUR_ACCESS_TOKEN`
- Нажмите **"Authorize"**

##### 3. **Создайте агентов:**
```json
POST /api/agents/create-all
```

##### 4. **Проверьте список агентов:**
```json
GET /api/agents/
```

##### 5. **Выполните задачу агентом:**
```json
POST /api/agents/lead_qualification/tasks
{
  "task_type": "lead_analysis",
  "input_data": {
    "company_data": {
      "company_name": "Test Company",
      "industry": "technology",
      "annual_revenue": "5000000",
      "employee_count": "50"
    }
  },
  "priority": "high"
}
```

##### 6. **Проверьте метрики дашборда:**
```json
GET /api/analytics/dashboard
```

---

## 🤖 Тестирование агентов

### Классические тесты агентов

#### MCP интеграционные тесты (рекомендуемое):
```bash
python test_mcp_integration.py
```

**🎯 Ожидаемые результаты:**
```
🚀 AI SEO Architects - MCP Integration Testing
==============================================

🔗 Инициализация MCP Agent Manager...
✅ MCP Agent Manager создан успешно

🏗️ Создание всех агентов с MCP поддержкой...
✅ 14/14 агентов созданы успешно с MCP интеграцией

🧪 Тестирование каждого агента...

📋 Executive Level:
✅ Chief SEO Strategist: Foundational analysis (Качество: 95/100)
✅ Business Development Director: Strategic assessment (Качество: 92/100)

📋 Management Level:
✅ Task Coordinator: Comprehensive routing (Качество: 88/100)
✅ Sales Operations Manager: Pipeline optimization (Качество: 89/100)
✅ Technical SEO Operations Manager: Advanced monitoring (Качество: 91/100)  
✅ Client Success Manager: Proactive management (Качество: 87/100)

📋 Operational Level:
✅ Lead Qualification: Hot Lead (Score: 90/100)
✅ Sales Conversation: Advanced objection handling (Качество: 93/100)
✅ Proposal Generation: ROI-focused proposal (Value: 2.8M ₽)
✅ Technical SEO Auditor: Comprehensive audit (Score: 68/100)
✅ Content Strategy: E-E-A-T optimization (Keywords: 850+)
✅ Link Building: Quality link acquisition (DA: 45+)
✅ Competitive Analysis: Deep SERP insights (Gaps: 12)
✅ Reporting: Automated insights (KPIs: 25+)

📊 Сводка результатов:
✅ Общий success rate: 100.0%
✅ Среднее качество: 90.2/100
✅ MCP интеграция: 100% работоспособность
✅ Время выполнения: 45.6s

🎉 Все агенты работают корректно с MCP!
```

#### Классические тесты:
```bash
# Базовое тестирование
python test_agents_integration.py

# Максимально подробное тестирование
python comprehensive_agent_test.py
```

### Индивидуальное тестирование агентов через API

**Примеры разных типов задач для разных агентов:**

#### Lead Qualification Agent:
```bash
curl -X POST "http://localhost:8000/api/agents/lead_qualification/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "lead_analysis",
    "input_data": {
      "company_data": {
        "company_name": "TechCorp Inc",
        "industry": "fintech",
        "annual_revenue": "15000000",
        "employee_count": "120",
        "website": "techcorp.com"
      }
    }
  }'
```

#### Technical SEO Auditor:
```bash
curl -X POST "http://localhost:8000/api/agents/technical_seo_auditor/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "technical_audit",
    "input_data": {
      "domain": "example.com",
      "audit_depth": "comprehensive"
    }
  }'
```

#### Content Strategy Agent:
```bash
curl -X POST "http://localhost:8000/api/agents/content_strategy/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "content_analysis",
    "input_data": {
      "target_keywords": ["seo optimization", "content marketing"],
      "industry": "digital marketing",
      "competitors": ["competitor1.com", "competitor2.com"]
    }
  }'
```

---

## 🐳 Production Infrastructure

### Docker Compose тестирование

#### Запуск полной инфраструктуры:
```bash
# Остановите обычный API сервер (Ctrl+C)

# Запустите Docker Compose
docker-compose up -d

# Проверьте статус контейнеров
docker-compose ps
```

**🎯 Ожидаемые сервисы:**
```
Name                   Command                State           Ports
------------------------------------------------------------------------
seo_api                python api/main.py      Up              0.0.0.0:8000->8000/tcp
seo_postgres           docker-entrypoint.s...  Up              0.0.0.0:5432->5432/tcp
seo_redis              docker-entrypoint.s...  Up              0.0.0.0:6379->6379/tcp
seo_nginx              /docker-entrypoint....   Up              0.0.0.0:80->80/tcp
seo_prometheus         /bin/prometheus --c...   Up              0.0.0.0:9090->9090/tcp
seo_grafana            /run.sh                  Up              0.0.0.0:3000->3000/tcp
seo_chromadb           uvicorn chromadb.app... Up              0.0.0.0:8001->8000/tcp
```

#### Доступные интерфейсы:
```bash
# Основной API (через Nginx)
http://localhost/dashboard          # Dashboard через Nginx
http://localhost/api/docs          # API docs через Nginx

# Прямой доступ к сервисам
http://localhost:8000/dashboard    # Прямой доступ к API
http://localhost:3000              # Grafana (admin/admin)
http://localhost:9090              # Prometheus
http://localhost:8001              # ChromaDB
```

#### Тестирование через Docker:
```bash
# Тестируйте API через Nginx
curl http://localhost/health

# Или прямо к контейнеру API
curl http://localhost:8000/health

# Проверьте логи
docker-compose logs api
docker-compose logs nginx
```

### Monitoring тестирование

#### Grafana Dashboard:
1. Откройте http://localhost:3000
2. Логин: `admin` / Пароль: `admin`
3. Импортируйте dashboard для мониторинга API метрик

#### Prometheus Metrics:
1. Откройте http://localhost:9090
2. Посмотрите доступные метрики: `http_requests_total`, `system_cpu_percent`

---

## 🔧 Troubleshooting

### Частые проблемы и решения

#### 1. **Port уже используется**
```bash
# Ошибка: [Errno 48] Address already in use
# Решение:
lsof -i :8000
kill -9 PID

# Или используйте другой порт:
uvicorn api.main:app --host 0.0.0.0 --port 8001
```

#### 2. **WebSocket подключение не работает**
```bash
# Проверьте в браузерной консоли:
# F12 -> Network -> WS -> Messages

# Если нет WebSocket соединения:
pip install websockets
```

#### 3. **Агенты не создаются**
```bash
# Проверьте логи API сервера
# Должны быть сообщения о создании агентов

# Если ошибки с MCP:
pip install --upgrade openai langchain
```

#### 4. **Dashboard не загружается**
```bash
# Проверьте файл dashboard.html
ls -la api/static/dashboard.html

# Если файла нет - он должен быть создан автоматически
```

#### 5. **Docker Compose проблемы**
```bash
# Очистите Docker кэш
docker-compose down -v
docker system prune -f

# Пересоберите образы
docker-compose build --no-cache
docker-compose up -d
```

### Debug режим

#### Включение подробного логирования:
```bash
# Добавьте в .env файл:
echo "LOG_LEVEL=DEBUG" > .env
echo "MCP_DEBUG=true" >> .env

# Перезапустите API
python run_api.py
```

#### Проверка состояния системы:
```bash
# Проверьте все компоненты
python -c "
import asyncio
from core.mcp.agent_manager import get_mcp_agent_manager

async def check():
    manager = await get_mcp_agent_manager()
    health = await manager.health_check_all_agents()
    print('Health Status:', health['summary'])

asyncio.run(check())
"
```

---

## 📊 Ожидаемые результаты

### ✅ Успешное тестирование включает:

#### 🎛️ Dashboard:
- ✅ Загружается без ошибок
- ✅ WebSocket соединение активно
- ✅ 14 агентов показывают статус "Active"
- ✅ Live обновления метрик каждые 5 секунд
- ✅ Charts отображаются и обновляются

#### 🔌 API:
- ✅ Все endpoints отвечают (health, auth, agents, analytics)
- ✅ JWT authentication работает
- ✅ Агенты создаются и выполняют задачи
- ✅ WebSocket поддержка функционирует
- ✅ OpenAPI документация доступна

#### 🤖 Agents:
- ✅ 14/14 агентов инициализируются
- ✅ MCP интеграция работает
- ✅ Success rate 100%
- ✅ Realistic результаты задач
- ✅ Быстрое время отклика (<5s)

#### 🐳 Infrastructure:
- ✅ Docker Compose запускается
- ✅ Все сервисы healthy
- ✅ Nginx proxy работает
- ✅ Grafana/Prometheus доступны
- ✅ Database соединения активны

---

## 🎯 Демо-сценарий

### Полная демонстрация возможностей (15 минут):

#### 1. **Запуск** (2 минуты)
```bash
python run_api.py
# Ожидать: ✅ API Server готов к работе!
```

#### 2. **Dashboard обзор** (3 минуты)
- Откройте http://localhost:8000/dashboard
- Покажите live метрики
- Обратите внимание на 14 активных агентов
- Продемонстрируйте WebSocket обновления

#### 3. **API тестирование** (5 минут)
```bash
python test_api_endpoints.py
```
- Наблюдайте обновления в Dashboard
- Покажите API документацию
- Продемонстрируйте JWT authentication

#### 4. **Агенты в действии** (3 минуты)
- Выполните задачу Lead Qualification через API
- Покажите результат (Lead Score)
- Продемонстрируйте Technical SEO Audit
- Обратите внимание на Activity Feed

#### 5. **Production готовность** (2 минуты)
```bash
docker-compose up -d
```
- Покажите полную инфраструктуру
- Откройте Grafana dashboard
- Продемонстрируйте scalability

---

## 📞 Поддержка

**При возникновении проблем:**

1. **Проверьте логи API сервера** - большинство ошибок видны в консоли
2. **Используйте health endpoint** - http://localhost:8000/health
3. **Проверьте браузерную консоль** - F12 для WebSocket ошибок
4. **Обратитесь к документации** - API_DOCUMENTATION.md, DEPLOYMENT_GUIDE.md

**Контакты:**
- **GitHub Issues:** https://github.com/Andrew821667/ai-seo-architects/issues
- **Email:** a.popov.gv@gmail.com

---

**🚀 Удачного тестирования! Все возможности проекта готовы к демонстрации.**

*Последнее обновление: 2025-08-06*