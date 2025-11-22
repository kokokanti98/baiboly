# Baiboly - Production Deployment Files

This directory contains all files needed for production deployment.

## Quick Start

### 1. Initial Server Setup (One-time)

On your production server:

```bash
# Copy this directory to server
scp -r deploy/ user@server:/opt/baiboly/

# SSH to server
ssh user@server

# Run setup script as root
cd /opt/baiboly/deploy
sudo bash server-setup.sh
```

This will:
- Install Docker & Docker Compose
- Configure Apache with required modules
- Install Certbot for SSL
- Create necessary directories
- Configure firewall

### 2. Configure Apache

```bash
# Copy Apache config
sudo cp baiboly.conf /etc/apache2/sites-available/

# Edit with your domain
sudo nano /etc/apache2/sites-available/baiboly.conf

# Enable site
sudo a2ensite baiboly.conf

# Disable default site
sudo a2dissite 000-default.conf

# Test configuration
sudo apache2ctl configtest

# Reload Apache
sudo systemctl reload apache2
```

### 3. Configure SSL

```bash
# Automatic with Let's Encrypt
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com

# Or use existing certificates
sudo cp your-cert.pem /etc/letsencrypt/live/yourdomain.com/fullchain.pem
sudo cp your-key.pem /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### 4. Configure Environment

```bash
cd /opt/baiboly/deploy

# Create .env from template
cp .env.production.example .env

# Edit with your values
nano .env
```

**Important:** Generate secure values:
```bash
# SECRET_KEY
openssl rand -hex 32

# POSTGRES_PASSWORD
openssl rand -base64 32
```

### 5. Copy Database Backup

```bash
# From your local machine
scp backend/db_backup.sql user@server:/opt/baiboly/deploy/backups/
```

### 6. Deploy Backend

```bash
cd /opt/baiboly/deploy
bash deploy-backend.sh
```

This will:
- Build Docker images
- Start database container
- Restore backup if first deployment
- Start backend container
- Run migrations
- Perform health checks

### 7. Deploy Frontend

On your **local machine**, build the frontend:

```bash
cd frontend
npm run build
```

Copy to server:

```bash
# From project root
scp -r frontend/dist/* user@server:/tmp/baiboly-frontend/
```

On the **server**, deploy:

```bash
cd /opt/baiboly/deploy
sudo bash deploy-frontend.sh
```

Or use the deployment script directly:

```bash
# If dist/ is already in deploy/
cd /opt/baiboly/deploy
sudo bash deploy-frontend.sh
```

## Deployment Workflow

### Manual Deployment

1. **Build frontend locally:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Copy to server:**
   ```bash
   scp -r frontend/dist user@server:/opt/baiboly/deploy/
   ```

3. **Deploy backend:**
   ```bash
   ssh user@server
   cd /opt/baiboly/deploy
   bash deploy-backend.sh
   ```

4. **Deploy frontend:**
   ```bash
   sudo bash deploy-frontend.sh
   ```

### Automated Deployment (CI/CD)

See `../.github/workflows/ci-cd.yml` for GitHub Actions workflow.

## Maintenance

### View Logs

```bash
# Backend
docker-compose -f docker-compose.prod.yml logs -f backend

# Database
docker-compose -f docker-compose.prod.yml logs -f db

# Apache
tail -f /var/log/apache2/baiboly-access.log
tail -f /var/log/apache2/baiboly-error.log
```

### Backup Database

```bash
cd /opt/baiboly/deploy
bash backup.sh
```

### Restore Database

```bash
cd /opt/baiboly/deploy
gunzip -c backups/baiboly_backup_YYYYMMDD_HHMMSS.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U baiboly -d baiboly
```

### Restart Services

```bash
# Backend only
docker-compose -f docker-compose.prod.yml restart backend

# All Docker services
docker-compose -f docker-compose.prod.yml restart

# Apache
sudo systemctl restart apache2
```

### Update Application

```bash
# Pull latest code
cd /opt/baiboly
git pull origin main

# Rebuild and deploy backend
cd deploy
bash deploy-backend.sh

# Rebuild and deploy frontend (on local machine first)
cd frontend
npm run build
scp -r dist user@server:/opt/baiboly/deploy/
# Then on server
sudo bash deploy-frontend.sh
```

## Rollback

### Rollback Frontend

```bash
cd /var/www
sudo cp -r baiboly-backups/baiboly-YYYYMMDD_HHMMSS/* baiboly/
sudo systemctl reload apache2
```

### Rollback Backend

```bash
cd /opt/baiboly
git checkout <previous-commit>
cd deploy
docker-compose -f docker-compose.prod.yml up -d --build backend
```

### Rollback Database

```bash
cd /opt/baiboly/deploy
gunzip -c backups/baiboly_backup_YYYYMMDD.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U baiboly -d baiboly
```

## Troubleshooting

### Backend not responding

```bash
# Check if container is running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Restart
docker-compose -f docker-compose.prod.yml restart backend
```

### Frontend 404 errors

```bash
# Check Apache config
sudo apache2ctl configtest

# Check if files exist
ls -la /var/www/html/baiboly/

# Check Apache logs
tail -f /var/log/apache2/baiboly-error.log
```

### Database connection issues

```bash
# Check if DB is running
docker-compose -f docker-compose.prod.yml ps db

# Check DB logs
docker-compose -f docker-compose.prod.yml logs db

# Test connection
docker-compose -f docker-compose.prod.yml exec db \
  psql -U baiboly -d baiboly -c "SELECT 1;"
```

### SSL certificate issues

```bash
# Renew certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

## Security Checklist

- [ ] Changed default passwords in `.env`
- [ ] Generated strong `SECRET_KEY`
- [ ] SSL/HTTPS enabled and working
- [ ] Firewall configured (ports 22, 80, 443 only)
- [ ] SSH key authentication enabled
- [ ] Regular backups scheduled
- [ ] Apache security headers configured
- [ ] Database not exposed to internet

## Support

For detailed documentation, see:
- Main deployment guide: `../DEPLOYMENT.md`
- CI/CD setup: `../CI_CD.md` (if exists)
- Docker guide: `../DOCKER.md`
** in the project root for complete deployment instructions.
