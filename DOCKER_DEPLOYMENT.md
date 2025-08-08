# 🐳 AI SEO Architects - Comprehensive Docker Deployment Guide

> **Production-ready Docker containerization с multi-service architecture**  
> Full orchestration: FastAPI + PostgreSQL + Redis + Nginx + Monitoring Stack

**Target Audience:** DevOps Engineers, System Administrators, Production Deployments  
**Deployment Time:** 5-15 minutes  
**Complexity Level:** Intermediate

---

## 📋 Contents

1. [🎯 Architecture Overview](#architecture-overview)
2. [⚙️ Prerequisites](#prerequisites)
3. [🚀 Quick Start](#quick-start)
4. [🔧 Advanced Configuration](#advanced-configuration)
5. [📊 Service Details](#service-details)
6. [🛡️ Security Configuration](#security-configuration)
7. [📈 Monitoring & Logging](#monitoring-logging)
8. [🔄 Maintenance & Updates](#maintenance-updates)
9. [🚨 Troubleshooting](#troubleshooting)

---

## 🎯 Architecture Overview

### **Multi-Service Docker Architecture**

AI SEO Architects utilizes a **comprehensive 8-service Docker Compose stack** for enterprise-grade deployment:

```yaml
Service Architecture:
  Application Layer:
    - ai-seo-api: FastAPI backend (Python 3.12)
    - ai-seo-nginx: Reverse proxy + SSL termination
    
  Data Layer:
    - postgres: PostgreSQL 15 primary database
    - redis: Redis 7 cache + session storage
    - chroma: ChromaDB vector database (optional)
    
  Monitoring Layer:
    - prometheus: Metrics collection
    - grafana: Visualization + alerting
    
  Network Layer:
    - ai-seo-network: Isolated Docker network
    - Shared volumes for persistent data
```

### **Container Communication**

```mermaid
graph TB
    Internet-->Nginx[Nginx Reverse Proxy]
    Nginx-->API[AI SEO API]
    API-->DB[PostgreSQL]
    API-->Cache[Redis]
    API-->Vector[ChromaDB]
    Prometheus-->API
    Prometheus-->DB
    Prometheus-->Cache
    Grafana-->Prometheus
```

## ⚙️ Prerequisites

### **System Requirements**

#### **Minimum Configuration**
```yaml
Hardware:
  CPU: 2 cores (x64 architecture)
  RAM: 8GB (4GB for containers + 4GB system)
  Storage: 40GB SSD (20GB for containers + 20GB system)
  Network: 100 Mbps stable connection
```

#### **Recommended Configuration**  
```yaml
Hardware:
  CPU: 4+ cores (Intel/AMD x64)
  RAM: 16GB+ (better performance for AI workloads)
  Storage: 100GB+ NVMe SSD (fast I/O for databases)
  Network: 1 Gbps unmetered
```

#### **Production Configuration**
```yaml
Hardware:
  CPU: 8+ cores (enterprise workloads)
  RAM: 32GB+ (high-availability setup)
  Storage: 200GB+ SSD with backup strategy
  Network: 1 Gbps+ with redundancy
  Backup: Automated daily backups
```

### **Software Prerequisites**

#### **Docker Installation (Required)**
```bash
# Install Docker Engine (latest stable)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Verify Docker installation
docker --version
# Expected: Docker version 24.0.0 or higher
```

#### **Docker Compose Installation (Required)**
```bash
# Docker Compose v2 (plugin method - recommended)
# Usually installed with Docker Engine

# Verify Docker Compose
docker compose version
# Expected: Docker Compose version v2.20.0 or higher

# Alternative: standalone installation if needed
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### **Additional Tools**
```bash
# Essential utilities
sudo apt update
sudo apt install -y git curl wget htop jq

# Optional but recommended
sudo apt install -y nano vim tree ncdu
```

### **Network Configuration**
```bash
# Check Docker daemon is running
sudo systemctl status docker
sudo systemctl enable docker

# Configure Docker to start on boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

## 🚀 Quick Start

### **Option 1: One-Command Deploy (Fastest)**
```bash
# Complete deployment in one command
curl -sSL https://raw.githubusercontent.com/Andrew821667/ai-seo-architects/main/deploy.sh | bash -s -- --quick-start

# Manual equivalent:
git clone https://github.com/Andrew821667/ai-seo-architects.git && \
cd ai-seo-architects && \
cp .env.example .env && \
echo "OPENAI_API_KEY=your-key-here" >> .env && \
docker compose up -d
```

### **Option 2: Step-by-Step Deployment**

#### **1. Repository Setup**
```bash
# Clone the project
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# Verify project structure
ls -la
# Expected: docker-compose.yml, .env.example, Dockerfile, etc.
```

#### **2. Environment Configuration**
```bash
# Create environment file from template
cp .env.example .env

# Edit configuration (required)
nano .env
# OR use your preferred editor: vim .env, code .env
```

#### **3. Critical Environment Variables**
```bash
# REQUIRED: Add your OpenAI API key
cat << EOF >> .env
# Essential Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
JWT_SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
GRAFANA_PASSWORD=$(openssl rand -base64 16)
EOF
```

#### **4. Docker Deployment**
```bash
# Pull latest images (recommended)
docker compose pull

# Start all services in background
docker compose up -d

# Wait for services to initialize (30-60 seconds)
sleep 60

# Verify deployment
docker compose ps
```

#### **5. Access Verification**
```bash
# Check all containers are running
docker compose ps
# Expected: All services should show "Up" status

# Test API health endpoint
curl -f http://localhost:8000/health
# Expected: {"status": "healthy", ...}

# Test dashboard access  
curl -I http://localhost:8000/dashboard
# Expected: HTTP/1.1 200 OK
```

### **Option 3: Development Mode**
```bash
# Development setup with hot reload
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# Development environment
cp .env.example .env.dev
sed -i 's/ENVIRONMENT=production/ENVIRONMENT=development/' .env.dev
sed -i 's/DEBUG=false/DEBUG=true/' .env.dev

# Start with development override
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### **Access Points After Deployment**

Once deployment is successful, the following services are available:

```yaml
Service Access Points:
  Application:
    - AI SEO API: http://your-server:8000
    - Web Dashboard: http://your-server:8000/dashboard  
    - API Documentation: http://your-server:8000/api/docs
    - Health Check: http://your-server:8000/health
    
  Monitoring:
    - Prometheus: http://your-server:9090
    - Grafana: http://your-server:3000 (admin/admin)
    
  Data Services:
    - PostgreSQL: your-server:5432 (internal)
    - Redis: your-server:6379 (internal)
    - ChromaDB: your-server:8001 (internal)
```

### **Initial Authentication**
Default admin credentials:
- **Username**: `admin`
- **Password**: `secret`

⚠️ **CRITICAL**: Change default password immediately after first login!

---

## 🔧 Advanced Configuration

### **Production Environment Variables**

#### **Essential Production Variables**
```bash
# .env.production
# ==========================================

# Security Configuration
JWT_SECRET_KEY=$(openssl rand -hex 64)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
GRAFANA_PASSWORD=$(openssl rand -base64 20)
SESSION_SECRET_KEY=$(openssl rand -hex 32)

# Database Configuration
DATABASE_URL=postgresql://ai_seo_user:${POSTGRES_PASSWORD}@postgres:5432/ai_seo_architects
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
DATABASE_POOL_TIMEOUT=30

# Redis Configuration
REDIS_URL=redis://redis:6379/0
REDIS_POOL_SIZE=20
REDIS_SOCKET_KEEPALIVE=True
REDIS_SOCKET_KEEPALIVE_OPTIONS={}

# AI Service Configuration
OPENAI_API_KEY=sk-your-production-openai-key
ANTHROPIC_API_KEY=your-production-anthropic-key
AI_REQUEST_TIMEOUT=300
AI_MAX_RETRIES=3

# Application Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=["https://yourdomain.com"]
ALLOWED_HOSTS=["yourdomain.com", "www.yourdomain.com"]

# Performance Configuration
WORKER_PROCESSES=4
WORKER_CONNECTIONS=1000
KEEPALIVE_TIMEOUT=2
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=50

# Security Headers
SECURE_SSL_REDIRECT=true
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SECURE_HSTS_SECONDS=31536000
SECURE_CONTENT_TYPE_NOSNIFF=true
SECURE_BROWSER_XSS_FILTER=true
```

### **Resource Limits and Scaling**

#### **Production docker-compose.override.yml**
```yaml
# docker-compose.override.yml
version: '3.8'

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
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "100m"
        max-file: "5"

  postgres:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
    command: >
      postgres -c max_connections=100
               -c shared_buffers=256MB
               -c effective_cache_size=1GB
               -c maintenance_work_mem=64MB
               -c checkpoint_completion_target=0.9
               -c wal_buffers=16MB
               -c default_statistics_target=100

  redis:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

  nginx:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.1'
          memory: 128M

  prometheus:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M

  grafana:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.1'
          memory: 128M
```

### **Custom Docker Compose Overrides**

#### **High-Availability Setup**
```yaml
# docker-compose.ha.yml
version: '3.8'

services:
  ai-seo-api:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 30s
        order: start-first
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

  nginx:
    volumes:
      - ./nginx/nginx-ha.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - ai-seo-api

networks:
  ai-seo-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### **Volume Management**

#### **Production Volume Configuration**
```bash
# Create named volumes for better management
docker volume create ai-seo-postgres-data
docker volume create ai-seo-redis-data
docker volume create ai-seo-chroma-data
docker volume create ai-seo-prometheus-data
docker volume create ai-seo-grafana-data

# Backup strategy
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# PostgreSQL backup
docker compose exec -T postgres pg_dump -U ai_seo_user ai_seo_architects | gzip > "$BACKUP_DIR/postgres_$DATE.sql.gz"

# Volume backups
docker run --rm -v ai-seo-postgres-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/postgres_volume_$DATE.tar.gz /data
docker run --rm -v ai-seo-redis-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/redis_volume_$DATE.tar.gz /data

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
```

---

## 📊 Service Details

### **AI SEO API Service (Core Application)**

```yaml
Service: ai-seo-api
Purpose: FastAPI backend application
Technology: Python 3.12 + FastAPI + Uvicorn
Resource Usage: 2-4GB RAM, 1-2 CPU cores
```

#### **Configuration Details**
```yaml
Ports:
  - 8000:8000 (HTTP API)
  
Dependencies:
  - postgres (database)
  - redis (cache/sessions)
  - chroma (vector database)
  
Environment Variables:
  - OPENAI_API_KEY (required)
  - DATABASE_URL (auto-configured)
  - REDIS_URL (auto-configured)
  
Health Check:
  - Endpoint: /health
  - Interval: 30s
  - Timeout: 10s
  - Retries: 3
  
Startup Sequence:
  1. Wait for PostgreSQL (30s timeout)
  2. Run database migrations
  3. Initialize AI agents
  4. Start Uvicorn server
```

#### **API Service Scaling**
```bash
# Scale API instances
docker compose up -d --scale ai-seo-api=3

# Load balancing via Nginx
upstream api_backend {
    server ai-seo-api_1:8000;
    server ai-seo-api_2:8000;
    server ai-seo-api_3:8000;
}
```

### **PostgreSQL Service (Primary Database)**

```yaml
Service: postgres
Purpose: Primary relational database
Technology: PostgreSQL 15
Resource Usage: 1-2GB RAM, 0.5-1 CPU cores
```

#### **Configuration Details**
```yaml
Ports:
  - 5432:5432 (internal only)
  
Volumes:
  - postgres_data:/var/lib/postgresql/data
  - ./init-scripts:/docker-entrypoint-initdb.d/
  
Environment Variables:
  - POSTGRES_DB=ai_seo_architects
  - POSTGRES_USER=ai_seo_user
  - POSTGRES_PASSWORD (from .env)
  
Health Check:
  - Command: pg_isready -U ai_seo_user -d ai_seo_architects
  - Interval: 10s
  - Timeout: 5s
  
Performance Tuning:
  - max_connections=100
  - shared_buffers=256MB
  - effective_cache_size=1GB
  - maintenance_work_mem=64MB
```

### **Redis Service (Cache & Sessions)**

```yaml
Service: redis
Purpose: Cache and session storage
Technology: Redis 7
Resource Usage: 256MB-1GB RAM, 0.25 CPU cores
```

#### **Configuration Details**
```yaml
Ports:
  - 6379:6379 (internal only)
  
Volumes:
  - redis_data:/data
  
Configuration:
  - maxmemory: 512mb
  - maxmemory-policy: allkeys-lru
  - persistence: RDB + AOF
  
Health Check:
  - Command: redis-cli ping
  - Interval: 10s
  - Timeout: 3s
```

### **Nginx Service (Reverse Proxy)**

```yaml
Service: nginx
Purpose: Reverse proxy and SSL termination
Technology: Nginx 1.25
Resource Usage: 128MB RAM, 0.1-0.5 CPU cores
```

#### **Configuration Details**
```yaml
Ports:
  - 80:80 (HTTP)
  - 443:443 (HTTPS)
  
Volumes:
  - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  - ./ssl:/etc/nginx/ssl:ro
  
Features:
  - SSL/TLS termination
  - Load balancing
  - Static file serving
  - Request rate limiting
  - Gzip compression
  
Security Headers:
  - X-Frame-Options: DENY
  - X-Content-Type-Options: nosniff
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security: max-age=31536000
```

### **ChromaDB Service (Vector Database)**

```yaml
Service: chroma
Purpose: Vector embeddings storage
Technology: ChromaDB
Resource Usage: 512MB-2GB RAM, 0.5-1 CPU cores
```

#### **Configuration Details**
```yaml
Ports:
  - 8001:8000 (internal only)
  
Volumes:
  - chroma_data:/chroma/chroma
  
Environment Variables:
  - IS_PERSISTENT=TRUE
  - PERSIST_DIRECTORY=/chroma/chroma
  
Health Check:
  - Endpoint: /api/v1/heartbeat
  - Interval: 30s
  - Timeout: 10s
```

### **Prometheus Service (Metrics Collection)**

```yaml
Service: prometheus
Purpose: Metrics collection and storage
Technology: Prometheus 2.45
Resource Usage: 256MB-1GB RAM, 0.25-1 CPU cores
```

#### **Configuration Details**
```yaml
Ports:
  - 9090:9090 (metrics UI)
  
Volumes:
  - ./monitoring/prometheus:/etc/prometheus:ro
  - prometheus_data:/prometheus
  
Scrape Targets:
  - ai-seo-api:8000/metrics (30s interval)
  - postgres:5432 (via postgres_exporter)
  - redis:6379 (via redis_exporter)
  - node-exporter:9100 (system metrics)
  
Retention: 30 days
Storage: Local TSDB
```

### **Grafana Service (Visualization)**

```yaml
Service: grafana
Purpose: Metrics visualization and alerting
Technology: Grafana 10
Resource Usage: 128MB-512MB RAM, 0.1-0.5 CPU cores
```

#### **Configuration Details**
```yaml
Ports:
  - 3000:3000 (dashboard UI)
  
Volumes:
  - grafana_data:/var/lib/grafana
  - ./monitoring/grafana:/etc/grafana/provisioning:ro
  
Data Sources:
  - Prometheus (metrics)
  - PostgreSQL (application data)
  
Pre-configured Dashboards:
  - Application Performance
  - Infrastructure Monitoring
  - Database Performance
  - API Request Analytics
```

### **Service Dependencies & Startup Order**

```yaml
Startup Sequence:
  1. postgres (database foundation)
  2. redis (cache layer)
  3. chroma (vector database)
  4. ai-seo-api (application)
  5. nginx (reverse proxy)
  6. prometheus (metrics)
  7. grafana (visualization)
  
Health Check Cascade:
  postgres -> redis -> chroma -> ai-seo-api -> nginx
  
Dependency Matrix:
  ai-seo-api: [postgres, redis, chroma]
  nginx: [ai-seo-api]
  prometheus: [ai-seo-api, postgres, redis]
  grafana: [prometheus]
```

---

## 🛡️ Security Configuration

### **Container Security Best Practices**

#### **User Privileges & Non-Root Execution**
```dockerfile
# Dockerfile security enhancements
FROM python:3.12-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set secure file permissions
RUN chown -R appuser:appuser /app
USER appuser

# Security scanning
RUN pip install safety
RUN safety check --json
```

#### **Container Runtime Security**
```yaml
# docker-compose.security.yml
services:
  ai-seo-api:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
    
  postgres:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
      - FOWNER
      - SETGID
      - SETUID
```

### **Network Isolation**

#### **Custom Network Configuration**
```yaml
# Network security isolation
networks:
  ai-seo-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
    driver_opts:
      com.docker.network.bridge.enable_icc: "false"
      com.docker.network.bridge.enable_ip_masquerade: "true"
      com.docker.network.driver.mtu: "1500"

  monitoring-network:
    driver: bridge
    internal: true  # No external access
    ipam:
      config:
        - subnet: 172.21.0.0/16
```

#### **Service Network Segmentation**
```yaml
services:
  ai-seo-api:
    networks:
      - ai-seo-network
      - monitoring-network
    
  postgres:
    networks:
      - ai-seo-network  # Only internal access
    
  prometheus:
    networks:
      - monitoring-network  # Isolated monitoring
    
  nginx:
    networks:
      - ai-seo-network
    ports:
      - "80:80"
      - "443:443"
```

### **Secret Management**

#### **Docker Secrets Implementation**
```yaml
# docker-compose.secrets.yml
version: '3.8'

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
  openai_api_key:
    file: ./secrets/openai_api_key.txt

services:
  ai-seo-api:
    secrets:
      - jwt_secret
      - openai_api_key
    environment:
      - JWT_SECRET_KEY_FILE=/run/secrets/jwt_secret
      - OPENAI_API_KEY_FILE=/run/secrets/openai_api_key
  
  postgres:
    secrets:
      - db_password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
```

#### **Secret Generation Script**
```bash
#!/bin/bash
# generate-secrets.sh

SECRETS_DIR="./secrets"
mkdir -p "$SECRETS_DIR"
chmod 700 "$SECRETS_DIR"

# Generate secure passwords
openssl rand -base64 32 > "$SECRETS_DIR/db_password.txt"
openssl rand -hex 64 > "$SECRETS_DIR/jwt_secret.txt"

# Set secure permissions
chmod 600 "$SECRETS_DIR"/*
chown root:root "$SECRETS_DIR"/*

echo "Secrets generated in $SECRETS_DIR"
echo "Remember to add your OpenAI API key to $SECRETS_DIR/openai_api_key.txt"
```

### **Image Security**

#### **Security Scanning Pipeline**
```bash
#!/bin/bash
# security-scan.sh

# Vulnerability scanning with Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image ai-seo-architects_ai-seo-api:latest

# Container security benchmarks
docker run --rm --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /etc:/etc:ro \
  --label docker_bench_security \
  docker/docker-bench-security

# Image signature verification
export DOCKER_CONTENT_TRUST=1
docker pull python:3.12-slim
```

#### **Base Image Security**
```dockerfile
# Use minimal, security-focused base images
FROM python:3.12-slim-bullseye

# Update package lists and install security updates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Remove unnecessary packages
RUN apt-get autoremove -y && apt-get autoclean

# Set security labels
LABEL security.scan="enabled"
LABEL security.updates="auto"
```

---

## 📈 Monitoring & Logging

### **Prometheus Configuration**

#### **Custom Prometheus Config**
```yaml
# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'ai-seo-production'
    replica: 'prometheus-1'

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'ai-seo-api'
    static_configs:
      - targets: ['ai-seo-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
    scrape_timeout: 10s
    
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
    scrape_interval: 30s
    
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
    scrape_interval: 30s
    
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
    scrape_interval: 30s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

#### **Alert Rules Configuration**
```yaml
# monitoring/prometheus/alert_rules.yml
groups:
  - name: ai-seo-api
    rules:
      - alert: APIHighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket{job="ai-seo-api"}) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API latency detected"
          description: "95th percentile latency is {{ $value }}s"
      
      - alert: APIHighErrorRate
        expr: rate(http_requests_total{job="ai-seo-api",status=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High API error rate"
          description: "Error rate is {{ $value }} req/sec"
  
  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: cpu_usage_percent > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value }}%"
      
      - alert: HighMemoryUsage
        expr: memory_usage_percent > 90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}%"
      
      - alert: DatabaseConnectionsHigh
        expr: postgres_connections > 80
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "High database connections"
          description: "{{ $value }} connections active"
```

### **Grafana Setup and Dashboards**

#### **Automated Dashboard Provisioning**
```yaml
# monitoring/grafana/provisioning/dashboards/dashboard.yml
apiVersion: 1

providers:
  - name: 'ai-seo-dashboards'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
```

#### **Data Source Configuration**
```yaml
# monitoring/grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    
  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    database: ai_seo_architects
    user: ai_seo_user
    secureJsonData:
      password: "${POSTGRES_PASSWORD}"
    jsonData:
      sslmode: "disable"
      maxOpenConns: 0
      maxIdleConns: 2
      connMaxLifetime: 14400
```

#### **Application Performance Dashboard**
```json
{
  "dashboard": {
    "title": "AI SEO Architects - Application Performance",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"ai-seo-api\"}[5m])",
            "legendFormat": "{{method}} {{handler}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket{job=\"ai-seo-api\"})",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, http_request_duration_seconds_bucket{job=\"ai-seo-api\"})",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"ai-seo-api\",status=~\"5..\"}[5m])",
            "legendFormat": "Errors/sec"
          }
        ]
      }
    ]
  }
}
```

### **Log Aggregation**

#### **Centralized Logging with ELK Stack**
```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
  
  logstash:
    image: logstash:8.8.0
    volumes:
      - ./logging/logstash:/usr/share/logstash/pipeline:ro
    ports:
      - "5044:5044"
    depends_on:
      - elasticsearch
  
  kibana:
    image: kibana:8.8.0
    environment:
      - ELASTICSEARCH_URL=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

  filebeat:
    image: elastic/filebeat:8.8.0
    user: root
    volumes:
      - ./logging/filebeat:/usr/share/filebeat/config:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: filebeat -e -c /usr/share/filebeat/config/filebeat.yml
    depends_on:
      - logstash
```

#### **Application Logging Configuration**
```python
# Application logging setup
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
            
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/application.log')
    ]
)
```

### **Performance Monitoring**

#### **Application Performance Monitoring (APM)**
```python
# APM integration with OpenTelemetry
from opentelemetry import trace, metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Initialize tracing
tracer = trace.get_tracer(__name__)

# Initialize metrics
metrics.set_meter_provider(
    MeterProvider(
        metric_readers=[
            PrometheusMetricReader(),
        ]
    )
)
meter = metrics.get_meter(__name__)

# Create custom metrics
request_counter = meter.create_counter(
    name="api_requests_total",
    description="Total API requests",
    unit="1"
)

request_duration = meter.create_histogram(
    name="api_request_duration_seconds",
    description="API request duration",
    unit="s"
)

# Usage in FastAPI endpoints
@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()
    
    with tracer.start_as_current_span(f"{request.method} {request.url.path}") as span:
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        request_counter.add(1, {
            "method": request.method,
            "endpoint": request.url.path,
            "status_code": response.status_code
        })
        
        request_duration.record(duration, {
            "method": request.method,
            "endpoint": request.url.path
        })
        
        span.set_attribute("http.status_code", response.status_code)
        span.set_attribute("http.duration", duration)
    
    return response
```

---

## 🔄 Maintenance & Updates

### **Container Updates**

#### **Rolling Update Strategy**
```bash
#!/bin/bash
# rolling-update.sh

set -e

echo "Starting rolling update process..."

# 1. Pull latest images
echo "Pulling latest images..."
docker compose pull

# 2. Update non-critical services first
echo "Updating monitoring services..."
docker compose up -d --no-deps prometheus grafana

# 3. Update data services with minimal downtime
echo "Updating database services..."
docker compose stop redis
docker compose up -d redis
sleep 10

# 4. Update application with zero downtime
echo "Performing zero-downtime application update..."

# Scale up with new version
docker compose up -d --scale ai-seo-api=3 --no-recreate ai-seo-api

# Wait for new instances to be healthy
sleep 30
for i in {1..10}; do
    if curl -f http://localhost:8000/health; then
        echo "New instances are healthy"
        break
    fi
    sleep 5
done

# Update nginx configuration if needed
docker compose up -d --no-deps nginx

# Scale down old instances
docker compose up -d --scale ai-seo-api=2 ai-seo-api
sleep 30
docker compose up -d --scale ai-seo-api=1 ai-seo-api

echo "Rolling update completed successfully!"
```

#### **Blue-Green Deployment**
```bash
#!/bin/bash
# blue-green-deploy.sh

CURRENT_ENV=${1:-blue}
TARGET_ENV=${2:-green}

echo "Deploying to $TARGET_ENV environment..."

# Deploy to target environment
docker compose -f docker-compose.yml -f docker-compose.$TARGET_ENV.yml up -d

# Health check
sleep 60
if curl -f http://localhost:800${TARGET_ENV#blue}0/health; then
    echo "Health check passed for $TARGET_ENV"
    
    # Switch traffic
    docker compose -f docker-compose.yml -f docker-compose.proxy.yml \
        exec nginx nginx -s reload
    
    echo "Traffic switched to $TARGET_ENV"
    
    # Stop old environment
    docker compose -f docker-compose.yml -f docker-compose.$CURRENT_ENV.yml down
    echo "Old environment ($CURRENT_ENV) stopped"
else
    echo "Health check failed for $TARGET_ENV"
    docker compose -f docker-compose.yml -f docker-compose.$TARGET_ENV.yml down
    exit 1
fi
```

### **Database Migrations**

#### **Automated Migration System**
```python
# migrations/migration_manager.py
import asyncio
import logging
from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command

class MigrationManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.alembic_cfg = Config("alembic.ini")
        
    async def check_migration_status(self):
        """Check current migration status"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT version_num FROM alembic_version"
                ))
                current_version = result.fetchone()[0]
                return current_version
        except Exception as e:
            logging.error(f"Failed to check migration status: {e}")
            return None
    
    async def run_migrations(self):
        """Run pending migrations"""
        try:
            command.upgrade(self.alembic_cfg, "head")
            logging.info("Migrations completed successfully")
            return True
        except Exception as e:
            logging.error(f"Migration failed: {e}")
            return False
    
    async def create_backup(self):
        """Create database backup before migration"""
        import subprocess
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"/backups/pre_migration_{timestamp}.sql"
        
        cmd = [
            "pg_dump",
            "--no-password",
            "--clean",
            "--create",
            self.database_url,
            "-f", backup_file
        ]
        
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"Backup created: {backup_file}")
            return backup_file
        except subprocess.CalledProcessError as e:
            logging.error(f"Backup failed: {e}")
            return None
```

#### **Migration Deployment Script**
```bash
#!/bin/bash
# migrate-deploy.sh

set -e

echo "Starting migration deployment..."

# 1. Create backup
echo "Creating database backup..."
docker compose exec postgres pg_dump -U ai_seo_user ai_seo_architects \
    > "backup_$(date +%Y%m%d_%H%M%S).sql"

# 2. Check migration status
echo "Checking migration status..."
docker compose exec ai-seo-api python -c "
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT version_num FROM alembic_version'))
    print(f'Current version: {result.fetchone()[0]}')
"

# 3. Run migrations
echo "Running migrations..."
docker compose exec ai-seo-api alembic upgrade head

# 4. Verify migration
echo "Verifying migration..."
docker compose exec ai-seo-api python -c "
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT version_num FROM alembic_version'))
    print(f'New version: {result.fetchone()[0]}')
"

# 5. Restart application
echo "Restarting application..."
docker compose restart ai-seo-api

# 6. Health check
sleep 30
if curl -f http://localhost:8000/health; then
    echo "Migration deployment completed successfully!"
else
    echo "Health check failed after migration!"
    exit 1
fi
```

### **Backup Procedures**

#### **Comprehensive Backup Strategy**
```bash
#!/bin/bash
# backup-system.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "Starting system backup..."

# 1. Database backup
echo "Backing up PostgreSQL..."
docker compose exec -T postgres pg_dump -U ai_seo_user \
    --clean --create --if-exists ai_seo_architects \
    | gzip > "$BACKUP_DIR/postgres_$DATE.sql.gz"

# 2. Redis backup
echo "Backing up Redis..."
docker compose exec -T redis redis-cli --rdb - \
    | gzip > "$BACKUP_DIR/redis_$DATE.rdb.gz"

# 3. Application data backup
echo "Backing up application data..."
docker run --rm \
    -v ai-seo-architects_postgres_data:/data/postgres:ro \
    -v ai-seo-architects_redis_data:/data/redis:ro \
    -v ai-seo-architects_chroma_data:/data/chroma:ro \
    -v "$BACKUP_DIR":/backup \
    alpine tar czf "/backup/volumes_$DATE.tar.gz" /data

# 4. Configuration backup
echo "Backing up configuration..."
tar czf "$BACKUP_DIR/config_$DATE.tar.gz" \
    .env docker-compose.yml nginx/ monitoring/

# 5. Application logs backup
echo "Backing up logs..."
docker compose logs --no-color > "$BACKUP_DIR/logs_$DATE.txt"
gzip "$BACKUP_DIR/logs_$DATE.txt"

# 6. Cleanup old backups
echo "Cleaning up old backups..."
find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete

# 7. Backup verification
echo "Verifying backups..."
for file in "$BACKUP_DIR"/*_$DATE.*; do
    if [ -f "$file" ]; then
        size=$(stat -c%s "$file")
        if [ $size -gt 0 ]; then
            echo "✓ $(basename "$file"): $size bytes"
        else
            echo "✗ $(basename "$file"): Empty file!"
        fi
    fi
done

echo "Backup completed: $DATE"
```

#### **Restore Procedures**
```bash
#!/bin/bash
# restore-system.sh

BACKUP_DATE=${1}
BACKUP_DIR="/backups"

if [ -z "$BACKUP_DATE" ]; then
    echo "Usage: $0 <backup_date>"
    echo "Available backups:"
    ls -la "$BACKUP_DIR"/postgres_* | awk '{print $9}' | sed 's/.*postgres_//' | sed 's/.sql.gz//'
    exit 1
fi

echo "Restoring system from backup: $BACKUP_DATE"

# 1. Stop services
echo "Stopping services..."
docker compose down

# 2. Restore database
echo "Restoring PostgreSQL..."
docker compose up -d postgres
sleep 30

zcat "$BACKUP_DIR/postgres_$BACKUP_DATE.sql.gz" | \
    docker compose exec -T postgres psql -U ai_seo_user

# 3. Restore Redis
echo "Restoring Redis..."
docker compose stop redis
zcat "$BACKUP_DIR/redis_$BACKUP_DATE.rdb.gz" > /tmp/dump.rdb
docker run --rm \
    -v ai-seo-architects_redis_data:/data \
    -v /tmp/dump.rdb:/data/dump.rdb \
    redis:7 redis-server --save ""

# 4. Restore volumes
echo "Restoring application data..."
docker run --rm \
    -v ai-seo-architects_postgres_data:/data/postgres \
    -v ai-seo-architects_redis_data:/data/redis \
    -v ai-seo-architects_chroma_data:/data/chroma \
    -v "$BACKUP_DIR":/backup \
    alpine tar xzf "/backup/volumes_$BACKUP_DATE.tar.gz"

# 5. Restore configuration
echo "Restoring configuration..."
tar xzf "$BACKUP_DIR/config_$BACKUP_DATE.tar.gz"

# 6. Start services
echo "Starting services..."
docker compose up -d

# 7. Health check
echo "Waiting for services to start..."
sleep 60

if curl -f http://localhost:8000/health; then
    echo "Restore completed successfully!"
else
    echo "Health check failed after restore!"
    exit 1
fi
```

### **Scaling Operations**

#### **Horizontal Scaling**
```bash
#!/bin/bash
# scale-services.sh

SERVICE=${1}
REPLICAS=${2}

if [ -z "$SERVICE" ] || [ -z "$REPLICAS" ]; then
    echo "Usage: $0 <service> <replicas>"
    echo "Available services: ai-seo-api, postgres, redis"
    exit 1
fi

echo "Scaling $SERVICE to $REPLICAS replicas..."

case $SERVICE in
    "ai-seo-api")
        # Scale API with load balancer update
        docker compose up -d --scale ai-seo-api=$REPLICAS ai-seo-api
        
        # Update Nginx configuration
        cat > nginx/upstream.conf << EOF
upstream api_backend {
$(for i in $(seq 1 $REPLICAS); do
    echo "    server ai-seo-api_$i:8000;"
done)
}
EOF
        
        docker compose restart nginx
        ;;
        
    "postgres")
        if [ $REPLICAS -gt 1 ]; then
            echo "Setting up PostgreSQL replication..."
            # Implement read replicas
            docker compose -f docker-compose.yml -f docker-compose.postgres-replica.yml \
                up -d --scale postgres-replica=$((REPLICAS-1))
        fi
        ;;
        
    *)
        echo "Standard scaling for $SERVICE"
        docker compose up -d --scale $SERVICE=$REPLICAS $SERVICE
        ;;
esac

echo "Scaling completed. Current status:"
docker compose ps $SERVICE
```

#### **Auto-scaling Configuration**
```python
# autoscaler.py
import asyncio
import docker
import psutil
from prometheus_client.parser import text_string_to_metric_families

class AutoScaler:
    def __init__(self):
        self.client = docker.from_env()
        self.min_replicas = 1
        self.max_replicas = 5
        self.cpu_threshold = 70
        self.memory_threshold = 80
        
    async def get_metrics(self):
        """Get current resource utilization"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        return cpu_percent, memory_percent
    
    async def get_container_count(self, service_name):
        """Get current container count for service"""
        containers = self.client.containers.list(
            filters={"label": f"com.docker.compose.service={service_name}"}
        )
        return len(containers)
    
    async def scale_service(self, service_name, target_replicas):
        """Scale service to target replicas"""
        import subprocess
        
        cmd = [
            "docker", "compose", "up", "-d", 
            "--scale", f"{service_name}={target_replicas}",
            service_name
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"Scaled {service_name} to {target_replicas} replicas")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to scale {service_name}: {e}")
            return False
    
    async def evaluate_scaling(self):
        """Evaluate if scaling is needed"""
        cpu_percent, memory_percent = await self.get_metrics()
        current_replicas = await self.get_container_count("ai-seo-api")
        
        # Scale up conditions
        if (cpu_percent > self.cpu_threshold or 
            memory_percent > self.memory_threshold) and \
           current_replicas < self.max_replicas:
            
            new_replicas = min(current_replicas + 1, self.max_replicas)
            await self.scale_service("ai-seo-api", new_replicas)
            
        # Scale down conditions
        elif (cpu_percent < self.cpu_threshold * 0.5 and 
              memory_percent < self.memory_threshold * 0.5) and \
             current_replicas > self.min_replicas:
            
            new_replicas = max(current_replicas - 1, self.min_replicas)
            await self.scale_service("ai-seo-api", new_replicas)
    
    async def run(self):
        """Run auto-scaler daemon"""
        while True:
            try:
                await self.evaluate_scaling()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Auto-scaler error: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    scaler = AutoScaler()
    asyncio.run(scaler.run())
```

---

## 🚨 Troubleshooting

### **Common Docker Issues**

#### **Container Startup Problems**

**Service Dependencies Not Ready**
```bash
# Problem: Service starts before dependencies are ready
# Solution: Implement health checks and wait conditions

# Check service health
docker compose exec ai-seo-api curl -f http://localhost:8000/health

# View startup logs
docker compose logs -f ai-seo-api --tail=50

# Manual dependency check
docker compose exec ai-seo-api nc -z postgres 5432
docker compose exec ai-seo-api nc -z redis 6379
```

**Port Conflicts**
```bash
# Problem: Port already in use
# Check what's using the port
sudo netstat -tulpn | grep :8000
sudo lsof -i :8000

# Solution: Kill conflicting process or change port
sudo kill -9 <PID>
# OR modify docker-compose.yml ports
```

**Memory/Resource Issues**
```bash
# Problem: Out of memory or resource limits
# Check Docker resource usage
docker stats

# Check system resources
free -h
df -h

# Increase Docker memory limits (Docker Desktop)
# Go to Docker Desktop -> Settings -> Resources

# For Linux, edit daemon.json
sudo nano /etc/docker/daemon.json
{
  "default-ulimits": {
    "memlock": {
      "Hard": -1,
      "Name": "memlock",
      "Soft": -1
    }
  }
}
```

**Image Build Failures**
```bash
# Problem: Docker build fails
# Clear build cache
docker builder prune -a

# Build with verbose output
docker compose build --no-cache --progress=plain

# Check disk space
docker system df
docker system prune -a  # Remove unused data
```

#### **Network Connectivity Issues**

**Service-to-Service Communication**
```bash
# Problem: Services can't communicate
# Check network configuration
docker network ls
docker network inspect ai-seo-network

# Test connectivity between containers
docker compose exec ai-seo-api ping postgres
docker compose exec ai-seo-api nslookup postgres

# Debug DNS resolution
docker compose exec ai-seo-api cat /etc/hosts
docker compose exec ai-seo-api cat /etc/resolv.conf
```

**External Network Access**
```bash
# Problem: Can't access external services
# Check firewall rules
sudo ufw status
iptables -L

# Test external connectivity
docker compose exec ai-seo-api curl -I https://api.openai.com
docker compose exec ai-seo-api ping 8.8.8.8
```

### **Service-Specific Problems**

#### **PostgreSQL Issues**

**Connection Problems**
```bash
# Check PostgreSQL status
docker compose logs postgres

# Test connection
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "\l"

# Check connection limits
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects \
    -c "SELECT count(*) FROM pg_stat_activity;"

# Monitor connections
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects \
    -c "SELECT datname, usename, state, query FROM pg_stat_activity;"
```

**Performance Issues**
```bash
# Check slow queries
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects \
    -c "SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# Check database size
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects \
    -c "SELECT pg_size_pretty(pg_database_size('ai_seo_architects'));"

# Analyze table statistics
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects \
    -c "SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del FROM pg_stat_user_tables;"
```

**Data Corruption Recovery**
```bash
# Check database integrity
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects \
    -c "SELECT datname, age(datfrozenxid) FROM pg_database;"

# Vacuum and analyze
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects \
    -c "VACUUM ANALYZE;"

# Restore from backup if needed
# See backup procedures section above
```

#### **Redis Issues**

**Memory Problems**
```bash
# Check Redis memory usage
docker compose exec redis redis-cli info memory

# Check Redis configuration
docker compose exec redis redis-cli config get maxmemory
docker compose exec redis redis-cli config get maxmemory-policy

# Monitor Redis commands
docker compose exec redis redis-cli monitor
```

**Connection Issues**
```bash
# Test Redis connectivity
docker compose exec redis redis-cli ping

# Check connected clients
docker compose exec redis redis-cli client list

# Monitor Redis logs
docker compose logs redis -f
```

#### **API Service Issues**

**Application Startup Problems**
```bash
# Check Python dependencies
docker compose exec ai-seo-api pip list

# Check environment variables
docker compose exec ai-seo-api env | grep -E "(DATABASE|REDIS|OPENAI)"

# Test Python imports
docker compose exec ai-seo-api python -c "import app; print('Import successful')"

# Check FastAPI startup
docker compose logs ai-seo-api | grep -E "(started|error|exception)"
```

**API Performance Issues**
```bash
# Monitor API requests
curl -s http://localhost:8000/metrics | grep http_requests

# Check active connections
netstat -an | grep :8000

# Profile API endpoints
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# curl-format.txt content:
cat > curl-format.txt << 'EOF'
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
EOF
```

### **Performance Optimization**

#### **Database Optimization**

**Query Performance Tuning**
```sql
-- Enable query statistics
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET pg_stat_statements.track = 'all';

-- Find slow queries
SELECT query, calls, total_time, mean_time, stddev_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- Analyze table usage
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del,
       n_live_tup, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_tup_read DESC;
```

**Connection Pooling Optimization**
```python
# SQLAlchemy connection pool tuning
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,              # Connections to maintain
    max_overflow=30,           # Additional connections allowed
    pool_timeout=30,           # Seconds to wait for connection
    pool_recycle=3600,         # Recycle connections after 1 hour
    pool_pre_ping=True,        # Validate connections
    echo=False                 # Disable SQL logging in production
)
```

#### **Redis Optimization**

**Memory Optimization**
```bash
# Configure Redis for optimal memory usage
docker compose exec redis redis-cli config set maxmemory 1gb
docker compose exec redis redis-cli config set maxmemory-policy allkeys-lru

# Enable compression for strings
docker compose exec redis redis-cli config set rdbcompression yes

# Monitor memory fragmentation
docker compose exec redis redis-cli info memory | grep fragmentation
```

**Performance Tuning**
```bash
# Tune Redis for performance
docker compose exec redis redis-cli config set tcp-keepalive 300
docker compose exec redis redis-cli config set timeout 0

# Enable keyspace notifications if needed
docker compose exec redis redis-cli config set notify-keyspace-events Ex
```

#### **Application Optimization**

**FastAPI Performance Tuning**
```python
# Optimize FastAPI for production
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="AI SEO Architects API",
    docs_url=None,      # Disable docs in production
    redoc_url=None,     # Disable redoc in production
    openapi_url=None    # Disable OpenAPI schema in production
)

