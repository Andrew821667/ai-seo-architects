# 🔗 MCP Integration для AI SEO Architects

## Model Context Protocol (MCP) - Стандартизированная интеграция данных

**AI SEO Architects** теперь поддерживает **Model Context Protocol (MCP)** - открытый стандарт от Anthropic для унифицированного взаимодействия AI-агентов с внешними источниками данных.

## 🎯 Что такое MCP?

MCP (Model Context Protocol) — это протокол, который позволяет AI-системам стандартизированным способом получать доступ к внешним данным и сервисам. В отличие от REST API или GraphQL, MCP специально разработан для AI-агентов и обеспечивает:

- **Контекстную осведомленность**: AI понимает тип и структуру запрашиваемых данных
- **Автоматическое кэширование**: Умное кэширование на основе типа данных и их "свежести"  
- **Fallback механизмы**: Автоматический переход на резервные источники данных
- **Типизированные запросы**: Строгая типизация запросов и ответов
- **Масштабируемость**: Поддержка множественных источников данных

## 🏗️ Архитектура MCP в проекте

```
AI SEO Architects
├── core/mcp/
│   ├── protocol.py          # Основной MCP протокол
│   ├── data_provider.py     # MCP провайдер данных
│   ├── agent_manager.py     # Менеджер агентов с MCP
│   └── __init__.py         # Публичный API
├── config/
│   └── mcp_config.py       # Конфигурации MCP
├── test_mcp_integration.py # Тесты MCP
└── agents/                 # Агенты с MCP поддержкой
    ├── executive/
    ├── management/
    └── operational/
```

## 🚀 Быстрый старт с MCP

### 1. Базовое использование

```python
from core.mcp.agent_manager import get_mcp_agent_manager
from config.mcp_config import get_development_config

# Создаем MCP менеджер
manager = await get_mcp_agent_manager()

# Создаем агента с MCP поддержкой
agent = await manager.create_agent(
    agent_class_name="LeadQualificationAgent",
    enable_mcp=True
)

# Агент автоматически использует MCP для получения данных
result = await agent.process_task({
    "input_data": {
        "company_data": {
            "company_name": "Test Company",
            "industry": "technology"
        }
    }
})
```

### 2. Создание всех агентов с MCP

```python
# Создаем всех 14 агентов с MCP поддержкой
agents = await manager.create_all_agents(enable_mcp=True)

# Запускаем комплексное тестирование
test_results = await manager.run_comprehensive_test()

print(f"Успешно протестировано: {test_results['summary']['success_rate']:.1f}%")
```

### 3. Health monitoring

```python
# Проверка здоровья MCP системы
health = await manager.health_check_all_agents()

print(f"Статус системы: {health['overall_status']}")
print(f"MCP агентов: {health['summary']['mcp_enabled']}")
print(f"Fallback агентов: {health['summary']['fallback_mode']}")
```

## ⚙️ Конфигурация MCP

### Environment переменные

```bash
# .env файл
MCP_ENABLED=true
MCP_CACHE_TTL=30
MCP_MAX_CONCURRENT=10
MCP_TIMEOUT=30

# API ключи для MCP серверов
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key

# Anthropic MCP
ANTHROPIC_MCP_ENABLED=true
ANTHROPIC_MCP_URL=https://api.anthropic.com/mcp/v1

# OpenAI MCP  
OPENAI_MCP_ENABLED=true
OPENAI_MCP_URL=https://api.openai.com/mcp/v1

# Fallback настройки
MCP_ENABLE_FALLBACK=true
MCP_FALLBACK_PROVIDER=mock
```

### Программная конфигурация

```python
from config.mcp_config import MCPSettings, create_mcp_config

# Создание настроек
settings = MCPSettings(
    mcp_enabled=True,
    cache_ttl_minutes=30,
    anthropic_api_key="your_key",
    openai_api_key="your_key"
)

# Генерация конфигурации
config = create_mcp_config(settings)

# Создание менеджера с кастомной конфигурацией
manager = MCPAgentManager(config)
```

## 🔌 Поддерживаемые MCP серверы

### 1. Anthropic MCP Server
- **Специализация**: SEO анализ, контент анализ
- **Качество**: 9.5/10
- **Поддерживаемые ресурсы**: `seo_data`, `content_data`, `technical_audit`

### 2. OpenAI MCP Server  
- **Специализация**: Генерация контента, конкурентный анализ
- **Качество**: 9.0/10
- **Поддерживаемые ресурсы**: `content_data`, `competitive_data`

