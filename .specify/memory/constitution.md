<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.2.0
Ratified: 2025-11-18
Last Amended: 2025-11-18

MINOR version bump: Technology stack finalized (PostgreSQL) based on data source analysis

Principles Defined:
- I. Code Quality & Maintainability (Python/Flask backend, React frontend)
- II. Testing Standards & Test-Driven Development
- III. User Experience Consistency (includes Malagasy language requirement)
- IV. Performance Requirements

Additional Sections:
- Technology Stack Constraints (Flask + React + PostgreSQL specifics)
- Development Workflow (review, quality gates)
- Governance (amendment procedures, compliance)

Key Requirements:
- Malagasy as default language for all user-facing content
- i18n implementation required (react-i18next, Flask-Babel)
- Malagasy locale conventions for dates, times, numbers
- PostgreSQL 13+ MANDATORY for all data storage (FINAL in v1.2.0)

Changes in v1.2.0:
- Changed from DynamoDB to PostgreSQL as mandatory database
- PostgreSQL chosen for: full-text search, relational structure, cost efficiency, existing data compatibility
- Added SQLAlchemy ORM requirement
- Added Alembic/Flask-Migrate for migrations
- Added full-text search requirement for Malagasy content

Data Sources Identified:
- Bible: RaveloMevaSoavina/baiboly-json (66 books in JSON format, Malagasy)
  - Testameta taloha: 39 Old Testament books
  - Testameta vaovao: 27 New Testament books
- Fihirana: Rohan29-AN/Fihirana-FFPM (3 JSON files with SQL generation script)
  - 01_fihirana_ffpm.json
  - 02_fihirana_fanampiny.json
  - 03_antema.json

Templates Status:
✅ plan-template.md - Reviewed, constitution check section aligns
✅ spec-template.md - Reviewed, user stories and requirements align
✅ tasks-template.md - Reviewed, test-first approach and task organization align

Follow-up TODOs:
- None - all placeholders filled

Notes:
- This constitution establishes foundational principles for a Flask/React web application
- Emphasizes TDD, code quality, UX consistency, and performance
- Malagasy language is mandatory for all user-facing content
- PostgreSQL chosen for superior full-text search and relational data modeling
- Data sources are open and available on GitHub
- Version 1.2.0 finalizes technology stack based on data analysis
-->

# Baiboly Constitution

## Core Principles

### I. Code Quality & Maintainability

**Backend (Python/Flask)**:
- All Python code MUST follow PEP 8 style guidelines with maximum line length of 100 characters
- Type hints MUST be used for all function signatures and class attributes
- Linting (flake8/pylint) and formatting (black) MUST pass with zero violations before commits
- Code complexity: Functions exceeding cyclomatic complexity of 10 REQUIRE justification and refactoring plan
- All modules MUST have docstrings explaining purpose, key classes, and usage examples
- Flask blueprints MUST be used for route organization; no monolithic route files

**Frontend (React)**:
- All React components MUST be functional components using hooks (no class components without justification)
- TypeScript MUST be used; `any` type requires explicit justification in code comments
- ESLint and Prettier MUST pass with zero violations before commits
- Component files MUST NOT exceed 300 lines; refactor into smaller components if exceeded
- PropTypes or TypeScript interfaces MUST define all component props
- CSS-in-JS or CSS Modules MUST be used; no global CSS without justification

**Rationale**: Consistent code quality reduces technical debt, improves collaboration, and ensures long-term maintainability. Specific rules for Python/Flask and React/TypeScript prevent common pitfalls in full-stack development.

### II. Testing Standards & Test-Driven Development (NON-NEGOTIABLE)

**Test-Driven Development Workflow**:
1. Write test(s) for new functionality or bug fix
2. Verify tests FAIL (red phase)
3. Implement minimal code to pass tests (green phase)
4. Refactor while keeping tests green (refactor phase)
5. Commit only after tests pass

**Backend Testing Requirements**:
- **Unit Tests**: All Flask routes, services, and utility functions MUST have unit tests with ≥80% code coverage
- **Integration Tests**: All API endpoints MUST have integration tests verifying request/response contracts
- **Contract Tests**: Any external API calls or database interactions MUST have contract tests
- Testing framework: pytest with pytest-flask
- Mocking: Use unittest.mock or pytest-mock for external dependencies
- Test files MUST mirror source structure: `src/services/auth.py` → `tests/unit/services/test_auth.py`

**Frontend Testing Requirements**:
- **Component Tests**: All React components MUST have tests verifying rendering and user interactions
- **Integration Tests**: Critical user flows MUST have end-to-end tests
- Testing frameworks: Jest + React Testing Library for components, Playwright/Cypress for E2E
- Test coverage: ≥75% for components, 100% for critical business logic
- Snapshot tests MAY be used for UI consistency but MUST NOT replace behavioral tests

**Rationale**: TDD ensures correctness from the start, reduces debugging time, provides living documentation, and enables confident refactoring. Separate requirements for backend/frontend acknowledge different testing paradigms.

### III. User Experience Consistency

**Design System & Component Library**:
- A shared design system MUST define colors, typography, spacing, and component patterns
- All UI components MUST come from a centralized component library (e.g., Material-UI, Chakra UI, or custom)
- Custom styling that deviates from the design system REQUIRES design team approval