# Run with optimized Uvicorn settings
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,                    # Number of worker processes
        worker_class="uvicorn.workers.UvicornWorker",
        max_requests=1000,           # Restart worker after N requests
        max_requests_jitter=50,      # Add randomness to restarts
        timeout_keep_alive=2,        # Keep-alive timeout
        limit_concurrency=1000,      # Max concurrent connections
        limit_max_requests=10000,    # Max requests per connection
    )
```

### **Debug Procedures**

#### **Comprehensive Debug Script**
```bash
#!/bin/bash
# debug-system.sh

echo "=== AI SEO Architects Debug Report ==="
echo "Generated: $(date)"
echo "======================================="

# System Information
echo -e "\n[SYSTEM INFO]"
echo "OS: $(uname -a)"
echo "Docker: $(docker --version)"
echo "Docker Compose: $(docker compose version)"
echo "Memory: $(free -h | grep Mem)"
echo "Disk: $(df -h / | tail -1)"

# Docker Status
echo -e "\n[DOCKER STATUS]"
docker system df
echo ""
docker system events --since=1h --until=now | tail -10

# Container Status
echo -e "\n[CONTAINER STATUS]"
docker compose ps

# Resource Usage
echo -e "\n[RESOURCE USAGE]"
docker stats --no-stream

