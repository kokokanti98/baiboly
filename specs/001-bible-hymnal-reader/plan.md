# Implementation Plan: Plateforme Baiboly sy Fihirana

**Branch**: `001-bible-hymnal-reader` | **Date**: 2025-11-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-bible-hymnal-reader/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements a responsive web and mobile platform for reading the Bible (Baiboly) and evangelical hymns (Fihirana) in Malagasy. The application consists of two main sections: (1) Bible reading with search by book, chapter, verse reference, or content; (2) Hymnal access with search by hymn number or content (title/lyrics). Data sources are open-source GitHub repositories containing 66 Bible books and 3 hymn collections in JSON format. The technical approach uses Flask/Python backend with PostgreSQL for full-text search capabilities, React/TypeScript frontend with responsive design, and PostgreSQL's native full-text search for Malagasy content.

## Technical Context

**Language/Version**: Python 3.9+ (backend), TypeScript 5+ / JavaScript ES2022 (frontend)
**Primary Dependencies**:
- Backend: Flask 3.x, Flask-RESTful, SQLAlchemy 2.x, Flask-Migrate, Flask-Babel, psycopg2
- Frontend: React 18+, React Router 6+, Axios, react-i18next, Vite

**Storage**: PostgreSQL 13+ with full-text search for Malagasy content (tsvector columns)
**Testing**:
- Backend: pytest, pytest-flask, pytest-cov (≥80% coverage required)
- Frontend: Jest, React Testing Library, Playwright/Cypress (≥75% coverage required)

**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge latest 2 versions) + mobile web (Android 8+, iOS 13+)
**Project Type**: Web application (separate backend and frontend)
**Performance Goals**:
- API response time: <200ms p95
- Search queries: <2 seconds
- Initial page load: <3 seconds on 3G
- Time to Interactive: <3.5 seconds on 3G

**Constraints**:
- All UI text MUST be in Malagasy (default language)
- Responsive design: mobile ≥375px, tablet ≥768px, desktop ≥1024px
- Touch targets: ≥44x44 pixels on mobile
- Bundle size: <500KB gzipped main bundle
- Accessibility: WCAG 2.1 AA compliance

**Scale/Scope**:
- 66 Bible books (~31,000 verses estimated)
- ~500-1000 hymns across 3 collections
- Expected concurrent users: 100-500 initially
- Database size: ~50-100MB (text content)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Code Quality & Maintainability
- ✅ Backend: Python 3.9+ with PEP 8, type hints, black formatting, flake8 linting
- ✅ Frontend: TypeScript 5+ with ESLint, Prettier, functional components with hooks
- ✅ Flask blueprints for route organization (bible, fihirana, search blueprints)
- ✅ Component files <300 lines, CSS-in-JS or CSS Modules
- ✅ Docstrings for all modules, TypeScript interfaces for all props

### Testing Standards & TDD (NON-NEGOTIABLE)
- ✅ TDD workflow: Red-Green-Refactor cycle mandatory
- ✅ Backend: pytest with ≥80% coverage, integration tests for all API endpoints
- ✅ Frontend: Jest + React Testing Library, ≥75% coverage, E2E with Playwright/Cypress
- ✅ Test structure mirrors source: `backend/src/services/bible.py` → `backend/tests/unit/services/test_bible.py`

### User Experience Consistency
- ✅ Malagasy as default language for ALL user-facing content
- ✅ i18n implementation: react-i18next (frontend), Flask-Babel (backend)
- ✅ Responsive design: mobile (≥375px), tablet (≥768px), desktop (≥1024px)
- ✅ Loading states for operations >500ms
- ✅ Error messages in Malagasy, user-friendly and actionable
- ✅ WCAG 2.1 AA compliance: keyboard navigation, ARIA labels, 4.5:1 contrast ratio
- ✅ Touch targets ≥44x44 pixels on mobile

