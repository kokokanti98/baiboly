# Research: Plateforme Baiboly sy Fihirana

**Feature**: 001-bible-hymnal-reader
**Phase**: 0 - Research & Design Decisions
**Date**: 2025-11-18

## Overview

This document captures research findings and design decisions for implementing the Bible and Hymnal reading platform. Key areas researched: PostgreSQL full-text search for Malagasy content, JSON data import strategies, Flask-React architecture patterns, and i18n implementation.

## 1. PostgreSQL Full-Text Search for Malagasy

### Decision

Use PostgreSQL native full-text search with `tsvector` and `tsquery` types, configured for simple search without stemming (Malagasy language not directly supported by PostgreSQL text search dictionaries).

### Rationale

**Why PostgreSQL FTS over alternatives:**
1. **No external dependencies**: ElasticSearch/Solr add complexity and infrastructure costs
2. **Atomic transactions**: Search indexes update in same transaction as data
3. **Cost effective**: No additional services to run and maintain
4. **Sufficient performance**: For ~31,000 verses + 1,000 hymns, PostgreSQL FTS handles <2s search requirement
5. **GIN indexes**: Provide fast full-text search with acceptable storage overhead

**Malagasy language considerations:**
- PostgreSQL doesn't have built-in Malagasy stemmer
- Use `simple` text search configuration (no stemming, just tokenization)
- Alternative considered: Custom Malagasy stemmer - **rejected** due to complexity and maintenance burden
- Simple tokenization sufficient for exact word matching

**Implementation approach:**
```sql
-- Add tsvector column with GIN index
ALTER TABLE verset ADD COLUMN search_vector tsvector;
CREATE INDEX idx_verset_search ON verset USING GIN(search_vector);

-- Update search vector on insert/update
CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON verset FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.simple', texte);

-- Search query example
SELECT * FROM verset
WHERE search_vector @@ to_tsquery('simple', 'fitiavana');
```

**Performance optimization:**
- GIN (Generalized Inverted Index) for fast lookups
- `ts_rank()` for relevance scoring
- Pagination with `LIMIT`/`OFFSET` for large result sets

### Alternatives Considered

1. **ElasticSearch**: More features but overkill for this scale, adds operational complexity, cost prohibitive
2. **LIKE queries**: Too slow for content search across thousands of verses
3. **External search service** (Algolia, Meilisearch): Monthly costs, data export dependency
4. **Custom Malagasy stemmer**: Development and maintenance effort not justified for MVP

### References