# Service Logs (last 50 lines)
for service in ai-seo-api postgres redis nginx prometheus grafana; do
    echo -e "\n[${service} LOGS - Last 50 lines]"
    docker compose logs --tail=50 $service 2>/dev/null | tail -20
done

# Network Information
echo -e "\n[NETWORK INFO]"
docker network ls
docker network inspect ai-seo-network | jq '.[] | .Containers'

# Volume Information
echo -e "\n[VOLUME INFO]"
docker volume ls
for volume in $(docker volume ls -q | grep ai-seo-architects); do
    echo "Volume: $volume"
    docker run --rm -v $volume:/data alpine du -sh /data
done

# Health Checks
echo -e "\n[HEALTH CHECKS]"
services=("http://localhost:8000/health" "http://localhost:9090/-/healthy" "http://localhost:3000/api/health")
for url in "${services[@]}"; do
    echo -n "$url: "
    if curl -fs --max-time 5 "$url" > /dev/null; then
        echo "✓ OK"
    else
        echo "✗ FAILED"
    fi
done

# Configuration Check
echo -e "\n[CONFIGURATION]"
echo "Environment variables:"
docker compose config | grep -E "(POSTGRES|REDIS|OPENAI)" | head -10

echo -e "\n[END DEBUG REPORT]"
```

#### **Performance Profiling**
```bash
#!/bin/bash
# profile-performance.sh