**Interaction Patterns**:
- Loading states MUST be shown for all async operations >500ms
- Error messages MUST be user-friendly, actionable, and consistent in tone
- Form validation MUST provide real-time feedback with clear error messages
- Success/failure feedback MUST use consistent notification patterns (toasts, alerts, etc.)

**Accessibility (A11y)**:
- All interactive elements MUST be keyboard navigable
- ARIA labels MUST be provided for screen readers where semantic HTML insufficient
- Color contrast MUST meet WCAG 2.1 AA standards (4.5:1 for normal text, 3:1 for large text)
- All images MUST have descriptive alt text

**Internationalization & Localization**:
- Malagasy MUST be the default language for all user-facing content
- All text content MUST be externalized using i18n libraries (react-i18next for frontend, Flask-Babel for backend)
- UI MUST support language switching if multiple languages are planned for future
- Date, time, and number formats MUST follow Malagasy locale conventions
- All error messages, validation feedback, and system notifications MUST be in Malagasy

**Responsive Design**:
- UI MUST be fully functional on mobile (≥375px), tablet (≥768px), and desktop (≥1024px) viewports
- Touch targets MUST be ≥44x44 pixels on mobile devices

**Rationale**: Consistent UX builds user trust, reduces cognitive load, and ensures accessibility for all users. Clear standards prevent fragmentation across the application. Malagasy as the default language ensures the application serves its primary audience effectively.

### IV. Performance Requirements

**Backend Performance**:
- API endpoints MUST respond within 200ms for p95 requests under normal load
- Database queries MUST be optimized; N+1 queries REQUIRE resolution before merge
- Pagination MUST be implemented for endpoints returning >50 records
- Caching strategy (Redis/in-memory) MUST be used for frequently accessed, slowly changing data
- Background tasks (Celery/RQ) MUST be used for operations >2 seconds

**Frontend Performance**:
- Initial page load (First Contentful Paint) MUST be <2 seconds on 3G networks
- Time to Interactive (TTI) MUST be <3.5 seconds on 3G networks
- Bundle size: Main bundle MUST be <500KB gzipped; lazy loading REQUIRED for route-based code splitting
- Images MUST be optimized (WebP format preferred, <200KB per image)
- React re-renders: Use React.memo, useMemo, useCallback to prevent unnecessary renders in lists/large components

**Monitoring & Measurement**:
- Backend: Flask instrumentation with logging for request/response times
- Frontend: Lighthouse CI MUST run on every PR; scores <85 REQUIRE optimization plan
- Real User Monitoring (RUM) SHOULD be implemented for production performance tracking

**Rationale**: Performance directly impacts user satisfaction and retention. Concrete metrics ensure accountability and prevent performance regressions during development.

## Technology Stack Constraints

**Backend Requirements**:
- Python: 3.9+ (for type hinting improvements)
- Flask: Latest stable version with Flask-RESTful or Flask-RESTX for API structure
- Database: PostgreSQL 13+ (MANDATORY) for all data storage and retrieval
- ORM: SQLAlchemy for database operations
- Migrations: Alembic or Flask-Migrate for schema versioning
- Full-Text Search: PostgreSQL native full-text search for Malagasy content
- Authentication: Flask-JWT-Extended or Flask-Login
- Environment management: python-dotenv for configuration

**Frontend Requirements**:
- React: 18+ (for concurrent features)
- TypeScript: 5+
- State Management: Context API + useReducer for simple state, Redux Toolkit or Zustand for complex state
- Routing: React Router 6+
- HTTP Client: Axios or Fetch API with custom hooks
- Build Tool: Vite (preferred) or Create React App

**Development Tools**:
- Version Control: Git with conventional commit messages
- API Documentation: OpenAPI/Swagger for backend endpoints
- Code Quality: pre-commit hooks for linting and formatting checks

## Development Workflow

**Code Review Requirements**:
- All code changes MUST be reviewed by at least one other developer before merge
- PR description MUST include: purpose, testing performed, screenshots (if UI changes)
- Reviewers MUST verify: tests pass, code quality standards met, constitution compliance

**Quality Gates (CI/CD)**:
- All tests (unit, integration, E2E) MUST pass
- Linting and formatting checks MUST pass
- Code coverage MUST NOT decrease below current baseline
- Lighthouse CI MUST show no performance regressions
- Security vulnerability scanning (Snyk/Dependabot) MUST show no high/critical issues

**Deployment Process**:
- Staging environment MUST mirror production configuration
- Manual QA testing MUST occur in staging before production deployment
- Database migrations MUST be tested in staging before production
- Rollback plan MUST be documented for each production deployment

## Governance

**Constitution Authority**:
- This constitution supersedes all other development practices and guidelines
- In case of conflict between this constitution and other documentation, constitution takes precedence

**Amendment Procedure**:
- Amendments MUST be proposed with clear rationale and impact analysis
- Amendments REQUIRE approval from project maintainers and technical lead
- Major amendments (principle changes) REQUIRE migration plan for existing code
- Constitution version MUST be incremented following semantic versioning:
  - MAJOR: Breaking changes to principles or governance
  - MINOR: New principles added or significant expansions
  - PATCH: Clarifications, wording improvements, non-semantic changes

**Compliance & Enforcement**:
- All pull requests MUST verify constitutional compliance before merge
- Complexity or deviations from principles MUST be explicitly justified in PR description
- Technical debt exceptions MAY be granted with documented repayment timeline

**Version**: 1.2.0 | **Ratified**: 2025-11-18 | **Last Amended**: 2025-11-18