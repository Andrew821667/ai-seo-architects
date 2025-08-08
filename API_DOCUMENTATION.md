# 📚 AI SEO Architects API Documentation v1.0.0

## 🚀 Обзор системы

AI SEO Architects API представляет собой enterprise-ready FastAPI микросервис для управления мультиагентной системой автоматизации SEO-агентства. Система предоставляет 25+ REST endpoints, real-time WebSocket коммуникацию, и комплексную инфраструктуру для production-grade развертывания.

### 🏛️ Архитектура системы

**Основные компоненты:**
- **FastAPI Backend**: Асинхронный REST API с автоматической документацией
- **PostgreSQL**: Персистентное хранение данных (клиенты, кампании, агенты, метрики)
- **Redis**: Кэширование, сессии, rate limiting, JWT token storage
- **WebSocket Manager**: Real-time коммуникация для дашборда
- **MCP Provider**: Model Context Protocol для интеграции с AI провайдерами
- **FAISS Vector Store**: 14 векторных баз знаний с 700K+ токенов (русский язык)
- **Prometheus + Grafana**: Мониторинг и метрики
- **Nginx**: Reverse proxy и load balancing

### ✨ Ключевые возможности

- 🤖 **14 специализированных агентов** (Executive/Management/Operational иерархия)
- 📊 **Comprehensive мониторинг** с системными и бизнес-метриками
- 🔐 **JWT аутентификация + RBAC** (admin/manager/operator роли)  
- 🔗 **MCP (Model Context Protocol)** интеграция с Anthropic/OpenAI
- 📈 **Real-time WebSocket дашборд** с live updates
- 🏗️ **Production-ready инфраструктура** с Docker Compose
- 🛡️ **Security features**: Rate limiting, request validation, structured logging
- ⚡ **High performance**: Async/await, connection pooling, background tasks
- 📈 **Scalable design**: Horizontal scaling, load balancing, health checks

### 🎯 Технические спецификации

- **API Framework**: FastAPI 0.100+
- **Python Version**: 3.11+
- **Database**: PostgreSQL 15+ с AsyncPG
- **Cache**: Redis 7+ 
- **Vector Store**: FAISS с 14 индексов знаний
- **Monitoring**: Prometheus, Grafana, structured JSON logging
- **Containerization**: Docker + Docker Compose
- **Performance**: ~1000 req/min, sub-100ms response times
- **Knowledge Base**: 700K+ токенов русскоязычных данных

## 🚀 Быстрый старт

### 1. Production развертывание (рекомендуемый)

```bash
# Клонирование репозитория
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env файл с вашими API ключами и паролями

# Запуск всей инфраструктуры
docker-compose up -d

# Проверка статуса сервисов
docker-compose ps

# Просмотр логов
docker-compose logs -f ai-seo-api
```

### 2. Development запуск

```bash
# Установка Python зависимостей
pip install -r requirements.txt

# Запуск локальных сервисов
docker-compose up -d redis postgres

# Запуск API сервера в dev режиме
python run_api.py
```

### 3. Доступ к сервисам

| Сервис | URL | Описание |
|--------|-----|----------|
| **API Server** | http://localhost:8000 | Основной REST API |
| **API Docs** | http://localhost:8000/api/docs | Swagger UI документация |
| **ReDoc** | http://localhost:8000/api/redoc | Alternative API docs |
| **Dashboard** | http://localhost:8000/dashboard | Web интерфейс |
| **Health Check** | http://localhost:8000/health | Системный health check |
| **Metrics** | http://localhost:8000/metrics | Prometheus метрики |
| **WebSocket** | ws://localhost:8000/ws/dashboard | Real-time соединение |
| **Grafana** | http://localhost:3000 | Мониторинг (admin/admin) |
| **Prometheus** | http://localhost:9090 | Метрики база |

### 4. Первое API обращение

```bash
# Health check
curl http://localhost:8000/health

# Авторизация (получение JWT токена)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'

# Получение списка агентов
curl -X GET http://localhost:8000/api/agents/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📡 API Endpoints Reference

Полная документация 25+ REST endpoints, сгруппированных по функциональности. Все endpoints возвращают JSON и поддерживают structured logging.

---

## 🔐 Аутентификация (Authentication)

### POST /auth/login
Авторизация пользователя с JWT token generation

**Headers:**
```http
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "admin",
  "password": "secret",
  "remember_me": false
}
```

**Response 200:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response 401:**
```json
{
  "detail": "Incorrect username or password"
}
```

### POST /auth/refresh
Обновление access token с помощью refresh token

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response 200:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### POST /auth/logout
Выход пользователя (revoke refresh token)

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Logout successful"
}
```

