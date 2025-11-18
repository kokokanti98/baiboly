# Docker Development Environment

This document provides detailed information about the Docker setup for Baiboly development.

## 🐳 Docker Architecture

### Services Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                   (baiboly_network)                      │
│                                                          │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐│
│  │   Frontend   │   │   Backend    │   │   Database   ││
│  │  (React)     │◄──┤   (Flask)    │◄──┤ (PostgreSQL) ││
│  │  Port: 5173  │   │  Port: 5000  │   │  Port: 5432  ││
│  └──────────────┘   └──────────────┘   └──────────────┘│
│         │                    │                    │      │
└─────────┼────────────────────┼────────────────────┼──────┘
          │                    │                    │
          ▼                    ▼                    ▼
    Host: 5173           Host: 5000          Host: 5432
```

### Service Details

#### 1. Database (db)
- **Image:** `postgres:13-alpine`
- **Container Name:** `baiboly_db`
- **Ports:** 5432:5432
- **Database:** `baiboly_dev`
- **User:** `baiboly_user`
- **Password:** `dev_password_2025`
- **Volume:** `postgres_data` (persistent storage)
- **Init Script:** `backend/scripts/init-db.sql`
- **Health Check:** `pg_isready -U baiboly_user -d baiboly_dev`

#### 2. Backend (backend)
- **Build Context:** `./backend`
- **Container Name:** `baiboly_backend`
- **Ports:** 5000:5000
- **Depends On:** db (waits for health check)
- **Auto-reload:** Enabled (Flask development mode)
- **Volume Mounts:**
  - `./backend:/app` (source code)
  - `/app/venv` (anonymous volume for dependencies)
- **Command:** Runs migrations then starts Flask server

#### 3. Frontend (frontend)
- **Build Context:** `./frontend`
- **Container Name:** `baiboly_frontend`
- **Ports:** 5173:5173
- **Depends On:** backend
- **Hot-reload:** Enabled (Vite HMR)
- **Volume Mounts:**
  - `./frontend:/app` (source code)
  - `/app/node_modules` (anonymous volume for dependencies)
- **Command:** Vite dev server with host 0.0.0.0

#### 4. pgAdmin (pgadmin) - Optional
- **Image:** `dpage/pgadmin4:latest`
- **Container Name:** `baiboly_pgadmin`
- **Ports:** 5050:80
- **Login:** admin@baiboly.local / admin
- **Profile:** `tools` (only starts with `--profile tools`)
- **Volume:** `pgadmin_data` (persistent configuration)

## 🚀 Usage

### Starting Services

**Quick start:**
```bash
# Windows
start.bat

# Linux/Mac
./start.sh
```

**Manual start:**
```bash
# Start all services
docker-compose up -d

# Start with build (recommended after code changes)
docker-compose up --build -d

# Start with pgAdmin
docker-compose --profile tools up -d
```

### Stopping Services

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes (WARNING: deletes database data)
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### Restarting Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up --build -d
```

## 📊 Monitoring & Logs

### View Logs

```bash
# All services (follow mode)
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Last N lines
docker-compose logs --tail=100 backend

# Since specific time
docker-compose logs --since="2024-01-01T12:00:00" backend
```

### Service Status

```bash
# List running containers
docker-compose ps

# View resource usage
docker stats baiboly_backend baiboly_frontend baiboly_db
```

### Health Checks

```bash
# Check backend health
curl http://localhost:5000/api/health

# Check frontend
curl http://localhost:5173

# Check database
docker-compose exec db pg_isready -U baiboly_user -d baiboly_dev
```

## 🔧 Development Tasks

### Running Commands Inside Containers

#### Backend Commands

```bash
# Open shell
docker-compose exec backend bash

# Run Flask commands
docker-compose exec backend flask db migrate -m "Add new table"
docker-compose exec backend flask db upgrade
docker-compose exec backend flask routes

# Run tests
docker-compose exec backend pytest
docker-compose exec backend pytest -v
docker-compose exec backend pytest --cov=src --cov-report=html

# Run linting
docker-compose exec backend black src/
docker-compose exec backend flake8 src/

# Install new dependency
docker-compose exec backend pip install package-name
# Then update requirements.txt manually
```

#### Frontend Commands

```bash
# Open shell
docker-compose exec frontend sh

# Install new dependency
docker-compose exec frontend npm install package-name

# Run tests
docker-compose exec frontend npm test
docker-compose exec frontend npm test -- --coverage

# Run build
docker-compose exec frontend npm run build

# Run linting
docker-compose exec frontend npm run lint
```

