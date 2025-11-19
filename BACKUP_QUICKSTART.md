# 🚀 Guide Rapide - Backup & Restauration

## 📦 Créer un Backup

### Windows
```bash
backup-db.bat
```

### Linux/Mac
```bash
./backup-db.sh
```

### Backup Manuel
```bash
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > backend/db_backup.sql
```

---

## 🔄 Restaurer un Backup

### Restauration Automatique (Nouvelle Installation)
```bash
# Supprime TOUTES les données existantes!
docker-compose down -v
docker-compose up -d
```

Le backup `backend/db_backup.sql` est **automatiquement importé** au démarrage.

### Restauration Manuelle (Base Existante)
```bash
docker-compose exec -T db psql -U baiboly_user -d baiboly_dev < backend/db_backup.sql
```

---

## 📊 Vérifier les Données

```bash
# Compter les hymnes
docker-compose exec db psql -U baiboly_user -d baiboly_dev -c "SELECT COUNT(*) FROM hira;"
# Résultat attendu: 892

# Compter les versets d'hymnes
docker-compose exec db psql -U baiboly_user -d baiboly_dev -c "SELECT COUNT(*) FROM tononkira;"
# Résultat attendu: 3520+

# Compter les livres de la Bible
docker-compose exec db psql -U baiboly_user -d baiboly_dev -c "SELECT COUNT(*) FROM livre;"
# Résultat attendu: 44
```

### Via API
```bash
# Fihirana
curl http://localhost:5000/api/fihirana?limit=5

# Bible
curl http://localhost:5000/api/bible/livres
```

---

## 📖 Documentation Complète

Voir [backend/DATABASE_BACKUP.md](backend/DATABASE_BACKUP.md) pour:
- Backups sélectifs (Fihirana uniquement, Bible uniquement)
- Stratégies de backup avancées
- Dépannage
- Cas d'usage détaillés

---

## ✅ Points Clés

1. **Import Automatique:** Le backup est importé automatiquement lors du premier `docker-compose up`
2. **Données Incluses:** 892 hymnes + 3,520 versets + Bible (44 livres)
3. **Compatible Production:** Le même système fonctionne en dev et prod
4. **Version Control:** Le backup est versionné dans Git pour la traçabilité

---

**Dernière mise à jour:** 2025-11-19