### GET /auth/me
Получить информацию о текущем пользователе

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "user_id": "12345",
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "System Administrator",
  "role": "admin",
  "permissions": ["read", "write", "admin"],
  "is_active": true,
  "last_login": "2025-08-06T10:00:00Z",
  "created_at": "2025-01-01T00:00:00Z"
}
```

### GET /auth/verify
Проверить валидность JWT token

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Token is valid",
  "data": {
    "user_id": "12345",
    "username": "admin",
    "role": "admin",
    "is_active": true
  }
}
```

### GET /auth/health
Health check для authentication системы

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-06T10:00:00Z",
  "components": {
    "postgresql": {
      "status": "healthy",
      "total_users": 25,
      "active_users": 20
    },
    "redis": {
      "status": "healthy",
      "info": {
        "connected_clients": 5,
        "used_memory_human": "1.23M"
      }
    }
  }
}
```

**Предустановленные пользователи:**
- `admin` / `secret` - полный доступ (RBAC role: admin)
- `manager` / `secret` - управленческий доступ (RBAC role: manager)
- `operator` / `secret` - только чтение (RBAC role: operator)

---

## 🤖 Агенты (Agents Management)

### GET /api/agents/
Получить список всех агентов с фильтрацией и пагинацией

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters:**
- `status` - фильтр по статусу (active, idle, busy, error, offline)
- `agent_type` - фильтр по типу (executive, management, operational)
- `mcp_enabled` - фильтр по MCP статусу (true/false)
- `page` - номер страницы (по умолчанию 1, min: 1)
- `size` - размер страницы (по умолчанию 20, min: 1, max: 100)

**Response 200:**
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
      "last_activity": "2025-08-06T10:05:00Z",
      "success_rate": 0.95,
      "processing_time_avg": 2.5,
      "current_task": null
    },
    {
      "agent_id": "business_development_director",
      "name": "Business Development Director Agent",
      "agent_type": "executive",
      "status": "active",
      "mcp_enabled": true,
      "created_at": "2025-08-06T10:00:00Z",
      "last_activity": "2025-08-06T10:03:00Z",
      "success_rate": 0.98,
      "processing_time_avg": 1.8,
      "current_task": "comprehensive_analysis"
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

### GET /api/agents/{agent_id}
Получить информацию о конкретном агенте

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Path Parameters:**
- `agent_id` - ID агента (например: "lead_qualification", "chief_seo_strategist")

**Response 200:**
```json
{
  "agent_id": "lead_qualification",
  "name": "Lead Qualification Agent",
  "agent_type": "operational",
  "status": "active",
  "mcp_enabled": true,
  "created_at": "2025-08-06T10:00:00Z",
  "last_activity": "2025-08-06T10:05:00Z",
  "success_rate": 0.95,
  "processing_time_avg": 2.5,
  "current_task": null
}
```

**Response 404:**
```json
{
  "detail": "Агент lead_qualification не найден"
}
```

### POST /api/agents/{agent_id}/tasks
Выполнить задачу для конкретного агента

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Path Parameters:**
- `agent_id` - ID агента

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
      "employee_count": "100",
      "website": "techcorp.com",
      "monthly_budget": "50000"
    }
  },
  "priority": "normal",
  "timeout": 300,
  "metadata": {
    "source": "api",
    "user_id": "admin"
  }
}
```

**Response 200:**
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
    },
    "recommendations": [
      "High-priority prospect for immediate follow-up",
      "Consider premium service tier",
      "Schedule demo within 3 days"
    ]
  },
  "error": null,
  "processing_time": 2.1,
  "started_at": "2025-08-06T10:00:00Z",
  "completed_at": "2025-08-06T10:00:02.1Z",
  "metadata": {
    "source": "api",
    "user_id": "admin"
  }
}
```

**Response 404:**
```json
{
  "detail": "Агент lead_qualification не найден"
}
```

### GET /api/agents/{agent_id}/health
Получить статус здоровья конкретного агента

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Health check for agent lead_qualification",
  "data": {
    "status": "healthy",
    "success_rate": 0.95,
    "avg_processing_time": 2.5,
    "total_tasks": 156,
    "last_task": "2025-08-06T10:05:00Z",
    "mcp_status": {
      "enabled": true,
      "provider_health": "healthy",
      "last_request": "2025-08-06T10:04:30Z"
    }
  }
}
```

