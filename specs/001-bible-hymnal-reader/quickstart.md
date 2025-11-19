# Quickstart Guide: Baiboly sy Fihirana Platform
[//]: # (# use: Lis QUICK_START_NOUVELLE_SESSION.md et mets-toi à jour)

**Feature**: 001-bible-hymnal-reader
**Last Updated**: 2025-11-18
**Estimated Setup Time**: 30-45 minutes

This guide will help you set up the development environment for the Baiboly sy Fihirana platform on your local machine.

## Prerequisites

### Required Software

- **Python**: 3.9 or higher
  - Check: `python --version` or `python3 --version`
  - Install: [python.org](https://www.python.org/downloads/)

- **Node.js**: 18.x or higher (for React frontend)
  - Check: `node --version`
  - Install: [nodejs.org](https://nodejs.org/)

- **PostgreSQL**: 13 or higher
  - Check: `psql --version`
  - Install: [postgresql.org](https://www.postgresql.org/download/)

- **Git**: For version control
  - Check: `git --version`
  - Install: [git-scm.com](https://git-scm.com/downloads/)

### Recommended Tools

- **VS Code** or **PyCharm** (IDE)
- **Postman** or **Insomnia** (API testing)
- **pgAdmin** or **DBeaver** (database GUI)

---

## Part 1: Backend Setup (Flask API)

### 1.1 Clone the Repository

```bash
git clone <repository-url> baiboly
cd baiboly
git checkout 001-bible-hymnal-reader
```

### 1.2 Create Backend Virtual Environment

```bash
cd backend
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 1.3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages:**
- Flask 3.x
- Flask-RESTful
- SQLAlchemy 2.x
- Flask-Migrate
- Flask-Babel
- psycopg2-binary
- pytest, pytest-flask, pytest-cov

### 1.4 Setup PostgreSQL Database

#### Create Database and User

```bash
# Connect to PostgreSQL
psql postgres

# In psql prompt:
CREATE DATABASE baiboly_dev;
CREATE USER baiboly_user WITH PASSWORD 'dev_password_2025';
GRANT ALL PRIVILEGES ON DATABASE baiboly_dev TO baiboly_user;
\q
```

#### Configure Environment Variables

Create `.env` file in `backend/` directory:

```bash
# backend/.env
FLASK_APP=src/app.py
FLASK_ENV=development
DATABASE_URL=postgresql://baiboly_user:dev_password_2025@localhost:5432/baiboly_dev
SECRET_KEY=dev-secret-key-change-in-production
CORS_ORIGINS=http://localhost:5173
```

### 1.5 Initialize Database Schema

```bash
# Run database migrations
flask db init
flask db migrate -m "Initial schema: livre, chapitre, verset, chant"
flask db upgrade
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Initial schema
```

### 1.6 Import Bible and Fihirana Data

#### Download Source Data

```bash
# From repository root
mkdir -p data
cd data

# Clone Bible data
git clone https://github.com/RaveloMevaSoavina/baiboly-json.git

# Clone Fihirana data
git clone https://github.com/Rohan29-AN/Fihirana-FFPM.git

cd ../backend
```

#### Run Import Scripts

```bash
# Import Bible (66 books, ~31,000 verses)
flask bible import --source=../data/baiboly-json

# Expected output:
# Importing Bible data from ../data/baiboly-json...
# ✓ Imported 66 books
# ✓ Imported 1189 chapters
# ✓ Imported 31102 verses
# ✓ Generated full-text search indexes
# Import completed successfully!

# Import Fihirana (~500-800 hymns)
flask fihirana import --source=../data/Fihirana-FFPM

# Expected output:
# Importing Fihirana data from ../data/Fihirana-FFPM...
# ✓ Imported 320 hymns from 01_fihirana_ffpm.json
# ✓ Imported 150 hymns from 02_fihirana_fanampiny.json
# ✓ Imported 80 antiphons from 03_antema.json
# ✓ Generated full-text search indexes
# Import completed successfully!

# Validate imported data
flask validate --check=bible,fihirana

# Expected output:
# ✓ Bible: 66 books, 1189 chapters, 31102 verses
# ✓ Fihirana: 550 hymns across 3 collections
# All validations passed!
```

### 1.7 Run Backend Server

```bash
flask run
# or
python -m flask run

# Server should start on http://localhost:5000
```

**Verify backend is running:**
```bash
curl http://localhost:5000/api/bible/books
# Should return JSON with 66 books
```

---

## Part 2: Frontend Setup (React)

### 2.1 Navigate to Frontend Directory

```bash
# From repository root
cd frontend
```

### 2.2 Install Node Dependencies

```bash
npm install
# or
yarn install
```

**Expected packages:**
- react 18.x
- react-router-dom 6.x
- @mui/material (Material-UI)
- axios
- react-i18next
- TypeScript

### 2.3 Configure Environment Variables

Create `.env` file in `frontend/` directory:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:5000/api
```

### 2.4 Run Frontend Development Server

```bash
npm run dev
# or
yarn dev

# Server should start on http://localhost:5173
```

**Verify frontend is running:**
- Open browser to http://localhost:5173
- You should see the Baiboly homepage with navigation to Bible and Fihirana

---

## Part 3: Verification & Testing

### 3.1 Backend API Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Open coverage report
# Open htmlcov/index.html in browser
```

**Expected output:**
```
=========== test session starts ===========
collected 45 items

tests/unit/models/test_bible.py ........... [ 24%]
tests/unit/services/test_bible_service.py ... [ 31%]
tests/integration/test_bible_api.py .......... [ 55%]
tests/integration/test_fihirana_api.py ........ [ 73%]
tests/integration/test_search_api.py ........... [100%]

=========== 45 passed in 3.21s ===========
```

### 3.2 Frontend Tests

```bash
cd frontend

# Run unit tests
npm test
# or
yarn test

# Run E2E tests (requires backend running)
npm run test:e2e
# or
yarn test:e2e
```

### 3.3 Manual Testing Checklist

**Bible Functionality:**
- [ ] Navigate to `/bible` page
- [ ] See list of 66 Bible books
- [ ] Click on "Genesisy" → see chapters 1-50
- [ ] Click on Chapter 1 → see all verses
- [ ] Use search to find "Jaona 3:16" → see correct verse
- [ ] Search for "fitiavana" → see results with highlights

**Fihirana Functionality:**
- [ ] Navigate to `/fihirana` page
- [ ] Enter hymn number "125" → see hymn details
- [ ] Search for "Jesosy" → see list of matching hymns
- [ ] Click on a hymn → see full lyrics
- [ ] Test on mobile viewport (DevTools, 375px width)

**Responsive Design:**
- [ ] Resize browser from 375px to 1920px
- [ ] Verify layout adapts correctly
- [ ] Check touch target sizes on mobile (≥44x44px)

---

## Part 4: Development Workflow

### 4.1 Running Both Servers Simultaneously

**Option 1: Two Terminal Windows**
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
flask run

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Option 2: Using `tmux` or `screen` (Linux/macOS)**
```bash
tmux new-session -s baiboly
# Split pane: Ctrl+B then "
# Switch panes: Ctrl+B then arrow keys
```

### 4.2 Code Quality Checks

**Backend (before committing):**
```bash
cd backend

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest
```

**Frontend (before committing):**
```bash
cd frontend

# Lint
npm run lint

# Type check
npm run type-check

# Format
npm run format

# Run tests
npm test
```

### 4.3 Database Management

**Reset database (careful - deletes all data!):**
```bash
cd backend
flask db downgrade base
flask db upgrade
flask bible import --source=../data/baiboly-json
flask fihirana import --source=../data/Fihirana-FFPM
```

**Create new migration:**
```bash
flask db migrate -m "Description of schema change"
flask db upgrade
```

---

## Part 5: Common Issues & Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Ensure virtual environment is activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "psycopg2.OperationalError: could not connect to server"

**Solution:**
1. Check PostgreSQL is running: `pg_ctl status` or `systemctl status postgresql`
2. Verify DATABASE_URL in `.env` file
3. Test connection: `psql -U baiboly_user -d baiboly_dev -h localhost`

### Issue: "CORS error" when frontend calls backend

**Solution:**
1. Verify backend `.env` has `CORS_ORIGINS=http://localhost:5173`
2. Restart Flask server after changing `.env`
3. Check browser console for exact error message

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process or use different port
flask run --port=5001
# Update frontend .env: VITE_API_BASE_URL=http://localhost:5001/api
```

### Issue: Frontend build errors related to TypeScript

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run type-check
```

### Issue: "Search returns no results" despite data being imported

**Solution:**
```bash
# Rebuild full-text search indexes
cd backend
flask db-utils rebuild-search-indexes
```

---

## Part 6: Next Steps

### Ready to Code?

1. **Read the spec**: Review `specs/001-bible-hymnal-reader/spec.md`
2. **Check data model**: See `specs/001-bible-hymnal-reader/data-model.md`
3. **Review API contracts**: OpenAPI specs in `specs/001-bible-hymnal-reader/contracts/`
4. **Run tasks**: Execute `/speckit.tasks` to generate implementation tasks

### Development Best Practices

1. **TDD Workflow**: Write tests first, then implement
2. **Small commits**: Commit after each task completion
3. **Branch naming**: `feature/task-id-description`
4. **PR templates**: Include testing performed, screenshots (if UI)
5. **Constitution compliance**: Review checklist before PR

### Useful Commands Reference

```bash
# Backend
flask run                    # Start dev server
flask db migrate -m "msg"    # Create migration
flask db upgrade             # Apply migrations
pytest                       # Run tests
black src/                   # Format code

# Frontend
npm run dev                  # Start dev server
npm test                     # Run tests
npm run lint                 # Lint code
npm run build                # Production build

# Database
psql baiboly_dev -U baiboly_user  # Connect to DB
flask bible import            # Import Bible data
flask fihirana import         # Import Fihirana data
```

---

## Support & Resources

- **Specification**: `specs/001-bible-hymnal-reader/spec.md`
- **API Docs**: `specs/001-bible-hymnal-reader/contracts/`
- **Constitution**: `.specify/memory/constitution.md`
- **GitHub Issues**: <repository-url>/issues

**Need help?** Check existing issues or create a new one with:
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python/Node versions)
- Error messages/logs

---

**Setup Complete!** 🎉

You should now have:
- ✅ Backend Flask API running on http://localhost:5000
- ✅ Frontend React app running on http://localhost:5173
- ✅ PostgreSQL database with Bible (66 books) and Fihirana (~550 hymns) data
- ✅ Tests passing for both backend and frontend
- ✅ Development environment ready for TDD workflow

Happy coding! Remember: **Test-Driven Development is NON-NEGOTIABLE** per constitution.
