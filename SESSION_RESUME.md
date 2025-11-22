# Résumé de Session - Projet Baiboly

**Date de dernière mise à jour:** 2025-11-22 (Session 3)
**Statut du projet:** ✅ Fonctionnel - Fihirana + Bible + Backup + CI/CD configuré

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

#### ✅ Bible
- **API Backend:** ✅ Fonctionnelle
  - `GET /api/bible/livres` - Liste des livres
  - `GET /api/bible/livres/{id}` - Détails d'un livre
  - `GET /api/bible/chapitres/{livre_id}/{chapitre_num}` - Versets d'un chapitre
  - `GET /api/bible/search` - Recherche dans la Bible
- **Base de données:** ✅ Livres importés (Genesisy, Eksodosy, Nomery, etc.)
- **Frontend:** ⚠️ À vérifier (composants peuvent exister mais statut non confirmé)

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

### 5. Workflow CI/CD pour Déploiement Production (2025-11-22)
**Problème:** Besoin d'automatiser le déploiement sur serveur VPS OVH avec architecture hybride (frontend Apache, backend+DB Docker).

**Solution Implémentée:**
- ✅ Workflow GitHub Actions complet avec tests automatiques
- ✅ Configuration Apache VirtualHost pour servir frontend statique
- ✅ Scripts de déploiement backend (`deploy-backend.sh`) et frontend (`deploy-frontend.sh`)
- ✅ Script d'initialisation serveur (`server-setup.sh`)
- ✅ Déploiement automatique sur push `main`
- ✅ Health checks et rollback automatique
- ✅ Ajout gunicorn comme serveur WSGI production

**Architecture Production:**
```
Internet → Apache (80/443)
              ├─→ /var/www/baiboly (Frontend Static)
              └─→ ProxyPass /api → Backend Docker:5000
                                        ↓
                                   PostgreSQL Docker:5432
```

**Fichiers créés:**
- `.github/workflows/ci-cd.yml` - Workflow GitHub Actions
- `deploy/baiboly.conf` - Configuration Apache VirtualHost
- `deploy/server-setup.sh` - Setup initial serveur
- `deploy/deploy-backend.sh` - Déploiement backend
- `deploy/deploy-frontend.sh` - Déploiement frontend
- `CI_CD.md` - Documentation complète CI/CD
- `GITHUB_SECRETS.md` - Guide configuration secrets

**Fichiers modifiés:**
- `deploy/docker-compose.prod.yml` - Retiré nginx/frontend (architecture hybride)
- `backend/requirements.txt` - Ajout gunicorn==21.2.0
- `deploy/.env.production.example` - Ajout CORS_ORIGINS
- `deploy/README.md` - Documentation Apache

**Workflow:**
1. Push sur `main` → Tests backend + frontend
2. Build frontend → Artifact
3. Déploiement backend via SSH + Docker
4. Déploiement frontend → Copie vers `/var/www/baiboly` + reload Apache
5. Health checks API + Frontend

**Secrets GitHub requis:**
- `SSH_PRIVATE_KEY` - Clé SSH pour accès serveur
- `SERVER_HOST` - IP/domaine VPS OVH
- `SERVER_USER` - Utilisateur SSH
- `DOMAIN` - Nom de domaine (optionnel)

### 4. Numérotation et Titres des Collections Fihirana (2025-11-19)
**Problème:** Les chansons de collections différentes (FFPM, FANAMPINY, ANTEMA) avec le même numéro étaient confondues. Par exemple, ANTEMA #1 et FFPM #1 sont deux chansons différentes.

**Solution Implémentée:**
- ✅ Ajout du champ `numero_affiche` distinct de l'ID
- ✅ Calcul du numéro d'affichage : ANTEMA (id-2000), FANAMPINY (id-1000), FFPM (id)
- ✅ Formatage des titres avec préfixes :
  - FFPM : "36 Andriananahary masina..."
  - FANAMPINY : "FNMP - 1 Hira Faneva..."
  - ANTEMA : "ANT - 1 Antema..."