### POST /api/agents/{agent_id}/enable-mcp
Включить MCP для конкретного агента

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "status": "success",
  "message": "MCP enabled for agent lead_qualification",
  "data": {
    "mcp_enabled": true
  }
}
```

### POST /api/agents/{agent_id}/disable-mcp
Отключить MCP для конкретного агента

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "status": "success",
  "message": "MCP disabled for agent lead_qualification",
  "data": {
    "mcp_enabled": false
  }
}
```

### GET /api/agents/{agent_id}/stats
Получить статистику работы агента за период

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters:**
- `timeframe_hours` - период в часах (1-168, по умолчанию: 1)

**Response 200:**
```json
{
  "status": "success",
  "message": "Statistics for agent lead_qualification",
  "data": {
    "agent_id": "lead_qualification",
    "timeframe_hours": 1,
    "current_metrics": {
      "total_tasks_1h": 25,
      "successful_tasks_1h": 24,
      "failed_tasks_1h": 1,
      "success_rate_1h": 0.96,
      "avg_duration_1h": 2.3,
      "tasks_per_minute": 0.42
    },
    "timestamp": "2025-08-06T10:00:00Z"
  }
}
```

### POST /api/agents/create-all
Создать всех 14 агентов с MCP интеграцией

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters:**
- `enable_mcp` - включить MCP для всех агентов (по умолчанию: true)

**Response 200:**
```json
{
  "status": "success",
  "message": "Created 14 agents",
  "data": {
    "created_count": 14,
    "mcp_enabled": true,
    "agent_ids": [
      "chief_seo_strategist",
      "business_development_director",
      "task_coordination",
      "sales_operations_manager",
      "technical_seo_operations_manager",
      "client_success_manager",
      "lead_qualification",
      "proposal_generation",
      "sales_conversation",
      "technical_seo_auditor",
      "content_strategy",
      "link_building",
      "competitive_analysis",
      "reporting"
    ]
  }
}
```

### GET /api/agents/health/all
Health check всех агентов

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Health check completed for all agents",
  "data": {
    "overall_status": "healthy",
    "timestamp": "2025-08-06T10:00:00Z",
    "agents": {
      "lead_qualification": {
        "status": "healthy",
        "success_rate": 0.95,
        "avg_processing_time": 2.5,
        "mcp_enabled": true,
        "mcp_status": {
          "provider_health": "healthy",
          "last_request": "2025-08-06T10:04:30Z"
        }
      }
    },
    "mcp_provider_status": {
      "status": "healthy",
      "overall_health": "healthy",
      "active_servers": 2,
      "last_health_check": "2025-08-06T10:05:00Z"
    },
    "summary": {
      "total_agents": 14,
      "healthy_agents": 14,
      "unhealthy_agents": 0,
      "mcp_enabled": 14,
      "fallback_mode": 0
    }
  }
}
```

### POST /api/agents/test/comprehensive
Запустить комплексное тестирование всех агентов

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "status": "success",
  "message": "Comprehensive test completed",
  "data": {
    "test_type": "comprehensive_mcp_test",
    "timestamp": "2025-08-06T10:00:00Z",
    "results": {
      "lead_qualification": {
        "status": "success",
        "processing_time": 2.1,
        "mcp_enabled": true,
        "mcp_used": true,
        "result_summary": {
          "has_data": true,
          "error": null,
          "agent_type": "operational"
        }
      }
    },
    "summary": {
      "total_tests": 14,
      "successful_tests": 14,
      "failed_tests": 0,
      "mcp_tests": 14,
      "fallback_tests": 0,
      "success_rate": 100.0
    }
  }
}
```

---

## 👥 Клиенты (Clients Management)

### GET /api/clients/
Получить список клиентов с фильтрацией и пагинацией (PostgreSQL)

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters:**
- `industry` - фильтр по отрасли (например: "technology", "healthcare")
- `country` - фильтр по стране
- `min_revenue` - минимальная выручка
- `max_revenue` - максимальная выручка
- `page` - номер страницы (по умолчанию: 1, min: 1)
- `size` - размер страницы (по умолчанию: 20, min: 1, max: 100)

**Response 200:**
```json
[
  {
    "id": "12345678-1234-5678-9abc-123456789012",
    "company_name": "TechCorp Inc",
    "industry": "technology",
    "country": "Russia",
    "contact_email": "ceo@techcorp.com",
    "contact_name": "John Smith",
    "phone": "+7-123-456-7890",
    "website": "https://techcorp.com",
    "monthly_budget": 50000,
    "annual_revenue": 10000000,
    "employee_count": 100,
    "created_at": "2025-08-06T10:00:00Z",
    "updated_at": "2025-08-06T10:00:00Z"
  }
]
```

