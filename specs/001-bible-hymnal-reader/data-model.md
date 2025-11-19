# Data Model: Plateforme Baiboly sy Fihirana

**Feature**: 001-bible-hymnal-reader
**Phase**: 1 - Database Schema Design
**Date**: 2025-11-18

## Overview

This document defines the PostgreSQL database schema for storing Bible books, chapters, verses, and hymns (Fihirana). The schema supports hierarchical Bible navigation (Book → Chapter → Verse), full-text search in Malagasy, and efficient hymn lookup by number or content.

## Entity Relationship Diagram

```
┌─────────────┐
│   Livre     │
│  (Books)    │
└──────┬──────┘
       │ 1
       │
       │ n
┌──────▼──────┐
│  Chapitre   │
│ (Chapters)  │
└──────┬──────┘
       │ 1
       │
       │ n
┌──────▼──────┐
│   Verset    │
│  (Verses)   │
└─────────────┘

┌─────────────┐
│    Chant    │
│  (Hymns)    │
└─────────────┘
(independent table)
```

## Tables

### 1. `livre` (Bible Books)

Stores the 66 books of the Bible with metadata for navigation and display.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-increment ID |
| `nom_malagasy` | VARCHAR(100) | NOT NULL, UNIQUE | Book name in Malagasy (e.g., "Genesisy") |
| `nom_francais` | VARCHAR(100) | NOT NULL | Book name in French (e.g., "Genèse") |
| `testament` | VARCHAR(20) | NOT NULL, CHECK | "taloha" (Old) or "vaovao" (New) |
| `ordre` | INTEGER | NOT NULL, UNIQUE | Display order (1-66) |
| `nombre_chapitres` | INTEGER | NOT NULL | Total chapters in book |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- `idx_livre_ordre` on `ordre` (for ordered book listings)
- `idx_livre_testament` on `testament` (for Old/New Testament filtering)

**Constraints:**
- `check_testament`: `testament IN ('taloha', 'vaovao')`
- `check_ordre`: `ordre BETWEEN 1 AND 66`
- `check_nombre_chapitres`: `nombre_chapitres > 0`

**Sample Data:**
```sql
INSERT INTO livre (nom_malagasy, nom_francais, testament, ordre, nombre_chapitres) VALUES
('Genesisy', 'Genèse', 'taloha', 1, 50),
('Eksodosy', 'Exode', 'taloha', 2, 40),
('Matio', 'Matthieu', 'vaovao', 40, 28),
('Jaona', 'Jean', 'vaovao', 43, 21);
```

---

### 2. `chapitre` (Bible Chapters)

Stores chapters within each book, linking verses to their parent book.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-increment ID |
| `livre_id` | INTEGER | NOT NULL, FOREIGN KEY | References `livre(id)` |
| `numero` | INTEGER | NOT NULL | Chapter number within book (1-based) |
| `nombre_versets` | INTEGER | NOT NULL | Total verses in chapter |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- `idx_chapitre_livre_numero` on `(livre_id, numero)` (UNIQUE, for fast lookup)

**Constraints:**
- `fk_chapitre_livre`: FOREIGN KEY `livre_id` REFERENCES `livre(id)` ON DELETE CASCADE
- `check_numero`: `numero > 0`
- `check_nombre_versets`: `nombre_versets > 0`
- UNIQUE constraint on `(livre_id, numero)` (no duplicate chapters in a book)

**Sample Data:**
```sql
INSERT INTO chapitre (livre_id, numero, nombre_versets) VALUES
(1, 1, 31),  -- Genesis Chapter 1 has 31 verses
(1, 2, 25),  -- Genesis Chapter 2 has 25 verses
(40, 1, 25); -- Matthew Chapter 1 has 25 verses
```

---

### 3. `verset` (Bible Verses)

Stores individual verses with full-text search support for Malagasy content.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-increment ID |
| `chapitre_id` | INTEGER | NOT NULL, FOREIGN KEY | References `chapitre(id)` |
| `numero` | INTEGER | NOT NULL | Verse number within chapter (1-based) |
| `texte` | TEXT | NOT NULL | Verse content in Malagasy |
| `search_vector` | TSVECTOR | | Full-text search index (auto-updated) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- `idx_verset_chapitre_numero` on `(chapitre_id, numero)` (UNIQUE, for fast lookup)
- `idx_verset_search` on `search_vector` USING GIN (for full-text search)