### Performance Requirements
- ✅ API endpoints <200ms p95 response time
- ✅ Pagination for results >50 records
- ✅ Full-text search optimized with PostgreSQL indexes
- ✅ Frontend: FCP <2s on 3G, TTI <3.5s on 3G
- ✅ Bundle size <500KB gzipped, lazy loading for routes
- ✅ Lighthouse CI on every PR, scores must be ≥85

### Technology Stack Compliance
- ✅ Backend: Python 3.9+, Flask, PostgreSQL 13+, SQLAlchemy, Flask-Migrate
- ✅ Frontend: React 18+, TypeScript 5+, Vite build tool
- ✅ Database: PostgreSQL 13+ with native full-text search for Malagasy
- ✅ State Management: Context API + useReducer (simple state), Redux Toolkit/Zustand if complex state needed
- ✅ API Documentation: OpenAPI/Swagger for all endpoints

### Gate Status: ✅ PASSED

All constitutional requirements are satisfied by the planned architecture. No violations or exceptions required.

## Project Structure

### Documentation (this feature)

```text
specs/001-bible-hymnal-reader/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification (completed)
├── research.md          # Phase 0 output (data import strategy, full-text search)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API specifications)
│   ├── bible-api.yaml
│   └── fihirana-api.yaml
├── checklists/
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created yet)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLAlchemy models (Livre, Chapitre, Verset, Chant)
│   │   ├── __init__.py
│   │   ├── bible.py     # Livre, Chapitre, Verset models
│   │   └── fihirana.py  # Chant model
│   ├── services/        # Business logic
│   │   ├── __init__.py
│   │   ├── bible_service.py
│   │   ├── fihirana_service.py
│   │   └── search_service.py
│   ├── api/             # Flask blueprints
│   │   ├── __init__.py
│   │   ├── bible.py     # Bible endpoints
│   │   ├── fihirana.py  # Fihirana endpoints
│   │   └── search.py    # Search endpoints
│   ├── utils/           # Helper functions
│   │   ├── __init__.py
│   │   └── validators.py
│   ├── config.py        # Configuration
│   ├── app.py           # Flask app factory
│   └── cli.py           # CLI commands for data import
├── migrations/          # Alembic migrations
├── tests/
│   ├── unit/            # Unit tests mirroring src/ structure
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   ├── integration/     # API integration tests
│   └── conftest.py      # Pytest fixtures
├── requirements.txt     # Python dependencies
├── setup.py
└── README.md

frontend/
├── src/
│   ├── components/      # Reusable React components
│   │   ├── common/      # Shared components (Button, Input, etc.)
│   │   ├── bible/       # Bible-specific components
│   │   └── fihirana/    # Fihirana-specific components
│   ├── pages/           # Page components (routes)
│   │   ├── Home.tsx
│   │   ├── Bible.tsx
│   │   └── Fihirana.tsx
│   ├── services/        # API client services
│   │   ├── api.ts       # Axios configuration
│   │   ├── bibleService.ts
│   │   └── fihiranaService.ts
│   ├── hooks/           # Custom React hooks
│   ├── i18n/            # Internationalization
│   │   ├── config.ts
│   │   └── mg/          # Malagasy translations
│   │       └── translation.json
│   ├── types/           # TypeScript type definitions
│   ├── App.tsx          # Root component
│   ├── main.tsx         # Entry point
│   └── vite-env.d.ts
├── tests/
│   ├── unit/            # Component unit tests
│   └── e2e/             # End-to-end tests (Playwright)
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md

scripts/                 # Data import scripts
├── import_bible.py      # Import Bible JSON data
└── import_fihirana.py   # Import Fihirana JSON data

.github/
└── workflows/           # CI/CD pipelines
    ├── backend-ci.yml
    └── frontend-ci.yml
```

**Structure Decision**: Web application structure (Option 2) selected due to clear separation between Flask REST API backend and React SPA frontend. This enables:
- Independent deployment and scaling of backend/frontend
- Clear API contracts between layers
- Separate testing strategies for each layer
- Team specialization (backend vs. frontend developers)
- Constitution compliance with Flask blueprints and React component organization

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitutional requirements are met by the proposed architecture.
