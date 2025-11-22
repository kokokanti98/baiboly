# CI/CD Workflow - Baiboly

## Vue d'Ensemble

Ce document décrit le workflow CI/CD pour déployer l'application Baiboly sur un serveur de production avec une architecture hybride.

## Architecture de Déploiement

### Environnement Local (Dev)
- Frontend: Docker (port 5173)
- Backend: Docker (port 5000)
- Database: Docker (port 5432)

### Environnement Production
- **Frontend**: Fichiers statiques servis par **Apache** (pas Docker)
- **Backend**: Docker (port 5000)
- **Database**: PostgreSQL Docker (port 5432)

```
┌─────────────────────────────────────────────────┐
│              Serveur Production                  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Apache (Port 80/443)                    │  │
│  │  ├─ /var/www/baiboly (Frontend Static)   │  │
│  │  └─ ProxyPass /api → localhost:5000      │  │
│  └──────────────────────────────────────────┘  │
│                      ↓                           │
│  ┌──────────────────────────────────────────┐  │
│  │  Backend Docker (Port 5000)              │  │
│  │  └─ Flask + Gunicorn                     │  │
│  └──────────────────────────────────────────┘  │
│                      ↓                           │
│  ┌──────────────────────────────────────────┐  │
│  │  PostgreSQL Docker (Port 5432)           │  │
│  │  └─ Données: 892 hymnes + Bible         │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Fichiers Créés

### Configuration Serveur
- ✅ `deploy/baiboly.conf` - Configuration Apache VirtualHost
- ✅ `deploy/server-setup.sh` - Script d'initialisation serveur
- ✅ `deploy/docker-compose.prod.yml` - Docker Compose production (backend + DB uniquement)
- ✅ `deploy/.env.production.example` - Template variables d'environnement

### Scripts de Déploiement
- ✅ `deploy/deploy-backend.sh` - Déploiement backend + DB
- ✅ `deploy/deploy-frontend.sh` - Déploiement frontend statique
- ✅ `deploy/README.md` - Documentation complète

### Modifications
- ✅ `backend/requirements.txt` - Ajout de gunicorn
- ✅ Plan d'implémentation mis à jour pour Apache

## Prochaines Étapes

### 1. Créer le Workflow GitHub Actions

Créer `.github/workflows/ci-cd.yml` avec:
- Tests automatiques (backend + frontend)
- Build frontend
- Déploiement SSH vers serveur

### 2. Configuration Serveur

Avant le premier déploiement:

1. **Provisionner un serveur** (VPS, cloud)
   - Ubuntu 20.04+ ou Debian 11+
   - Minimum 2GB RAM, 20GB disque
   - Accès SSH configuré

2. **Exécuter le script de setup**
   ```bash
   scp deploy/server-setup.sh user@server:/tmp/
   ssh user@server
   sudo bash /tmp/server-setup.sh
   ```

3. **Configurer Apache**
   ```bash
   sudo cp /opt/baiboly/deploy/baiboly.conf /etc/apache2/sites-available/
   sudo nano /etc/apache2/sites-available/baiboly.conf  # Éditer domaine
   sudo a2ensite baiboly.conf
   sudo a2dissite 000-default.conf
   sudo apache2ctl configtest
   sudo systemctl reload apache2
   ```

4. **Configurer SSL**
   ```bash
   sudo certbot --apache -d votredomaine.com
   ```

5. **Configurer .env**
   ```bash
   cd /opt/baiboly/deploy
   cp .env.production.example .env
   nano .env  # Éditer avec vos valeurs
   ```

6. **Copier le backup initial**
   ```bash
   # Depuis votre machine locale
   scp backend/db_backup.sql user@server:/opt/baiboly/deploy/backups/
   ```

### 3. Premier Déploiement Manuel

```bash
# Sur le serveur
cd /opt/baiboly/deploy

# Déployer backend + DB
bash deploy-backend.sh

# Depuis votre machine locale, build frontend
cd frontend
npm run build

# Copier vers serveur
scp -r dist user@server:/opt/baiboly/deploy/

