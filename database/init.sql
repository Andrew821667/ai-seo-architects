-- Инициализация базы данных AI SEO Architects
-- Создание схем, таблиц и начальных данных

-- Создание расширений
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Создание схем
CREATE SCHEMA IF NOT EXISTS ai_seo;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Установка search_path
SET search_path TO ai_seo, public;

-- Таблица пользователей системы
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'operator' CHECK (role IN ('admin', 'manager', 'operator')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Таблица агентов
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    agent_id VARCHAR(50) UNIQUE NOT NULL,
    agent_level VARCHAR(20) NOT NULL CHECK (agent_level IN ('executive', 'management', 'operational')),
    description TEXT,
    knowledge_base_path VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    config JSONB DEFAULT '{}'::jsonb
);

-- Таблица клиентов
CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(200) NOT NULL,
    industry VARCHAR(100),
    website VARCHAR(255),
    annual_revenue BIGINT,
    employee_count INTEGER,
    country VARCHAR(2) DEFAULT 'RU',
    contact_person VARCHAR(100),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Таблица кампаний
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    campaign_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('draft', 'active', 'paused', 'completed', 'cancelled')),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(10,2),
    objectives TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    config JSONB DEFAULT '{}'::jsonb
);

-- Таблица задач агентов
CREATE TABLE IF NOT EXISTS agent_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'failed')),
    input_data JSONB NOT NULL,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Таблица метрик агентов
CREATE TABLE IF NOT EXISTS agent_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL,
    metric_value DECIMAL(10,4),
    metric_unit VARCHAR(20),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Таблица сессий (для JWT refresh tokens)
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    user_agent TEXT,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Аналитическая схема
SET search_path TO analytics, public;

-- Таблица событий системы
CREATE TABLE IF NOT EXISTS system_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(50) NOT NULL,
    source VARCHAR(50) NOT NULL,
    user_id UUID,
    agent_id UUID,
    event_data JSONB NOT NULL,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Материализованное представление для дашборда
CREATE MATERIALIZED VIEW IF NOT EXISTS dashboard_metrics AS
SELECT 
    date_trunc('hour', t.created_at) as time_bucket,
    a.agent_level,
    COUNT(*) as total_tasks,
    COUNT(*) FILTER (WHERE t.status = 'completed') as completed_tasks,
    COUNT(*) FILTER (WHERE t.status = 'failed') as failed_tasks,
    AVG(t.processing_time_ms) as avg_processing_time,
    MAX(t.processing_time_ms) as max_processing_time
FROM ai_seo.agent_tasks t
JOIN ai_seo.agents a ON t.agent_id = a.id
WHERE t.created_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY time_bucket, a.agent_level
ORDER BY time_bucket DESC;

-- Возвращаемся к основной схеме
SET search_path TO ai_seo, public;

-- Создание индексов для производительности
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

CREATE INDEX IF NOT EXISTS idx_agents_agent_id ON agents(agent_id);
CREATE INDEX IF NOT EXISTS idx_agents_level ON agents(agent_level);
CREATE INDEX IF NOT EXISTS idx_agents_active ON agents(is_active);