- ✅ Mise à jour des services backend pour rechercher par `numero_affiche`
- ✅ Ré-import de toutes les données avec les nouveaux formats

**Fichiers modifiés:**
- `backend/src/models/fihirana.py` (ajout `numero_affiche`)
- `backend/src/scripts/import_fihirana_json.py` (formatage des titres)
- `backend/src/services/fihirana_service.py` (recherche par `numero_affiche`)
- Base de données : migration ajout colonne + index

**Résultat:**
- ANTEMA #1 → ID 2001, numero_affiche=1, titre="ANT - 1 Antema..."
- FANAMPINY #1 → ID 1001, numero_affiche=1, titre="FNMP - 1 Hira Faneva..."
- FFPM #36 → ID 36, numero_affiche=36, titre="36 Andriananahary..."

### 3. Système de Backup et Restauration Automatique (2025-11-19)
**Problème:** Pas de mécanisme pour sauvegarder et restaurer facilement les données de la base.

**Solution Implémentée:**
- ✅ Backup automatique de la BDD (892 hymnes + 3,520 versets + 44 livres Bible)
- ✅ Import automatique au premier démarrage via docker-compose
- ✅ Scripts de backup simplifiés (Windows: `backup-db.bat`, Linux: `backup-db.sh`)
- ✅ Scripts de restauration manuelle
- ✅ Documentation complète dans `backend/DATABASE_BACKUP.md`
- ✅ Guide rapide dans `BACKUP_QUICKSTART.md`

**Fichiers créés/modifiés:**
- `backend/db_backup.sql` (backup complet ~2-5 MB)
- `docker-compose.yml` (volumes pour auto-import)
- `backend/DATABASE_BACKUP.md` (documentation)
- `BACKUP_QUICKSTART.md` (guide rapide)
- `backup-db.bat` et `backup-db.sh` (scripts utilitaires)

**Commits:**
- `97d152a` - Système de backup/restauration automatique
- `731ebf1` - Scripts de backup simplifiés
- `c5e3b15` - Guide rapide

### 2. Erreur "Cannot read properties of undefined (reading 'substring')" (2025-11-18)
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

### 1. Recherche par Numéro Ne Fonctionnait Pas (2025-11-18)
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
id            INTEGER PRIMARY KEY     -- ID unique avec offset (FFPM: 1-814, FANAMPINY: 1001-1054, ANTEMA: 2001-2024)
numero_affiche INTEGER NOT NULL       -- Numéro affiché aux utilisateurs (ANTEMA: id-2000, FANAMPINY: id-1000, FFPM: id)
sokajy_id     INTEGER                 -- Catégorie (optionnel)
lohateny      VARCHAR(255)            -- Titre formaté avec préfixe (ANT - 1, FNMP - 1, ou numero pour FFPM)
isa_andininy  INTEGER                 -- Nombre de versets
mpanoratra    VARCHAR(255)            -- Auteur (optionnel)
collection    VARCHAR(50)             -- FFPM, FANAMPINY, ou ANTEMA
```

**Exemples de titres formatés :**
- FFPM : "36 Andriananahary masina..."
- FANAMPINY : "FNMP - 1 Hira Faneva..."
- ANTEMA : "ANT - 1 Antema..."

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

### Backup & Restauration de la Base de Données
```bash
# Créer un backup
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > backend/db_backup.sql

# Restaurer automatiquement (supprime toutes les données!)
docker-compose down -v
docker-compose up -d

# Voir la documentation complète
cat backend/DATABASE_BACKUP.md
```

**Note:** Le backup est automatiquement importé lors du premier démarrage si la base est vide.

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

**Dernière modification:** 2025-11-19 (Session 2) par Claude Code
**Commits de cette session:**
- `97d152a` - Système de backup/restauration automatique
- `731ebf1` - Scripts de backup simplifiés
- `c5e3b15` - Guide rapide backup

**Commit précédent:** `54cd059` - "Corriger la recherche Fihirana: support numéro + fix paroles undefined"
