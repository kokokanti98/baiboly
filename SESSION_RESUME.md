# Résumé de Session - Projet Baiboly

**Date de dernière mise à jour:** 2025-11-19
**Statut du projet:** ✅ Fonctionnel - Fihirana complètement opérationnel

## 📋 État Actuel du Projet

### Fonctionnalités Implémentées

#### ✅ Fihirana (Hymnes)
- **Structure base de données:** Système basé sur les versets (Hira + Tononkira)
- **Collections importées:**
  - FFPM: 814 chansons (IDs 1-814)
  - FANAMPINY: 54 chansons (IDs 1001-1054)
  - ANTEMA: 24 antiennes (IDs 2001-2024)
  - **Total: 892 hymnes avec 3,520 versets**

- **Affichage:**
  - Versets numérotés avec retours à la ligne préservés (`\n` → line breaks)
  - Refrains mis en évidence avec fond coloré
  - Navigation par collection (FFPM, FANAMPINY, ANTEMA)

- **Recherche:**
  - Par numéro exact (ex: "36" → trouve chanson #36)
  - Par titre (ex: "Andriananahary")
  - Par contenu des paroles (ex: "Jeso")
  - Fonctionne dans 2 onglets: Fihirana (avec barre intégrée) et Karohy (recherche dédiée)

#### 🚧 Bible
- Structure de base créée mais pas encore complètement implémentée
- À développer dans les prochaines sessions

### Architecture Technique

**Backend (Python/Flask):**
- PostgreSQL avec structure normalisée
- SQLAlchemy ORM avec relations
- Full-text search avec tsvector
- API RESTful

**Frontend (React/TypeScript):**
- Material-UI pour l'interface
- React Router pour la navigation
- i18n pour la traduction (français/malgache)
- Vite pour le build

**Infrastructure:**
- Docker Compose (3 conteneurs: frontend, backend, db)
- Volumes persistants pour la base de données

## 🔧 Problèmes Résolus Récemment

### 1. Erreur "Cannot read properties of undefined (reading 'substring')"
**Fichier:** `frontend/src/components/fihirana/FihiranaSearch.tsx:262`

**Solution:**
```typescript
// Avant (causait l'erreur):
result.paroles.substring(0, 200)

// Après (avec optional chaining):
result.paroles?.substring(0, 200)

// Plus condition stricte:
result.paroles && result.paroles.length > 0 ? (...) : (...)
```

### 2. Recherche par Numéro Ne Fonctionnait Pas
**Fichier:** `backend/src/services/fihirana_service.py:139-156`

**Solution:** Ajout de la détection de numéro dans la recherche
```python
try:
    numero = int(query_text)
    query = self.session.query(Hira).filter(
        or_(
            Hira.lohateny.ilike(search_term),
            Hira.id.in_(hira_ids_from_verses),
            Hira.id == numero  # ← Ajouté
        )
    )
except ValueError:
    # Pas un numéro, recherche textuelle seulement
```

## 📂 Structure des Fichiers Importants

### Backend
```
backend/
├── src/
│   ├── models/
│   │   └── fihirana.py          # Modèles: Sokajy, Hira, Tononkira
│   ├── services/
│   │   └── fihirana_service.py  # Logique métier (recherche, récupération)
│   ├── routes/
│   │   └── fihirana.py          # Endpoints API
│   └── scripts/
│       └── import_fihirana_json.py  # Import depuis GitHub JSON
```

### Frontend
```
frontend/
├── src/
│   ├── components/
│   │   └── fihirana/
│   │       ├── FihiranaReader.tsx   # Liste + lecture (onglet principal)
│   │       ├── FihiranaSearch.tsx   # Recherche dédiée (onglet Karohy)
│   │       ├── FihiranaDetail.tsx   # Affichage versets détaillés
│   │       └── FihiranaList.tsx     # Liste avec filtres
│   ├── pages/
│   │   └── FihiranaPage.tsx         # Page principale avec tabs
│   └── services/
│       └── api.ts                   # Client HTTP Axios
```

### Documentation
```
specs/001-bible-hymnal-reader/
├── spec.md           # Spécification complète
├── plan.md           # Plan d'implémentation
├── tasks.md          # Tâches détaillées
└── data-model.md     # Modèle de données avec exemples
```

## 🗄️ Schéma Base de Données

### Table: hira (hymnes)
```sql
id            INTEGER PRIMARY KEY     -- Numéro de la chanson (avec offset par collection)
sokajy_id     INTEGER                 -- Catégorie (optionnel)
lohateny      VARCHAR(255)            -- Titre (extrait du 1er verset)
isa_andininy  INTEGER                 -- Nombre de versets
mpanoratra    VARCHAR(255)            -- Auteur (optionnel)
collection    VARCHAR(50)             -- FFPM, FANAMPINY, ou ANTEMA
```

### Table: tononkira (versets)
```sql
id            INTEGER PRIMARY KEY AUTO_INCREMENT
hira_id       INTEGER                 -- Référence à hira(id)
andininy      INTEGER                 -- Numéro du verset (1, 2, 3...)
tononkira     TEXT                    -- Paroles avec \n pour line breaks
fiverenany    BOOLEAN                 -- TRUE si c'est un refrain
search_vector TSVECTOR                -- Index full-text search
```

**Important:** Les `\n` dans `tononkira` DOIVENT être affichés comme des retours à la ligne réels avec CSS `whiteSpace: 'pre-line'`

## 🚀 Commandes Utiles

### Démarrer l'Application
```bash
cd C:\Dev\baiboly
docker-compose up -d
```

### Voir les Logs
```bash
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Redémarrer un Service
```bash
docker-compose restart frontend
docker-compose restart backend
```

### Accéder à la Base de Données
```bash
docker-compose exec db psql -U postgres baiboly
```

### Ré-importer les Fihirana
```bash
docker-compose exec backend python src/scripts/import_fihirana_json.py
# Choisir 'y' pour effacer, puis 'all' pour importer les 3 collections
```

## 🌐 URLs

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **Documentation API:** http://localhost:5000/api/docs (si implémenté)

### Endpoints API Principaux

```bash
# Liste tous les hymnes
GET /api/fihirana?limit=200&offset=0&collection=FFPM

# Récupère un hymne avec ses versets
GET /api/fihirana/{id}

# Recherche
GET /api/fihirana/search?q=36&limit=20&offset=0&collection=FFPM
```

## 📝 Pour la Prochaine Session

### Comment me mettre à jour rapidement

**Méthode 1: Lire ce fichier**
Demandez-moi simplement: "Lis le fichier SESSION_RESUME.md et dis-moi où nous en sommes"

**Méthode 2: Pointer vers les documents**
Dites: "Regarde les specs dans specs/001-bible-hymnal-reader/ pour comprendre le contexte"

**Méthode 3: Résumé court**
Dites simplement: "Résume l'état actuel du projet Baiboly"

### Tâches Potentielles à Venir

1. **Bible:**
   - Implémenter la structure de données (Livres, Chapitres, Versets)
   - Importer les données bibliques
   - Créer les composants de lecture
   - Implémenter la recherche

2. **Améliorations Fihirana:**
   - Ajouter favoris/signets
   - Historique de lecture
   - Partage de chansons
   - Mode hors ligne (PWA)

3. **UI/UX:**
   - Mode sombre
   - Ajustement taille police
   - Impression/PDF
   - Multilingue (français, malgache, anglais)

4. **Performance:**
   - Pagination côté serveur améliorée
   - Cache Redis
   - Optimisation des requêtes SQL

## 🐛 Bugs Connus

Aucun bug majeur connu pour le moment. L'application Fihirana est complètement fonctionnelle.

## 💡 Notes Importantes

1. **Windows Case-Insensitive:** Sur Windows, `Fihirana/` et `fihirana/` sont identiques, mais Vite peut cacher différemment. Toujours utiliser le même case.

2. **Vite Cache:** Si des changements ne s'appliquent pas, supprimer le cache:
   ```bash
   docker-compose exec frontend sh -c "rm -rf node_modules/.vite"
   docker-compose restart frontend
   ```

3. **Git Commits:** Toujours utiliser des messages descriptifs avec le format:
   ```
   Titre court (50 chars max)

   Description détaillée

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

4. **Source des Données:** Les hymnes proviennent de https://github.com/Rohan29-AN/Fihirana-FFPM (JSON format)

---

**Dernière modification:** 2025-11-19 par Claude Code
**Commit actuel:** 54cd059 - "Corriger la recherche Fihirana: support numéro + fix paroles undefined"
