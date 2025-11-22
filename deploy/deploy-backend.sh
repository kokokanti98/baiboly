#!/bin/bash

set -e

echo "=========================================="
echo "Baiboly - Backend Deployment"
echo "=========================================="
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
    exit 1
fi

# Load environment variables
source .env

# Pull latest images (if using registry)
echo "Pulling latest Docker images..."
docker-compose -f docker-compose.prod.yml pull || echo -e "${YELLOW}No images to pull (using local build)${NC}"

# Build images
echo ""
echo "Building Docker images..."
docker-compose -f docker-compose.prod.yml build backend

# Stop existing containers
echo ""
echo "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml stop backend db || true

# Start database first
echo ""
echo "Starting database..."
docker-compose -f docker-compose.prod.yml up -d db

# Wait for database to be ready
echo ""
echo "Waiting for database to be ready..."
sleep 10

# Check if this is first deployment (database empty)
echo ""
echo "Checking database status..."
DB_EXISTS=$(docker-compose -f docker-compose.prod.yml exec -T db psql -U ${POSTGRES_USER:-baiboly} -d ${POSTGRES_DB:-baiboly} -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null || echo "0")

if [ "$DB_EXISTS" -eq "0" ] || [ -z "$DB_EXISTS" ]; then
    echo -e "${YELLOW}Database is empty - first deployment${NC}"
    
    # Check if backup file exists
    if [ -f "backups/db_backup.sql" ]; then
        echo "Restoring database from backup..."
        docker-compose -f docker-compose.prod.yml exec -T db psql -U ${POSTGRES_USER:-baiboly} -d ${POSTGRES_DB:-baiboly} < backups/db_backup.sql
        echo -e "${GREEN}✓${NC} Database restored from backup"
    else
        echo -e "${YELLOW}Warning: No backup file found at backups/db_backup.sql${NC}"
        echo "Database will be initialized empty"
    fi
else
    echo -e "${GREEN}✓${NC} Database already initialized"
fi

# Start backend
echo ""
echo "Starting backend..."
docker-compose -f docker-compose.prod.yml up -d backend

# Run migrations
echo ""
echo "Running database migrations..."
sleep 5
docker-compose -f docker-compose.prod.yml exec -T backend flask db upgrade || echo -e "${YELLOW}Migrations may have already been applied${NC}"

# Health check
echo ""
echo "Performing health check..."
sleep 5

MAX_RETRIES=10
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f -s http://localhost:5000/api/health > /dev/null; then
        echo -e "${GREEN}✓${NC} Backend is healthy"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT+1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "Waiting for backend to be ready... ($RETRY_COUNT/$MAX_RETRIES)"
            sleep 3
        else
            echo -e "${RED}✗${NC} Backend health check failed after $MAX_RETRIES attempts"
            echo "Check logs: docker-compose -f docker-compose.prod.yml logs backend"
            exit 1
        fi
    fi
done

# Check data
echo ""
echo "Checking database data..."
HIRA_COUNT=$(docker-compose -f docker-compose.prod.yml exec -T db psql -U ${POSTGRES_USER:-baiboly} -d ${POSTGRES_DB:-baiboly} -tAc "SELECT COUNT(*) FROM hira;" 2>/dev/null || echo "0")
LIVRE_COUNT=$(docker-compose -f docker-compose.prod.yml exec -T db psql -U ${POSTGRES_USER:-baiboly} -d ${POSTGRES_DB:-baiboly} -tAc "SELECT COUNT(*) FROM livre;" 2>/dev/null || echo "0")

echo "  Hymnes (Hira): $HIRA_COUNT"
echo "  Livres Bible: $LIVRE_COUNT"

if [ "$HIRA_COUNT" -eq "0" ] && [ "$LIVRE_COUNT" -eq "0" ]; then
    echo -e "${YELLOW}Warning: Database appears to be empty${NC}"
    echo "You may need to import data manually or restore from backup"
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Backend Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Services status:"
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "Useful commands:"
echo "  View logs: docker-compose -f docker-compose.prod.yml logs -f backend"
echo "  Restart: docker-compose -f docker-compose.prod.yml restart backend"
echo "  Shell: docker-compose -f docker-compose.prod.yml exec backend bash"
echo ""
