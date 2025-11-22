#!/bin/bash

set -e

echo "=========================================="
echo "Baiboly - Frontend Deployment"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_DIR="/var/www/html/baiboly"
BACKUP_DIR="/var/www/html/baiboly-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo -e "${RED}Error: dist/ directory not found${NC}"
    echo "Please build the frontend first: npm run build"
    exit 1
fi

# Create backup of current deployment
echo "Creating backup of current deployment..."
if [ -d "$DEPLOY_DIR" ] && [ "$(ls -A $DEPLOY_DIR)" ]; then
    mkdir -p "$BACKUP_DIR"
    cp -r "$DEPLOY_DIR" "$BACKUP_DIR/baiboly-$TIMESTAMP"
    echo -e "${GREEN}✓${NC} Backup created: $BACKUP_DIR/baiboly-$TIMESTAMP"
    
    # Keep only last 5 backups
    cd "$BACKUP_DIR"
    ls -t | tail -n +6 | xargs -r rm -rf
    echo -e "${GREEN}✓${NC} Old backups cleaned (keeping last 5)"
else
    echo -e "${YELLOW}No existing deployment to backup${NC}"
fi

# Deploy new version
echo ""
echo "Deploying new frontend version..."
rm -rf "$DEPLOY_DIR"/*
cp -r dist/* "$DEPLOY_DIR/"
echo -e "${GREEN}✓${NC} Files copied to $DEPLOY_DIR"

# Set correct permissions
echo ""
echo "Setting permissions..."
chown -R www-data:www-data "$DEPLOY_DIR"
chmod -R 755 "$DEPLOY_DIR"
echo -e "${GREEN}✓${NC} Permissions set"

# Test Apache configuration
echo ""
echo "Testing Apache configuration..."
if apache2ctl configtest; then
    echo -e "${GREEN}✓${NC} Apache configuration is valid"
else
    echo -e "${RED}✗${NC} Apache configuration has errors"
    echo "Restoring previous version..."
    if [ -d "$BACKUP_DIR/baiboly-$TIMESTAMP" ]; then
        rm -rf "$DEPLOY_DIR"/*
        cp -r "$BACKUP_DIR/baiboly-$TIMESTAMP"/* "$DEPLOY_DIR/"
        echo -e "${YELLOW}Previous version restored${NC}"
    fi
    exit 1
fi

# Reload Apache
echo ""
echo "Reloading Apache..."
systemctl reload apache2
echo -e "${GREEN}✓${NC} Apache reloaded"

# Health check
echo ""
echo "Performing health check..."
sleep 2

if curl -f -s -o /dev/null http://localhost; then
    echo -e "${GREEN}✓${NC} Frontend is accessible"
else
    echo -e "${RED}✗${NC} Frontend health check failed"
    echo "Check Apache logs: tail -f /var/log/apache2/baiboly-error.log"
    exit 1
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Frontend Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Deployment details:"
echo "  Timestamp: $TIMESTAMP"
echo "  Location: $DEPLOY_DIR"
echo "  Backup: $BACKUP_DIR/baiboly-$TIMESTAMP"
echo ""
echo "Useful commands:"
echo "  View logs: tail -f /var/log/apache2/baiboly-access.log"
echo "  Rollback: cp -r $BACKUP_DIR/baiboly-$TIMESTAMP/* $DEPLOY_DIR/ && systemctl reload apache2"
echo ""
