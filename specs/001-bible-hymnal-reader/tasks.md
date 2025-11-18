# Tasks: Plateforme Baiboly sy Fihirana

**Input**: Design documents from `/specs/001-bible-hymnal-reader/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: TDD approach is MANDATORY per constitution. All tests must be written FIRST and FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Scripts**: `scripts/` (data import scripts)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure (src/models, src/services, src/api, src/utils, tests/)
- [X] T002 Create frontend directory structure (src/components, src/pages, src/services, src/hooks, src/i18n, tests/)
- [X] T003 [P] Initialize Python virtual environment and install dependencies in backend/requirements.txt
- [X] T004 [P] Initialize Node.js project and install dependencies in frontend/package.json
- [ ] T005 [P] Setup PostgreSQL database and create baiboly_dev database
- [X] T006 [P] Configure backend environment variables in backend/.env
- [X] T007 [P] Configure frontend environment variables in frontend/.env
- [X] T008 [P] Setup pre-commit hooks for code quality (black, flake8, eslint, prettier)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Initialize Flask application factory in backend/src/app.py
- [ ] T010 Configure Flask-Migrate for database migrations in backend/src/config.py
- [ ] T011 Setup Flask-Babel for i18n in backend/src/app.py
- [ ] T012 Create base SQLAlchemy models structure in backend/src/models/__init__.py
- [ ] T013 [P] Setup React Router configuration in frontend/src/App.tsx
- [ ] T014 [P] Configure react-i18next with Malagasy translations in frontend/src/i18n/config.ts
- [ ] T015 [P] Create Malagasy translation file in frontend/src/i18n/mg/translation.json
- [ ] T016 [P] Setup Material-UI theme with custom configuration in frontend/src/theme.ts
- [ ] T017 [P] Create Axios API client configuration in frontend/src/services/api.ts
- [ ] T018 Create pytest configuration and fixtures in backend/tests/conftest.py
- [ ] T019 Create Jest configuration in frontend/jest.config.js
- [ ] T020 Run initial database migration to create empty schema

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Lecture et recherche de versets bibliques (Priority: P1) 🎯 MVP

**Goal**: Permettre aux utilisateurs de lire la Bible en Malagasy et rechercher des versets par référence ou contenu

**Independent Test**: Un utilisateur peut lister les 66 livres de la Bible, naviguer vers un chapitre/verset, et effectuer une recherche de contenu qui retourne des résultats pertinents

### Tests for User Story 1 (TDD - Write FIRST) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T021 [P] [US1] Write unit tests for Livre model in backend/tests/unit/models/test_bible.py
- [ ] T022 [P] [US1] Write unit tests for Chapitre model in backend/tests/unit/models/test_bible.py
- [ ] T023 [P] [US1] Write unit tests for Verset model in backend/tests/unit/models/test_bible.py
- [ ] T024 [P] [US1] Write unit tests for BibleService in backend/tests/unit/services/test_bible_service.py
- [ ] T025 [P] [US1] Write unit tests for SearchService (Bible search) in backend/tests/unit/services/test_search_service.py
- [ ] T026 [P] [US1] Write integration tests for GET /api/bible/books in backend/tests/integration/test_bible_api.py
- [ ] T027 [P] [US1] Write integration tests for GET /api/bible/books/{id}/chapters in backend/tests/integration/test_bible_api.py
- [ ] T028 [P] [US1] Write integration tests for GET /api/bible/books/{id}/chapters/{num}/verses in backend/tests/integration/test_bible_api.py
- [ ] T029 [P] [US1] Write integration tests for POST /api/bible/search in backend/tests/integration/test_bible_api.py
- [ ] T030 [P] [US1] Write component tests for BookList component in frontend/tests/unit/components/bible/BookList.test.tsx
- [ ] T031 [P] [US1] Write component tests for ChapterList component in frontend/tests/unit/components/bible/ChapterList.test.tsx
- [ ] T032 [P] [US1] Write component tests for VerseList component in frontend/tests/unit/components/bible/VerseList.test.tsx
- [ ] T033 [P] [US1] Write component tests for BibleSearch component in frontend/tests/unit/components/bible/BibleSearch.test.tsx

### Database & Models for User Story 1

- [ ] T034 [P] [US1] Create Livre model in backend/src/models/bible.py
- [ ] T035 [P] [US1] Create Chapitre model in backend/src/models/bible.py
- [ ] T036 [P] [US1] Create Verset model with tsvector field in backend/src/models/bible.py
- [ ] T037 [US1] Create database migration for Bible tables (livre, chapitre, verset) with GIN indexes
- [ ] T038 [US1] Apply migration and verify tables created

### Services for User Story 1

- [ ] T039 [US1] Implement BibleService.get_all_books() in backend/src/services/bible_service.py
- [ ] T040 [US1] Implement BibleService.get_book_by_id() in backend/src/services/bible_service.py
- [ ] T041 [US1] Implement BibleService.get_chapters_by_book() in backend/src/services/bible_service.py
- [ ] T042 [US1] Implement BibleService.get_chapter_by_id() in backend/src/services/bible_service.py
- [ ] T043 [US1] Implement BibleService.get_verses_by_chapter() in backend/src/services/bible_service.py
- [ ] T044 [US1] Implement SearchService.search_verses_by_reference() in backend/src/services/search_service.py
- [ ] T045 [US1] Implement SearchService.search_verses_by_content() with PostgreSQL FTS in backend/src/services/search_service.py

### API Endpoints for User Story 1

- [ ] T046 [US1] Create Bible blueprint in backend/src/api/bible.py
- [ ] T047 [US1] Implement GET /api/bible/books endpoint in backend/src/api/bible.py
- [ ] T048 [US1] Implement GET /api/bible/books/{bookId} endpoint in backend/src/api/bible.py
- [ ] T049 [US1] Implement GET /api/bible/books/{bookId}/chapters endpoint in backend/src/api/bible.py
- [ ] T050 [US1] Implement GET /api/bible/books/{bookId}/chapters/{chapterNum} endpoint in backend/src/api/bible.py
- [ ] T051 [US1] Implement GET /api/bible/books/{bookId}/chapters/{chapterNum}/verses endpoint in backend/src/api/bible.py
- [ ] T052 [US1] Create Search blueprint in backend/src/api/search.py
- [ ] T053 [US1] Implement POST /api/bible/search endpoint in backend/src/api/search.py
- [ ] T054 [US1] Register Bible and Search blueprints in backend/src/app.py

### Data Import for User Story 1

- [ ] T055 [US1] Create Bible data import CLI command in backend/src/cli.py
- [ ] T056 [US1] Implement JSON parser for baiboly-json repository in scripts/import_bible.py
- [ ] T057 [US1] Implement data validation for Bible import in scripts/import_bible.py
- [ ] T058 [US1] Run Bible data import: flask bible import --source=./data/baiboly-json
- [ ] T059 [US1] Validate imported data: flask validate --check=bible (66 books, ~31K verses)

### Frontend for User Story 1

- [ ] T060 [P] [US1] Create BibleContext with state management in frontend/src/contexts/BibleContext.tsx
- [ ] T061 [P] [US1] Create useBible custom hook in frontend/src/hooks/useBible.ts
- [ ] T062 [P] [US1] Create bibleService API client in frontend/src/services/bibleService.ts
- [ ] T063 [P] [US1] Create BookList component in frontend/src/components/bible/BookList.tsx
- [ ] T064 [P] [US1] Create ChapterList component in frontend/src/components/bible/ChapterList.tsx
- [ ] T065 [P] [US1] Create VerseList component in frontend/src/components/bible/VerseList.tsx
- [ ] T066 [P] [US1] Create BibleSearch component in frontend/src/components/bible/BibleSearch.tsx
- [ ] T067 [P] [US1] Create SearchResults component in frontend/src/components/bible/SearchResults.tsx
- [ ] T068 [US1] Create Bible page component in frontend/src/pages/Bible.tsx
- [ ] T069 [US1] Add Bible route to React Router in frontend/src/App.tsx
- [ ] T070 [US1] Add Malagasy translations for Bible UI in frontend/src/i18n/mg/translation.json

### Verification for User Story 1

- [ ] T071 [US1] Run all User Story 1 backend tests and verify ≥80% coverage
- [ ] T072 [US1] Run all User Story 1 frontend tests and verify ≥75% coverage
- [ ] T073 [US1] Manual test: Navigate to /bible, verify 66 books displayed
- [ ] T074 [US1] Manual test: Click Genesisy, verify 50 chapters listed
- [ ] T075 [US1] Manual test: Click Chapter 1, verify all verses displayed
- [ ] T076 [US1] Manual test: Search "Jaona 3:16", verify correct verse returned
- [ ] T077 [US1] Manual test: Search "fitiavana", verify results with references

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently ✅

---

## Phase 4: User Story 2 - Lecture et recherche des chants évangéliques (Priority: P2)

**Goal**: Permettre aux utilisateurs d'accéder aux paroles des chants évangéliques luthériens et FJKM avec recherche par numéro ou contenu

**Independent Test**: Un utilisateur peut rechercher un chant par son numéro (ex: 125), effectuer une recherche par contenu (ex: "Jesosy"), et afficher les paroles complètes

### Tests for User Story 2 (TDD - Write FIRST) ⚠️

- [ ] T078 [P] [US2] Write unit tests for Chant model in backend/tests/unit/models/test_fihirana.py
- [ ] T079 [P] [US2] Write unit tests for FihiranaService in backend/tests/unit/services/test_fihirana_service.py
- [ ] T080 [P] [US2] Write unit tests for SearchService (Fihirana search) in backend/tests/unit/services/test_search_service.py
- [ ] T081 [P] [US2] Write integration tests for GET /api/fihirana/hymns in backend/tests/integration/test_fihirana_api.py
- [ ] T082 [P] [US2] Write integration tests for GET /api/fihirana/hymns/by-number/{source}/{numero} in backend/tests/integration/test_fihirana_api.py
- [ ] T083 [P] [US2] Write integration tests for POST /api/fihirana/search in backend/tests/integration/test_fihirana_api.py
- [ ] T084 [P] [US2] Write component tests for HymnList component in frontend/tests/unit/components/fihirana/HymnList.test.tsx
- [ ] T085 [P] [US2] Write component tests for HymnDetail component in frontend/tests/unit/components/fihirana/HymnDetail.test.tsx
- [ ] T086 [P] [US2] Write component tests for FihiranaSearch component in frontend/tests/unit/components/fihirana/FihiranaSearch.test.tsx

### Database & Models for User Story 2

- [ ] T087 [US2] Create Chant model with tsvector field in backend/src/models/fihirana.py
- [ ] T088 [US2] Create database migration for Fihirana table (chant) with GIN indexes
- [ ] T089 [US2] Apply migration and verify chant table created

### Services for User Story 2

- [ ] T090 [US2] Implement FihiranaService.get_all_hymns() with pagination in backend/src/services/fihirana_service.py
- [ ] T091 [US2] Implement FihiranaService.get_hymn_by_id() in backend/src/services/fihirana_service.py
- [ ] T092 [US2] Implement FihiranaService.get_hymn_by_number() in backend/src/services/fihirana_service.py
- [ ] T093 [US2] Implement FihiranaService.get_collections() in backend/src/services/fihirana_service.py
- [ ] T094 [US2] Implement SearchService.search_hymns_by_number() in backend/src/services/search_service.py
- [ ] T095 [US2] Implement SearchService.search_hymns_by_content() with PostgreSQL FTS in backend/src/services/search_service.py

### API Endpoints for User Story 2

- [ ] T096 [US2] Create Fihirana blueprint in backend/src/api/fihirana.py
- [ ] T097 [US2] Implement GET /api/fihirana/hymns endpoint with filtering in backend/src/api/fihirana.py
- [ ] T098 [US2] Implement GET /api/fihirana/hymns/{hymnId} endpoint in backend/src/api/fihirana.py
- [ ] T099 [US2] Implement GET /api/fihirana/hymns/by-number/{source}/{numero} endpoint in backend/src/api/fihirana.py
- [ ] T100 [US2] Implement GET /api/fihirana/collections endpoint in backend/src/api/fihirana.py
- [ ] T101 [US2] Implement POST /api/fihirana/search endpoint in backend/src/api/search.py
- [ ] T102 [US2] Register Fihirana blueprint in backend/src/app.py

### Data Import for User Story 2

- [ ] T103 [US2] Create Fihirana data import CLI command in backend/src/cli.py
- [ ] T104 [US2] Implement JSON parser for Fihirana-FFPM repository in scripts/import_fihirana.py
- [ ] T105 [US2] Implement data validation for Fihirana import in scripts/import_fihirana.py
- [ ] T106 [US2] Run Fihirana data import: flask fihirana import --source=./data/Fihirana-FFPM
- [ ] T107 [US2] Validate imported data: flask validate --check=fihirana (~550 hymns)

### Frontend for User Story 2

- [ ] T108 [P] [US2] Create FihiranaContext with state management in frontend/src/contexts/FihiranaContext.tsx
- [ ] T109 [P] [US2] Create useFihirana custom hook in frontend/src/hooks/useFihirana.ts
- [ ] T110 [P] [US2] Create fihiranaService API client in frontend/src/services/fihiranaService.ts
- [ ] T111 [P] [US2] Create HymnList component in frontend/src/components/fihirana/HymnList.tsx
- [ ] T112 [P] [US2] Create HymnDetail component in frontend/src/components/fihirana/HymnDetail.tsx
- [ ] T113 [P] [US2] Create FihiranaSearch component in frontend/src/components/fihirana/FihiranaSearch.tsx
- [ ] T114 [P] [US2] Create CollectionFilter component in frontend/src/components/fihirana/CollectionFilter.tsx
- [ ] T115 [US2] Create Fihirana page component in frontend/src/pages/Fihirana.tsx
- [ ] T116 [US2] Add Fihirana route to React Router in frontend/src/App.tsx
- [ ] T117 [US2] Add Malagasy translations for Fihirana UI in frontend/src/i18n/mg/translation.json

### Verification for User Story 2

- [ ] T118 [US2] Run all User Story 2 backend tests and verify ≥80% coverage
- [ ] T119 [US2] Run all User Story 2 frontend tests and verify ≥75% coverage
- [ ] T120 [US2] Manual test: Navigate to /fihirana, verify hymns displayed
- [ ] T121 [US2] Manual test: Enter hymn number 125, verify hymn displayed
- [ ] T122 [US2] Manual test: Search "Jesosy", verify results with numbers/titles
- [ ] T123 [US2] Manual test: Click on hymn, verify full lyrics displayed
- [ ] T124 [US2] Manual test: Test on mobile viewport (375px), verify responsive

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently ✅

---

## Phase 5: User Story 3 - Navigation principale et expérience responsive (Priority: P3)

**Goal**: Fournir une navigation fluide entre Bible et Fihirana avec une interface responsive adaptée à tous les appareils

**Independent Test**: Un utilisateur peut naviguer entre les sections Bible et Fihirana sur mobile, tablette, et desktop avec une expérience cohérente

### Tests for User Story 3 (TDD - Write FIRST) ⚠️

- [ ] T125 [P] [US3] Write component tests for Navigation component in frontend/tests/unit/components/common/Navigation.test.tsx
- [ ] T126 [P] [US3] Write component tests for Home page in frontend/tests/unit/pages/Home.test.tsx
- [ ] T127 [P] [US3] Write E2E tests for navigation flow in frontend/tests/e2e/navigation.spec.ts
- [ ] T128 [P] [US3] Write E2E tests for responsive behavior in frontend/tests/e2e/responsive.spec.ts

### Frontend for User Story 3

- [ ] T129 [P] [US3] Create Navigation component with MUI AppBar in frontend/src/components/common/Navigation.tsx
- [ ] T130 [P] [US3] Create responsive mobile menu in frontend/src/components/common/MobileMenu.tsx
- [ ] T131 [P] [US3] Create Home page component in frontend/src/pages/Home.tsx
- [ ] T132 [P] [US3] Create Loading component in frontend/src/components/common/Loading.tsx
- [ ] T133 [P] [US3] Create ErrorMessage component in frontend/src/components/common/ErrorMessage.tsx
- [ ] T134 [US3] Implement responsive breakpoints in MUI theme in frontend/src/theme.ts
- [ ] T135 [US3] Add home route "/" to React Router in frontend/src/App.tsx
- [ ] T136 [US3] Add navigation translations in frontend/src/i18n/mg/translation.json
- [ ] T137 [US3] Verify touch targets ≥44x44px on mobile components
- [ ] T138 [US3] Verify WCAG 2.1 AA color contrast ratios

### Verification for User Story 3

- [ ] T139 [US3] Run all User Story 3 frontend tests and verify ≥75% coverage
- [ ] T140 [US3] Run Playwright E2E tests for navigation and responsive behavior
- [ ] T141 [US3] Manual test: Open on smartphone (375px), verify navigation works
- [ ] T142 [US3] Manual test: Navigate Home → Bible → Fihirana, verify transitions
- [ ] T143 [US3] Manual test: Resize from 375px to 1920px, verify layout adapts
- [ ] T144 [US3] Manual test: Test on Chrome, Firefox, Safari (latest versions)
- [ ] T145 [US3] Run Lighthouse CI, verify scores ≥85 for all pages

**Checkpoint**: All user stories should now be independently functional ✅

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality assurance

- [ ] T146 [P] Add comprehensive error handling to all backend endpoints
- [ ] T147 [P] Add request logging with Flask instrumentation in backend/src/app.py
- [ ] T148 [P] Implement pagination helper utilities in backend/src/utils/pagination.py
- [ ] T149 [P] Add input validation utilities in backend/src/utils/validators.py
- [ ] T150 [P] Optimize database queries with eager loading in backend/src/services/
- [ ] T151 [P] Add database query performance logging
- [ ] T152 [P] Create reusable Button component in frontend/src/components/common/Button.tsx
- [ ] T153 [P] Create reusable Input component in frontend/src/components/common/Input.tsx
- [ ] T154 [P] Create reusable Card component in frontend/src/components/common/Card.tsx
- [ ] T155 [P] Implement React.memo for list components to prevent re-renders
- [ ] T156 [P] Add lazy loading for routes in frontend/src/App.tsx
- [ ] T157 [P] Optimize bundle size with code splitting
- [ ] T158 [P] Add service worker for offline capability (optional enhancement)
- [ ] T159 Setup GitHub Actions CI/CD pipeline in .github/workflows/backend-ci.yml
- [ ] T160 Setup GitHub Actions CI/CD pipeline in .github/workflows/frontend-ci.yml
- [ ] T161 Create comprehensive README.md at repository root
- [ ] T162 Create API documentation with Swagger UI at /api/docs
- [ ] T163 Run full test suite (backend + frontend) and generate coverage reports
- [ ] T164 Run Lighthouse CI on all pages, verify scores ≥85
- [ ] T165 Perform security audit with Snyk/Dependabot
- [ ] T166 Load test API endpoints with 100-500 concurrent users
- [ ] T167 Verify all constitutional requirements met (code quality, testing, i18n, performance)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent from US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD workflow)
- Models before services
- Services before endpoints
- Backend endpoints before frontend components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can be written in parallel
- Models within a story marked [P] can be implemented in parallel
- Frontend components marked [P] can be built in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Write all tests in parallel (TDD red phase):
Task T021-T025: Backend unit tests (models, services)
Task T026-T029: Backend integration tests (API endpoints)
Task T030-T033: Frontend component tests

# Implement models in parallel (green phase):
Task T034-T036: Livre, Chapitre, Verset models

# Implement frontend components in parallel:
Task T063-T067: BookList, ChapterList, VerseList, BibleSearch, SearchResults components
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**MVP Deliverable**: Bible reading with search (core value)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Polish phase → Final quality assurance
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T021-T077)
   - Developer B: User Story 2 (T078-T124)
   - Developer C: User Story 3 (T125-T145)
3. Stories complete and integrate independently
4. Team collaborates on Polish phase

---

## Task Summary

**Total Tasks**: 167 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 12 tasks (BLOCKING)
- Phase 3 (User Story 1 - Bible): 57 tasks (including 13 test tasks)
- Phase 4 (User Story 2 - Fihirana): 47 tasks (including 9 test tasks)
- Phase 5 (User Story 3 - Navigation): 17 tasks (including 4 test tasks)
- Phase 6 (Polish): 22 tasks

**Test Tasks**: 26 test tasks (TDD workflow enforced)

**Parallel Opportunities**: 76 tasks marked [P] (can run concurrently)

**Independent Test Criteria**:
- US1: Bible reading + search functional
- US2: Fihirana reading + search functional
- US3: Navigation between sections functional

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 77 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD MANDATORY**: Verify tests FAIL before implementing (constitutional requirement)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution compliance: ≥80% backend coverage, ≥75% frontend coverage, Malagasy default, WCAG 2.1 AA