**Constraints:**
- `fk_verset_chapitre`: FOREIGN KEY `chapitre_id` REFERENCES `chapitre(id)` ON DELETE CASCADE
- `check_numero`: `numero > 0`
- UNIQUE constraint on `(chapitre_id, numero)` (no duplicate verses in a chapter)

**Triggers:**
```sql
-- Auto-update search_vector when texte changes
CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON verset FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.simple', texte);
```

**Sample Data:**
```sql
INSERT INTO verset (chapitre_id, numero, texte) VALUES
(1, 1, 'Tamin''ny voalohany dia nahary ny lanitra sy ny tany Andriamanitra.'),
(1, 2, 'Ary ny tany dia tsy nisy endrika sady foana; ary aizina ny fanambanin-tany ...'),
(300, 16, 'Fa toy izao no nitiavan''Andriamanitra izao tontolo izao: nomeny ny Zanani-lahy Tokana...');
-- search_vector auto-populated by trigger
```

---

### 4. Fihirana Schema (Hymns) - Verse-Based Structure

The Fihirana data is stored in a normalized verse-based structure with three tables:

#### 4a. `sokajy` (Hymn Categories)

Optional categorization for hymns (currently unused, reserved for future use).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-increment ID |
| `anarana` | VARCHAR(255) | NOT NULL | Category name in Malagasy |

#### 4b. `hira` (Hymns)

Stores hymn metadata with one record per hymn.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique ID with collection offset (FFPM: 1-814, FANAMPINY: 1001-1054, ANTEMA: 2001-2024) |
| `numero_affiche` | INTEGER | NOT NULL, INDEX | Display number shown to users (ANTEMA: id-2000, FANAMPINY: id-1000, FFPM: id) |
| `sokajy_id` | INTEGER | FOREIGN KEY, NULLABLE | References `sokajy(id)` (optional category) |
| `lohateny` | VARCHAR(255) | NOT NULL | Hymn title with prefix (ANT - 1, FNMP - 1, or just numero for FFPM) |
| `isa_andininy` | INTEGER | NOT NULL | Total number of verses in hymn |
| `mpanoratra` | VARCHAR(255) | NULLABLE | Composer/author name (may be null) |
| `collection` | VARCHAR(50) | NOT NULL, INDEX | Collection source: "FFPM", "FANAMPINY", "ANTEMA" |

