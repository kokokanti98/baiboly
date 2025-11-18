# Baiboly - Project Overview

**Version:** 0.1.0 (In Development)
**Last Updated:** 2025-11-18
**Status:** Phase 3 - User Story 1 Implementation (Bible Reading Feature)

---

## 📋 Table of Contents

1. [Project Description](#project-description)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Development Environment](#development-environment)
5. [Current Implementation Status](#current-implementation-status)
6. [Constitution & Principles](#constitution--principles)
7. [Data Sources](#data-sources)
8. [Key Features](#key-features)
9. [Getting Started](#getting-started)
10. [Testing Strategy](#testing-strategy)
11. [Next Steps](#next-steps)

---

## 🎯 Project Description

**Baiboly** is a responsive web/mobile application for reading the Bible and evangelical hymns (Lutheran and FJKM) in **Malagasy language**. The application provides:

- **Bible (Baiboly):** Search and read Bible verses by book, chapter, verse reference, or full-text content search
- **Fihirana (Hymnal):** Search hymns by number or content (title/lyrics) from FFPM, Fanampiny, and Antema collections

### Primary Language
- **Malagasy (mg)** is the default and primary language throughout the entire application (UI, API responses, error messages, documentation)

### Target Users
- Malagasy-speaking Christians
- Mobile-first audience (responsive design required)
- Users seeking Bible study and worship resources

---

## 🛠 Technology Stack

### Backend
- **Language:** Python 3.9+
- **Framework:** Flask 3.x
- **API:** Flask-RESTful (RESTful API design)
- **Database:** PostgreSQL 13+ (with full-text search using tsvector and GIN indexes)
- **ORM:** SQLAlchemy 2.x
- **Migrations:** Flask-Migrate (Alembic)
- **i18n:** Flask-Babel (Malagasy default)
- **Testing:** pytest, pytest-flask (≥80% coverage required)
- **Code Quality:** black (formatter), flake8 (linter), pre-commit hooks

### Frontend
- **Language:** TypeScript 5+
- **Framework:** React 18+
- **Build Tool:** Vite
- **Routing:** React Router 6+
- **UI Library:** Material-UI v5 (MUI)
- **HTTP Client:** Axios
- **i18n:** react-i18next (Malagasy default)
- **Testing:** Jest, React Testing Library, Playwright (≥75% coverage required)
- **Code Quality:** ESLint, Prettier, pre-commit hooks

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Database:** PostgreSQL 13 (Alpine) in Docker
- **Development:** Hot-reload enabled for both frontend and backend

---

## 📁 Project Structure

```
baiboly/
├── backend/                    # Flask backend API
│   ├── src/
│   │   ├── app.py             # Flask application factory
│   │   ├── config.py          # Environment-based configuration
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   └── bible.py       # Livre, Chapitre, Verset models
│   │   ├── services/          # Business logic layer
│   │   │   ├── bible_service.py    # Bible data operations
│   │   │   └── search_service.py   # Full-text search
│   │   ├── routes/            # API endpoints (Flask blueprints)
│   │   └── utils/             # Utility functions
│   ├── tests/                 # Pytest tests
│   │   ├── conftest.py        # Test fixtures
│   │   ├── test_models_bible.py
│   │   ├── test_services_bible.py
│   │   └── test_api_bible.py
│   ├── migrations/            # Database migrations (Alembic)
│   ├── scripts/               # Utility scripts
│   │   └── init-db.sql        # PostgreSQL initialization
│   ├── requirements.txt       # Python dependencies
│   ├── pytest.ini             # Pytest configuration
│   ├── Dockerfile             # Backend Docker image
│   ├── .env.example           # Environment template
│   └── SETUP.md               # Detailed setup instructions
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── main.tsx           # Application entry point
│   │   ├── App.tsx            # Root component with routing
│   │   ├── theme.ts           # Material-UI theme (green/red palette)
│   │   ├── components/        # React components
│   │   │   ├── Bible/         # Bible reading components
│   │   │   └── Fihirana/      # Hymnal components
│   │   ├── services/
│   │   │   └── api.ts         # Axios API client
│   │   ├── i18n/              # Internationalization
│   │   │   ├── config.ts      # i18next setup
│   │   │   └── mg/            # Malagasy translations
│   │   │       └── translation.json
│   │   └── __mocks__/         # Jest mocks
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.ts         # Vite configuration
│   ├── jest.config.ts         # Jest configuration
│   ├── Dockerfile             # Frontend Docker image
│   └── .env.example           # Environment template
│
├── specs/                      # Project specifications
│   └── 001-bible-hymnal-reader/
│       ├── spec.md            # Feature specification
│       ├── plan.md            # Implementation plan
│       ├── research.md        # Design decisions
│       ├── data-model.md      # Database schema
│       ├── tasks.md           # Implementation tasks (167 tasks)
│       ├── quickstart.md      # Developer quickstart guide
│       └── contracts/         # API contracts (OpenAPI)
│           ├── bible-api.yaml
│           └── fihirana-api.yaml
│
├── .specify/                   # Speckit configuration
│   └── memory/
│       └── constitution.md    # Project constitution (v1.2.0)
│
├── docker-compose.yml          # Multi-container orchestration
├── .dockerignore              # Docker build exclusions
├── .gitignore                 # Git exclusions
├── .pre-commit-config.yaml    # Pre-commit hooks
├── start.sh                   # Launch script (Linux/Mac)
├── start.bat                  # Launch script (Windows)
└── PROJECT_OVERVIEW.md        # This file
```

---

## 🚀 Development Environment

### Docker Compose Services

The application runs in Docker containers:

1. **db** (PostgreSQL 13)
   - Port: 5432
   - Database: `baiboly_dev`
   - User: `baiboly_user`
   - Password: `dev_password_2025`

2. **backend** (Flask API)
   - Port: 5000
   - Health check: `http://localhost:5000/api/health`
   - Auto-reload enabled

3. **frontend** (React + Vite)
   - Port: 5173
   - Hot-reload enabled
   - Proxies `/api` to backend

4. **pgadmin** (Optional - Database Management)
   - Port: 5050
   - Login: `admin@baiboly.local` / `admin`
   - Start with: `docker-compose --profile tools up -d pgadmin`

### Quick Start

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Manual Docker Compose:**
```bash
docker-compose up --build -d
```

### Accessing Services
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- API Health: http://localhost:5000/api/health
- pgAdmin: http://localhost:5050 (if started)

### Viewing Logs
```bash
docker-compose logs -f              # All services
docker-compose logs -f backend      # Backend only
docker-compose logs -f frontend     # Frontend only
```

### Stopping Services
```bash
docker-compose down                 # Stop containers
docker-compose down -v              # Stop and remove volumes
```

---

## ✅ Current Implementation Status

### Phase 1: Setup (T001-T008) ✅ COMPLETED
- ✅ Project structure created
- ✅ `.gitignore` configured
- ✅ Pre-commit hooks setup
- ✅ Environment templates created

### Phase 2: Foundational (T009-T020) ✅ COMPLETED
- ✅ Flask application factory (`backend/src/app.py`)
- ✅ Configuration management (`backend/src/config.py`)
- ✅ React Router setup (`frontend/src/App.tsx`)
- ✅ i18next configuration (Malagasy default)
- ✅ Material-UI theme (green/red palette, ≥44px touch targets)
- ✅ Axios API client with Malagasy error messages
- ✅ Pytest configuration (≥80% coverage)
- ✅ Jest configuration (≥75% coverage)
- ⏸️ T020: Database migration (ready, will run on Docker startup)

### Phase 3: User Story 1 - Bible Reading (T021-T077) 🚧 IN PROGRESS

#### Tests Written (TDD) ✅ COMPLETED
- ✅ T021: Model tests (`test_models_bible.py` - 30+ tests)
- ✅ T022: Service tests (`test_services_bible.py` - 25+ tests)
- ✅ T023: API tests (`test_api_bible.py` - 25+ tests)
- ✅ T024: BibleReader component tests (13 tests)
- ✅ T025: BibleSearch component tests (18 tests)

#### Backend Implementation ✅ PARTIALLY COMPLETED
- ✅ T034: Bible models (`Livre`, `Chapitre`, `Verset`)
- ✅ T035-T038: Database migrations (ready)
- ✅ T039-T041: BibleService implementation
- ✅ T042-T043: SearchService implementation
- ⏳ T044-T054: API endpoints (Flask-RESTful resources) - **NEXT**

#### Frontend Implementation ⏳ NOT STARTED
- ⏳ T060-T070: React components (BibleReader, BibleSearch, etc.)

#### Data Import ⏳ NOT STARTED
- ⏳ T055-T059: Import scripts for Bible data from GitHub sources

#### Verification ⏳ NOT STARTED
- ⏳ T071-T077: End-to-end testing and documentation

### Phase 4-6: Remaining User Stories ⏳ NOT STARTED
- Phase 4: User Story 2 - Fihirana (T078-T124)
- Phase 5: User Story 3 - Navigation (T125-T145)
- Phase 6: Polish & Optimization (T146-T167)

---

## 📜 Constitution & Principles

**Version:** 1.2.0
**Location:** `.specify/memory/constitution.md`

### Core Principles

1. **Code Quality**
   - PEP 8 compliance (Python)
   - Type hints required
   - ESLint + Prettier (TypeScript/React)
   - Pre-commit hooks enforced

2. **Testing & TDD**
   - **Non-negotiable:** Write tests BEFORE implementation
   - Backend: ≥80% coverage (pytest)
   - Frontend: ≥75% coverage (Jest + RTL + Playwright)
   - Test markers: `unit`, `integration`, `bible`, `fihirana`, `search`, `slow`

3. **UX Consistency**
   - Material-UI v5 components only
   - Touch targets: ≥44x44px (constitutional requirement)
   - Mobile-first responsive design (375px, 768px, 1024px breakpoints)
   - Color palette: Green primary (#2e7d32), Red secondary (#c62828)

4. **Performance Requirements**
   - API response time: <200ms (p95)
   - Search operations: <2s
   - First Contentful Paint (FCP): <2s on 3G
   - Time to Interactive (TTI): <3.5s on 3G

### Technology Constraints (Must Haves)

- **Database:** PostgreSQL 13+ (with full-text search)
- **Backend:** Python 3.9+, Flask 3.x
- **Frontend:** React 18+, TypeScript 5+
- **Default Language:** Malagasy (`mg`) throughout entire stack

---

## 📊 Data Sources

### Bible Data
- **Repository:** https://github.com/RaveloMevaSoavina/baiboly-json
- **Format:** JSON files
- **Structure:** 66 books (39 Old Testament, 27 New Testament)
- **Language:** Malagasy
- **Files:**
  - Old Testament: `Testameta taloha/` (e.g., `genesisy.json`)
  - New Testament: `Testameta vaovao/` (e.g., `matio.json`)

### Fihirana (Hymnal) Data
- **Repository:** https://github.com/Rohan29-AN/Fihirana-FFPM
- **Format:** JSON files + SQL schema
- **Collections:**
  - FFPM (Primary collection)
  - Fanampiny (Supplementary)
  - Antema (Anthems)
- **Fields:** numero (number), titre (title), paroles (lyrics)

---

## 🎯 Key Features

### User Story 1: Bible Reading (Current Focus)
**Priority:** P1 (MVP)

**Functional Requirements:**
- FR-001: Display all Bible books ordered by testament and canonical order
- FR-002: Filter books by testament (Old/New)
- FR-003: Display chapters for selected book
- FR-004: Display verses for selected chapter with verse numbers
- FR-005: Full-text search across all verses
- FR-006: Search results show book, chapter, verse reference
- FR-007: Highlight search terms in results
- FR-008: Reference-based verse lookup (e.g., "Gen 1:1")
- FR-009: Responsive mobile/desktop layout
- FR-010: All UI in Malagasy

### User Story 2: Fihirana (Hymnal)
**Priority:** P2

**Functional Requirements:**
- FR-011: Display hymns by collection (FFPM, Fanampiny, Antema)
- FR-012: Search hymns by number
- FR-013: Search hymns by title or lyrics (full-text)
- FR-014: Display complete hymn with title, number, and lyrics
- FR-015: Responsive layout
- FR-016: All UI in Malagasy

### User Story 3: Navigation
**Priority:** P3

**Functional Requirements:**
- FR-017: Home page with navigation to Bible/Fihirana
- FR-018: Persistent navigation bar
- FR-019: Breadcrumb navigation
- FR-020: Responsive hamburger menu on mobile

---

## 🏃 Getting Started

### Prerequisites
- Docker Desktop installed
- Git installed
- Terminal/Command Prompt

### First-Time Setup

1. **Clone repository:**
   ```bash
   cd C:\Dev
   git clone <repository-url> baiboly
   cd baiboly
   ```

2. **Start application:**
   ```bash
   # Windows
   start.bat

   # Linux/Mac
   chmod +x start.sh
   ./start.sh
   ```

3. **Wait for services to start** (~30-60 seconds)

4. **Access application:**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:5000/api/health

### Development Workflow

1. **Make code changes** in `backend/` or `frontend/`
2. **Changes auto-reload** (no restart needed)
3. **Run tests:**
   ```bash
   # Backend tests
   docker-compose exec backend pytest

   # Frontend tests
   docker-compose exec frontend npm test
   ```

4. **View logs:**
   ```bash
   docker-compose logs -f
   ```

5. **Stop application:**
   ```bash
   docker-compose down
   ```

### Database Access

**Via pgAdmin:**
1. Start pgAdmin: `docker-compose --profile tools up -d pgadmin`
2. Open: http://localhost:5050
3. Login: `admin@baiboly.local` / `admin`
4. Add server:
   - Host: `db`
   - Port: `5432`
   - Database: `baiboly_dev`
   - Username: `baiboly_user`
   - Password: `dev_password_2025`

**Via psql:**
```bash
docker-compose exec db psql -U baiboly_user -d baiboly_dev
```

---

## 🧪 Testing Strategy

### Test-Driven Development (TDD)
**Constitutional requirement:** Tests MUST be written before implementation.

### Backend Testing (pytest)

**Run tests:**
```bash
docker-compose exec backend pytest                    # All tests
docker-compose exec backend pytest -m unit            # Unit tests only
docker-compose exec backend pytest -m integration     # Integration tests
docker-compose exec backend pytest -m bible           # Bible feature tests
docker-compose exec backend pytest --cov=src          # With coverage
```

**Test files:**
- `backend/tests/test_models_bible.py` - Model tests
- `backend/tests/test_services_bible.py` - Service tests
- `backend/tests/test_api_bible.py` - API endpoint tests

**Coverage requirement:** ≥80%

### Frontend Testing (Jest + RTL)

**Run tests:**
```bash
docker-compose exec frontend npm test                 # All tests
docker-compose exec frontend npm test -- --coverage   # With coverage
docker-compose exec frontend npm run test:e2e         # E2E tests (Playwright)
```

**Test files:**
- `frontend/src/components/Bible/__tests__/BibleReader.test.tsx`
- `frontend/src/components/Bible/__tests__/BibleSearch.test.tsx`

**Coverage requirement:** ≥75%

### Test Markers

Backend test markers (pytest):
- `@pytest.mark.unit` - Fast, isolated tests
- `@pytest.mark.integration` - Database/API tests
- `@pytest.mark.bible` - Bible feature tests
- `@pytest.mark.fihirana` - Hymnal feature tests
- `@pytest.mark.search` - Full-text search tests
- `@pytest.mark.slow` - Performance tests

---

## 🔜 Next Steps

### Immediate Tasks (Next Session)

1. **T044-T054: Implement Bible API Endpoints**
   - Create Flask-RESTful resources
   - Endpoints for livres, chapitres, versets, search
   - Error handling in Malagasy
   - Performance optimization

2. **T055-T059: Data Import**
   - Write Python script to import Bible JSON data
   - Populate `livre`, `chapitre`, `verset` tables
   - Update `texte_search_vector` for full-text search

3. **T060-T070: Frontend Components**
   - Implement `BibleReader` component
   - Implement `BibleSearch` component
   - Implement `BibleBookList` component
   - Implement `BibleChapterView` component
   - Implement `BibleVerseList` component

4. **T071-T077: Verification & Testing**
   - Run all tests (backend + frontend)
   - End-to-end testing
   - Performance testing
   - Documentation updates

### Mid-Term Tasks

- Complete User Story 2: Fihirana (Hymnal)
- Complete User Story 3: Navigation
- Polish and optimization phase

### Long-Term Goals

- Production deployment setup
- CI/CD pipeline
- Additional features (bookmarks, notes, sharing)

---

## 📝 Important Notes

### Malagasy Language
All user-facing text MUST be in Malagasy:
- UI labels and buttons
- Error messages
- API responses
- Form validation messages
- Search placeholders

### Touch Target Sizes
All interactive elements (buttons, links) MUST be ≥44x44px for mobile accessibility.

### Performance Monitoring
Monitor and ensure:
- API responses <200ms (p95)
- Search operations <2s
- Page load times <2s FCP, <3.5s TTI on 3G

### Database Full-Text Search
PostgreSQL tsvector is used for Malagasy text search with 'simple' configuration (no stemming). GIN indexes ensure fast search performance.

---

## 🤝 Contributing

1. Follow TDD: Write tests first
2. Run tests before committing
3. Use pre-commit hooks (automatic)
4. Follow code style (black, ESLint, Prettier)
5. All commits in Malagasy or English
6. Reference task IDs in commits (e.g., "T044: Implement Bible API endpoints")

---

## 📞 Contact & Resources

- **Project Spec:** `specs/001-bible-hymnal-reader/spec.md`
- **Constitution:** `.specify/memory/constitution.md`
- **Tasks:** `specs/001-bible-hymnal-reader/tasks.md`
- **API Contracts:** `specs/001-bible-hymnal-reader/contracts/`

---

**Last Updated:** 2025-11-18
**Current Phase:** Phase 3 - User Story 1 Implementation
**Next Milestone:** Complete Bible Reading MVP (T044-T077)
