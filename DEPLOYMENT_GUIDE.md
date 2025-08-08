# 🚀 AI SEO Architects - Production Deployment Guide

Полное руководство по развертыванию enterprise-ready мультиагентной системы AI SEO Architects с FastAPI backend, RAG-системой, мониторингом и production инфраструктурой.

## 📋 Содержание

1. [Системные требования](#системные-требования)
2. [Быстрое развертывание](#быстрое-развертывание)  
3. [Production Infrastructure](#production-infrastructure)
4. [Конфигурация и безопасность](#конфигурация-и-безопасность)
5. [Мониторинг и наблюдение](#мониторинг-и-наблюдение)
6. [Масштабирование](#масштабирование)
7. [Обслуживание и troubleshooting](#обслуживание-и-troubleshooting)

## 🎯 Системные требования

### Минимальные требования
```yaml
Hardware:
  CPU: 2+ cores (4 cores рекомендуется)
  RAM: 8GB (16GB для production)
  Disk: 20GB SSD (50GB для production с логами)
  Network: 100Mbps стабильное соединение

Software:
  OS: Ubuntu 20.04+, CentOS 8+, RHEL 8+, macOS 12+, Windows 11 + WSL2
  Python: 3.11+ (3.12 рекомендуется)
  Docker: 20.10+ (для production deployment)
  Docker Compose: v2.0+ (CLI plugin предпочтителен)

External Dependencies:
  OpenAI API: Обязательно (GPT-4 доступ)
  Anthropic API: Опционально (для MCP enhancement)
  Internet: Стабильное соединение для AI API calls
```

### Production требования
```yaml
Infrastructure:
  Load Balancer: Nginx (включен в Docker stack)
  Database: PostgreSQL 15+ (8GB+ RAM для DB)
  Cache: Redis 7+ (4GB+ memory allocation)
  Monitoring: Prometheus + Grafana stack
  Security: SSL certificates, firewall configuration

Performance Targets:
  Throughput: 1000+ requests/min
  Response Time: <100ms average
  Uptime: 99.9% availability
  Concurrent Users: 100+ simultaneous
```

## 🚀 Быстрое развертывание

### Option 1: Development Setup (30 секунд)
```bash
# 1. Клонирование и переход в директорию
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# 2. Создание виртуального окружения (рекомендуется)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ИЛИ для Windows: venv\Scripts\activate

# 3. Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# 4. Настройка environment переменных
export OPENAI_API_KEY="your-openai-api-key-here"
export JWT_SECRET_KEY="your-secure-jwt-secret-at-least-32-chars"
export ENVIRONMENT="development"

# 5. 🚀 Запуск системы
python run_api.py

# ✅ Система доступна:
# - Dashboard: http://localhost:8000/dashboard
# - API Docs: http://localhost:8000/docs
# - Health Check: http://localhost:8000/health
```

### Option 2: Production Docker (2 минуты)
```bash
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# 1. Создание .env файла
cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-key-optional
POSTGRES_PASSWORD=your-secure-db-password
JWT_SECRET_KEY=your-super-secure-jwt-key
GRAFANA_PASSWORD=your-grafana-password
EOF

# 2. 🐳 Запуск всей инфраструктуры
docker-compose up -d

# ✅ Production инфраструктура развернута:
# - AI SEO API: http://localhost:8000 (Nginx proxy)
# - Grafana Monitoring: http://localhost:3000
# - Prometheus Metrics: http://localhost:9090  
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
# - ChromaDB: localhost:8001
```

#### Option 3: Быстрое тестирование системы
```bash
# Тестирование русскоязычных агентов с RAG
python test_russian_agents_integration.py

# Проверка FAISS векторной базы знаний
python test_all_agents_vectorization.py

# Тестирование всех API endpoints
python test_api_endpoints.py

# MCP интеграционные тесты
python test_mcp_integration.py
```

**🎉 Система готова! Доступные интерфейсы:**
- 🎛️ **Dashboard**: http://localhost:8000/dashboard
- 📚 **API Docs**: http://localhost:8000/docs  
- 🔍 **Health Check**: http://localhost:8000/health
- 📊 **Monitoring**: http://localhost:3000 (Grafana)
- 📈 **Metrics**: http://localhost:9090 (Prometheus)

## 🏗️ Production Infrastructure

### 🐳 Docker Services Overview

AI SEO Architects использует **8-service Docker Compose** архитектуру:

```yaml
Infrastructure Components:
  Application Tier:
    - ai-seo-api: FastAPI backend с WebSocket
    - nginx: Reverse proxy + SSL termination
    
  Data Tier:  
    - postgres: PostgreSQL 15 database
    - redis: Redis cache + sessions
    - chroma: ChromaDB vector database (optional)
    
  Monitoring Tier:
    - prometheus: Metrics collection
    - grafana: Dashboards + alerting
    
  Network:
    - ai-seo-network: Isolated container network
```

### 🔧 Advanced Configuration

#### Environment Variables (Production)
```bash
# Core Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000

# Security Configuration
JWT_SECRET_KEY=your-cryptographically-secure-64-char-key
DEFAULT_ADMIN_PASSWORD=YourSecureAdminPassword123!
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# AI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL_PRIMARY=gpt-4o
OPENAI_MODEL_SECONDARY=gpt-4o-mini
ANTHROPIC_API_KEY=your-anthropic-key-optional

# Database Configuration  
POSTGRES_PASSWORD=YourSecureDBPassword123!
DB_POOL_SIZE=25
DB_MAX_OVERFLOW=50

# Performance Tuning
REDIS_MAX_CONNECTIONS=100
RATE_LIMIT_ADMIN=2000
RATE_LIMIT_MANAGER=1000
RATE_LIMIT_OPERATOR=500

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_PASSWORD=YourGrafanaPassword123!
```

#### Resource Limits (docker-compose.yml)
```yaml
services:
  ai-seo-api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
    
  postgres:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'  
          memory: 2G
```

## 📊 Monitoring Setup

### Grafana Dashboard Configuration

The system provides comprehensive monitoring dashboards through Grafana:

#### Pre-configured Dashboards
```yaml
Available Dashboards:
  - AI SEO System Overview
  - Agent Performance Metrics
  - Database & Redis Monitoring
  - API Response Times & Throughput
  - Resource Utilization
  - Error Rate & Success Metrics
```

#### Dashboard Import
```bash
# Access Grafana
http://localhost:3000
Username: admin
Password: <GRAFANA_PASSWORD from .env>

# Import dashboards from monitoring/grafana/dashboards/
# - system-overview.json
# - agent-performance.json
# - database-metrics.json
```

#### Custom Metrics Configuration
```yaml
# Grafana datasources configuration
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
    
  - name: PostgreSQL
    type: postgres
    host: postgres:5432
    database: ai_seo_architects
    user: ai_seo_user
```

### Prometheus Metrics and Alerts

#### Key Metrics Collected
```promql
# System Metrics
ai_seo_cpu_percent
ai_seo_memory_percent
ai_seo_disk_usage_percent
ai_seo_network_io_bytes_total

# Application Metrics
ai_seo_http_requests_total{method, endpoint, status}
ai_seo_http_request_duration_seconds
ai_seo_active_connections
ai_seo_websocket_connections

# Agent-specific Metrics
ai_seo_agent_processing_time_seconds{agent_name}
ai_seo_agent_success_rate{agent_name}
ai_seo_agent_error_count{agent_name}
ai_seo_agent_queue_size{agent_name}

# Database Metrics
ai_seo_db_connections_active
ai_seo_db_query_duration_seconds
ai_seo_cache_hit_ratio
ai_seo_vector_search_time_seconds
```

#### Alert Rules Configuration
```yaml
# monitoring/prometheus/rules/alerts.yml
groups:
  - name: ai-seo-alerts
    rules:
      - alert: HighCPUUsage
        expr: ai_seo_cpu_percent > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          
      - alert: AgentFailureRate
        expr: ai_seo_agent_success_rate < 0.8
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ $labels.agent_name }} failure rate too high"
          
      - alert: DatabaseConnectionsHigh
        expr: ai_seo_db_connections_active > 80
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Database connection pool nearly exhausted"
```

### Health Monitoring and Alerts

#### Health Check Endpoints
```bash
# Overall system health
curl http://localhost:8000/health

# Individual service health
curl http://localhost:8000/health/database
curl http://localhost:8000/health/redis
curl http://localhost:8000/health/agents

# Detailed health with metrics
curl http://localhost:8000/health/detailed
```

#### Automated Health Monitoring
```bash
# monitoring/healthcheck.sh
#!/bin/bash
SERVICES=("api" "database" "redis" "agents")
WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"

for service in "${SERVICES[@]}"; do
  if ! curl -f -s http://localhost:8000/health/$service > /dev/null; then
    echo "ALERT: $service is unhealthy"
    if [[ -n "$WEBHOOK_URL" ]]; then
      curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"🚨 AI SEO Architects: $service is down\"}" \
        "$WEBHOOK_URL"
    fi
  fi
done
```

## 🔒 Security Best Practices

### Production Security Checklist

#### Environment Security
```bash
# 1. Generate secure secrets
POSTGRES_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
GRAFANA_PASSWORD=$(openssl rand -base64 16)

# 2. Set secure file permissions
chmod 600 .env
chown root:root .env

# 3. Disable debug mode
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

#### Access Control Configuration
```yaml
# User roles and permissions
security:
  roles:
    admin:
      - full_system_access
      - user_management
      - configuration_access
    manager:
      - agent_management
      - analytics_access
      - limited_config
    operator:
      - agent_execution
      - basic_analytics
      - read_only_config
      
  rate_limits:
    admin: 2000/hour
    manager: 1000/hour
    operator: 500/hour
    anonymous: 100/hour
```

### SSL/TLS Configuration

#### Let's Encrypt Setup (Production)
```bash
# Install Certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet --deploy-hook "docker-compose restart nginx"
```

#### Nginx SSL Configuration
```nginx
# nginx/conf.d/ssl.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Rate limiting
    limit_req zone=api_limit burst=20 nodelay;
    
    location / {
        proxy_pass http://ai-seo-api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Environment Variable Security

#### Secrets Management
```bash
# Use external secrets management in production
# Example with Docker Secrets
echo "your-secret-key" | docker secret create jwt_secret_key -
echo "your-db-password" | docker secret create postgres_password -

# Update docker-compose.yml
services:
  ai-seo-api:
    secrets:
      - jwt_secret_key
      - postgres_password
    environment:
      - JWT_SECRET_KEY_FILE=/run/secrets/jwt_secret_key
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password

secrets:
  jwt_secret_key:
    external: true
  postgres_password:
    external: true
```

#### Environment Validation
```python
# security/env_validator.py
import os
import re
from typing import List, Dict

def validate_production_env() -> Dict[str, bool]:
    """Validate production environment variables"""
    checks = {
        'jwt_secret_strong': len(os.getenv('JWT_SECRET_KEY', '')) >= 32,
        'postgres_password_strong': len(os.getenv('POSTGRES_PASSWORD', '')) >= 12,
        'debug_disabled': os.getenv('DEBUG', '').lower() == 'false',
        'environment_production': os.getenv('ENVIRONMENT') == 'production',
        'cors_origins_set': bool(os.getenv('CORS_ORIGINS')),
        'ssl_configured': bool(os.getenv('SSL_CERT_PATH') and os.getenv('SSL_KEY_PATH'))
    }
    
    return checks
```

### Firewall Configuration

#### UFW Setup (Ubuntu/Debian)
```bash
# Reset firewall
sudo ufw --force reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH access
sudo ufw allow 22/tcp

# HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Monitoring (restrict to specific IPs)
sudo ufw allow from 10.0.0.0/8 to any port 3000  # Grafana
sudo ufw allow from 10.0.0.0/8 to any port 9090  # Prometheus

# Block direct API access (force through nginx)
sudo ufw deny 8000/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose
```

#### iptables Advanced Rules
```bash
# Advanced iptables configuration
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -m limit --limit 4/min -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Rate limiting for API endpoints
sudo iptables -A INPUT -p tcp --dport 80 -m limit --limit 100/min --limit-burst 200 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -m limit --limit 100/min --limit-burst 200 -j ACCEPT

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

## 📈 Scaling & Performance

### Horizontal Scaling

#### Multi-instance API Deployment
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  ai-seo-api:
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
      update_config:
        parallelism: 1
        delay: 30s
        order: start-first
```

#### Load Balancer Configuration
```nginx
# nginx/conf.d/upstream.conf
upstream ai_seo_backend {
    least_conn;
    server ai-seo-api-1:8000 max_fails=3 fail_timeout=30s;
    server ai-seo-api-2:8000 max_fails=3 fail_timeout=30s;
    server ai-seo-api-3:8000 max_fails=3 fail_timeout=30s;
    
    # Health check
    keepalive 32;
}

server {
    location / {
        proxy_pass http://ai_seo_backend;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

#### Auto-scaling with Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.swarm.yml ai-seo-stack

# Scale service
docker service scale ai-seo-stack_ai-seo-api=5

# Update service
docker service update --image ai-seo-architects:latest ai-seo-stack_ai-seo-api
```

### Database Optimization

#### PostgreSQL Performance Tuning
```postgresql
-- postgresql.conf optimizations
shared_buffers = '256MB'                # 25% of RAM
effective_cache_size = '1GB'            # 75% of RAM
work_mem = '4MB'                        # Per connection
maintenance_work_mem = '64MB'           # For maintenance ops
checkpoint_completion_target = 0.9
wal_buffers = '16MB'
default_statistics_target = 100
random_page_cost = 1.1                  # For SSD

-- Connection pooling
max_connections = 200
shared_preload_libraries = 'pg_stat_statements'
```

#### Database Indexing Strategy
```sql
-- Agent performance indexes
CREATE INDEX CONCURRENTLY idx_agent_executions_timestamp 
ON agent_executions(created_at DESC);

CREATE INDEX CONCURRENTLY idx_agent_executions_status 
ON agent_executions(status, agent_name);

CREATE INDEX CONCURRENTLY idx_agent_executions_composite 
ON agent_executions(agent_name, status, created_at DESC);

-- Analytics indexes
CREATE INDEX CONCURRENTLY idx_analytics_events_timestamp 
ON analytics_events(timestamp DESC);

-- Partial indexes for active sessions
CREATE INDEX CONCURRENTLY idx_active_sessions 
ON user_sessions(user_id, expires_at) WHERE active = true;

-- Analyze tables after index creation
ANALYZE agent_executions;
ANALYZE analytics_events;
ANALYZE user_sessions;
```

#### Connection Pooling (PgBouncer)
```ini
# pgbouncer.ini
[databases]
ai_seo_architects = host=postgres port=5432 dbname=ai_seo_architects

[pgbouncer]
pool_mode = transaction
max_client_conn = 100
default_pool_size = 25
max_db_connections = 100
reserve_pool_size = 5
server_round_robin = 1
ignore_startup_parameters = extra_float_digits
```

### Caching Strategies

#### Redis Configuration Optimization
```redis
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000

# Persistence optimization
appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Network optimization
tcp-keepalive 300
timeout 300
```

#### Application-level Caching
```python
# caching/strategy.py
from enum import Enum
from typing import Optional, Any
import redis
import json
from datetime import timedelta

class CacheStrategy(Enum):
    AGENT_RESULTS = "agent_results"      # 1 hour
    USER_SESSIONS = "user_sessions"      # 24 hours  
    ANALYTICS_DATA = "analytics"         # 6 hours
    VECTOR_EMBEDDINGS = "embeddings"     # 7 days

CACHE_TTL = {
    CacheStrategy.AGENT_RESULTS: 3600,
    CacheStrategy.USER_SESSIONS: 86400,
    CacheStrategy.ANALYTICS_DATA: 21600,
    CacheStrategy.VECTOR_EMBEDDINGS: 604800,
}

class CacheManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def get_cache_key(self, strategy: CacheStrategy, identifier: str) -> str:
        return f"{strategy.value}:{identifier}"
    
    def set_cached_data(self, strategy: CacheStrategy, identifier: str, data: Any) -> bool:
        key = self.get_cache_key(strategy, identifier)
        ttl = CACHE_TTL[strategy]
        return self.redis.setex(key, ttl, json.dumps(data, default=str))
    
    def get_cached_data(self, strategy: CacheStrategy, identifier: str) -> Optional[Any]:
        key = self.get_cache_key(strategy, identifier)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None
```

#### CDN Configuration for Static Assets
```nginx
# Static asset optimization
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header X-Served-By "ai-seo-nginx";
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/css application/javascript image/svg+xml;
}
```

### Performance Tuning

#### FastAPI Optimization
```python
# performance/config.py
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

def configure_performance_middleware(app: FastAPI):
    # Gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Trusted hosts
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
    )

# Connection pool optimization
DATABASE_CONFIG = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "pool_pre_ping": True,
}

# Redis connection pool
REDIS_CONFIG = {
    "max_connections": 100,
    "retry_on_timeout": True,
    "socket_keepalive": True,
    "socket_keepalive_options": {},
}
```

#### Async Optimization
```python
# performance/async_config.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
import uvloop

# Use uvloop for better async performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Configure thread pool for CPU-bound tasks
CPU_BOUND_EXECUTOR = ThreadPoolExecutor(
    max_workers=4,
    thread_name_prefix="cpu_bound"
)

# Configure thread pool for I/O-bound tasks  
IO_BOUND_EXECUTOR = ThreadPoolExecutor(
    max_workers=20,
    thread_name_prefix="io_bound"
)

# Semaphore for controlling concurrent AI API calls
AI_API_SEMAPHORE = asyncio.Semaphore(10)
```

## 💾 Backup & Recovery

### Automated Backup Procedures

#### Database Backup Script
```bash
#!/bin/bash
# backup/db_backup.sh

set -euo pipefail

# Configuration
BACKUP_DIR="/var/backups/ai-seo-architects"
RETENTION_DAYS=30
DATE=$(date +"%Y%m%d_%H%M%S")
DB_NAME="ai_seo_architects"
DB_USER="ai_seo_user"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Create database backup
echo "Starting database backup..."
docker-compose exec -T postgres pg_dump \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --verbose \
    --clean \
    --if-exists \
    --format=custom \
    --no-owner \
    --no-privileges > "$BACKUP_DIR/db_backup_$DATE.sql"

# Compress backup
gzip "$BACKUP_DIR/db_backup_$DATE.sql"

# Remove old backups
find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Database backup completed: db_backup_$DATE.sql.gz"

# Verify backup integrity
if docker-compose exec -T postgres pg_restore --list "$BACKUP_DIR/db_backup_$DATE.sql.gz" > /dev/null 2>&1; then
    echo "✅ Backup integrity verified"
else
    echo "❌ Backup integrity check failed"
    exit 1
fi
```

#### Redis Backup Script
```bash
#!/bin/bash
# backup/redis_backup.sh

BACKUP_DIR="/var/backups/ai-seo-architects/redis"
DATE=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

# Trigger Redis save
docker-compose exec redis redis-cli BGSAVE

# Wait for background save to complete
while docker-compose exec redis redis-cli LASTSAVE | grep -q "$(docker-compose exec redis redis-cli LASTSAVE)"; do
    sleep 1
done

# Copy RDB file
docker-compose exec redis cp /data/dump.rdb "/backup/redis_backup_$DATE.rdb"

# Compress backup
docker-compose exec redis gzip "/backup/redis_backup_$DATE.rdb"

# Clean old backups
find "$BACKUP_DIR" -name "redis_backup_*.rdb.gz" -mtime +$RETENTION_DAYS -delete

echo "Redis backup completed: redis_backup_$DATE.rdb.gz"
```

### Database Backup and Restore

#### Automated Backup Scheduling
```bash
# Setup cron jobs
sudo crontab -e

# Daily database backup at 2 AM
0 2 * * * /opt/ai-seo-architects/backup/db_backup.sh

# Hourly Redis backup
0 */1 * * * /opt/ai-seo-architects/backup/redis_backup.sh

# Weekly configuration backup
0 3 * * 0 /opt/ai-seo-architects/backup/config_backup.sh

# Monthly cleanup of old backups
0 4 1 * * /opt/ai-seo-architects/backup/cleanup_backups.sh
```

#### Point-in-Time Recovery Setup
```bash
# Enable WAL archiving in PostgreSQL
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /var/lib/postgresql/wal_archive/%f'
max_wal_senders = 3
```

#### Database Restore Procedure
```bash
#!/bin/bash
# backup/restore_database.sh

BACKUP_FILE="$1"
DB_NAME="ai_seo_architects"
DB_USER="ai_seo_user"

if [[ -z "$BACKUP_FILE" ]]; then
    echo "Usage: $0 <backup_file.sql.gz>"
    exit 1
fi

echo "🚨 WARNING: This will REPLACE the current database!"
read -p "Are you sure? (yes/no): " confirm

if [[ "$confirm" != "yes" ]]; then
    echo "Restore cancelled"
    exit 1
fi

# Stop API to prevent new connections
docker-compose stop ai-seo-api

# Restore database
echo "Restoring database from $BACKUP_FILE..."
zcat "$BACKUP_FILE" | docker-compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME"

# Start API
docker-compose start ai-seo-api

echo "✅ Database restore completed"
```

### Configuration Backup

#### Environment and Configuration Backup
```bash
#!/bin/bash
# backup/config_backup.sh

BACKUP_DIR="/var/backups/ai-seo-architects/config"
DATE=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

# Create configuration archive
tar -czf "$BACKUP_DIR/config_backup_$DATE.tar.gz" \
    .env \
    docker-compose.yml \
    nginx/conf.d/ \
    monitoring/prometheus/ \
    monitoring/grafana/ \
    ssl/ \
    --exclude='*.log' \
    --exclude='*.tmp'

echo "Configuration backup completed: config_backup_$DATE.tar.gz"
```

#### Docker Volume Backup
```bash
#!/bin/bash
# backup/volume_backup.sh

VOLUMES=("ai-seo_postgres_data" "ai-seo_redis_data" "ai-seo_grafana_data")
BACKUP_DIR="/var/backups/ai-seo-architects/volumes"
DATE=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"

for volume in "${VOLUMES[@]}"; do
    echo "Backing up volume: $volume"
    
    docker run --rm \
        -v "$volume:/data" \
        -v "$BACKUP_DIR:/backup" \
        alpine tar czf "/backup/${volume}_$DATE.tar.gz" -C /data .
    
    echo "✅ Volume backup completed: ${volume}_$DATE.tar.gz"
done
```

### Disaster Recovery

#### Complete System Restore Procedure
```bash
#!/bin/bash
# disaster_recovery/full_restore.sh

set -euo pipefail

BACKUP_DATE="$1"
BACKUP_DIR="/var/backups/ai-seo-architects"

if [[ -z "$BACKUP_DATE" ]]; then
    echo "Usage: $0 <backup_date_YYYYMMDD_HHMMSS>"
    exit 1
fi

echo "🚨 DISASTER RECOVERY MODE"
echo "This will restore the complete system to state: $BACKUP_DATE"
read -p "Continue? (yes/no): " confirm

if [[ "$confirm" != "yes" ]]; then
    exit 1
fi

# 1. Stop all services
echo "Stopping all services..."
docker-compose down -v

# 2. Restore configuration
echo "Restoring configuration..."
tar -xzf "$BACKUP_DIR/config/config_backup_$BACKUP_DATE.tar.gz" -C /opt/ai-seo-architects/

# 3. Recreate volumes
echo "Recreating volumes..."
docker volume create ai-seo_postgres_data
docker volume create ai-seo_redis_data
docker volume create ai-seo_grafana_data

# 4. Restore volume data
for volume in postgres_data redis_data grafana_data; do
    echo "Restoring volume: ai-seo_$volume"
    docker run --rm \
        -v "ai-seo_$volume:/data" \
        -v "$BACKUP_DIR/volumes:/backup" \
        alpine tar xzf "/backup/ai-seo_${volume}_$BACKUP_DATE.tar.gz" -C /data
done

# 5. Start services
echo "Starting services..."
docker-compose up -d

# 6. Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# 7. Verify restoration
echo "Verifying system health..."
curl -f http://localhost:8000/health || {
    echo "❌ Health check failed"
    exit 1
}

echo "✅ Disaster recovery completed successfully"
echo "📊 Dashboard: http://localhost:8000/dashboard"
echo "📈 Monitoring: http://localhost:3000"
```

#### Recovery Testing
```bash
#!/bin/bash
# disaster_recovery/test_recovery.sh

# Create test environment
docker-compose -f docker-compose.test.yml up -d

# Test restore procedure
./disaster_recovery/full_restore.sh "$(date +"%Y%m%d_%H%M%S")"

# Run integration tests
python test_agents_integration.py
python test_api_endpoints.py

# Cleanup test environment
docker-compose -f docker-compose.test.yml down -v

echo "Recovery test completed"
```

## 🔧 Troubleshooting

### Common Deployment Issues

#### Service Startup Problems
```bash
# Debug service startup issues
docker-compose ps                    # Check service status
docker-compose logs ai-seo-api      # View API logs
docker-compose logs postgres        # View database logs
docker-compose logs redis           # View Redis logs

# Check resource usage
docker stats --no-stream

# Verify environment variables
docker-compose exec ai-seo-api env | grep -E "(API_|DB_|REDIS_)"

# Test database connection
docker-compose exec ai-seo-api python -c "
from database.connection import test_connection
print('DB Connection:', test_connection())
"
```

#### Port Conflicts Resolution
```bash
# Check port usage
netstat -tulnp | grep :8000
ss -tulnp | grep :8000

# Find and stop conflicting processes
sudo lsof -i :8000
sudo kill -9 <PID>

# Use alternative ports in docker-compose.yml
services:
  ai-seo-api:
    ports:
      - "8080:8000"  # Changed from 8000:8000
  nginx:
    ports:
      - "8081:80"    # Changed from 80:80
```

#### Memory and Resource Issues
```bash
# Monitor memory usage
free -h
docker system df
docker system prune -a  # Clean up unused resources

# Adjust memory limits
# docker-compose.yml
services:
  ai-seo-api:
    deploy:
      resources:
        limits:
          memory: 1G      # Reduce if needed
        reservations:
          memory: 512M
```

### Service Debugging

#### API Service Debugging
```bash
# Enable debug mode temporarily
docker-compose exec ai-seo-api python -c "
import os
os.environ['DEBUG'] = 'true'
os.environ['LOG_LEVEL'] = 'DEBUG'
from api.main import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
"

# Check API health endpoints
curl -v http://localhost:8000/health
curl -v http://localhost:8000/health/detailed

# Test individual agent endpoints
curl -X POST http://localhost:8000/api/agents/seo-analyst/execute \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "parameters": {}}'
```

#### Database Connection Issues
```bash
# Test PostgreSQL connectivity
docker-compose exec postgres pg_isready -U ai_seo_user

# Connect to database manually
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects

# Check database tables and data
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
FROM pg_stat_user_tables;
"

# Monitor active connections
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
SELECT pid, usename, application_name, client_addr, state, query_start 
FROM pg_stat_activity 
WHERE state = 'active';
"
```

#### Redis Connection Issues
```bash
# Test Redis connectivity
docker-compose exec redis redis-cli ping

# Check Redis info
docker-compose exec redis redis-cli info

# Monitor Redis operations
docker-compose exec redis redis-cli monitor

# Check cache keys
docker-compose exec redis redis-cli --scan --pattern "agent_*"
```

### Log Analysis

#### Structured Log Analysis
```bash
# Parse JSON logs with jq
docker-compose logs ai-seo-api | jq 'select(.level == "ERROR")'

# Find slow requests
docker-compose logs ai-seo-api | jq 'select(.processing_time_seconds > 5.0)'

# Agent-specific errors
docker-compose logs ai-seo-api | jq 'select(.agent_name == "seo-analyst" and .level == "ERROR")'

# Correlation ID tracking
docker-compose logs ai-seo-api | jq 'select(.correlation_id == "req_12345")'
```

#### Log Monitoring with Tail
```bash
# Real-time log monitoring
docker-compose logs -f ai-seo-api | grep -E "(ERROR|WARNING|CRITICAL)"

# Multi-service log monitoring
docker-compose logs -f | grep -E "(error|exception|failed)"

# WebSocket connection logs
docker-compose logs -f ai-seo-api | grep -i websocket
```

#### Log Rotation and Management
```bash
# Configure log rotation
# /etc/logrotate.d/ai-seo-architects
/var/lib/docker/containers/*/*-json.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
    postrotate
        docker-compose restart nginx
    endscript
}

# Manual log cleanup
docker system prune -a
docker volume prune
```

### Performance Issues

#### Response Time Analysis
```bash
# Measure API response times
time curl -s http://localhost:8000/health
time curl -s http://localhost:8000/api/agents/

# Load testing with Apache Bench
ab -n 100 -c 10 http://localhost:8000/health

# Monitor with htop/top
htop -p $(docker-compose exec ai-seo-api pgrep -f "python")
```

#### Database Performance Analysis
```bash
# Check slow queries
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
SELECT query, calls, total_time, mean_time, stddev_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
"

# Check table sizes
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"

# Analyze query plans
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
EXPLAIN ANALYZE SELECT * FROM agent_executions WHERE created_at > NOW() - INTERVAL '1 hour';
"
```

#### Memory Usage Optimization
```bash
# Check Python memory usage
docker-compose exec ai-seo-api python -c "
import psutil, os
process = psutil.Process(os.getpid())
print(f'Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB')
print(f'CPU: {process.cpu_percent()}%')
"

# Profile memory usage
docker-compose exec ai-seo-api pip install memory_profiler
docker-compose exec ai-seo-api python -m memory_profiler api/main.py
```

## 🔧 Maintenance

### Update Procedures

#### Application Updates
```bash
#!/bin/bash
# maintenance/update_app.sh

set -euo pipefail

echo "🔄 Starting AI SEO Architects update..."

# 1. Backup current state
./backup/full_backup.sh "pre_update_$(date +%Y%m%d_%H%M%S)"

# 2. Pull latest code
git fetch origin
git checkout main
git pull origin main

# 3. Update dependencies
pip install --upgrade -r requirements.txt

# 4. Run database migrations
python database/migrate.py

# 5. Update Docker images
docker-compose pull

# 6. Rolling update with zero downtime
docker-compose up -d --no-deps --build ai-seo-api

# 7. Wait for health check
sleep 30
curl -f http://localhost:8000/health || {
    echo "❌ Health check failed, rolling back..."
    docker-compose restart ai-seo-api
    exit 1
}

# 8. Update other services
docker-compose up -d

echo "✅ Update completed successfully"
```

#### Security Updates
```bash
#!/bin/bash
# maintenance/security_update.sh

# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Rotate secrets
NEW_JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(64))")
echo "New JWT secret generated, update .env file manually"

# Update SSL certificates
sudo certbot renew --dry-run

# Security audit
docker run --rm -v "$(pwd)":/src returntocorp/semgrep --config=auto /src

echo "🔒 Security update completed"
```

### Health Checks

#### Automated Health Monitoring
```bash
#!/bin/bash
# maintenance/health_monitor.sh

HEALTH_ENDPOINTS=(
    "http://localhost:8000/health"
    "http://localhost:8000/health/database"
    "http://localhost:8000/health/redis"
    "http://localhost:8000/health/agents"
)

ALERT_EMAIL="admin@yourdomain.com"
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"

check_health() {
    local endpoint="$1"
    local response
    local http_code
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$endpoint" 2>/dev/null)
    http_code=$(echo "$response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    
    if [[ "$http_code" -eq 200 ]]; then
        return 0
    else
        return 1
    fi
}

send_alert() {
    local message="$1"
    echo "$message"
    
    # Email alert
    if command -v mail >/dev/null 2>&1; then
        echo "$message" | mail -s "AI SEO Architects Alert" "$ALERT_EMAIL"
    fi
    
    # Slack alert
    if [[ -n "$SLACK_WEBHOOK" ]]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"🚨 $message\"}" \
            "$SLACK_WEBHOOK"
    fi
}

main() {
    local failed_checks=0
    
    for endpoint in "${HEALTH_ENDPOINTS[@]}"; do
        if ! check_health "$endpoint"; then
            send_alert "Health check failed for: $endpoint"
            ((failed_checks++))
        fi
    done
    
    if [[ $failed_checks -eq 0 ]]; then
        echo "✅ All health checks passed"
    else
        echo "❌ $failed_checks health checks failed"
        exit 1
    fi
}

main "$@"
```

#### Performance Health Checks
```bash
#!/bin/bash
# maintenance/performance_monitor.sh

# Check response times
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' http://localhost:8000/health)
if (( $(echo "$RESPONSE_TIME > 2.0" | bc -l) )); then
    echo "⚠️ High response time: ${RESPONSE_TIME}s"
fi

# Check memory usage
MEMORY_USAGE=$(docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}" | grep ai-seo-api | awk '{print $2}' | sed 's/MiB.*//')
if [[ $MEMORY_USAGE -gt 1500 ]]; then
    echo "⚠️ High memory usage: ${MEMORY_USAGE}MB"
fi

# Check disk space
DISK_USAGE=$(df /var/lib/docker | tail -1 | awk '{print $5}' | sed 's/%//')
if [[ $DISK_USAGE -gt 80 ]]; then
    echo "⚠️ High disk usage: ${DISK_USAGE}%"
fi

echo "📊 Performance check completed"
```

### System Maintenance

#### Database Maintenance
```bash
#!/bin/bash
# maintenance/db_maintenance.sh

# Vacuum and analyze database
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
VACUUM ANALYZE;
REINDEX DATABASE ai_seo_architects;
"

# Update statistics
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
ANALYZE;
"

# Clean up old data (older than 30 days)
docker-compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
DELETE FROM agent_executions WHERE created_at < NOW() - INTERVAL '30 days';
DELETE FROM analytics_events WHERE timestamp < NOW() - INTERVAL '30 days';
"

echo "🗄️ Database maintenance completed"
```

#### Cache Maintenance
```bash
#!/bin/bash
# maintenance/cache_maintenance.sh

# Redis memory optimization
docker-compose exec redis redis-cli MEMORY PURGE

# Clean expired keys
docker-compose exec redis redis-cli --scan --pattern "*" | while read -r key; do
    ttl=$(docker-compose exec redis redis-cli TTL "$key")
    if [[ "$ttl" == "-1" ]]; then
        echo "Key without TTL: $key"
    fi
done

# Analyze Redis memory usage
docker-compose exec redis redis-cli INFO memory

echo "🔄 Cache maintenance completed"
```

#### Log Cleanup
```bash
#!/bin/bash
# maintenance/log_cleanup.sh

LOG_DIR="/var/lib/docker/containers"
RETENTION_DAYS=7

# Clean Docker logs
find "$LOG_DIR" -name "*.log" -mtime +$RETENTION_DAYS -exec truncate -s 0 {} \;

# Clean application logs
find /opt/ai-seo-architects/logs -name "*.log" -mtime +$RETENTION_DAYS -delete

# Clean temp files
find /tmp -name "*ai-seo*" -mtime +1 -delete

echo "🧹 Log cleanup completed"
```

### Monitoring and Alerting

#### Alerting Configuration
```yaml
# monitoring/alertmanager/config.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@yourdomain.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
- name: 'web.hook'
  email_configs:
  - to: 'admin@yourdomain.com'
    subject: 'AI SEO Architects Alert: {{ .GroupLabels.alertname }}'
    body: |
      {{ range .Alerts }}
      Alert: {{ .Annotations.summary }}
      Description: {{ .Annotations.description }}
      Labels: {{ range .Labels.SortedPairs }} • {{ .Name }} = {{ .Value }} {{ end }}
      {{ end }}
  slack_configs:
  - api_url: '${SLACK_WEBHOOK_URL}'
    channel: '#alerts'
    title: 'AI SEO Architects Alert'
    text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

#### Custom Metrics Dashboard
```json
{
  "dashboard": {
    "title": "AI SEO Architects Operations",
    "panels": [
      {
        "title": "API Response Time",
        "type": "stat",
        "targets": [
          {
            "expr": "avg(ai_seo_http_request_duration_seconds)",
            "legendFormat": "Avg Response Time"
          }
        ]
      },
      {
        "title": "Agent Success Rate",
        "type": "stat", 
        "targets": [
          {
            "expr": "avg(ai_seo_agent_success_rate)",
            "legendFormat": "Success Rate"
          }
        ]
      },
      {
        "title": "Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "ai_seo_db_connections_active",
            "legendFormat": "Active Connections"
          }
        ]
      }
    ]
  }
}
```

---

**🚀 AI SEO Architects - Production Ready!**

This comprehensive deployment guide covers all aspects of production deployment, from basic setup to advanced monitoring and maintenance. The system is designed for enterprise-grade reliability and performance.

**Author**: Andrew Popov (a.popov.gv@gmail.com)  
**Version**: 2.0.0  
**Last Updated**: 2025-08-08