### GET /api/clients/{client_id}
Получить информацию о конкретном клиенте

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Path Parameters:**
- `client_id` - UUID клиента

**Query Parameters:**
- `include_campaigns` - включить кампании клиента (true/false)

**Response 200:**
```json
{
  "id": "12345678-1234-5678-9abc-123456789012",
  "company_name": "TechCorp Inc",
  "industry": "technology",
  "country": "Russia",
  "contact_email": "ceo@techcorp.com",
  "contact_name": "John Smith",
  "phone": "+7-123-456-7890",
  "website": "https://techcorp.com",
  "monthly_budget": 50000,
  "annual_revenue": 10000000,
  "employee_count": 100,
  "campaigns": [
    {
      "id": "87654321-4321-8765-dcba-210987654321",
      "name": "SEO Campaign Q4 2025",
      "status": "active",
      "domain": "techcorp.com"
    }
  ],
  "created_at": "2025-08-06T10:00:00Z",
  "updated_at": "2025-08-06T10:00:00Z"
}
```

### POST /api/clients/
Создать нового клиента с фоновым анализом

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Request Body:**
```json
{
  "company_name": "TechCorp Inc",
  "industry": "technology",
  "country": "Russia",
  "contact_email": "ceo@techcorp.com",
  "contact_name": "John Smith",
  "phone": "+7-123-456-7890",
  "website": "https://techcorp.com",
  "monthly_budget": 50000,
  "annual_revenue": 10000000,
  "employee_count": 100
}
```

**Response 201:**
```json
{
  "id": "12345678-1234-5678-9abc-123456789012",
  "company_name": "TechCorp Inc",
  "industry": "technology",
  "country": "Russia",
  "contact_email": "ceo@techcorp.com",
  "contact_name": "John Smith",
  "phone": "+7-123-456-7890",
  "website": "https://techcorp.com",
  "monthly_budget": 50000,
  "annual_revenue": 10000000,
  "employee_count": 100,
  "created_at": "2025-08-06T10:00:00Z",
  "updated_at": "2025-08-06T10:00:00Z"
}
```

### PUT /api/clients/{client_id}
Обновить данные клиента

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Request Body:** (аналогично POST /api/clients/)

**Response 200:** (обновленный объект клиента)