echo "Starting performance profiling..."

# 1. CPU profiling
echo "CPU utilization over 60 seconds:"
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" --no-stream &
PID=$!
sleep 60
kill $PID

# 2. Memory profiling
echo "Memory growth analysis:"
for i in {1..10}; do
    echo "Sample $i:"
    docker compose exec ai-seo-api ps aux | grep python
    sleep 10
done

# 3. Database performance
echo "Database performance check:"
docker compose exec postgres psql -U ai_seo_user -d ai_seo_architects -c "
    SELECT pid, usename, state, query_start, query
    FROM pg_stat_activity 
    WHERE state != 'idle' 
    ORDER BY query_start;
"

# 4. API endpoint profiling
echo "API endpoint response times:"
endpoints=("/health" "/api/agents" "/dashboard")
for endpoint in "${endpoints[@]}"; do
    echo "Testing $endpoint:"
    curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000$endpoint"
done

echo "Performance profiling completed."
```

This comprehensive update to the DOCKER_DEPLOYMENT.md file includes:

1. **Advanced Configuration** - Production environment variables, resource limits, scaling options, and volume management
2. **Service Details** - Detailed breakdown of all 8 services with ports, dependencies, health checks, and configuration
3. **Security Configuration** - Container security, network isolation, secret management, and image security
4. **Monitoring & Logging** - Prometheus setup, Grafana dashboards, log aggregation with ELK stack, and APM integration
5. **Maintenance & Updates** - Rolling updates, blue-green deployment, database migrations, backup/restore procedures, and auto-scaling
6. **Troubleshooting** - Common Docker issues, service-specific problems, performance optimization, and comprehensive debug procedures

The document is now production-ready and suitable for DevOps engineers and system administrators managing enterprise deployments.