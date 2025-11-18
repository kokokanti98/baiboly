#!/bin/bash
# Launch script for Baiboly application on Linux/Mac
# This script starts the entire application stack using Docker Compose

set -e

echo "=================================="
echo "  Baiboly Application Launcher   "
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo "Please install Docker from: https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed.${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

# Use docker compose (v2) or docker-compose (v1)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo -e "${YELLOW}Starting Baiboly application...${NC}"
echo ""

# Build and start containers
$DOCKER_COMPOSE up --build -d

echo ""
echo -e "${GREEN}✓ Application started successfully!${NC}"
echo ""
echo "Services running:"
echo "  • Frontend:  http://localhost:5173"
echo "  • Backend:   http://localhost:5000"
echo "  • Database:  localhost:5432"
echo ""
echo "To view logs:"
echo "  $DOCKER_COMPOSE logs -f"
echo ""
echo "To stop the application:"
echo "  $DOCKER_COMPOSE down"
echo ""
echo "To start pgAdmin (database management):"
echo "  $DOCKER_COMPOSE --profile tools up -d pgadmin"
echo "  Then open: http://localhost:5050"
echo "  Login: admin@baiboly.local / admin"
echo ""

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 5

# Check if backend is responding
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${YELLOW}⚠ Backend is still starting... Check logs: $DOCKER_COMPOSE logs backend${NC}"
fi

# Check if frontend is responding
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is healthy${NC}"
else
    echo -e "${YELLOW}⚠ Frontend is still starting... Check logs: $DOCKER_COMPOSE logs frontend${NC}"
fi

echo ""
echo -e "${GREEN}Ready to develop!${NC}"
