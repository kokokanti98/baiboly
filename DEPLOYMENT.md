# Baiboly - Production Deployment Guide

Complete guide for deploying the Baiboly application (Bible and Hymnal reader) to a production server.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Server Requirements](#server-requirements)
- [Installation Steps](#installation-steps)
- [SSL/HTTPS Configuration](#sslhttps-configuration)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Data Import](#data-import)
- [Backup and Maintenance](#backup-and-maintenance)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Docker** (version 20.10 or higher)
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

2. **Docker Compose** (version 2.0 or higher)
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Git**
   ```bash
   sudo apt-get update
   sudo apt-get install git
   ```

4. **Optional: Certbot** (for Let's Encrypt SSL)
   ```bash
   sudo apt-get install certbot
   ```

### Domain Name (Optional but Recommended)

- A domain name pointing to your server's IP address
- DNS A record configured: `yourdomain.com` → `your_server_ip`

---

## Server Requirements

### Minimum Specifications

- **CPU**: 2 cores
- **RAM**: 2 GB (4 GB recommended)
- **Storage**: 20 GB (for application, database, and backups)
- **OS**: Ubuntu 20.04 LTS or newer (or any Linux with Docker support)
- **Network**: Open ports 80 (HTTP) and 443 (HTTPS)

### Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

---

## Installation Steps

### 1. Clone the Repository

```bash
cd /opt
sudo git clone https://github.com/yourusername/baiboly.git
cd baiboly/deploy
```

### 2. Create Environment File

```bash
cp .env.production.example .env
nano .env
```

Edit the following values:

```env
# Database Configuration
POSTGRES_DB=baiboly
POSTGRES_USER=baiboly
POSTGRES_PASSWORD=your_very_secure_password_here

# Flask Backend Configuration
FLASK_ENV=production
SECRET_KEY=generate_with_openssl_rand_hex_32

# API Configuration
VITE_API_URL=/api

# Domain (for SSL)
DOMAIN=yourdomain.com
LETSENCRYPT_EMAIL=admin@yourdomain.com
```

**Generate a secure SECRET_KEY:**

```bash
openssl rand -hex 32
```

### 3. Make Scripts Executable

```bash
chmod +x deploy.sh backup.sh
```

### 4. Run Deployment Script

```bash
./deploy.sh
```

The script will:
- Check prerequisites
- Create necessary directories
- Build Docker images
- Start containers
- Run database migrations
- Import Bible data (44 books, 21,527 verses)
- Import first 100 Fihirana hymns

---

## SSL/HTTPS Configuration

### Option 1: Let's Encrypt (Recommended for Production)

```bash
# Stop nginx temporarily
docker-compose -f docker-compose.prod.yml stop nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/

# Start nginx
docker-compose -f docker-compose.prod.yml start nginx
```

**Auto-renewal setup:**

```bash
# Add to crontab
sudo crontab -e

# Add this line (renew daily at 3am)
0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/yourdomain.com/*.pem /opt/baiboly/deploy/ssl/ && docker-compose -f /opt/baiboly/deploy/docker-compose.prod.yml restart nginx
```

### Option 2: Self-Signed Certificate (Development Only)

```bash
cd ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out fullchain.pem \
  -subj "/C=MG/ST=Antananarivo/L=Antananarivo/O=Baiboly/CN=localhost"
```

### Option 3: Existing Certificates

Copy your existing certificates to `deploy/ssl/`:
- `fullchain.pem` (certificate + chain)
- `privkey.pem` (private key)

---

## Environment Configuration

### Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_DB` | Database name | `baiboly` |
| `POSTGRES_USER` | Database user | `baiboly` |
| `POSTGRES_PASSWORD` | Database password | `secure_password_123` |
| `SECRET_KEY` | Flask secret key | `generated_hex_string` |
| `FLASK_ENV` | Flask environment | `production` |
| `VITE_API_URL` | API URL for frontend | `/api` |
| `DOMAIN` | Your domain name | `yourdomain.com` |

---

## Database Setup

### Initial Migration

The `deploy.sh` script automatically runs migrations, but if needed manually:

```bash
docker-compose -f docker-compose.prod.yml exec backend flask db upgrade
```

### Check Database Status

```bash
# Access PostgreSQL
docker-compose -f docker-compose.prod.yml exec db psql -U baiboly -d baiboly

# Check tables
\dt

# Check Bible data
SELECT COUNT(*) FROM livre;  -- Should be 44
SELECT COUNT(*) FROM verset; -- Should be 21,527

# Check Fihirana data
SELECT COUNT(*) FROM fihirana; -- Should be 100+ (up to 519 when fully imported)

# Exit
\q
```

---

## Data Import

### Bible Data

Bible data is automatically imported by `deploy.sh`. To re-import:

```bash
docker-compose -f docker-compose.prod.yml exec backend python src/scripts/import_bible.py
```

### Fihirana Hymns

**Quick import (first 100 hymns - 5 minutes):**

```bash
docker-compose -f docker-compose.prod.yml exec backend python src/scripts/import_first_100.py
```

**Full import (all 519 hymns - 30-40 minutes):**

```bash
docker-compose -f docker-compose.prod.yml exec backend python src/scripts/import_all_fihirana_with_titles.py
```

**Monitor import progress:**

```bash
docker-compose -f docker-compose.prod.yml logs -f backend
```

**Hymn collections:**
- **FFPM**: 437 hymns (Fihirana Fiderana sy Pitoloana ho an'ny Malagasy)
- **Fanampiny**: 82 hymns (Supplement)
- **Total**: 519 hymns

---

## Backup and Maintenance

### Automated Backup

```bash
# Run backup script
./backup.sh
```

This creates a compressed PostgreSQL dump in `backups/` directory and automatically cleans backups older than 7 days.

### Schedule Automatic Backups

```bash
# Add to crontab
crontab -e

# Daily backup at 2am
0 2 * * * cd /opt/baiboly/deploy && ./backup.sh >> logs/backup.log 2>&1
```

### Manual Backup

```bash
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U baiboly baiboly > backup_$(date +%Y%m%d).sql
gzip backup_$(date +%Y%m%d).sql
```

### Restore from Backup

```bash
# Stop application
docker-compose -f docker-compose.prod.yml stop backend

# Restore database
gunzip -c backups/baiboly_backup_YYYYMMDD_HHMMSS.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T db psql -U baiboly baiboly

# Restart application
docker-compose -f docker-compose.prod.yml start backend
```

---

## Monitoring

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f nginx

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 backend
```

### Check Service Status

```bash
docker-compose -f docker-compose.prod.yml ps
```

### Health Checks

```bash
# API health check
curl http://localhost/api/health

# Database health
docker-compose -f docker-compose.prod.yml exec db pg_isready -U baiboly
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df
df -h
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build backend
```

### Database Connection Issues

```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps db

# Check database logs
docker-compose -f docker-compose.prod.yml logs db

# Verify credentials in .env file
cat .env

# Test connection from backend
docker-compose -f docker-compose.prod.yml exec backend flask shell
>>> from src.app import db
>>> db.engine.execute("SELECT 1")
```

### Frontend 404 Errors

```bash
# Check nginx configuration
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# Reload nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

# Check frontend build
docker-compose -f docker-compose.prod.yml logs frontend
```

### SSL Certificate Issues

```bash
# Check certificate expiry
openssl x509 -in ssl/fullchain.pem -noout -enddate

# Verify certificate and key match
openssl x509 -noout -modulus -in ssl/fullchain.pem | openssl md5
openssl rsa -noout -modulus -in ssl/privkey.pem | openssl md5
# (The MD5 hashes should match)
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Check database performance
docker-compose -f docker-compose.prod.yml exec db psql -U baiboly -d baiboly
SELECT * FROM pg_stat_activity;

# Clear nginx cache
docker-compose -f docker-compose.prod.yml exec nginx rm -rf /var/cache/nginx/*
docker-compose -f docker-compose.prod.yml restart nginx
```

### API Slow Response

```bash
# Check database indexes
docker-compose -f docker-compose.prod.yml exec db psql -U baiboly -d baiboly
SELECT tablename, indexname FROM pg_indexes WHERE schemaname = 'public';

# Rebuild full-text search indexes
docker-compose -f docker-compose.prod.yml exec backend flask shell
>>> from src.app import db
>>> db.engine.execute("REINDEX TABLE verset;")
>>> db.engine.execute("REINDEX TABLE fihirana;")
```

### Clear All Data and Restart

```bash
# Stop and remove containers
docker-compose -f docker-compose.prod.yml down

# Remove volumes (WARNING: deletes all data)
docker-compose -f docker-compose.prod.yml down -v

# Restart
./deploy.sh
```

---

## Useful Commands

### Docker Compose Commands

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Stop all services
docker-compose -f docker-compose.prod.yml stop

# Restart all services
docker-compose -f docker-compose.prod.yml restart

# View running containers
docker-compose -f docker-compose.prod.yml ps

# Remove all containers
docker-compose -f docker-compose.prod.yml down

# Rebuild specific service
docker-compose -f docker-compose.prod.yml build backend
docker-compose -f docker-compose.prod.yml up -d backend
```

### Flask Commands

```bash
# Access Flask shell
docker-compose -f docker-compose.prod.yml exec backend flask shell

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend flask db upgrade

# Create new migration
docker-compose -f docker-compose.prod.yml exec backend flask db migrate -m "description"
```

### Database Commands

```bash
# Access PostgreSQL
docker-compose -f docker-compose.prod.yml exec db psql -U baiboly -d baiboly

# Backup database
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U baiboly baiboly > backup.sql

# Execute SQL file
docker-compose -f docker-compose.prod.yml exec -T db psql -U baiboly baiboly < backup.sql
```

---

## Updates and Upgrades

### Update Application Code

```bash
cd /opt/baiboly
git pull origin main

cd deploy
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run any new migrations
docker-compose -f docker-compose.prod.yml exec backend flask db upgrade
```

### Update Dependencies

```bash
# Rebuild images
docker-compose -f docker-compose.prod.yml build --no-cache

# Restart services
docker-compose -f docker-compose.prod.yml up -d
```

---

## Security Recommendations

1. **Change default passwords** in `.env` file
2. **Use strong SECRET_KEY** (32+ characters)
3. **Enable HTTPS** with valid SSL certificates
4. **Keep Docker updated** (`sudo apt-get update && sudo apt-get upgrade`)
5. **Regularly backup database** (automated with cron)
6. **Monitor logs** for suspicious activity
7. **Restrict database access** (PostgreSQL only accessible from backend)
8. **Use firewall** to restrict unnecessary ports
9. **Regular security updates** for the OS

---

## Support

For issues or questions:
- Check logs: `docker-compose -f docker-compose.prod.yml logs`
- Review troubleshooting section above
- Check GitHub issues: https://github.com/yourusername/baiboly/issues

---

## License

[Your License Here]
