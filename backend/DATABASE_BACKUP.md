# 📦 Guide de Backup et Restauration de la Base de Données

## 📋 Vue d'ensemble

Ce projet inclut un système de backup/restauration automatique pour la base de données PostgreSQL contenant:
- **892 hymnes Fihirana** (FFPM, FANAMPINY, ANTEMA)
- **3,520+ versets d'hymnes**
- **Livres de la Bible** avec chapitres et versets

## 🚀 Installation Automatique (Nouveau Projet)

### Lors du premier démarrage

Quand vous démarrez le projet pour la première fois, le backup est **automatiquement importé**:

```bash
# Première installation
docker-compose up -d
```

**Ce qui se passe automatiquement:**
1. PostgreSQL crée la base de données `baiboly_dev`
2. Exécute `01-init-db.sql` (extensions, permissions)
3. Exécute `02-db_backup.sql` (import complet des données)
4. La base est prête avec toutes les données!

### Vérification de l'import

```bash
# Vérifier que les conteneurs sont démarrés
docker-compose ps

# Vérifier les données importées
docker-compose exec db psql -U baiboly_user -d baiboly_dev -c "SELECT COUNT(*) FROM hira;"
# Résultat attendu: 892

docker-compose exec db psql -U baiboly_user -d baiboly_dev -c "SELECT COUNT(*) FROM tononkira;"
# Résultat attendu: 3520+
```

## 💾 Créer un Nouveau Backup

### Backup complet de la base de données

```bash
# Créer un backup avec la date actuelle
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > backend/db_backup_$(date +%Y%m%d).sql

# Remplacer le backup principal (utilisé pour l'auto-import)
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > backend/db_backup.sql
```

### Backup des hymnes uniquement

```bash
# Backup seulement des tables Fihirana
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev \
  --clean --if-exists \
  -t hira -t tononkira -t sokajy \
  > backend/db_backup_fihirana_only.sql
```

### Backup de la Bible uniquement

```bash
# Backup seulement des tables Bible
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev \
  --clean --if-exists \
  -t livre -t chapitre -t verset \
  > backend/db_backup_bible_only.sql
```

## 🔄 Restaurer un Backup

### Méthode 1: Restauration Automatique (Nouvelle Installation)

Si vous n'avez jamais démarré les conteneurs:

```bash
# Supprimer le volume PostgreSQL existant
docker-compose down -v

# Redémarrer (l'import sera automatique)
docker-compose up -d
```

**⚠️ ATTENTION:** Cette commande supprime **TOUTES** les données existantes!

### Méthode 2: Restauration Manuelle (Base Existante)

Si vous voulez restaurer un backup sur une base existante:

```bash
# Méthode A: Via le conteneur db
docker-compose exec -T db psql -U baiboly_user -d baiboly_dev < backend/db_backup.sql

# Méthode B: Via le script de restauration manuel
docker-compose cp backend/scripts/manual-restore.sh db:/tmp/
docker-compose exec db bash /tmp/manual-restore.sh
```

### Méthode 3: Restauration d'un Backup Spécifique

```bash
# Restaurer un backup avec une date spécifique
docker-compose exec -T db psql -U baiboly_user -d baiboly_dev < backend/db_backup_20250119.sql
```

## 🗂️ Structure des Fichiers

```
backend/
├── db_backup.sql                    # ⭐ Backup principal (auto-import)
├── db_backup_YYYYMMDD.sql          # Backups archivés par date
├── scripts/
│   ├── init-db.sql                 # Script d'initialisation (extensions, permissions)
│   ├── manual-restore.sh           # Script de restauration manuel
│   └── restore-backup.sh           # Script de restauration automatique (legacy)
└── DATABASE_BACKUP.md              # 📖 Ce fichier
```

## 📊 Statistiques de la Base de Données

### Tables Principales