### DELETE /api/clients/{client_id}
Удалить клиента (только если нет активных кампаний)

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "message": "Клиент 12345678-1234-5678-9abc-123456789012 успешно удален"
}
```

**Response 400:**
```json
{
  "detail": "Нельзя удалить клиента с активными кампаниями"
}
```

### GET /api/clients/{client_id}/campaigns
Получить кампании конкретного клиента

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters:**
- `status` - фильтр по статусу кампании

**Response 200:**
```json
[
  {
    "id": "87654321-4321-8765-dcba-210987654321",
    "name": "SEO Campaign Q4 2025",
    "status": "active",
    "domain": "techcorp.com",
    "budget": 100000,
    "start_date": "2025-08-01T00:00:00Z",
    "assigned_agents": [
      "technical_seo_auditor",
      "content_strategy",
      "link_building"
    ]
  }
]
```

### GET /api/clients/stats/overview
Получить общую статистику по клиентам

**Headers:**
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response 200:**
```json
{
  "total_clients": 125,
  "by_industry": [
    {
      "industry": "technology",
      "count": 45
    },
    {
      "industry": "healthcare",
      "count": 25
    },
    {
      "industry": "finance",
      "count": 20
    }
  ],
  "by_country": [
    {
      "country": "Russia",
      "count": 80
    },
    {
      "country": "USA",
      "count": 25
    },
    {
      "country": "Germany",
      "count": 20
    }
  ],
  "average_revenue": 8500000
}
```

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

---

## 🤖 Иерархия агентов и возможности

### Executive Level (Исполнительный уровень)

**Высший управленческий уровень с стратегическими функциями**

#### Chief SEO Strategist Agent
- **ID**: `chief_seo_strategist`
- **Функции**: Стратегическое планирование SEO, анализ трендов, долгосрочные стратегии
- **Knowledge Base**: 700K+ токенов стратегических SEO данных (русский язык)
- **MCP Integration**: ✅ Anthropic + OpenAI
- **Capabilities**:
  - Разработка comprehensive SEO стратегий
  - Анализ competitive landscape  
  - Планирование long-term кампаний
  - ROI optimization и budget allocation

#### Business Development Director Agent
- **ID**: `business_development_director`
- **Функции**: Бизнес-развитие, анализ клиентов, стратегическое партнерство
- **Knowledge Base**: 700K+ токенов бизнес-данных (русский язык)
- **MCP Integration**: ✅ Anthropic + OpenAI
- **Capabilities**:
  - Анализ потенциала клиентов
  - Разработка growth strategies
  - Market opportunity assessment
  - Strategic partnership planning

### Management Level (Управленческий уровень)

**Средний управленческий уровень для координации и операционного управления**

#### Task Coordination Agent
- **ID**: `task_coordination`
- **Функции**: Координация задач, workflow management, resource allocation
- **Knowledge Base**: FAISS vector store с coordination данными
- **MCP Integration**: ✅ Anthropic + OpenAI

#### Sales Operations Manager Agent
- **ID**: `sales_operations_manager`
- **Функции**: Управление продажами, pipeline optimization, CRM integration
- **Knowledge Base**: Sales process optimization данные
- **MCP Integration**: ✅ Anthropic + OpenAI

#### Technical SEO Operations Manager Agent
- **ID**: `technical_seo_operations_manager`
- **Функции**: Управление техническими SEO процессами, audit coordination
- **Knowledge Base**: Technical SEO best practices база
- **MCP Integration**: ✅ Anthropic + OpenAI

#### Client Success Manager Agent
- **ID**: `client_success_manager`
- **Функции**: Customer success, retention optimization, satisfaction tracking
- **Knowledge Base**: Client success methodology данные
- **MCP Integration**: ✅ Anthropic + OpenAI

### Operational Level (Операционный уровень)

**Исполнительский уровень для конкретных SEO задач**

#### Lead Qualification Agent
- **ID**: `lead_qualification`
- **Функции**: Квалификация лидов, scoring, BANT analysis
- **Knowledge Base**: Lead qualification framework
- **Sample Task**:
```json
{
  "task_type": "lead_analysis",
  "input_data": {
    "company_data": {
      "company_name": "TechCorp",
      "industry": "technology",
      "annual_revenue": "10000000",
      "employee_count": "100"
    }
  }
}
```

#### Proposal Generation Agent
- **ID**: `proposal_generation`
- **Функции**: Генерация коммерческих предложений, pricing strategies
- **Knowledge Base**: Proposal templates и pricing данные

#### Sales Conversation Agent
- **ID**: `sales_conversation`
- **Функции**: Ведение продажных диалогов, objection handling
- **Knowledge Base**: Sales conversation scripts и techniques

#### Technical SEO Auditor Agent
- **ID**: `technical_seo_auditor`
- **Функции**: Технический аудит сайтов, performance analysis
- **Knowledge Base**: Technical SEO audit методология

#### Content Strategy Agent
- **ID**: `content_strategy`
- **Функции**: Контентная стратегия, keyword research, content planning
- **Knowledge Base**: Content marketing best practices

#### Link Building Agent
- **ID**: `link_building`
- **Функции**: Link building strategies, outreach campaigns
- **Knowledge Base**: Link building techniques и tools

#### Competitive Analysis Agent
- **ID**: `competitive_analysis`
- **Функции**: Анализ конкурентов, market intelligence
- **Knowledge Base**: Competitive analysis framework

#### Reporting Agent
- **ID**: `reporting`
- **Функции**: Генерация отчетов, data visualization, KPI tracking
- **Knowledge Base**: Reporting templates и analytics данные

---

## 📡 Real-time WebSocket API

### Connection Management
Система поддерживает множественные WebSocket подключения с группировкой по типам клиентов.

**Endpoint:** `ws://localhost:8000/ws/dashboard`

### Подключение к дашборду

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/dashboard');

