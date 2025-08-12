# 🚀 AI SEO Architects - Production VDS/VPS Deployment Guide

> **Enterprise-ready руководство по развертыванию на production серверах**  
> Поддержка Ubuntu 22.04+, CentOS 8+, Debian 12+, RHEL 8+ с retry механизмами и полной отказоустойчивостью

**Время развертывания:** 15-30 минут  
**Уровень сложности:** Intermediate to Advanced  
**Production готовность:** 100% + Retry механизмы**

---

## 📋 Содержание

1. [🎯 Server Requirements](#server-requirements)
2. [🔧 Server Preparation](#server-preparation)
3. [🐳 Docker Installation](#docker-installation)
4. [🔥 Firewall Configuration](#firewall-configuration)
5. [🔒 SSL Setup](#ssl-setup)
6. [🌐 Domain Configuration](#domain-configuration)
7. [📋 Environment Setup](#environment-setup)
8. [🔄 Retry Configuration](#retry-configuration)
9. [🚀 Deployment Process](#deployment-process)
10. [📊 Monitoring Setup](#monitoring-setup)
11. [🛡️ Security Hardening](#security-hardening)
12. [📈 Performance Optimization](#performance-optimization)
13. [🔧 Maintenance & Updates](#maintenance-updates)

---

## 🎯 Server Requirements

### **📊 Production Specifications**

#### **Small Deployment (100-500 requests/day)**
```yaml
CPU: 2 cores (Intel/AMD x64)
RAM: 8GB DDR4
Storage: 40GB NVMe SSD
Network: 100 Mbps unmetered
OS: Ubuntu 22.04 LTS (recommended)
```

#### **Medium Deployment (1K-10K requests/day)**  
```yaml
CPU: 4 cores (Intel/AMD x64)
RAM: 16GB DDR4
Storage: 100GB NVMe SSD  
Network: 1 Gbps unmetered
OS: Ubuntu 22.04 LTS or CentOS 9
```

#### **Large Deployment (10K+ requests/day)**
```yaml
CPU: 8+ cores (Intel/AMD x64)
RAM: 32GB+ DDR4
Storage: 200GB+ NVMe SSD
Network: 1 Gbps+ unmetered
OS: Ubuntu 22.04 LTS or RHEL 9
Load Balancer: Recommended
```

### **🌍 Supported Operating Systems**
- ✅ **Ubuntu 22.04 LTS** (Recommended)
- ✅ **Ubuntu 20.04 LTS** 
- ✅ **CentOS 8/9**
- ✅ **RHEL 8/9**
- ✅ **Debian 12**
- ✅ **Amazon Linux 2**

### **☁️ Tested VPS Providers**
- **DigitalOcean** - Docker Droplets
- **Hetzner** - Cloud Servers  
- **Linode** - Dedicated CPU
- **Vultr** - High Frequency
- **AWS EC2** - t3.medium+
- **Google Cloud** - e2-standard-2+

## 🔧 Server Preparation

### **1. Initial System Setup**

#### **Ubuntu 22.04/20.04 (Recommended)**
```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install essential packages
sudo apt install -y curl wget git htop unzip software-properties-common \
    apt-transport-https ca-certificates gnupg lsb-release ufw fail2ban \
    logrotate cron

# 3. Configure timezone
sudo timedatectl set-timezone Europe/Moscow
# OR: sudo timedatectl set-timezone UTC

# 4. Create application user (security best practice)
sudo useradd -m -s /bin/bash aiseo
sudo usermod -aG sudo aiseo
sudo mkdir -p /home/aiseo/.ssh
sudo chmod 700 /home/aiseo/.ssh
```

#### **CentOS 8/9 / RHEL**
```bash
# 1. Update system packages
sudo dnf update -y

# 2. Install essential packages  
sudo dnf install -y curl wget git htop unzip tar firewalld fail2ban \
    logrotate cronie

# 3. Enable and start services
sudo systemctl enable --now firewalld
sudo systemctl enable --now fail2ban
sudo systemctl enable --now crond

# 4. Configure timezone
sudo timedatectl set-timezone Europe/Moscow

# 5. Create application user
sudo useradd -m -s /bin/bash aiseo
sudo usermod -aG wheel aiseo
```

### **2. SSH Hardening**
```bash
# 1. Edit SSH configuration
sudo nano /etc/ssh/sshd_config

# Add/modify these settings:
Port 2222                    # Change default SSH port
PermitRootLogin no          # Disable root login
PasswordAuthentication no   # Use key-based auth only
MaxAuthTries 3             # Limit auth attempts
ClientAliveInterval 300     # Keep-alive interval
ClientAliveCountMax 2      # Max keep-alive messages

# 2. Restart SSH service
sudo systemctl restart sshd
```

### **3. Swap Configuration (for servers with <16GB RAM)**
```bash
# Create 4GB swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make swap persistent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Optimize swap usage
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
## 🐳 Docker Installation

### **Official Docker Installation (All Systems)**

#### **Ubuntu/Debian Systems**
```bash
# 1. Remove old Docker versions
sudo apt remove -y docker docker-engine docker.io containerd runc

# 2. Add Docker official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 3. Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 5. Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# 6. Add user to docker group
sudo usermod -aG docker aiseo
sudo usermod -aG docker $USER
```

#### **CentOS/RHEL Systems**  
```bash
# 1. Remove old Docker versions
sudo dnf remove -y docker docker-client docker-client-latest docker-common \
    docker-latest docker-latest-logrotate docker-logrotate docker-selinux \
    docker-engine-selinux docker-engine

# 2. Add Docker repository
sudo dnf install -y dnf-utils
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 3. Install Docker Engine
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# 5. Add user to docker group
sudo usermod -aG docker aiseo
sudo usermod -aG docker $USER
```

### **Docker Compose Verification**
```bash
# Verify Docker installation
docker --version
# Expected: Docker version 24.0.0+

# Verify Docker Compose (v2 plugin)
docker compose version  
# Expected: Docker Compose version v2.20.0+

# Test Docker with hello-world
docker run hello-world
```

## 🔥 Firewall Configuration

### **Ubuntu/Debian (UFW)**
```bash
# 1. Enable UFW firewall
sudo ufw --force enable

# 2. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. Allow essential services
sudo ufw allow 2222/tcp          # SSH (custom port)
sudo ufw allow 80/tcp            # HTTP
sudo ufw allow 443/tcp           # HTTPS
sudo ufw allow 8000/tcp          # API (optional, for direct access)

# 4. Allow monitoring ports (restrict to specific IPs in production)
sudo ufw allow 3000/tcp          # Grafana
sudo ufw allow 9090/tcp          # Prometheus

# 5. Check firewall status
sudo ufw status verbose
```

### **CentOS/RHEL (firewalld)**
```bash
# 1. Configure firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=8000/tcp  # API
sudo firewall-cmd --permanent --add-port=3000/tcp  # Grafana
sudo firewall-cmd --permanent --add-port=9090/tcp  # Prometheus

# 2. Reload firewall
sudo firewall-cmd --reload

# 3. Check firewall status
sudo firewall-cmd --list-all
```

### **Fail2ban Configuration**
```bash
# 1. Create custom SSH jail
sudo nano /etc/fail2ban/jail.local

# Add content:
cat << 'EOF' | sudo tee /etc/fail2ban/jail.local
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 3

[sshd]
enabled = true
port = 2222
logpath = /var/log/auth.log
backend = systemd

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
EOF

# 2. Restart fail2ban
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban
```

## 🔒 SSL Setup & Domain Configuration

### **1. Domain DNS Configuration**
```bash
# Configure your DNS records (at your domain provider):
# A record: yourdomain.com -> Your_Server_IP
# A record: api.yourdomain.com -> Your_Server_IP  
# A record: monitoring.yourdomain.com -> Your_Server_IP
# CNAME: www.yourdomain.com -> yourdomain.com
```

### **2. Let's Encrypt SSL Certificate**
```bash
# 1. Install Certbot
# Ubuntu/Debian:
sudo apt install -y certbot python3-certbot-nginx

# CentOS/RHEL:
sudo dnf install -y certbot python3-certbot-nginx

# 2. Obtain SSL certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com \
    -d api.yourdomain.com -d monitoring.yourdomain.com

# 3. Test automatic renewal
sudo certbot renew --dry-run

# 4. Set up automatic renewal cron job
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet --deploy-hook 'systemctl reload nginx'") | crontab -
```

### **3. Manual SSL Certificate (Alternative)**
```bash
# If using custom certificates
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/private.key \
    -out /etc/nginx/ssl/certificate.crt
sudo chmod 600 /etc/nginx/ssl/private.key
sudo chmod 644 /etc/nginx/ssl/certificate.crt
```

## 📋 Environment Setup

### **1. Project Deployment**
```bash
# 1. Switch to application user
sudo su - aiseo

# 2. Clone the repository
git clone https://github.com/Andrew821667/ai-seo-architects.git
cd ai-seo-architects

# 3. Create production environment file
cp .env.example .env
nano .env  # Edit with your values
```

### **2. Production Environment Configuration**
```bash
# Create comprehensive production .env
cat << 'EOF' > .env
# =============================================================================
# PRODUCTION CONFIGURATION - AI SEO Architects
# =============================================================================

# Core Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000

# AI Configuration (REQUIRED)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-key-optional

# Security (CHANGE ALL VALUES!)
JWT_SECRET_KEY=your-cryptographically-secure-key-minimum-64-characters-long
DEFAULT_ADMIN_PASSWORD=YourSecureAdminPassword123!

# Database Configuration
POSTGRES_PASSWORD=YourSecureDBPassword123!
GRAFANA_PASSWORD=YourSecureGrafanaPassword123!

# Domain Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com

# Production Optimizations
REDIS_MAX_CONNECTIONS=100
DB_POOL_SIZE=25
RATE_LIMIT_ADMIN=2000
RATE_LIMIT_MANAGER=1000
RATE_LIMIT_OPERATOR=500

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLE_ALERTING=true
LOG_FILE_PATH=/app/logs/api.log

# Feature Flags (Production)
ENABLE_API_DOCS=false          # Security: disable in production
ENABLE_DEBUG_ENDPOINTS=false   # Security: never enable in production
ENABLE_ANALYTICS=true
SSL_ENABLED=true

# Contact Information
CONTACT_EMAIL=admin@yourdomain.com
EOF

# 3. Secure the environment file
chmod 600 .env
```

### **3. Directory Structure Setup**
```bash
# Create required directories
mkdir -p logs exports backups
mkdir -p nginx/ssl
mkdir -p monitoring/{prometheus,grafana}

# Set proper permissions
chmod -R 755 logs exports
chmod -R 700 backups
chmod -R 755 monitoring
```

## 🚀 Deployment Process

### **1. Pre-deployment Verification**
```bash
# 1. Verify Docker is running
docker --version
docker compose version

# 2. Check system resources
free -h
df -h
htop  # Press q to quit

# 3. Test network connectivity
curl -I https://api.openai.com/v1/models
# Should return HTTP/2 200

# 4. Verify environment configuration
echo "Checking critical environment variables..."
grep -E "OPENAI_API_KEY|JWT_SECRET_KEY|POSTGRES_PASSWORD" .env | wc -l
# Should return 3
```

### **2. Initial Deployment**
```bash
# 1. Pull and build containers (first time)
docker compose pull
docker compose build --no-cache

# 2. Start the infrastructure in production mode
docker compose up -d

# 3. Wait for services to initialize (2-3 minutes)
echo "Waiting for services to start..."
sleep 120

# 4. Check container health
docker compose ps
docker compose logs --tail=20
```

### **3. Service Verification**
```bash
# 1. Check all containers are running
docker compose ps
# Expected: All services should be "Up"

# 2. Check service health endpoints
curl -f http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "..."}

# 3. Test API authentication
curl -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"YourSecureAdminPassword123!"}'
# Expected: {"access_token": "...", "token_type": "bearer"}

# 4. Check monitoring services
curl -f http://localhost:3000  # Grafana
curl -f http://localhost:9090  # Prometheus
```

### **4. Domain and SSL Configuration**
```bash
# 1. Test domain resolution
nslookup yourdomain.com
nslookup api.yourdomain.com

# 2. Verify SSL certificates
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com < /dev/null
# Should show valid certificate

# 3. Test HTTPS endpoints
curl -f https://yourdomain.com/health
curl -f https://api.yourdomain.com/health
```

## 📊 Monitoring Setup

### **1. Grafana Initial Configuration**
```bash
# 1. Access Grafana web interface
# URL: https://monitoring.yourdomain.com:3000
# Default: admin / YourSecureGrafanaPassword123!

# 2. Configure Prometheus data source via UI:
# URL: http://prometheus:9090
# Access: Server (default)
# Save & Test

# 3. Import AI SEO Architects dashboards
# - Navigate to + → Import Dashboard
# - Use dashboard IDs or JSON files from monitoring/grafana/dashboards/
```

### **2. Prometheus Configuration Verification**
```bash
# 1. Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# 2. Verify metrics collection
curl 'http://localhost:9090/api/v1/query?query=up'

# 3. Test alerting (if configured)
curl http://localhost:9090/api/v1/alerts
```

### **3. Log Management**
```bash
# 1. Configure log rotation
sudo nano /etc/logrotate.d/aiseo

# Add content:
/home/aiseo/ai-seo-architects/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 aiseo aiseo
    postrotate
        docker compose kill -s USR1 ai-seo-api
    endscript
}

# 2. Set up centralized logging
docker compose logs -f --tail=100 > logs/deployment.log 2>&1 &
```

## 🛡️ Security Hardening

### **1. System Hardening**
```bash
# 1. Disable unnecessary services
sudo systemctl disable cups bluetooth avahi-daemon

# 2. Set secure kernel parameters
cat << 'EOF' | sudo tee -a /etc/sysctl.conf
# Network security
net.ipv4.ip_forward = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.tcp_syncookies = 1
EOF

sudo sysctl -p

# 3. Configure Docker daemon security
sudo mkdir -p /etc/docker
cat << 'EOF' | sudo tee /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5"
  },
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true
}
EOF

sudo systemctl restart docker
```

### **2. File System Permissions**
```bash
# 1. Secure application files
find /home/aiseo/ai-seo-architects -type f -name "*.py" -exec chmod 644 {} \;
find /home/aiseo/ai-seo-architects -type f -name "*.sh" -exec chmod 755 {} \;
chmod 600 /home/aiseo/ai-seo-architects/.env

# 2. Secure log directories
chmod -R 755 /home/aiseo/ai-seo-architects/logs
chown -R aiseo:aiseo /home/aiseo/ai-seo-architects
```

## 📈 Performance Optimization

### **1. System Performance Tuning**
```bash
# 1. Optimize Docker performance
cat << 'EOF' | sudo tee -a /etc/docker/daemon.json
{
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
EOF

# 2. Optimize PostgreSQL settings (add to docker-compose.yml)
# command: postgres -c 'max_connections=200' -c 'shared_buffers=256MB' -c 'effective_cache_size=1GB'

# 3. Set resource limits in docker-compose.yml
# deploy:
#   resources:
#     limits:
#       cpus: '2.0'
#       memory: 2G
#     reservations:
#       memory: 1G
```

### **2. Application Performance**
```bash
# 1. Enable Redis persistence for better performance
echo 'save 900 1' | docker exec -i ai-seo-redis redis-cli --raw

# 2. Optimize Nginx configuration
sudo nano /home/aiseo/ai-seo-architects/nginx/nginx.conf

# Add performance optimizations:
# worker_processes auto;
# worker_connections 2048;
# gzip on;
# gzip_types text/plain application/json text/css application/javascript;
```

## 🔧 Maintenance & Updates

### **1. Backup Procedures**
```bash
# 1. Create backup script
cat << 'EOF' > /home/aiseo/backup.sh
#!/bin/bash
BACKUP_DIR="/home/aiseo/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
docker exec ai-seo-postgres pg_dump -U ai_seo_user ai_seo_architects | gzip > "$BACKUP_DIR/database_$DATE.sql.gz"

# Backup configuration
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" /home/aiseo/ai-seo-architects/.env /home/aiseo/ai-seo-architects/docker-compose.yml

# Backup logs (last 7 days)
find /home/aiseo/ai-seo-architects/logs -name "*.log" -mtime -7 -exec tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" {} +

# Clean old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

chmod +x /home/aiseo/backup.sh

# 2. Schedule daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /home/aiseo/backup.sh >> /home/aiseo/logs/backup.log 2>&1") | crontab -
```

### **2. Update Procedures**
```bash
# 1. Update system packages (monthly)
sudo apt update && sudo apt upgrade -y  # Ubuntu
sudo dnf update -y                      # CentOS

# 2. Update Docker images
cd /home/aiseo/ai-seo-architects
docker compose pull
docker compose up -d --force-recreate

# 3. Update application code
git fetch origin
git merge origin/main
docker compose build --no-cache
docker compose up -d
```

### **3. Health Monitoring**
```bash
# 1. Create health check script
cat << 'EOF' > /home/aiseo/health-check.sh
#!/bin/bash
SERVICES=("ai-seo-api" "ai-seo-postgres" "ai-seo-redis" "ai-seo-nginx")
FAILED_SERVICES=()

for service in "${SERVICES[@]}"; do
    if ! docker compose ps "$service" | grep -q "Up"; then
        FAILED_SERVICES+=("$service")
    fi
done

if [ ${#FAILED_SERVICES[@]} -ne 0 ]; then
    echo "ALERT: Failed services: ${FAILED_SERVICES[*]}"
    # Add notification logic here (email, Slack, etc.)
    exit 1
else
    echo "All services running normally"
    exit 0
fi
EOF

chmod +x /home/aiseo/health-check.sh

# 2. Schedule health checks
(crontab -l 2>/dev/null; echo "*/5 * * * * /home/aiseo/health-check.sh >> /home/aiseo/logs/health.log 2>&1") | crontab -
```

---

## 🎯 Deployment Checklist

### **Pre-deployment**
- [ ] Server meets minimum requirements (8GB RAM, 4 cores, 50GB SSD)
- [ ] Domain DNS properly configured (A records)
- [ ] SSL certificates obtained and valid
- [ ] OpenAI API key tested and valid
- [ ] All passwords and secrets generated and secured

### **Deployment**
- [ ] Docker and Docker Compose installed correctly
- [ ] All containers start successfully
- [ ] Health endpoints return 200 OK
- [ ] Authentication system working
- [ ] Monitoring dashboard accessible

### **Post-deployment**
- [ ] Automated backups configured and tested
- [ ] Log rotation configured
- [ ] Firewall rules verified
- [ ] SSL certificate auto-renewal working
- [ ] Performance monitoring alerts configured

---

## 📞 Support & Troubleshooting

### **Common Issues**
1. **Container won't start**: Check logs with `docker compose logs service-name`
2. **Database connection failed**: Verify PostgreSQL container and credentials
3. **SSL certificate issues**: Check Certbot logs and domain DNS
4. **High memory usage**: Review Docker resource limits and application settings

### **Getting Help**
- **Documentation**: Check project README and API docs
- **Logs**: Always check application logs first
- **Community**: GitHub Issues for project-specific problems
- **Monitoring**: Use Grafana dashboards for system insights

**🚀 Production deployment complete! Your AI SEO Architects system is now running securely and efficiently.**