#### Database Commands

```bash
# Open psql
docker-compose exec db psql -U baiboly_user -d baiboly_dev

# Create database dump
docker-compose exec db pg_dump -U baiboly_user baiboly_dev > backup.sql

# Restore database dump
docker-compose exec -T db psql -U baiboly_user -d baiboly_dev < backup.sql

# View database logs
docker-compose logs db
```

## 🗄️ Database Management

### Using pgAdmin

1. **Start pgAdmin:**
   ```bash
   docker-compose --profile tools up -d pgadmin
   ```

2. **Access pgAdmin:**
   - URL: http://localhost:5050
   - Email: admin@baiboly.local
   - Password: admin

3. **Add Server Connection:**
   - Right-click "Servers" → "Create" → "Server"
   - **General Tab:**
     - Name: `Baiboly Dev`
   - **Connection Tab:**
     - Host: `db` (Docker service name)
     - Port: `5432`
     - Database: `baiboly_dev`
     - Username: `baiboly_user`
     - Password: `dev_password_2025`
   - Click "Save"

### Direct psql Access

```bash
# Interactive psql shell
docker-compose exec db psql -U baiboly_user -d baiboly_dev

# Run single query
docker-compose exec db psql -U baiboly_user -d baiboly_dev -c "SELECT * FROM livre;"

# Execute SQL file
docker-compose exec -T db psql -U baiboly_user -d baiboly_dev < script.sql
```

### Common SQL Queries

```sql
-- List all tables
\dt

-- Describe table structure
\d livre

-- Count records
SELECT COUNT(*) FROM verset;

-- View recent data
SELECT * FROM livre ORDER BY ordre LIMIT 10;

-- Search verses
SELECT * FROM verset WHERE texte ILIKE '%Andriamanitra%' LIMIT 5;
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Check container status
docker-compose ps

# Remove and recreate
docker-compose down
docker-compose up --build -d
```

### Database Connection Issues

```bash
# Check if database is healthy
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Wait for database to be ready
docker-compose exec db pg_isready -U baiboly_user -d baiboly_dev
```

### Port Already in Use

```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Kill process or change port in docker-compose.yml
```

### Volume Permission Issues (Linux)

```bash
# Fix ownership
sudo chown -R $USER:$USER backend/ frontend/

# Or run containers with current user
docker-compose run --user $(id -u):$(id -g) backend bash
```

### Clean Slate (Nuclear Option)

```bash
# Stop all containers
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Remove volumes
docker volume rm baiboly_postgres_data baiboly_pgadmin_data

# Rebuild everything
docker-compose up --build -d
```

## 🔐 Environment Variables

Environment variables are configured in `docker-compose.yml`. For local overrides:

1. **Create `.env` file in project root:**
   ```env
   # Custom database password
   POSTGRES_PASSWORD=my_secure_password

   # Custom ports
   BACKEND_PORT=8000
   FRONTEND_PORT=3000
   ```

2. **Reference in docker-compose.yml:**
   ```yaml
   environment:
     POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-dev_password_2025}
   ports:
     - "${BACKEND_PORT:-5000}:5000"
   ```

## 📦 Volumes

### Named Volumes

- **postgres_data:** Database files (persistent)
- **pgadmin_data:** pgAdmin configuration (persistent)

### Anonymous Volumes

- `/app/venv` (backend): Python virtual environment
- `/app/node_modules` (frontend): Node.js packages

### Backup Volumes

```bash
# Backup database volume
docker run --rm -v baiboly_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data

# Restore database volume
docker run --rm -v baiboly_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /
```

## 🚢 Production Considerations

**Note:** This Docker setup is for **DEVELOPMENT ONLY**.

For production:
1. Use multi-stage builds for smaller images
2. Set `FLASK_ENV=production`
3. Use production WSGI server (gunicorn, uWSGI)
4. Use nginx as reverse proxy
5. Enable HTTPS/TLS
6. Use Docker secrets for sensitive data
7. Set resource limits (memory, CPU)
8. Use orchestration (Docker Swarm, Kubernetes)
9. Implement proper logging and monitoring
10. Regular security updates

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Flask Development with Docker](https://flask.palletsprojects.com/en/latest/deploying/)
- [Vite with Docker](https://vitejs.dev/guide/)

---

**For general project information, see [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)**
