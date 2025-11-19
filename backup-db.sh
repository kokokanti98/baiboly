#!/bin/bash
# Script pour créer un backup de la base de données
# Usage: ./backup-db.sh [nom-optionnel]

set -e

# Obtenir la date
date_stamp=$(date +%Y%m%d)

# Déterminer le nom du backup
if [ -z "$1" ]; then
    backup_name="db_backup_${date_stamp}.sql"
else
    backup_name="${1}.sql"
fi

echo ""
echo "================================"
echo "   Backup Base de Données"
echo "================================"
echo ""
echo "Fichier: backend/${backup_name}"
echo ""

# Créer le backup
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > "backend/${backup_name}"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Backup créé avec succès!"
    echo ""

    # Afficher la taille du fichier
    size=$(du -h "backend/${backup_name}" | cut -f1)
    echo "Taille: ${size}"

    # Afficher les statistiques
    echo ""
    echo "📊 Contenu du backup:"
    grep -c "COPY public.hira" "backend/${backup_name}" > /dev/null && echo "   - Table hira: présente"
    grep -c "COPY public.tononkira" "backend/${backup_name}" > /dev/null && echo "   - Table tononkira: présente"
    grep -c "COPY public.livre" "backend/${backup_name}" > /dev/null && echo "   - Table livre: présente"

    # Demander si on veut remplacer le backup principal
    echo ""
    read -p "Remplacer le backup principal (backend/db_backup.sql)? [o/N]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        cp "backend/${backup_name}" backend/db_backup.sql
        echo "✅ Backup principal mis à jour"
    fi

    echo ""
    echo "Pour restaurer ce backup:"
    echo "  docker-compose down -v"
    echo "  docker-compose up -d"
else
    echo ""
    echo "❌ Échec de la création du backup"
    exit 1
fi

echo ""
