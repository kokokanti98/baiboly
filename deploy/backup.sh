#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Load environment
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Create backup directory
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/baiboly_backup_$TIMESTAMP.sql"

echo "========================================"
echo "Baiboly Database Backup"
echo "========================================"
echo ""
echo "Creating backup: $BACKUP_FILE"

# Create backup
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U ${POSTGRES_USER:-baiboly} ${POSTGRES_DB:-baiboly} > $BACKUP_FILE

# Compress backup
echo "Compressing backup..."
gzip $BACKUP_FILE

echo ""
echo -e "${GREEN}✓${NC} Backup created: ${BACKUP_FILE}.gz"
echo ""

# Show backup size
BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
echo "Backup size: $BACKUP_SIZE"

# Clean old backups (keep last 7 days)
echo ""
echo "Cleaning old backups (keeping last 7 days)..."
find $BACKUP_DIR -name "baiboly_backup_*.sql.gz" -mtime +7 -delete
echo -e "${GREEN}✓${NC} Old backups cleaned"

# List recent backups
echo ""
echo "Recent backups:"
ls -lh $BACKUP_DIR/baiboly_backup_*.sql.gz | tail -5

echo ""
echo "To restore a backup:"
echo "  gunzip -c $BACKUP_FILE.gz | docker-compose -f docker-compose.prod.yml exec -T db psql -U ${POSTGRES_USER:-baiboly} ${POSTGRES_DB:-baiboly}"
echo ""