**Important Notes:**
- `id` is a unique identifier with offset to avoid conflicts between collections
- `numero_affiche` is the actual hymn number displayed to users (e.g., ANTEMA #1 has id=2001, numero_affiche=1)
- `lohateny` (title) is formatted with collection prefix:
  - FFPM: "36 Mba mitadiava..." (numero only)
  - FANAMPINY: "FNMP - 1 Hira Faneva..."
  - ANTEMA: "ANT - 1 Antema..."
- Each hymn can have multiple verses stored in `tononkira` table

#### 4c. `tononkira` (Hymn Verses)

Stores individual verses for each hymn with full-text search support.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-increment ID |
| `hira_id` | INTEGER | NOT NULL, FOREIGN KEY | References `hira(id)` |
| `andininy` | INTEGER | NOT NULL | Verse number within hymn (1, 2, 3, ...) |
| `tononkira` | TEXT | NOT NULL | Verse lyrics text with `\n` for line breaks |
| `fiverenany` | BOOLEAN | DEFAULT FALSE | TRUE if this verse is a refrain/chorus |
| `search_vector` | TSVECTOR | | Full-text search index (auto-updated) |

**CRITICAL Display Requirements:**
- `tononkira` text contains `\n` characters representing line breaks
- Frontend MUST use `whiteSpace: 'pre-line'` CSS to preserve line breaks
- Verses must be displayed with their number (e.g., "1.", "2.", etc.)
- Refrains should be visually distinguished (different background color)

**Example Data:**
```sql
-- Hymn #1 FFPM: "1 Andriananahary masina indrindra!"
INSERT INTO hira (id, numero_affiche, sokajy_id, lohateny, isa_andininy, mpanoratra, collection)
VALUES (1, 1, NULL, '1 Andriananahary masina indrindra!', 5, NULL, 'FFPM');

-- Hymn #1 FANAMPINY: "FNMP - 1 Hira Faneva..."
INSERT INTO hira (id, numero_affiche, sokajy_id, lohateny, isa_andininy, mpanoratra, collection)
VALUES (1001, 1, NULL, 'FNMP - 1 Hira Faneva Faha-30 Taonan''ny Fjkm', 4, NULL, 'FANAMPINY');

-- Hymn #1 ANTEMA: "ANT - 1 Antema"
INSERT INTO hira (id, numero_affiche, sokajy_id, lohateny, isa_andininy, mpanoratra, collection)
VALUES (2001, 1, NULL, 'ANT - 1 Antema', 1, NULL, 'ANTEMA');

INSERT INTO tononkira (hira_id, andininy, tononkira, fiverenany) VALUES
(1, 1, 'Andriananahary masina indrindra!\nNy anjelinao izay mitoetra Aminao\nMifamaly hoe : Masina indrindra\nAndriananahary, Telo Izay Iray.', FALSE),
(1, 2, 'Andriananahary masina indrindra!\nNa tsy hita aza izao ny voninahitrao!\nMasina indrindra Hianao irery.\nAndriananahary, Telo Izay Iray.', FALSE);
-- ... verses 3-5
```

**Display Format:**
```
1. Andriananahary masina indrindra!
   Ny anjelinao izay mitoetra Aminao
   Mifamaly hoe : Masina indrindra
   Andriananahary, Telo Izay Iray.

2. Andriananahary masina indrindra!
   Na tsy hita aza izao ny voninahitrao!
   Masina indrindra Hianao irery.
   Andriananahary, Telo Izay Iray.
```

**Indexes:**
- `idx_hira_collection` on `collection` (for filtering by collection)
- `idx_tononkira_hira_andininy` on `(hira_id, andininy)` (for ordered verse retrieval)
- `idx_tononkira_search` on `search_vector` USING GIN (for full-text search)

**Constraints:**
- `fk_hira_sokajy`: FOREIGN KEY `sokajy_id` REFERENCES `sokajy(id)` ON DELETE SET NULL
- `fk_tononkira_hira`: FOREIGN KEY `hira_id` REFERENCES `hira(id)` ON DELETE CASCADE
- `check_collection`: `collection IN ('FFPM', 'FANAMPINY', 'ANTEMA')`
- `check_isa_andininy`: `isa_andininy > 0`
- `check_andininy`: `andininy > 0`

**Triggers:**
```sql
-- Auto-update search_vector when tononkira text changes
CREATE TRIGGER tononkira_tsvectorupdate BEFORE INSERT OR UPDATE
ON tononkira FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.simple', tononkira);
```

---

## Views

### `v_verset_complet` (Complete Verse View)

Convenience view joining verse, chapter, and book for easy querying.

```sql
CREATE VIEW v_verset_complet AS
SELECT
    v.id AS verset_id,
    v.numero AS verset_numero,
    v.texte AS verset_texte,
    c.id AS chapitre_id,
    c.numero AS chapitre_numero,
    l.id AS livre_id,
    l.nom_malagasy AS livre_nom,
    l.testament,
    CONCAT(l.nom_malagasy, ' ', c.numero, ':', v.numero) AS reference
FROM verset v
JOIN chapitre c ON v.chapitre_id = c.id
JOIN livre l ON c.livre_id = l.id;
```

**Usage Example:**
```sql
-- Get Genesisy 1:1
SELECT * FROM v_verset_complet
WHERE livre_nom = 'Genesisy'
  AND chapitre_numero = 1
  AND verset_numero = 1;
```

---

## Queries & Performance

### Common Query Patterns

**1. Get all books (ordered)**
```sql
SELECT * FROM livre ORDER BY ordre;
-- Uses idx_livre_ordre
```

**2. Get chapters for a book**
```sql
SELECT * FROM chapitre WHERE livre_id = $1 ORDER BY numero;
-- Uses idx_chapitre_livre_numero
```

**3. Get verses for a chapter**
```sql
SELECT * FROM verset WHERE chapitre_id = $1 ORDER BY numero;
-- Uses idx_verset_chapitre_numero
```

**4. Search verses by content (full-text)**
```sql
SELECT v.*, l.nom_malagasy, c.numero AS chapitre_numero, v.numero AS verset_numero,
       ts_rank(v.search_vector, query) AS rank
FROM verset v
JOIN chapitre c ON v.chapitre_id = c.id
JOIN livre l ON c.livre_id = l.id,
     to_tsquery('simple', 'fitiavana') AS query
WHERE v.search_vector @@ query
ORDER BY rank DESC
LIMIT 50 OFFSET 0;
-- Uses idx_verset_search (GIN index)
```

**5. Search verses by reference (e.g., "Jaona 3:16")**
```sql
SELECT v.* FROM v_verset_complet v
WHERE v.livre_nom = 'Jaona'
  AND v.chapitre_numero = 3
  AND v.verset_numero = 16;
-- Uses indexes through view
```

**6. Get hymn by ID with all verses**
```sql
SELECT h.*, array_agg(t.* ORDER BY t.andininy) AS verses
FROM hira h
LEFT JOIN tononkira t ON h.id = t.hira_id
WHERE h.id = $1
GROUP BY h.id;
-- Uses primary key on hira, idx_tononkira_hira_andininy for verses
```

**7. Search hymns by content (full-text in verses)**
```sql
SELECT DISTINCT h.id, h.lohateny, h.collection, h.isa_andininy,
       MAX(ts_rank(t.search_vector, query)) AS rank
FROM hira h
JOIN tononkira t ON h.id = t.hira_id,
     to_tsquery('simple', 'Jesosy') AS query
WHERE t.search_vector @@ query
   OR h.lohateny ILIKE '%Jesosy%'
GROUP BY h.id
ORDER BY rank DESC
LIMIT 50 OFFSET 0;
-- Uses idx_tononkira_search (GIN index)
```

**8. Get all hymns from a collection (list view)**
```sql
SELECT id, lohateny, isa_andininy, collection
FROM hira
WHERE collection = 'FFPM'
ORDER BY id
LIMIT 50 OFFSET 0;
-- Uses idx_hira_collection
```

### Expected Performance

| Operation | Expected Time | Index Used |
|-----------|---------------|------------|
| List all books | <10ms | idx_livre_ordre |
| List chapters for book | <10ms | idx_chapitre_livre_numero |
| List verses for chapter | <20ms | idx_verset_chapitre_numero |
| Search verses (content) | <500ms | idx_verset_search (GIN) |
| Search hymns (content) | <200ms | idx_chant_search (GIN) |
| Get specific verse by reference | <15ms | Composite indexes |
| Get hymn by number | <10ms | idx_chant_numero_source |

---

## Data Migration Strategy

### Initial Data Load

**Step 1: Create tables and indexes**
```bash
flask db init
flask db migrate -m "Initial schema: livre, chapitre, verset, chant"
flask db upgrade
```

**Step 2: Import Bible data**
```bash
# Download baiboly-json repository
git clone https://github.com/RaveloMevaSoavina/baiboly-json.git data/baiboly-json

# Run import command
flask bible import --source=./data/baiboly-json

# Validate import
flask validate --check=bible
```

**Expected output:**
- 66 books imported (39 Old Testament + 27 New Testament)
- ~1,189 chapters imported
- ~31,102 verses imported (approximate, depends on source)

**Step 3: Import Fihirana data**
```bash
# Import using the GitHub SQL import script
docker-compose exec backend python src/scripts/import_github_sql_simple.py

# When prompted, choose:
# - '1' for FFPM only (for testing)
# - 'all' for all three collections (FFPM, FANAMPINY, ANTEMA)
```

**Expected output:**
- **FFPM**: ~797 hymns with ~3,222 verses from `01_fihirana_ffpm.sql`
- **FANAMPINY**: ~82 hymns from `02_fihirana_fanampiny.sql`
- **ANTEMA**: ~117 antiphons from `03_antema.sql`
- **Total**: ~996 hymns with proper verse separation and line breaks

**IMPORTANT**: The import script:
1. Downloads SQL files directly from GitHub
2. Parses INSERT statements preserving `\n` line breaks
3. Extracts titles from first verse first line
4. Creates both `hira` (hymn metadata) and `tononkira` (verses) records
5. Updates search vectors for full-text search

### Schema Versioning

Use Alembic/Flask-Migrate for all schema changes:
1. Never edit database directly in production
2. All changes via migration scripts
3. Test migrations on staging before production
4. Keep rollback scripts for critical migrations

---

## Database Size Estimates

| Table | Rows | Avg Row Size | Total Size |
|-------|------|--------------|------------|
| `livre` | 66 | ~200 bytes | ~13 KB |
| `chapitre` | ~1,200 | ~50 bytes | ~60 KB |
| `verset` | ~31,000 | ~500 bytes | ~15 MB |
| `sokajy` | ~10 | ~100 bytes | ~1 KB |
| `hira` | ~1,000 | ~300 bytes | ~300 KB |
| `tononkira` | ~4,000 | ~500 bytes | ~2 MB |
| **Total Data** | | | **~18 MB** |
| **Indexes (GIN + B-tree)** | | | **~35 MB** |
| **Total Database** | | | **~55 MB** |

*Estimates include PostgreSQL overhead and search indexes*

**Current Actual Data (FFPM only):**
- `hira`: 797 hymns
- `tononkira`: 3,222 verses

---

## Validation Rules

### Application-Level Validation (SQLAlchemy Models)

**Livre model:**
- `nom_malagasy`: Required, max 100 chars, unique
- `nom_francais`: Required, max 100 chars
- `testament`: Required, must be "taloha" or "vaovao"
- `ordre`: Required, integer 1-66, unique
- `nombre_chapitres`: Required, integer > 0

**Chapitre model:**
- `livre_id`: Required, valid foreign key
- `numero`: Required, integer > 0
- `nombre_versets`: Required, integer > 0
- Unique constraint: (livre_id, numero)

**Verset model:**
- `chapitre_id`: Required, valid foreign key
- `numero`: Required, integer > 0
- `texte`: Required, non-empty string
- Unique constraint: (chapitre_id, numero)

**Hira model:**
- `id`: Required, integer > 0 (hymn number, NOT auto-increment)
- `lohateny`: Required, non-empty string (extracted from first verse)
- `isa_andininy`: Required, integer > 0 (number of verses)
- `collection`: Required, must be "FFPM", "FANAMPINY", or "ANTEMA"
- `mpanoratra`: Optional (composer/author name)
- `sokajy_id`: Optional foreign key

**Tononkira model:**
- `hira_id`: Required, valid foreign key to `hira(id)`
- `andininy`: Required, integer > 0 (verse number)
- `tononkira`: Required, non-empty string with `\n` for line breaks
- `fiverenany`: Boolean, defaults to FALSE (TRUE for refrains)
- Relationship: Multiple tononkira per hira (one-to-many)

---

## Future Enhancements

**Considered for v2.0:**
1. **User Bookmarks**: Track favorite verses/hymns per user
2. **Reading History**: Store last-read chapter/verse
3. **Verse Notes**: User annotations on verses
4. **Verse Cross-References**: Link related verses
5. **Audio Files**: Link hymns to audio recordings
6. **Translations**: Multiple Bible translations (KJV, NIV, etc.)

**Not planned for MVP** - focus on core reading and search functionality.

---

## Summary

This schema supports all functional requirements (FR-001 through FR-020):
- ✅ Hierarchical Bible navigation (Livre → Chapitre → Verset)
- ✅ Full-text search on verses and hymns in Malagasy
- ✅ Efficient queries with GIN and B-tree indexes
- ✅ Normalized design (3NF) with referential integrity
- ✅ Data import from GitHub JSON sources
- ✅ Performance targets met (<2s search, <200ms API)
- ✅ Scalable for future enhancements (user features, translations)

**Next Steps:**
1. Generate OpenAPI contracts for REST API
2. Create quickstart.md with development setup
3. Implement SQLAlchemy models based on this schema
