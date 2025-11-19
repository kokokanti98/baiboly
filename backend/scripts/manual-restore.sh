#!/bin/bash
# Script pour restaurer manuellement le backup sur une base de données existante
# Usage: docker-compose exec db bash /scripts/manual-restore.sh

set -e

BACKUP_FILE="/docker-entrypoint-initdb.d/02-db_backup.sql"
DB_NAME="${POSTGRES_DB:-baiboly_dev}"
DB_USER="${POSTGRES_USER:-baiboly_user}"

echo "⚠️  ATTENTION: Ce script va EFFACER toutes les données existantes!"
echo "📦 Import du backup depuis: $BACKUP_FILE"
echo "🗄️  Base de données: $DB_NAME"
echo ""

# Restaurer le backup (le backup contient déjà les commandes DROP)
psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"

echo ""
echo "✅ Backup restauré avec succès!"

# Afficher les statistiques
hira_count=$(psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM hira;" 2>/dev/null || echo "0")
tononkira_count=$(psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM tononkira;" 2>/dev/null || echo "0")
livre_count=$(psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM livre;" 2>/dev/null || echo "0")

echo ""
echo "📊 Statistiques de la base de données:"
echo "   - Hymnes (hira): $hira_count"
echo "   - Versets hymnes (tononkira): $tononkira_count"
echo "   - Livres Bible (livre): $livre_count"
