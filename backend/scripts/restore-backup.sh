#!/bin/bash
# Script pour restaurer le backup de la base de données
# Ce script est exécuté automatiquement au démarrage du conteneur si la base est vide

set -e

BACKUP_FILE="/docker-entrypoint-initdb.d/db_backup.sql"
DB_NAME="${POSTGRES_DB:-baiboly_dev}"
DB_USER="${POSTGRES_USER:-baiboly_user}"

echo "🔍 Vérification de l'existence du backup..."

if [ -f "$BACKUP_FILE" ]; then
    echo "✅ Backup trouvé: $BACKUP_FILE"

    # Vérifier si la base de données est déjà initialisée
    table_count=$(psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null || echo "0")

    if [ "$table_count" -eq "0" ]; then
        echo "📦 Base de données vide détectée, import du backup..."
        psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"
        echo "✅ Backup importé avec succès!"

        # Vérifier le nombre de hymnes importés
        hira_count=$(psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM hira;" 2>/dev/null || echo "0")
        tononkira_count=$(psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM tononkira;" 2>/dev/null || echo "0")

        echo "📊 Statistiques d'import:"
        echo "   - Hymnes (hira): $hira_count"
        echo "   - Versets (tononkira): $tononkira_count"
    else
        echo "ℹ️  Base de données déjà initialisée (${table_count} tables), skip de l'import"
    fi
else
    echo "⚠️  Aucun backup trouvé à $BACKUP_FILE"
    echo "ℹ️  La base de données sera initialisée avec les migrations Flask"
fi
