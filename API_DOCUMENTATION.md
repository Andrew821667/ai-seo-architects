# 📚 AI SEO Architects API Documentation

## Обзор

AI SEO Architects API представляет собой enterprise-ready RESTful API с WebSocket поддержкой для управления мультиагентной системой автоматизации SEO-агентства.

### Основные возможности

- 🤖 **Управление 14 специализированными агентами**
- 📊 **Real-time мониторинг и аналитика**
- 🔐 **JWT аутентификация с ролевой моделью**
- 🔗 **MCP (Model Context Protocol) интеграция**
- 📈 **WebSocket для live обновлений дашборда**
- 🏗️ **Docker контейнеризация**

## Быстрый старт

### 1. Установка и запуск

```bash
# Клонирование репозитория
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# Установка зависимостей
pip install -r requirements.txt

# Запуск API сервера
python run_api.py
```

### 2. Доступ к интерфейсам

- **🎛️ Dashboard**: http://localhost:8000/dashboard
- **📖 API Docs**: http://localhost:8000/api/docs
- **🔍 Health Check**: http://localhost:8000/health
- **⚡ WebSocket**: ws://localhost:8000/ws/dashboard

### 3. Docker запуск

```bash
# Сборка и запуск всей инфраструктуры
docker-compose up -d

# Просмотр логов
docker-compose logs -f ai-seo-api

# Остановка
docker-compose down
```

## API Endpoints

### Аутентификация

#### POST /auth/login
Авторизация пользователя

**Request Body:**
```json
{
  "username": "admin",
  "password": "secret"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Предустановленные пользователи:**
- `admin` / `secret` - полный доступ
- `manager` / `secret` - управленческий доступ
- `operator` / `secret` - только чтение

### Агенты

#### GET /api/agents/
Получить список всех агентов

**Query Parameters:**
- `status` - фильтр по статусу (active, idle, error)
- `agent_type` - фильтр по типу (executive, management, operational)
- `mcp_enabled` - фильтр по MCP статусу
- `page` - номер страницы (по умолчанию 1)
- `size` - размер страницы (по умолчанию 20)

**Response:**
```json
{
  "agents": [
    {
      "agent_id": "lead_qualification",
      "name": "Lead Qualification Agent",
      "agent_type": "operational",
      "status": "active",
      "mcp_enabled": true,
      "created_at": "2025-08-06T10:00:00Z",
      "success_rate": 0.95,
      "processing_time_avg": 2.5
    }
  ],
  "total_count": 14,
  "active_count": 12,
  "mcp_enabled_count": 14,
  "categories": {
    "executive": 2,
    "management": 4,
    "operational": 8
  }
}
```

#### GET /api/agents/{agent_id}
Получить информацию о конкретном агенте

#### POST /api/agents/{agent_id}/tasks
Выполнить задачу для агента

**Request Body:**
```json
{
  "task_id": "task_123",
  "agent_id": "lead_qualification",
  "task_type": "lead_analysis",
  "input_data": {
    "company_data": {
      "company_name": "TechCorp",
      "industry": "technology",
      "annual_revenue": "10000000",
      "employee_count": "100"
    }
  },
  "priority": "normal",
  "timeout": 300
}
```

**Response:**
```json
{
  "task_id": "task_123",
  "agent_id": "lead_qualification",
  "status": "completed",
  "result": {
    "lead_score": 85,
    "lead_quality": "Hot Lead",
    "qualification_details": {
      "budget_score": 90,
      "authority_score": 80,
      "need_score": 85,
      "timeline_score": 85
    }
  },
  "processing_time": 2.1,
  "started_at": "2025-08-06T10:00:00Z",
  "completed_at": "2025-08-06T10:00:02.1Z"
}
```

#### POST /api/agents/create-all
Создать всех 14 агентов

#### GET /api/agents/health/all
Health check всех агентов

### Клиенты

#### GET /api/clients/
Получить список клиентов

#### POST /api/clients/
Создать нового клиента

**Request Body:**
```json
{
  "company_name": "TechCorp Inc",
  "industry": "technology",
  "contact_email": "ceo@techcorp.com",
  "contact_name": "John Smith",
  "phone": "+7-123-456-7890",
  "website": "https://techcorp.com",
  "monthly_budget": 50000,
  "annual_revenue": 10000000,
  "employee_count": 100
}
```

#### GET /api/clients/{client_id}
Получить информацию о клиенте

#### POST /api/clients/{client_id}/qualify
Квалифицировать лид клиента

#### POST /api/clients/{client_id}/proposal
Сгенерировать коммерческое предложение

### Кампании

#### GET /api/campaigns/
Получить список SEO кампаний

#### POST /api/campaigns/
Создать новую кампанию

**Request Body:**
```json
{
  "client_id": "client_123",
  "name": "SEO Campaign for TechCorp",
  "description": "Comprehensive SEO optimization",
  "domain": "techcorp.com",
  "keywords": ["technology", "software", "development"],
  "budget": 100000,
  "start_date": "2025-08-01T00:00:00Z",
  "end_date": "2025-12-31T23:59:59Z"
}
```

#### POST /api/campaigns/{campaign_id}/start
Запустить кампанию

#### GET /api/campaigns/{campaign_id}/metrics
Получить метрики кампании

### Аналитика

#### GET /api/analytics/system
Получить системные метрики

**Query Parameters:**
- `timeframe` - период (1h, 24h, 7d, 30d, 90d, 365d)

#### GET /api/analytics/agents
Получить метрики производительности агентов

#### GET /api/analytics/business
Получить бизнес-метрики

#### GET /api/analytics/dashboard
Получить агрегированные данные для дашборда

**Response:**
```json
{
  "status": "success",
  "data": {
    "system_health": {
      "uptime_seconds": 3600,
      "cpu_percent": 25.5,
      "memory_percent": 45.2,
      "active_connections": 12,
      "status": "healthy"
    },
    "agents_summary": {
      "total_agents": 14,
      "active_agents": 12,
      "avg_success_rate": 0.94,
      "total_tasks_1h": 156
    },
    "business_summary": {
      "total_clients": 25,
      "total_campaigns": 15,
      "active_campaigns": 8,
      "total_revenue": 2500000,
      "total_leads": 145
    }
  }
}
```

## WebSocket API

### Подключение к дашборду

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/dashboard');

ws.onopen = function() {
    console.log('Connected to dashboard');
    
    // Подписка на обновления метрик
    ws.send(JSON.stringify({
        type: 'subscribe',
        subscription_type: 'metrics_update'
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch (data.type) {
        case 'metrics_update':
            updateDashboardMetrics(data.data);
            break;
        case 'agents_status':
            updateAgentsStatus(data.data);
            break;
    }
};
```