ws.onopen = function() {
    console.log('✅ Connected to AI SEO Architects Dashboard');
    
    // Подписка на обновления метрик
    ws.send(JSON.stringify({
        type: 'subscribe',
        subscription_type: 'metrics_update'
    }));
    
    // Подписка на статус агентов
    ws.send(JSON.stringify({
        type: 'subscribe', 
        subscription_type: 'agents_status'
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch (data.type) {
        case 'connection_established':
            console.log(`Connected as client: ${data.client_id}`);
            break;
        case 'metrics_update':
            updateDashboardMetrics(data.data);
            break;
        case 'agents_status':
            updateAgentsStatus(data.data);
            break;
        case 'server_heartbeat':
            console.log('Server heartbeat received');
            break;
    }
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};

ws.onclose = function() {
    console.log('WebSocket connection closed');
};
```

### WebSocket Message Types

#### 📤 Исходящие (клиент -> сервер)
- `heartbeat` - проверка связи (keep-alive)
- `subscribe` - подписка на тип обновлений
- `unsubscribe` - отписка от обновлений  
- `request_metrics` - запрос текущих метрик
- `request_agents_status` - запрос статуса агентов
- `join_group` - присоединение к группе (dashboard, monitoring, agents, campaigns)
- `leave_group` - выход из группы

#### 📥 Входящие (сервер -> клиент)
- `connection_established` - подтверждение подключения с client_id
- `metrics_update` - real-time обновление метрик (каждые 30 сек)
- `agents_status` - статус агентов и MCP провайдеров
- `server_heartbeat` - heartbeat от сервера (каждые 30 сек)
- `subscription_confirmed` - подтверждение подписки
- `group_joined` - подтверждение присоединения к группе
- `server_shutdown` - уведомление о graceful shutdown

### Connection Groups
```javascript
// Присоединение к специфической группе
ws.send(JSON.stringify({
    type: 'join_group',
    group: 'monitoring'  // dashboard, monitoring, agents, campaigns
}));
```

**Группы подключений:**
- `dashboard` - real-time дашборд данные
- `monitoring` - системные метрики и алерты  
- `agents` - статус агентов и выполнение задач
- `campaigns` - обновления кампаний и метрики

---

## 🔗 Model Context Protocol (MCP) Integration

### MCP Configuration
Система поддерживает множественные MCP серверы с приоритизацией и fallback режимом.

#### Поддерживаемые MCP серверы
```yaml
mcp_servers:
  anthropic:
    priority: 10  # Высший приоритет
    capabilities: ["seo_analysis", "content_analysis"]
    health_check: "https://api.anthropic.com/health"
    
  openai:  
    priority: 8
    capabilities: ["content_generation", "competitive_analysis"]
    health_check: "https://api.openai.com/health"
    
  google:  # Планируется
    priority: 9
    capabilities: ["search_data", "analytics_data"]
```

### MCP Endpoints

#### GET /api/mcp/health
Health check всех MCP серверов

```json
{
  "overall_health": "healthy",
  "servers": {
    "anthropic": {
      "status": "healthy",
      "last_check": "2025-08-06T10:05:00Z",
      "response_time": 45
    },
    "openai": {
      "status": "healthy", 
      "last_check": "2025-08-06T10:05:00Z",
      "response_time": 62
    }
  },
  "fallback_enabled": true
}
```

#### POST /api/mcp/test
Тестирование MCP интеграции

```json
{
  "test_type": "comprehensive",
  "results": {
    "anthropic": {
      "status": "success",
      "capabilities_tested": 4,
      "avg_response_time": 1.2
    }
  }
}
```

---

## 📊 Analytics & Monitoring Endpoints

### GET /api/analytics/system
Получить системные метрики

**Query Parameters:**
- `timeframe` - период (1h, 24h, 7d, 30d, 90d, 365d)

**Response:**
```json
{
  "status": "success",
  "data": {
    "metrics": {
      "timestamp": "2025-08-06T10:00:00Z",
      "timeframe": "1h",
      "total_requests": 1248,
      "successful_requests": 1195,
      "error_rate": 0.042,
      "avg_response_time": 87.5,
      "active_agents": 14,
      "active_campaigns": 8,
      "active_clients": 125,
      "system_load": 25.5,
      "memory_usage_percent": 45.2,
      "cpu_usage_percent": 25.5
    },
    "raw_metrics": {
      "uptime_seconds": 86400,
      "system": {
        "cpu_percent": 25.5,
        "memory_percent": 45.2,
        "active_connections": 12
      }
    }
  }
}
```

### GET /api/analytics/agents
Метрики производительности агентов

```json
{
  "status": "success",
  "data": {
    "metrics": [
      {
        "agent_id": "lead_qualification",
        "timeframe": "1h", 
        "total_tasks": 156,
        "successful_tasks": 148,
        "failed_tasks": 8,
        "success_rate": 0.948,
        "avg_processing_time": 2.3,
        "throughput_per_hour": 156,
        "error_types": {
          "timeout": 3,
          "mcp_error": 2,
          "validation_error": 3
        },
        "resource_usage": {
          "memory_mb": 45.2,
          "cpu_percent": 8.5
        }
      }
    ],
    "total_agents": 14
  }
}
```

### GET /api/analytics/business
Бизнес-метрики и KPI

```json
{
  "status": "success",
  "data": {
    "metrics": {
      "timestamp": "2025-08-06T10:00:00Z",
      "timeframe": "24h",
      "total_revenue": 2500000.0,
      "new_clients": 3,
      "churned_clients": 0,
      "client_retention_rate": 0.96,
      "average_deal_size": 125000.0,
      "pipeline_value": 5000000.0,
      "lead_conversion_rate": 0.23,
      "customer_satisfaction": 4.2
    },
    "additional_stats": {
      "total_clients": 125,
      "total_campaigns": 45,
      "active_campaigns": 32,
      "total_leads": 1250,
      "qualified_leads": 287
    }
  }
}
```

### GET /api/analytics/dashboard
Агрегированные данные для дашборда

```json
{
  "status": "success", 
  "data": {
    "system_health": {
      "uptime_seconds": 86400,
      "cpu_percent": 25.5,
      "memory_percent": 45.2,
      "active_connections": 12,
      "status": "healthy"
    },
    "agents_summary": {
      "total_agents": 14,
      "active_agents": 14,
      "avg_success_rate": 0.94,
      "total_tasks_1h": 1562
    },
    "business_summary": {
      "total_clients": 125,
      "total_campaigns": 45,
      "active_campaigns": 32,
      "total_revenue": 2500000.0,
      "total_leads": 1250
    },
    "http_summary": {
      "requests_1h": 1248,
      "error_rate_1h": 0.042,
      "avg_response_time_1h": 87.5,
      "requests_per_minute": 20.8
    },
    "recent_activity": [
      {
        "timestamp": "2025-08-06T10:00:00Z",
        "type": "agent_task_completed",
        "message": "Technical SEO Audit completed for client XYZ",
        "agent_id": "technical_seo_auditor"
      }
    ],
    "top_performing_agents": [
      {
        "agent_id": "lead_qualification",
        "success_rate": 0.948,
        "total_tasks": 156,
        "performance_score": 147.9
      }
    ],
    "alerts": [
      {
        "type": "warning",
        "message": "High CPU usage: 81.2%",
        "timestamp": "2025-08-06T10:00:00Z"
      }
    ]
  }
}
```

### GET /api/analytics/export
Экспорт метрик в файл

**Query Parameters:**
- `timeframe` - период для экспорта
- `format` - формат файла (json, csv)

```json
{
  "status": "success",
  "data": {
    "filename": "metrics_export_24h_20250806_100000.json",
    "filepath": "exports/metrics_export_24h_20250806_100000.json",
    "format": "json",
    "timeframe": "24h",
    "exported_at": "2025-08-06T10:00:00Z"
  }
}
```

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

---

## 🏗️ Production Infrastructure & Deployment

### Docker Compose Architecture (Рекомендуемый)

Полная microservices архитектура с 8 сервисами:

```bash
# Запуск всей инфраструктуры
docker-compose up -d

# Проверка статуса всех сервисов  
docker-compose ps

# Мониторинг логов
docker-compose logs -f ai-seo-api
```

#### Сервисы инфраструктуры:

| Сервис | Контейнер | Порт | Описание |
|--------|-----------|------|----------|
| **ai-seo-api** | ai-seo-architects-api | 8000 | FastAPI backend с 25+ endpoints |
| **postgres** | ai-seo-postgres | 5432 | PostgreSQL 15 база данных |
| **redis** | ai-seo-redis | 6379 | Redis для кэширования и сессий |
| **nginx** | ai-seo-nginx | 80/443 | Reverse proxy и load balancer |
| **prometheus** | ai-seo-prometheus | 9090 | Сбор метрик и мониторинг |
| **grafana** | ai-seo-grafana | 3000 | Визуализация метрик |
| **chroma** | ai-seo-chroma | 8001 | Vector database (опционально) |

### Environment Configuration

#### Production .env файл:
```bash
# === ОСНОВНЫЕ НАСТРОЙКИ ===
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# === БАЗЫ ДАННЫХ ===
DATABASE_URL=postgresql+asyncpg://ai_seo_user:secure_password_change_me@postgres:5432/ai_seo_architects
POSTGRES_PASSWORD=secure_password_change_me
REDIS_URL=redis://redis:6379/0

# === БЕЗОПАСНОСТЬ ===
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# === MCP ИНТЕГРАЦИЯ ===
MCP_ENABLED=true
MCP_CACHE_TTL_MINUTES=30
MCP_MAX_CONCURRENT=10
MCP_TIMEOUT=30
MCP_ENABLE_FALLBACK=true

# API КЛЮЧИ
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# === МОНИТОРИНГ ===
PROMETHEUS_ENABLED=true
GRAFANA_PASSWORD=admin_password_change_me

# === MIDDLEWARE ===
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
VALIDATION_ENABLED=true
VALIDATION_STRICT_MODE=false

# === SEO AI MODELS ===
SEO_AI_MODELS_MOCK_MODE=false
```

### Health Checks & Monitoring

#### Системный Health Check
```bash
# Основной health check
curl http://localhost:8000/health

# Health check с детализацией
curl http://localhost:8000/health | jq '.'
```

**Пример ответа:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-06T10:00:00Z", 
  "version": "1.0.0",
  "agents_status": {
    "overall_status": "healthy",
    "summary": {
      "total_agents": 14,
      "healthy_agents": 14,
      "unhealthy_agents": 0,
      "mcp_enabled": 14,
      "fallback_mode": 0
    }
  },
  "metrics": {
    "uptime_seconds": 86400,
    "infrastructure": {
      "database": "healthy",
      "redis": "healthy",
      "agent_manager": "healthy"
    },
    "system": {
      "cpu_percent": 25.5,
      "memory_percent": 45.2,
      "active_connections": 12
    }
  }
}
```

#### Prometheus Metrics Endpoint
```bash
# Prometheus метрики в exposition format
curl http://localhost:8000/metrics
```

### Rate Limiting & Security

#### Rate Limits (по ролям):
- **Admin**: 1000 запросов/час
- **Manager**: 500 запросов/час  
- **Operator**: 200 запросов/час
- **WebSocket**: 10 одновременных соединений на пользователя
- **Неавторизованные**: 100 запросов/час

#### Security Headers:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1625097600
X-Request-ID: req_12345
```

### Performance Specifications

#### Benchmarks:
- **Throughput**: ~1000 requests/minute
- **Response Time**: <100ms (p95), <50ms (p50)
- **Concurrent Users**: 100+ одновременных соединений
- **Database Connections**: Connection pooling (10-50 connections)
- **Memory Usage**: ~512MB (production), ~256MB (development)
- **CPU Usage**: <30% при normal load

#### Scaling Configuration:
```yaml
# docker-compose.override.yml для scaling
services:
  ai-seo-api:
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
```

### Database Schema & Migrations

#### PostgreSQL Schema:
- **Users Table**: JWT authentication, RBAC
- **Clients Table**: Client management with UUID primary keys  
- **Campaigns Table**: SEO campaigns with relationships
- **Agents Table**: Agent registry and configuration
- **Tasks Table**: Task execution history
- **Metrics Tables**: Performance and business metrics

#### Redis Usage:
- **JWT Tokens**: Refresh token storage с TTL
- **Session Data**: User sessions и preferences
- **Rate Limiting**: Request counters per user/IP
- **Cache**: API response caching (30min TTL)

### Monitoring & Alerting

#### Grafana Dashboards:
1. **System Overview**: CPU, Memory, Network, Disk usage
2. **API Performance**: Request rates, response times, error rates  
3. **Agents Performance**: Task success rates, processing times
4. **Business Metrics**: Revenue, clients, campaigns, conversions
5. **MCP Integration**: MCP server health, request success rates

#### Prometheus Alerts:
```yaml
groups:
  - name: ai_seo_architects
    rules:
      - alert: HighErrorRate
        expr: http_errors_total / http_requests_total > 0.1
        for: 5m
        
      - alert: HighCPUUsage  
        expr: system_cpu_percent > 80
        for: 10m
        
      - alert: AgentFailureRate
        expr: agent_success_rate < 0.8
        for: 15m
```

### Backup & Recovery

#### Automated Backups:
```bash
# PostgreSQL backup (daily)
docker exec ai-seo-postgres pg_dump -U ai_seo_user ai_seo_architects > backup_$(date +%Y%m%d).sql

# Redis backup (daily) 
docker exec ai-seo-redis redis-cli --rdb backup_redis_$(date +%Y%m%d).rdb

# FAISS indexes backup
tar -czf faiss_backup_$(date +%Y%m%d).tar.gz data/vector_stores/
```

### Troubleshooting

#### Общие проблемы:

1. **503 Service Unavailable**
   - Проверьте статус контейнеров: `docker-compose ps`
   - Проверьте логи: `docker-compose logs ai-seo-api`

2. **JWT Token Expired**
   - Используйте refresh token: `POST /auth/refresh`
   - Проверьте Redis доступность

3. **MCP Integration Errors**  
   - Проверьте API ключи в .env файле
   - Запустите MCP health check: `GET /api/agents/health/all`

4. **High Memory Usage**
   - Перезапустите API сервис: `docker-compose restart ai-seo-api`
   - Проверьте FAISS индексы и memory leaks

#### Логи и отладка:
```bash
# Structured JSON logs
docker-compose logs ai-seo-api | jq '.'

# Metrics export для анализа
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/analytics/export?timeframe=24h&format=json"
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