- [PostgreSQL Full Text Search Documentation](https://www.postgresql.org/docs/current/textsearch.html)
- [GIN Index Performance](https://www.postgresql.org/docs/current/gin.html)

---

## 2. JSON Data Import Strategy

### Decision

Implement one-time CLI import scripts using Flask CLI commands to parse GitHub JSON repositories and populate PostgreSQL database with proper relationships and search indexes.

### Rationale

**Import approach:**
1. **One-time setup**: Data is static (Bible text, hymns), not continuously updating
2. **CLI commands**: Use Flask Click commands for controlled import process
3. **Idempotent**: Scripts should be re-runnable without duplicating data
4. **Transaction safety**: Wrap imports in database transactions for atomicity

**Bible import process:**
1. Clone/download `RaveloMevaSoavina/baiboly-json` repository
2. Parse JSON structure to extract:
   - Book name (Malagasy), French name, testament, order
   - Chapters with numbers
   - Verses with numbers and text content
3. Create database records with relationships: Livre → Chapitre → Verset
4. Generate full-text search vectors for verse content
5. Validate data integrity (all 66 books, chapter/verse counts)

**Fihirana import process:**
1. Clone/download `Rohan29-AN/Fihirana-FFPM` repository
2. Parse 3 JSON files: `01_fihirana_ffpm.json`, `02_fihirana_fanampiny.json`, `03_antema.json`
3. Extract: hymn number, title, lyrics, source (FFPM/Lutheran/FJKM)
4. Handle duplicate numbers across collections with collection identifier
5. Generate full-text search vectors for title and lyrics

**Error handling:**
- Validate JSON schema before import
- Log errors for manual review (missing fields, malformed data)
- Continue import on non-critical errors, fail on critical errors
- Report import statistics (success/failure counts)

**Sample CLI commands:**
```bash
# Import Bible data
flask bible import --source=./data/baiboly-json

# Import Fihirana data
flask fihirana import --source=./data/Fihirana-FFPM

# Validate imported data
flask validate --check=bible,fihirana
```

### Alternatives Considered

1. **Real-time API integration**: GitHub repos are static, unnecessary complexity
2. **Manual SQL import**: Error-prone, not repeatable, no validation
3. **Admin UI import**: Over-engineering for one-time operation
4. **Database seed files**: JSON format more maintainable than SQL INSERTs

### References

- [Flask CLI Documentation](https://flask.palletsprojects.com/en/3.0.x/cli/)
- [SQLAlchemy Bulk Operations](https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-bulk-insert-statements)

---

## 3. Flask-React Architecture & API Design

### Decision

RESTful API with Flask backend, React SPA frontend, CORS-enabled communication, JWT for future authentication needs.

### Rationale

**Architecture pattern:**
- **REST over GraphQL**: Simpler for CRUD operations, better caching, easier debugging
- **Stateless API**: Each request self-contained, enables horizontal scaling
- **JSON responses**: Universal format, TypeScript-friendly
- **Blueprint organization**: Separate modules for bible, fihirana, search

**API design principles:**
1. **Resource-based URLs**: `/api/bible/books`, `/api/fihirana/hymns`
2. **HTTP verbs**: GET for reads (only GET needed for MVP)
3. **Pagination**: Query params `?page=1&limit=50` for lists
4. **Search endpoint**: POST `/api/search` with JSON body for complex queries
5. **Error responses**: Consistent JSON structure with Malagasy messages

**CORS configuration:**
- Development: Allow `http://localhost:5173` (Vite default)
- Production: Whitelist frontend domain only
- Credentials: Enable for future session/auth support

**Response format standardization:**
```json
{
  "success": true,
  "data": { ... },
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 1500,
    "pages": 30
  },
  "message": "Nahomby" // Success in Malagasy
}
```

**Error format:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Tsy hita ny boky" // Book not found in Malagasy
  }
}
```

### Alternatives Considered

1. **GraphQL**: Over-engineered for simple read operations, added complexity
2. **Server-side rendering (SSR)**: Not needed, SPA sufficient for this use case
3. **Monolithic Flask app with templates**: Couples frontend/backend, harder to scale and test
4. **gRPC**: Binary protocol unnecessary, REST more accessible

### References

- [Flask RESTful Best Practices](https://flask-restful.readthedocs.io/)
- [REST API Design Guidelines](https://restfulapi.net/)

---

## 4. Internationalization (i18n) Implementation

### Decision

Use react-i18next for frontend and Flask-Babel for backend with Malagasy as default language, structured for future multi-language support.

### Rationale

**Frontend (react-i18next):**
- Industry standard for React i18n
- JSON-based translations, easy to maintain
- Component-level translation with `useTranslation` hook
- Interpolation for dynamic content
- Language detection (default to Malagasy)

**Backend (Flask-Babel):**
- API error messages in Malagasy
- Date/number formatting per Malagasy locale
- `.po` files for translation management

**Translation structure:**
```json
// frontend/src/i18n/mg/translation.json
{
  "common": {
    "search": "Karohy",
    "loading": "Mahandrasa...",
    "error": "Tsy nety"
  },
  "bible": {
    "books": "Boky",
    "chapter": "Toko",
    "verse": "Andininy",
    "search_placeholder": "Karohy andininy..."
  },
  "fihirana": {
    "hymns": "Fihirana",
    "number": "Laharana",
    "search_placeholder": "Karohy fihirana..."
  }
}
```

**Malagasy locale considerations:**
- Date format: DD/MM/YYYY (day/month/year)
- Number format: 1 000,50 (space separator, comma decimal)
- No pluralization rules needed for MVP (Malagasy pluralization is context-based)

**Future extensibility:**
- Add `fr/translation.json` for French
- Add `en/translation.json` for English
- User preference stored in localStorage
- Language switcher component in nav

### Alternatives Considered

1. **i18next without React wrapper**: react-i18next provides better hooks integration
2. **Hard-coded strings**: Not maintainable, violates constitution requirement
3. **Backend-only translation**: Frontend needs translations for instant feedback
4. **Polyglot.js**: Less mature ecosystem than i18next

### References

- [react-i18next Documentation](https://react.i18next.com/)
- [Flask-Babel Documentation](https://python-babel.github.io/flask-babel/)
- [Malagasy Language Resources](https://en.wikipedia.org/wiki/Malagasy_language#Writing_system)

---

## 5. Frontend State Management

### Decision

Use React Context API + useReducer for global state (current book/chapter, search results), local useState for component state.

### Rationale

**Why Context + useReducer:**
1. **Simplicity**: No external library, built into React
2. **Constitutional compliance**: "Context API + useReducer for simple state"
3. **Sufficient for MVP**: Navigation state, search results, current location
4. **Performance**: Minimal re-renders with proper context splitting

**State structure:**
```typescript
// Bible context
interface BibleState {
  currentBook: Book | null;
  currentChapter: Chapter | null;
  verses: Verse[];
  loading: boolean;
}

// Fihirana context
interface FihiranaState {
  currentHymn: Hymn | null;
  searchResults: Hymn[];
  loading: boolean;
}

// Search context
interface SearchState {
  query: string;
  results: SearchResult[];
  loading: boolean;
  type: 'bible' | 'fihirana';
}
```

**Context organization:**
- Separate contexts for Bible, Fihirana, Search (avoid unnecessary re-renders)
- Provider composition in `App.tsx`
- Custom hooks: `useBible()`, `useFihirana()`, `useSearch()`

**When to consider Redux Toolkit/Zustand:**
- User authentication state (future)
- Complex cross-feature state dependencies
- Undo/redo functionality
- Offline sync requirements

### Alternatives Considered

1. **Redux Toolkit**: Overkill for current requirements, added boilerplate
2. **Zustand**: Lighter than Redux but unnecessary for Context-solvable problems
3. **Recoil**: Experimental, smaller ecosystem than Context API
4. **MobX**: Mutable state pattern conflicts with React conventions

### References

- [React Context API](https://react.dev/learn/passing-data-deeply-with-context)
- [useReducer Hook](https://react.dev/reference/react/useReducer)

---

## 6. Responsive Design & UI Component Library

### Decision

Use Material-UI (MUI) v5 component library with custom theme for Malagasy context, responsive breakpoints aligned with constitution requirements.

### Rationale

**Why Material-UI:**
1. **Constitutional compliance**: "centralized component library (e.g., Material-UI)"
2. **Accessibility**: WCAG 2.1 AA compliant out of box
3. **Responsive**: Built-in breakpoint system
4. **Theming**: Customizable for brand colors
5. **Icon library**: Comprehensive icon set included
6. **TypeScript support**: First-class TypeScript support

**Custom theme configuration:**
```typescript
const theme = createTheme({
  palette: {
    primary: { main: '#2E7D32' }, // Green for spiritual content
    secondary: { main: '#D32F2F' }, // Red accent
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h1: { fontSize: '2rem' }, // Mobile-first sizing
  },
  breakpoints: {
    values: {
      xs: 0,
      sm: 375,  // Constitution: mobile ≥375px
      md: 768,  // Constitution: tablet ≥768px
      lg: 1024, // Constitution: desktop ≥1024px
      xl: 1536,
    },
  },
});
```

**Touch target compliance:**
- MUI buttons default to 44x44px minimum (constitutional requirement met)
- IconButton `size="large"` for mobile
- Input fields with adequate padding

**Component strategy:**
- Use MUI components as base: `Button`, `TextField`, `Card`, `AppBar`
- Custom wrapper components in `components/common/` for consistency
- Styled components with MUI `styled()` API for customization

### Alternatives Considered

1. **Chakra UI**: Excellent but less mature ecosystem than MUI
2. **Ant Design**: Great but Chinese-centric design language
3. **Tailwind CSS**: Requires more custom component development
4. **Custom component library**: Time-intensive, not justified for MVP
5. **Headless UI**: Too low-level, would need extensive styling

### References

- [Material-UI Documentation](https://mui.com/material-ui/)
- [MUI Theming Guide](https://mui.com/material-ui/customization/theming/)

---

## 7. Testing Strategy

### Decision

Layered testing approach: Backend unit + integration tests with pytest, Frontend component + E2E tests with Jest and Playwright.

### Rationale

**Backend testing (pytest):**
- **Unit tests**: Models, services, utils (≥80% coverage)
- **Integration tests**: API endpoints with test database
- **Fixtures**: Reusable test data in `conftest.py`
- **Mocking**: Database queries during unit tests
- **Test database**: SQLite in-memory for speed

**Frontend testing (Jest + React Testing Library):**
- **Component tests**: Render, user interactions, props
- **Custom hooks tests**: State management logic
- **Service tests**: API client mocking with MSW (Mock Service Worker)
- **Coverage target**: ≥75% (constitutional requirement)

**E2E testing (Playwright):**
- **Critical user flows**: Bible search, hymn lookup, navigation
- **Cross-browser**: Chrome, Firefox, Safari (WebKit)
- **Mobile viewport**: Test responsive behavior
- **Frequency**: Run on PR to main branch

**TDD workflow enforcement:**
1. Write failing test (red)
2. Implement minimal code (green)
3. Refactor while keeping tests passing
4. CI pipeline blocks merge if tests fail

**Example test structure:**
```python
# backend/tests/integration/test_bible_api.py
def test_get_books_returns_66_books(client):
    response = client.get('/api/bible/books')
    assert response.status_code == 200
    assert len(response.json['data']) == 66
```

```typescript
// frontend/tests/unit/Bible.test.tsx
test('displays book list when loaded', async () => {
  render(<Bible />);
  await waitFor(() => {
    expect(screen.getByText(/Genesisy/i)).toBeInTheDocument();
  });
});
```

### Alternatives Considered

1. **Backend**: unittest (Python standard) - pytest more powerful and readable
2. **Frontend**: Enzyme - deprecated, RTL is modern standard
3. **E2E**: Cypress - Playwright supports more browsers and has better TypeScript support
4. **Integration**: Postman/Insomnia - Code-based tests are version controlled and automatable

### References

- [pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|-------------------|
| **Search** | PostgreSQL FTS with GIN indexes | Native, cost-effective, sufficient performance |
| **Data Import** | Flask CLI commands | One-time operation, idempotent, validates data |
| **API Architecture** | RESTful with Flask blueprints | Simple, stateless, cacheable, standard |
| **Frontend Framework** | React 18 + TypeScript | Constitutional requirement, modern, type-safe |
| **State Management** | Context API + useReducer | Constitutional recommendation, sufficient for MVP |
| **UI Library** | Material-UI v5 | Constitutional example, accessible, responsive |
| **i18n** | react-i18next + Flask-Babel | Standard libraries, Malagasy default, extensible |
| **Testing** | pytest + Jest + Playwright | Constitutional coverage requirements, TDD-friendly |
| **Database** | PostgreSQL 13+ | Constitutional requirement, full-text search native |

## Next Steps (Phase 1)

1. ✅ Create `data-model.md` with detailed database schema
2. ✅ Generate OpenAPI contracts for Bible and Fihirana APIs
3. ✅ Create `quickstart.md` with development setup instructions
4. ✅ Update agent context with technology stack decisions

All research findings support constitutional compliance and enable successful implementation of user stories P1-P3.