### Типы сообщений

#### Исходящие (клиент -> сервер):
- `heartbeat` - проверка связи
- `subscribe` - подписка на тип обновлений
- `unsubscribe` - отписка от обновлений
- `request_metrics` - запрос текущих метрик
- `request_agents_status` - запрос статуса агентов

#### Входящие (сервер -> клиент):
- `connection_established` - подтверждение подключения
- `metrics_update` - обновление метрик
- `agents_status` - статус агентов
- `server_heartbeat` - heartbeat от сервера

## Модели данных

### Agent
```json
{
  "agent_id": "string",
  "name": "string", 
  "agent_type": "executive | management | operational",
  "status": "active | idle | busy | error | offline",
  "mcp_enabled": "boolean",
  "created_at": "string",
  "last_activity": "string",
  "processing_time_avg": "number",
  "success_rate": "number",
  "current_task": "string"
}
```

### Client
```json
{
  "client_id": "string",
  "company_name": "string",
  "industry": "string",
  "tier": "startup | smb | enterprise",
  "contact_email": "string",
  "contact_name": "string",
  "phone": "string",
  "website": "string",
  "monthly_budget": "number",
  "annual_revenue": "number",
  "employee_count": "number",
  "active_campaigns": ["string"],
  "created_at": "string"
}
```

### Campaign
```json
{
  "campaign_id": "string",
  "client_id": "string",
  "name": "string",
  "description": "string",
  "status": "draft | active | paused | completed | cancelled",
  "domain": "string",
  "keywords": ["string"],
  "budget": "number",
  "start_date": "string",
  "end_date": "string",
  "assigned_agents": ["string"],
  "created_at": "string"
}
```

## Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | OK - Успешный запрос |
| 201 | Created - Ресурс создан |
| 400 | Bad Request - Неверный запрос |
| 401 | Unauthorized - Не авторизован |
| 403 | Forbidden - Недостаточно прав |
| 404 | Not Found - Ресурс не найден |
| 422 | Validation Error - Ошибка валидации |
| 500 | Internal Server Error - Внутренняя ошибка сервера |
| 503 | Service Unavailable - Сервис недоступен |

## Rate Limiting

API использует rate limiting для предотвращения злоупотреблений:

- **Аутентифицированные пользователи**: 1000 запросов/час
- **WebSocket подключения**: 10 одновременных соединений на пользователя
- **Неаутентифицированные запросы**: 100 запросов/час

## Мониторинг и логирование

### Structured Logging
Все операции логируются в структурированном JSON формате:

```json
{
  "timestamp": "2025-08-06T10:00:00Z",
  "level": "INFO",
  "logger": "api.routes.agents",
  "message": "Agent task completed",
  "correlation_id": "req_12345",
  "agent_id": "lead_qualification",
  "task_id": "task_123",
  "processing_time_seconds": 2.1
}
```

### Метрики
API собирает следующие метрики:

