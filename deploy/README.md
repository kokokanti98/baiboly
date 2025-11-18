# Baiboly - Production Deployment Files

This directory contains all files needed for production deployment.

## Quick Start

```bash
# 1. Create environment file
cp .env.production.example .env
nano .env  # Edit with your values

# 2. Make scripts executable
chmod +x deploy.sh backup.sh

# 3. Deploy
./deploy.sh
```

## Files

- **docker-compose.prod.yml** - Production Docker Compose configuration
- **nginx.conf** - Nginx reverse proxy configuration
- **deploy.sh** - Automated deployment script
- **backup.sh** - Database backup script
- **.env.production.example** - Environment variables template
- **Dockerfile.prod** (in frontend/) - Production frontend build

## Directories Created

- **ssl/** - SSL certificates (create this and add certificates)
- **backups/** - Database backups
- **logs/** - Application and nginx logs

## Complete Documentation

See **DEPLOYMENT.md** in the project root for complete deployment instructions.