CREATE INDEX IF NOT EXISTS idx_clients_company ON clients USING gin(company_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_clients_industry ON clients(industry);

CREATE INDEX IF NOT EXISTS idx_campaigns_client ON campaigns(client_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_dates ON campaigns(start_date, end_date);

CREATE INDEX IF NOT EXISTS idx_tasks_agent ON agent_tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_campaign ON agent_tasks(campaign_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON agent_tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON agent_tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_type ON agent_tasks(task_type);

CREATE INDEX IF NOT EXISTS idx_metrics_agent ON agent_metrics(agent_id);
CREATE INDEX IF NOT EXISTS idx_metrics_recorded ON agent_metrics(recorded_at);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(refresh_token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at);

CREATE INDEX IF NOT EXISTS idx_events_type ON analytics.system_events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_occurred ON analytics.system_events(occurred_at);

-- Инициализация базовых данных
-- Добавление администратора системы
INSERT INTO users (username, email, password_hash, full_name, role, is_active)
VALUES (
    'admin',
    'admin@ai-seo-architects.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewmVgdWP0q2x3K1q', -- bcrypt hash of 'secret'
    'System Administrator',
    'admin',
    true
) ON CONFLICT (username) DO NOTHING;

-- Инициализация 14 агентов системы
INSERT INTO agents (name, agent_id, agent_level, description, knowledge_base_path, is_active, config) VALUES
-- Executive Level (2)
('Chief SEO Strategist', 'chief_seo_strategist', 'executive', 'Стратегическое SEO планирование и алгоритмы поисковых систем', 'knowledge/executive/chief_seo_strategist.md', true, '{"mcp_enabled": true, "specialization": "strategic_planning"}'),
('Business Development Director', 'business_development_director', 'executive', 'Enterprise сделки 2.5M+ ₽/MRR и стратегические партнерства', 'knowledge/executive/business_development_director.md', true, '{"mcp_enabled": true, "specialization": "enterprise_sales"}'),

-- Management Level (4)
('Task Coordination Agent', 'task_coordination', 'management', 'LangGraph маршрутизация и приоритизация задач', 'knowledge/management/task_coordination_manager.md', true, '{"mcp_enabled": true, "specialization": "workflow_orchestration"}'),
('Sales Operations Manager', 'sales_operations_manager', 'management', 'Pipeline velocity и lead scoring с A/B testing', 'knowledge/management/sales_operations_manager.md', true, '{"mcp_enabled": true, "specialization": "sales_analytics"}'),
('Technical SEO Operations Manager', 'technical_seo_operations_manager', 'management', 'Core Web Vitals координация и log file анализ', 'knowledge/management/technical_seo_operations_manager.md', true, '{"mcp_enabled": true, "specialization": "technical_operations"}'),
('Client Success Manager', 'client_success_manager', 'management', 'Churn prediction и upselling матрицы с QBR generation', 'knowledge/management/client_success_manager.md', true, '{"mcp_enabled": true, "specialization": "client_retention"}'),

-- Operational Level (8)
('Lead Qualification Agent', 'lead_qualification', 'operational', 'BANT/MEDDIC квалификация с ML scoring', 'knowledge/operational/lead_qualification.md', true, '{"mcp_enabled": true, "specialization": "lead_scoring"}'),
('Proposal Generation Agent', 'proposal_generation', 'operational', 'Динамическое ценообразование и ROI калькуляции', 'knowledge/operational/proposal_generation.md', true, '{"mcp_enabled": true, "specialization": "proposal_automation"}'),
('Sales Conversation Agent', 'sales_conversation', 'operational', 'СПИН методология B2B переговоров с российской спецификой', 'knowledge/operational/sales_conversation.md', true, '{"mcp_enabled": true, "specialization": "conversation_optimization"}'),
('Technical SEO Auditor', 'technical_seo_auditor', 'operational', 'Комплексный технический SEO аудит и Core Web Vitals', 'knowledge/operational/technical_seo_auditor.md', true, '{"mcp_enabled": true, "specialization": "technical_analysis"}'),
('Content Strategy Agent', 'content_strategy', 'operational', 'Keyword research и контентная стратегия с E-E-A-T оптимизацией', 'knowledge/operational/content_strategy.md', true, '{"mcp_enabled": true, "specialization": "content_optimization"}'),
('Link Building Agent', 'link_building', 'operational', 'Outreach automation и domain authority с toxic link detection', 'knowledge/operational/link_building.md', true, '{"mcp_enabled": true, "specialization": "link_acquisition"}'),
('Competitive Analysis Agent', 'competitive_analysis', 'operational', 'SERP analysis и share of voice с competitive gap analysis', 'knowledge/operational/competitive_analysis.md', true, '{"mcp_enabled": true, "specialization": "market_intelligence"}'),
('Reporting Agent', 'reporting', 'operational', 'BI integration и automated insights с anomaly detection', 'knowledge/operational/reporting.md', true, '{"mcp_enabled": true, "specialization": "analytics_reporting"}')
ON CONFLICT (agent_id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    updated_at = CURRENT_TIMESTAMP;

-- Добавление тестовых клиентов для демонстрации
INSERT INTO clients (company_name, industry, website, annual_revenue, employee_count, country, contact_person, contact_email) VALUES
('TechCorp Solutions', 'SaaS', 'https://techcorp-solutions.com', 50000000, 250, 'RU', 'Алексей Петров', 'a.petrov@techcorp.com'),
('FinanceHub Ltd', 'FinTech', 'https://financehub.ru', 120000000, 450, 'RU', 'Мария Сидорова', 'm.sidorova@financehub.ru'),
('E-Commerce Plus', 'E-Commerce', 'https://ecom-plus.ru', 25000000, 150, 'RU', 'Дмитрий Кузнецов', 'd.kuznetsov@ecom-plus.ru')
ON CONFLICT (company_name) DO NOTHING;

-- Триггер для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Вставка начальных данных

-- Администратор по умолчанию (пароль: admin123)
INSERT INTO users (username, email, password_hash, full_name, role) 
VALUES (
    'admin',
    'admin@ai-seo-architects.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXzgVrqUm/5W',
    'System Administrator',
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- Вставка агентов системы
INSERT INTO agents (name, agent_id, agent_level, description, knowledge_base_path) VALUES
-- Executive Level
('Chief SEO Strategist', 'chief_seo_strategist', 'executive', 
 'Стратегическое SEO планирование и архитектура решений', 
 'knowledge/executive/chief_seo_strategist.md'),
('Business Development Director', 'business_development_director', 'executive',
 'Стратегический анализ и enterprise assessment',
 'knowledge/executive/business_development_director.md'),

-- Management Level  
('Task Coordinator', 'task_coordination', 'management',
 'Маршрутизация задач и приоритизация',
 'knowledge/management/task_coordination.md'),
('Sales Operations Manager', 'sales_operations_manager', 'management',
 'Pipeline velocity, lead scoring, A/B testing email campaigns',
 'knowledge/management/sales_operations_manager.md'),
('Technical SEO Operations Manager', 'technical_seo_operations_manager', 'management',
 'Core Web Vitals, crawling coordination, log file analysis',
 'knowledge/management/technical_seo_operations_manager.md'),
('Client Success Manager', 'client_success_manager', 'management',
 'Churn prediction, upselling матрицы, QBR generation',
 'knowledge/management/client_success_manager.md'),

-- Operational Level
('Lead Qualification Agent', 'lead_qualification', 'operational',
 'BANT/MEDDIC квалификация с ML scoring',
 'knowledge/operational/lead_qualification.md'),
('Sales Conversation Agent', 'sales_conversation', 'operational',
 'СПИН методология, B2B переговоры с российской спецификой',
 'knowledge/operational/sales_conversation.md'),
('Proposal Generation Agent', 'proposal_generation', 'operational',
 'Динамическое ценообразование, ROI калькуляции',
 'knowledge/operational/proposal_generation.md'),
('Technical SEO Auditor', 'technical_seo_auditor', 'operational',
 'Комплексный технический SEO аудит, Core Web Vitals, crawling',
 'knowledge/operational/technical_seo_auditor.md'),
('Content Strategy Agent', 'content_strategy', 'operational',
 'Keyword research, контентная стратегия, E-E-A-T оптимизация',
 'knowledge/operational/content_strategy.md'),
('Link Building Agent', 'link_building', 'operational',
 'Outreach automation, domain authority, toxic link detection',
 'knowledge/operational/link_building.md'),
('Competitive Analysis Agent', 'competitive_analysis', 'operational',
 'SERP analysis, share of voice, competitive gap analysis',
 'knowledge/operational/competitive_analysis.md'),
('Reporting Agent', 'reporting', 'operational',
 'BI integration, automated insights, anomaly detection',
 'knowledge/operational/reporting.md')

ON CONFLICT (agent_id) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    knowledge_base_path = EXCLUDED.knowledge_base_path,
    updated_at = CURRENT_TIMESTAMP;

-- Процедура для автоматического обновления материализованного представления
CREATE OR REPLACE FUNCTION refresh_dashboard_metrics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY analytics.dashboard_metrics;
END;
$$ LANGUAGE plpgsql;

-- Настройка автоматического обновления каждые 5 минут (через cron если доступен)
-- SELECT cron.schedule('refresh-dashboard', '*/5 * * * *', 'SELECT refresh_dashboard_metrics();');

-- Финальные команды
ANALYZE;

-- Вывод статистики
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_tuples
FROM pg_stat_user_tables 
WHERE schemaname IN ('ai_seo', 'analytics')
ORDER BY schemaname, tablename;

-- Сообщение об успешной инициализации
DO $$
BEGIN
    RAISE NOTICE '🎉 База данных AI SEO Architects успешно инициализирована!';
    RAISE NOTICE '👤 Создан администратор: admin / admin123';
    RAISE NOTICE '🤖 Добавлено агентов: %', (SELECT COUNT(*) FROM ai_seo.agents);
    RAISE NOTICE '📊 Схемы: ai_seo (основная), analytics (аналитика)';
END $$;