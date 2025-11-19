@echo off
REM Script Windows pour créer un backup de la base de données
REM Usage: backup-db.bat [nom-optionnel]

setlocal enabledelayedexpansion

REM Obtenir la date au format YYYYMMDD
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set date_stamp=%datetime:~0,8%

REM Déterminer le nom du backup
if "%~1"=="" (
    set backup_name=db_backup_%date_stamp%.sql
) else (
    set backup_name=%~1.sql
)

echo.
echo ================================
echo   Backup Base de Donnees
echo ================================
echo.
echo Fichier: backend\%backup_name%
echo.

REM Créer le backup
docker-compose exec -T db pg_dump -U baiboly_user -d baiboly_dev --clean --if-exists > backend\%backup_name%

if %errorlevel% equ 0 (
    echo.
    echo [OK] Backup cree avec succes!
    echo.

    REM Afficher la taille du fichier
    for %%A in (backend\%backup_name%) do set size=%%~zA
    set /a size_kb=!size! / 1024
    echo Taille: !size_kb! KB

    REM Demander si on veut remplacer le backup principal
    echo.
    set /p replace="Remplacer le backup principal (backend\db_backup.sql)? [o/N]: "
    if /i "!replace!"=="o" (
        copy /Y backend\%backup_name% backend\db_backup.sql >nul
        echo [OK] Backup principal mis a jour
    )

    echo.
    echo Pour restaurer ce backup:
    echo   docker-compose down -v
    echo   docker-compose up -d
) else (
    echo.
    echo [ERREUR] Echec de la creation du backup
    exit /b 1
)

echo.
pause