| Table       | Description                    | Nombre de lignes (approx) |
|-------------|--------------------------------|---------------------------|
| `hira`      | Hymnes                         | 892                       |
| `tononkira` | Versets d'hymnes               | 3,520                     |
| `sokajy`    | Catégories d'hymnes            | Variable                  |
| `livre`     | Livres de la Bible             | 66+                       |
| `chapitre`  | Chapitres de la Bible          | 1,189                     |
| `verset`    | Versets de la Bible            | 31,000+                   |

### Requêtes Utiles

```sql
-- Statistiques générales
SELECT
    'Hymnes' as type, COUNT(*) as count FROM hira
UNION ALL
SELECT 'Versets hymnes', COUNT(*) FROM tononkira
UNION ALL
SELECT 'Livres Bible', COUNT(*) FROM livre
UNION ALL
SELECT 'Versets Bible', COUNT(*) FROM verset;

-- Détail par collection Fihirana
SELECT collection, COUNT(*) as count
FROM hira
GROUP BY collection
ORDER BY collection;

-- Taille de la base de données
SELECT pg_size_pretty(pg_database_size('baiboly_dev')) as database_size;
```

## 🔧 Dépannage

### Problème: Le backup n'est pas importé automatiquement

**Cause:** Le volume PostgreSQL existe déjà avec des données.

**Solution:**
```bash
# Supprimer le volume et redémarrer
docker-compose down -v
docker-compose up -d
```

### Problème: Permission denied lors de la restauration

**Cause:** Les droits sur les fichiers de backup.

**Solution:**
```bash
# Windows
icacls backend\db_backup.sql /grant Everyone:F

# Linux/Mac
chmod 644 backend/db_backup.sql
```

### Problème: Le backup est corrompu ou incomplet

**Solution:**
```bash
# Vérifier l'intégrité du backup
head -50 backend/db_backup.sql
tail -50 backend/db_backup.sql

# Recréer le backup
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > backend/db_backup.sql
```

## 📝 Bonnes Pratiques

### 1. Backups Réguliers

Créez des backups avant toute modification importante:

```bash
# Avant une migration
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev > backend/db_backup_before_migration.sql

# Backup quotidien (à automatiser avec cron)
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev > backend/db_backup_daily_$(date +%Y%m%d).sql
```

### 2. Versionner les Backups

Commitez le backup principal dans Git:

```bash
git add backend/db_backup.sql
git commit -m "Update database backup with latest data"
```

### 3. Backups Incrémentaux

Pour les grosses bases de données, utilisez des backups incrémentaux:

```bash
# Backup complet
pg_basebackup -U baiboly_user -D /backup/base

# WAL archiving (configuration PostgreSQL)
archive_mode = on
archive_command = 'cp %p /backup/wal/%f'
```

## 🎯 Cas d'Usage

### Cas 1: Développement Local Initial

```bash
# Clone du repo
git clone <repo-url>
cd baiboly

# Premier démarrage (auto-import)
docker-compose up -d

# Vérification
curl http://localhost:5000/api/fihirana?limit=5
```

### Cas 2: Mise à Jour des Données

```bash
# 1. Modifier les données via l'application
# 2. Créer un nouveau backup
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > backend/db_backup.sql

# 3. Committer
git add backend/db_backup.sql
git commit -m "Update Fihirana data: add new hymns"
git push
```

### Cas 3: Restauration Après Erreur

```bash
# Restaurer la dernière version stable
docker-compose down -v
git checkout backend/db_backup.sql
docker-compose up -d
```

## 🔗 Liens Utiles

- **PostgreSQL Backup Documentation:** https://www.postgresql.org/docs/current/backup.html
- **pg_dump Documentation:** https://www.postgresql.org/docs/current/app-pgdump.html
- **Docker Volumes:** https://docs.docker.com/storage/volumes/

---

**Dernière mise à jour:** 2025-11-19
**Taille du backup:** ~2-5 MB (compressé)
**Temps d'import:** ~5-10 secondes