- **HTTP метрики**: количество запросов, время ответа, коды ошибок
- **Системные метрики**: CPU, память, диск, сетевая активность
- **Агентские метрики**: производительность, success rate, throughput
- **Бизнес метрики**: revenue, конверсии, retention

### Health Checks
- `/health` - общее состояние API
- `/api/agents/health/all` - состояние всех агентов
- `/api/analytics/health` - состояние аналитического модуля

## MCP Integration

API поддерживает Model Context Protocol для стандартизированного доступа к данным:

```python
# Включение MCP для агента
POST /api/agents/{agent_id}/enable-mcp

# Отключение MCP
POST /api/agents/{agent_id}/disable-mcp

# Статус MCP
GET /api/agents/{agent_id}/health
```

### MCP серверы
- **Anthropic MCP Server** - SEO анализ, контент анализ
- **OpenAI MCP Server** - генерация контента, конкурентный анализ
- **Fallback режим** - автоматический переход на mock данные

## Развертывание

### Docker Compose (Рекомендуемый)
```bash
# Полная инфраструктура
docker-compose up -d

# Включает:
# - AI SEO Architects API (порт 8000)
# - PostgreSQL (порт 5432)
# - Redis (порт 6379)
# - Nginx reverse proxy (порт 80/443)
# - Prometheus (порт 9090)
# - Grafana (порт 3000)
# - ChromaDB (порт 8001)
```

### Переменные окружения
```bash
# Основные
ENVIRONMENT=production
API_PORT=8000

# MCP
MCP_ENABLED=true
MCP_CACHE_TTL=30
MCP_ENABLE_FALLBACK=true

# База данных
POSTGRES_PASSWORD=secure_password
REDIS_URL=redis://localhost:6379

# Мониторинг
GRAFANA_PASSWORD=admin_password
```

## Примеры использования

### Python клиент
```python
import httpx
import asyncio

class AISeOArchitectsClient:
    def __init__(self, base_url="http://localhost:8000", token=None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    async def get_agents(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/agents/",
                headers=self.headers
            )
            return response.json()
    
    async def run_agent_task(self, agent_id, task_data):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/agents/{agent_id}/tasks",
                json=task_data,
                headers=self.headers
            )
            return response.json()

# Использование
async def main():
    # Авторизация
    auth_client = httpx.AsyncClient()
    auth_response = await auth_client.post("http://localhost:8000/auth/login", json={
        "username": "admin",
        "password": "secret"
    })
    token = auth_response.json()["access_token"]
    
    # Создание клиента
    client = AISeOArchitectsClient(token=token)
    
    # Получение агентов
    agents = await client.get_agents()
    print(f"Доступно агентов: {agents['total_count']}")
    
    # Запуск задачи
    task_result = await client.run_agent_task("lead_qualification", {
        "task_type": "lead_analysis",
        "input_data": {
            "company_data": {
                "company_name": "Test Company",
                "industry": "technology"
            }
        }
    })
    print(f"Результат задачи: {task_result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript/TypeScript клиент
```typescript
interface AgentTask {
  task_id: string;
  agent_id: string;
  task_type: string;
  input_data: any;
}

class AISeOArchitectsClient {
  private baseUrl: string;
  private token: string | null;

  constructor(baseUrl = 'http://localhost:8000', token: string | null = null) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  async authenticate(username: string, password: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    this.token = data.access_token;
    return this.token;
  }

  async getAgents() {
    const response = await fetch(`${this.baseUrl}/api/agents/`, {
      headers: this.getHeaders()
    });
    return response.json();
  }

  async runAgentTask(agentId: string, taskData: Partial<AgentTask>) {
    const response = await fetch(`${this.baseUrl}/api/agents/${agentId}/tasks`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(taskData)
    });
    return response.json();
  }

  private getHeaders() {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };
    
    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }
    
    return headers;
  }
}
```

## FAQ

### Как добавить нового агента?
1. Создайте класс агента, наследуясь от `BaseAgent`
2. Реализуйте метод `process_task()`
3. Добавьте knowledge base в `/knowledge/`
4. Обновите интеграционные тесты
5. Добавьте в `MCPAgentManager`

### Как настроить MCP серверы?
Обновите `/config/mcp_config.py` с новыми серверами и их endpoints.

### Как масштабировать API?
Используйте несколько worker процессов в production или добавьте больше реплик в Docker Compose.

### Как мониторить производительность?
Используйте встроенные метрики через `/api/analytics/` endpoints или подключите Prometheus/Grafana.

## Поддержка

- **GitHub Issues**: https://github.com/Andrew821667/ai-seo-architects/issues
- **Email**: a.popov.gv@gmail.com
- **Документация**: см. TECHNICAL_DEFENSE_DOCUMENTATION.md

---

**🤖 AI SEO Architects API v1.0.0**  
**Автор**: Andrew Popov  
**Лицензия**: MIT