### 3. Google MCP Server (планируется)
- **Специализация**: Поисковые данные, аналитика
- **Качество**: 10.0/10
- **Поддерживаемые ресурсы**: `seo_data`, `analytics_data`

### 4. Custom MCP Servers
Возможность подключения собственных MCP серверов:

```python
custom_config = {
    "mcp_servers": {
        "custom_seo_server": {
            "name": "custom_seo",
            "endpoints": {"http": "https://your-server.com/mcp/v1"},
            "authentication": {"type": "api_key", "api_key": "your_key"},
            "capabilities": {
                "seo_analysis": {
                    "supported_resources": ["seo_data", "keyword_data"]
                }
            }
        }
    }
}
```

## 📊 Типы ресурсов MCP

### SEO данные (`seo_data`)
```python
# Получение SEO данных через MCP
seo_data = await agent.get_seo_data(
    domain="example.com",
    parameters={
        "include_technical": True,
        "include_content": True,
        "include_performance": True
    }
)
```

### Клиентские данные (`client_data`)
```python
# Получение данных клиента
client_data = await agent.get_client_data(
    client_id="client_123",
    parameters={
        "include_history": True,
        "include_analytics": True
    }
)
```

### Конкурентные данные (`competitive_data`)
```python
# Конкурентный анализ
competitive_data = await agent.get_competitive_data(
    domain="example.com",
    competitors=["competitor1.com", "competitor2.com"],
    parameters={
        "analysis_depth": "comprehensive"
    }
)
```

## 🔄 Fallback механизм

Если MCP серверы недоступны, система автоматически переключается на fallback режим:

```python
# Агент автоматически определяет доступность MCP
agent = await manager.create_agent(
    "LeadQualificationAgent", 
    enable_mcp=True  # Попытается использовать MCP
)

# Если MCP недоступен, будет использован MockDataProvider
print(f"MCP включен: {agent.mcp_enabled}")
print(f"Провайдер: {type(agent.data_provider).__name__}")
```

## 🧪 Тестирование MCP интеграции

### Запуск MCP тестов

```bash
# Полный набор MCP тестов
python test_mcp_integration.py

# Тесты покрывают:
# ✅ Инициализацию MCP конфигурации
# ✅ Создание MCP провайдера
# ✅ Создание агентов с MCP
# ✅ Fallback режим
# ✅ Комплексное тестирование всех агентов
# ✅ Health checks
```

### Пример вывода тестов

```
🧪 === MCP Integration Testing Suite ===

🔧 Тест: mcp_config_initialization
  ✅ MCP конфигурация инициализирована корректно

🔗 Тест: mcp_provider_creation  
  ✅ MCP провайдер создан и протестирован

🤖 Тест: agent_creation_mcp
  ✅ Создано 3/3 агентов с MCP

⚠️ Тест: fallback_mode
  ✅ Fallback режим работает корректно

🏗️ Тест: comprehensive_all_agents
  ✅ Протестировано 14 агентов: 100.0% успеха

🔍 Тест: health_checks
  ✅ Health check: 14/14 агентов здоровы

============================================================
🎯 ИТОГОВЫЙ ОТЧЕТ MCP ИНТЕГРАЦИИ
============================================================
📊 Общая статистика:
   Всего тестов: 6
   Успешно: 6
   Неудачно: 0
   Процент успеха: 100.0%
   MCP тесты: 4
   Fallback тесты: 2

🎉 ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО
============================================================
```

## 🎛️ API Reference

### MCPDataProvider

```python
class MCPDataProvider:
    async def initialize() -> bool
    async def get_seo_data(domain: str, parameters: Dict = None) -> SEOData
    async def get_client_data(client_id: str, parameters: Dict = None) -> ClientData
    async def get_competitive_data(domain: str, competitors: List, parameters: Dict = None) -> CompetitiveData
    async def search_resources(resource_type: MCPResourceType, query: str) -> List[Dict]
    async def health_check() -> Dict[str, Any]
    def get_stats() -> Dict[str, Any]
    async def close()
```

### MCPAgentManager

```python
class MCPAgentManager:
    async def initialize() -> bool
    async def create_agent(agent_class_name: str, enable_mcp: bool = True) -> BaseAgent
    async def create_all_agents(enable_mcp: bool = True) -> Dict[str, BaseAgent]
    async def health_check_all_agents() -> Dict[str, Any]
    async def run_comprehensive_test() -> Dict[str, Any]
    def get_stats() -> Dict[str, Any]
    async def shutdown()
```

