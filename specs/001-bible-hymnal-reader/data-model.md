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

### 4. `chant` (Hymns/Fihirana)

Stores evangelical hymns from Lutheran and FJKM traditions with full-text search.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-increment ID |
| `numero` | INTEGER | NOT NULL | Hymn number in collection |
| `titre` | VARCHAR(255) | | Hymn title in Malagasy (may be null if incomplete) |
| `paroles` | TEXT | NOT NULL | Complete hymn lyrics |
| `source` | VARCHAR(50) | NOT NULL | Collection source: "ffpm", "fanampiny", "antema" |
| `compositeur` | VARCHAR(255) | | Composer name (may be null, metadata incomplete) |
| `search_vector` | TSVECTOR | | Full-text search on titre + paroles |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- `idx_chant_numero_source` on `(numero, source)` (UNIQUE, hymn number per collection)
- `idx_chant_search` on `search_vector` USING GIN (for full-text search)
- `idx_chant_source` on `source` (for filtering by collection)

**Constraints:**
- `check_source`: `source IN ('ffpm', 'fanampiny', 'antema')`
- `check_numero`: `numero > 0`
- UNIQUE constraint on `(numero, source)` (same number can exist in different collections)

**Triggers:**
```sql
-- Auto-update search_vector when titre or paroles change
CREATE TRIGGER chant_tsvectorupdate BEFORE INSERT OR UPDATE
ON chant FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.simple', titre, paroles);
```

**Sample Data:**
```sql
INSERT INTO chant (numero, titre, paroles, source, compositeur) VALUES
(1, 'Miainga isika', 'Miainga isika\nHandeha any Ziona...\n(Refrain)', 'ffpm', NULL),
(125, 'Jesosy Tompo', 'Jesosy Tompo soa\nMitaraina aminao aho...', 'ffpm', 'Andriamanitra Jehovah'),
(1, 'Fihirana fanampiny', 'Midera an''Andriamanitra...', 'fanampiny', NULL);
-- search_vector auto-populated by trigger
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

**6. Get hymn by number and collection**
```sql
SELECT * FROM chant
WHERE numero = $1 AND source = $2;
-- Uses idx_chant_numero_source (UNIQUE index)
```

**7. Search hymns by content (full-text)**
```sql
SELECT id, numero, titre, source,
       ts_rank(search_vector, query) AS rank
FROM chant,
     to_tsquery('simple', 'Jesosy') AS query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 50 OFFSET 0;
-- Uses idx_chant_search (GIN index)
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
# Download Fihirana-FFPM repository
git clone https://github.com/Rohan29-AN/Fihirana-FFPM.git data/Fihirana-FFPM

# Run import command
flask fihirana import --source=./data/Fihirana-FFPM

# Validate import
flask validate --check=fihirana
```

**Expected output:**
- ~300-500 hymns from `01_fihirana_ffpm.json`
- ~100-200 hymns from `02_fihirana_fanampiny.json`
- ~50-100 antiphons from `03_antema.json`
- Total: ~500-1000 hymns

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
| `chant` | ~800 | ~2 KB | ~1.6 MB |
| **Total Data** | | | **~17 MB** |
| **Indexes (GIN + B-tree)** | | | **~30 MB** |
| **Total Database** | | | **~50 MB** |

*Estimates include PostgreSQL overhead and search indexes*

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

**Chant model:**
- `numero`: Required, integer > 0
- `paroles`: Required, non-empty string
- `source`: Required, must be "ffpm", "fanampiny", or "antema"
- `titre`: Optional (metadata incomplete in source data)
- `compositeur`: Optional (metadata incomplete)
- Unique constraint: (numero, source)

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