# Sur le serveur, déployer frontend
sudo bash deploy-frontend.sh
```

### 4. Configurer GitHub Secrets

Dans votre repository GitHub → Settings → Secrets and variables → Actions:

- `SSH_PRIVATE_KEY` - Clé SSH pour accès serveur
- `SERVER_HOST` - IP ou domaine du serveur
- `SERVER_USER` - Utilisateur SSH
- `POSTGRES_PASSWORD` - Mot de passe DB production
- `SECRET_KEY` - Clé secrète Flask
- `DOMAIN` - Votre domaine

### 5. Créer le Workflow GitHub Actions

Créer `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install backend dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run backend tests
        run: |
          cd backend
          pytest --cov=src --cov-report=term
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install frontend dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run frontend tests
        run: |
          cd frontend
          npm test -- --coverage
      
      - name: Build frontend
        run: |
          cd frontend
          npm run build
      
      - name: Upload frontend build
        uses: actions/upload-artifact@v3
        with:
          name: frontend-dist
          path: frontend/dist

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Download frontend build
        uses: actions/download-artifact@v3
        with:
          name: frontend-dist
          path: frontend/dist
      
      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts
      
      - name: Deploy Backend
        run: |
          ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'EOF'
            cd /opt/baiboly
            git pull origin main
            cd deploy
            bash deploy-backend.sh
          EOF
      
      - name: Deploy Frontend
        run: |
          scp -r frontend/dist/* ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }}:/tmp/baiboly-frontend/
          ssh ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'EOF'
            sudo cp -r /tmp/baiboly-frontend/* /var/www/baiboly/
            sudo chown -R www-data:www-data /var/www/baiboly
            sudo systemctl reload apache2
            rm -rf /tmp/baiboly-frontend
          EOF
      
      - name: Health Check
        run: |
          sleep 10
          curl -f https://${{ secrets.DOMAIN }}/api/health || exit 1
```

## Workflow de Développement

### Développement Local

1. Créer une branche feature
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```

2. Développer et tester localement
   ```bash
   docker-compose up -d
   # Faire vos modifications
   docker-compose exec backend pytest
   cd frontend && npm test
   ```

3. Commit et push
   ```bash
   git add .
   git commit -m "feat: ma nouvelle fonctionnalité"
   git push origin feature/ma-fonctionnalite
   ```

4. Créer une Pull Request
   - Les tests s'exécutent automatiquement
   - Attendre la review

5. Merge dans `main`
   - Déploiement automatique en production

### Déploiement Manuel (si besoin)

```bash
# Sur le serveur
cd /opt/baiboly
git pull origin main
cd deploy
bash deploy-backend.sh

# Depuis local
cd frontend
npm run build
scp -r dist user@server:/opt/baiboly/deploy/
ssh user@server "cd /opt/baiboly/deploy && sudo bash deploy-frontend.sh"
```

## Rollback

### Rollback Frontend

```bash
ssh user@server
cd /var/www
sudo cp -r baiboly-backups/baiboly-YYYYMMDD_HHMMSS/* baiboly/
sudo systemctl reload apache2
```

### Rollback Backend

```bash
ssh user@server
cd /opt/baiboly
git checkout <commit-precedent>
cd deploy
docker-compose -f docker-compose.prod.yml up -d --build backend
```

### Rollback Database

```bash
ssh user@server
cd /opt/baiboly/deploy
gunzip -c backups/baiboly_backup_YYYYMMDD.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U baiboly -d baiboly
```

## Monitoring

### Logs

```bash
# Backend
ssh user@server
docker-compose -f /opt/baiboly/deploy/docker-compose.prod.yml logs -f backend

# Apache
tail -f /var/log/apache2/baiboly-access.log
tail -f /var/log/apache2/baiboly-error.log
```

### Health Checks

```bash
# API
curl https://votredomaine.com/api/health

# Frontend
curl https://votredomaine.com
```

### Métriques

- Uptime monitoring: UptimeRobot, Pingdom
- Logs centralisés: Papertrail, Loggly
- APM: New Relic, Datadog (optionnel)

## Sécurité

### Checklist

- [ ] SSH key authentication uniquement
- [ ] Firewall configuré (UFW)
- [ ] SSL/HTTPS activé
- [ ] Secrets dans GitHub Secrets (pas dans le code)
- [ ] `.env` avec permissions 600
- [ ] Backups automatiques quotidiens
- [ ] Mises à jour système régulières

### Bonnes Pratiques

1. **Secrets Management**
   - Jamais de secrets en clair dans le code
   - Utiliser GitHub Secrets pour CI/CD
   - `.env` sur serveur uniquement

2. **SSH**
   - Clé SSH dédiée pour CI/CD
   - Désactiver authentification par mot de passe
   - Fail2ban configuré

3. **Docker**
   - Images officielles uniquement
   - Scan vulnérabilités régulier
   - Utilisateur non-root dans conteneurs

4. **Apache**
   - HTTPS obligatoire
   - Headers de sécurité configurés
   - Rate limiting activé

## Coûts Estimés

| Service | Coût Mensuel | Notes |
|---------|--------------|-------|
| VPS (2GB RAM) | 5-10€ | DigitalOcean, Hetzner, OVH |
| Domaine | 1-2€ | .com, .mg |
| SSL (Let's Encrypt) | Gratuit | Renouvellement auto |
| GitHub Actions | Gratuit | 2000 min/mois (public repo) |
| **Total** | **~10€/mois** | |

## Support

- Documentation complète: `deploy/README.md`
- Plan d'implémentation: `.gemini/antigravity/brain/.../implementation_plan.md`
- Guide déploiement: `DEPLOYMENT.md`
