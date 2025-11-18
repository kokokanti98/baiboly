#!/bin/bash

set -e

echo "========================================"
echo "Baiboly Production Deployment Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env from .env.production.example"
    echo "  cp .env.production.example .env"
    echo "  nano .env  # Edit with your values"
    exit 1
fi

# Load environment variables
source .env

echo -e "${GREEN}✓${NC} Environment variables loaded"

# Check prerequisites
echo ""
echo "Checking prerequisites..."

command -v docker >/dev/null 2>&1 || { echo -e "${RED}✗${NC} Docker is not installed"; exit 1; }
echo -e "${GREEN}✓${NC} Docker installed"

command -v docker-compose >/dev/null 2>&1 || { echo -e "${RED}✗${NC} Docker Compose is not installed"; exit 1; }
echo -e "${GREEN}✓${NC} Docker Compose installed"

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p ssl backups logs logs/nginx
echo -e "${GREEN}✓${NC} Directories created"

# Generate SECRET_KEY if not set
if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" == "your_very_long_random_secret_key_here_generate_with_openssl" ]; then
    echo ""
    echo -e "${YELLOW}Warning: SECRET_KEY not configured${NC}"
    echo "Generate one with: openssl rand -hex 32"
    echo "Then update .env file"
    exit 1
fi

# Check PostgreSQL password
if [ "$POSTGRES_PASSWORD" == "your_secure_password_here" ]; then
    echo ""
    echo -e "${YELLOW}Warning: POSTGRES_PASSWORD is default${NC}"
    echo "Please update .env with a secure password"
    exit 1
fi

# SSL certificate check
echo ""
echo "Checking SSL certificates..."
if [ ! -f ssl/fullchain.pem ] || [ ! -f ssl/privkey.pem ]; then
    echo -e "${YELLOW}Warning: SSL certificates not found in ssl/ directory${NC}"
    echo "You can:"
    echo "  1. Use Let's Encrypt: certbot certonly --standalone -d $DOMAIN"
    echo "  2. Copy existing certificates to ssl/ directory"
    echo "  3. Generate self-signed (development only):"
    echo "     openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/privkey.pem -out ssl/fullchain.pem"
    echo ""
    read -p "Continue without SSL? (development only) [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build and start containers
echo ""
echo "Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo ""
echo "Starting containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for database
echo ""
echo "Waiting for database to be ready..."
sleep 10

# Run database migrations
echo ""
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend flask db upgrade

# Check if Bible data exists
echo ""
echo "Checking Bible data..."
BIBLE_COUNT=$(docker-compose -f docker-compose.prod.yml exec -T backend flask shell << 'EOF'
from src.models.bible import Livre
from src.app import db
print(Livre.query.count())
exit()
EOF
)

if [ "$BIBLE_COUNT" -eq "0" ]; then
    echo "Importing Bible data..."
    docker-compose -f docker-compose.prod.yml exec -T backend python src/scripts/import_bible.py
else
    echo -e "${GREEN}✓${NC} Bible data already imported"
fi

# Check if Fihirana data exists
echo ""
echo "Checking Fihirana data..."
FIHIRANA_COUNT=$(docker-compose -f docker-compose.prod.yml exec -T backend flask shell << 'EOF'
from src.models.fihirana import Fihirana
from src.app import db
print(Fihirana.query.count())
exit()
EOF
)

if [ "$FIHIRANA_COUNT" -lt "100" ]; then
    echo "Importing Fihirana data (this may take 30-40 minutes)..."
    echo "First 100 hymns will be imported quickly for testing..."
    docker-compose -f docker-compose.prod.yml exec -T backend python src/scripts/import_first_100.py

    echo ""
    read -p "Import all 519 hymns now? (takes 30-40 min) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose -f docker-compose.prod.yml exec -T backend python src/scripts/import_all_fihirana_with_titles.py
    else
        echo "You can import all hymns later with:"
        echo "  docker-compose -f docker-compose.prod.yml exec backend python src/scripts/import_all_fihirana_with_titles.py"
    fi
else
    echo -e "${GREEN}✓${NC} Fihirana data already imported ($FIHIRANA_COUNT hymns)"
fi

# Show status
echo ""
echo "========================================"
echo -e "${GREEN}Deployment Complete!${NC}"
echo "========================================"
echo ""
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "Application URLs:"
echo "  HTTP:  http://localhost"
echo "  HTTPS: https://localhost (if SSL configured)"
echo ""
echo "Useful commands:"
echo "  View logs:    docker-compose -f docker-compose.prod.yml logs -f"
echo "  Stop:         docker-compose -f docker-compose.prod.yml stop"
echo "  Restart:      docker-compose -f docker-compose.prod.yml restart"
echo "  Backup DB:    ./backup.sh"
echo ""
