# Backend Setup Instructions

## Prerequisites

### 1. Python 3.9+
Verify Python is installed:
```bash
python --version
```

### 2. PostgreSQL 13+
Download and install PostgreSQL from: https://www.postgresql.org/download/windows/

After installation:
1. Add PostgreSQL bin directory to PATH (e.g., `C:\Program Files\PostgreSQL\13\bin`)
2. Verify installation:
   ```bash
   psql --version
   ```

### 3. Create Database

Connect to PostgreSQL as superuser:
```bash
psql -U postgres
```

Run these commands in psql:
```sql
-- Create database user
CREATE USER baiboly_user WITH PASSWORD 'dev_password_2025';

-- Create development database
CREATE DATABASE baiboly_dev OWNER baiboly_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE baiboly_dev TO baiboly_user;

-- Connect to database and grant schema privileges
\c baiboly_dev
GRANT ALL ON SCHEMA public TO baiboly_user;

-- Exit psql
\q
```

## Installation Steps

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

**If psycopg2-binary installation fails on Windows:**
```bash
# Try installing Visual C++ Build Tools first, then:
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
```

**Alternative: Use psycopg binary wheel**
Download the appropriate wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg
Then:
```bash
pip install psycopg2_binary-<version>-cp<python_version>-cp<python_version>-win_amd64.whl
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
# Make sure DATABASE_URL matches your PostgreSQL setup
```

### 5. Initialize Database
```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### 6. Run Development Server
```bash
flask run
```

The API will be available at: http://localhost:5000

## Verify Installation

Test the health check endpoint:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Baiboly API is running"
}
```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test markers
pytest -m unit
pytest -m integration
pytest -m bible
pytest -m fihirana

# Generate HTML coverage report
pytest --cov=src --cov-report=html
```

Coverage report will be in `htmlcov/index.html`

## Troubleshooting

### psycopg2 installation fails
- Install Microsoft Visual C++ 14.0 or greater
- Or use psycopg2-binary wheel file
- Or try: `pip install psycopg2-binary --no-binary :all:`

### Database connection fails
- Verify PostgreSQL service is running
- Check DATABASE_URL in .env file
- Verify database and user exist
- Check PostgreSQL logs

### Import errors
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Flask commands not found
- Set FLASK_APP: `set FLASK_APP=src/app.py` (Windows) or `export FLASK_APP=src/app.py` (Linux/Mac)
- Ensure virtual environment is activated