### BaseAgent (MCP-enhanced)

```python
class BaseAgent:
    # Новые MCP методы
    async def get_seo_data(domain: str, parameters: Dict = None) -> Any
    async def get_client_data(client_id: str, parameters: Dict = None) -> Any  
    async def get_competitive_data(domain: str, competitors: List, parameters: Dict = None) -> Any
    async def get_mcp_health_status() -> Dict[str, Any]
    def enable_mcp(data_provider: MCPDataProvider)
    def disable_mcp()
    def get_mcp_stats() -> Dict[str, Any]
```

## 🔍 Мониторинг и отладка

### Логирование MCP операций

```python
import logging

# Настройка логирования MCP
logging.getLogger("mcp").setLevel(logging.DEBUG)

# Логи будут показывать:
# - MCP запросы и ответы
# - Время выполнения
# - Cache hits/misses  
# - Fallback активации
# - Ошибки и retry попытки
```

### Метрики производительности

```python
# Получение статистики MCP провайдера
stats = provider.get_stats()

print(f"Всего запросов: {stats['total_requests']}")
print(f"Cache hit rate: {stats['cache_hit_rate']:.2%}")
print(f"Error rate: {stats['error_rate']:.2%}")
print(f"Среднее время ответа: {stats['average_response_time_seconds']:.3f}s")
```

## 🚧 Планы развития MCP

### Ближайшие планы (Q1 2025)

- [ ] **Real-time MCP**: WebSocket поддержка для real-time обновлений
- [ ] **Advanced caching**: Интеллектуальное кэширование на основе типа данных
- [ ] **Circuit breaker**: Защита от каскадных отказов
- [ ] **Batch operations**: Пакетные MCP запросы

### Среднесрочные планы (Q2-Q3 2025)

- [ ] **Custom MCP servers**: Упрощенное создание собственных MCP серверов
- [ ] **GraphQL MCP**: Поддержка GraphQL в качестве транспорта
- [ ] **Multi-region**: Геораспределенные MCP серверы
- [ ] **ML-enhanced routing**: Умная маршрутизация запросов на основе ML

### Долгосрочные планы (Q4 2025+)

- [ ] **Federated MCP**: Федеративные MCP сети
- [ ] **Blockchain integration**: Децентрализованные MCP реестры
- [ ] **AI-to-AI MCP**: Прямое взаимодействие AI-агентов через MCP

## 💡 Best Practices

### 1. Конфигурация для production

```python
# Используйте environment-specific конфигурации
config = get_config_for_environment("production")

# Настройте мониторинг
config["enable_metrics"] = True
config["health_check_interval"] = 30

# Настройте fallback
config["enable_fallback"] = True
config["fallback_provider"] = "cached_mock"
```

### 2. Обработка ошибок

```python
try:
    data = await agent.get_seo_data(domain)
    if data.source == "fallback":
        # Логируем использование fallback
        logger.warning(f"Using fallback data for {domain}")
except Exception as e:
    # Graceful degradation
    logger.error(f"MCP error: {e}")
    # Используем cached или default данные
```

### 3. Оптимизация производительности

```python
# Используйте батчинг для множественных запросов
domains = ["example1.com", "example2.com", "example3.com"]

# Вместо последовательных запросов
results = await asyncio.gather(*[
    agent.get_seo_data(domain) for domain in domains
])
```

## 📝 Changelog

### v1.0.0 (2025-08-05)
- ✅ Базовая MCP интеграция
- ✅ HTTP MCP клиент
- ✅ MCPDataProvider с кэшированием
- ✅ Поддержка Anthropic и OpenAI MCP серверов
- ✅ Fallback механизм на MockDataProvider
- ✅ MCPAgentManager для управления агентами
- ✅ Комплексные тесты интеграции
- ✅ Health monitoring
- ✅ Конфигурация через environment переменные

---

## 🤝 Contributing

Если вы хотите внести вклад в развитие MCP интеграции:

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/mcp-enhancement`)
3. Commit изменения (`git commit -am 'Add MCP feature'`)
4. Push в branch (`git push origin feature/mcp-enhancement`)
5. Создайте Pull Request

## 📞 Support

- **GitHub Issues**: https://github.com/Andrew821667/ai-seo-architects/issues
- **Email**: a.popov.gv@gmail.com
- **Telegram**: @your_telegram

---

**🎉 AI SEO Architects теперь поддерживает MCP - будущее AI-интеграций!**