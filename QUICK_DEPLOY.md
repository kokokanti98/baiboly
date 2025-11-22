# 🚀 Guide de Déploiement Rapide - Baiboly

Ce guide vous permet de déployer Baiboly sur votre VPS OVH en quelques étapes.

## ✅ Prérequis

- [ ] VPS OVH avec Ubuntu 20.04+ ou Debian 11+
- [ ] Accès SSH au serveur
- [ ] Repository GitHub du projet
- [ ] (Optionnel) Nom de domaine pointant vers le serveur

## 📋 Étapes de Déploiement

### Étape 1: Préparer la Clé SSH (5 min)

**Sur votre machine locale:**

```bash
# Générer une clé SSH dédiée
ssh-keygen -t ed25519 -C "github-actions-baiboly" -f ~/.ssh/baiboly_deploy

# Copier la clé publique sur le serveur
ssh-copy-id -i ~/.ssh/baiboly_deploy.pub user@votre-serveur-ovh

# Tester la connexion
ssh -i ~/.ssh/baiboly_deploy user@votre-serveur-ovh
```

### Étape 2: Initialiser le Serveur (10 min)

**Sur le serveur:**

```bash
# Copier le script de setup
# (depuis votre machine locale)
scp deploy/server-setup.sh user@serveur:/tmp/

# Sur le serveur, exécuter le script
ssh user@serveur
sudo bash /tmp/server-setup.sh
```

Ce script installe:
- Docker & Docker Compose
- Apache avec modules nécessaires
- Certbot pour SSL
- Configure le firewall

### Étape 3: Cloner le Repository (2 min)

**Sur le serveur:**

```bash
# Créer le répertoire
sudo mkdir -p /opt/baiboly
sudo chown $USER:$USER /opt/baiboly

# Cloner le projet
cd /opt
git clone https://github.com/votre-username/baiboly.git
cd baiboly
```

### Étape 4: Configurer Apache (5 min)

**Sur le serveur:**

```bash
# Copier la configuration
sudo cp deploy/baiboly.conf /etc/apache2/sites-available/

# Éditer avec votre domaine (ou laisser localhost pour test)
sudo nano /etc/apache2/sites-available/baiboly.conf
# Remplacer "votredomaine.com" par votre domaine

# Activer le site
sudo a2ensite baiboly.conf
sudo a2dissite 000-default.conf

# Tester la configuration
sudo apache2ctl configtest

# Recharger Apache
sudo systemctl reload apache2
```

### Étape 5: Configurer l'Environnement (3 min)

**Sur le serveur:**

```bash
cd /opt/baiboly/deploy

# Créer le fichier .env
cp .env.production.example .env

# Générer les secrets
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)" >> .env

# Éditer le fichier
nano .env
# Vérifier/ajuster les valeurs
```

### Étape 6: Copier le Backup Initial (2 min)

**Depuis votre machine locale:**

```bash
# Copier le backup SQL
scp backend/db_backup.sql user@serveur:/opt/baiboly/deploy/backups/
```

### Étape 7: Premier Déploiement (10 min)

**Sur le serveur:**

```bash
cd /opt/baiboly/deploy

# Déployer le backend + DB
bash deploy-backend.sh
# Attendre que tout démarre (~5 min)

# Vérifier que ça fonctionne
curl http://localhost:5000/api/health
# Devrait retourner: {"status": "healthy"}
```

**Sur votre machine locale:**

```bash
# Build le frontend
cd frontend
npm install
npm run build

# Copier vers le serveur
scp -r dist user@serveur:/opt/baiboly/deploy/
```

**Sur le serveur:**

```bash
cd /opt/baiboly/deploy
sudo bash deploy-frontend.sh

# Vérifier
curl http://localhost
# Devrait afficher la page HTML
```

### Étape 8: Configurer SSL (Optionnel, 5 min)

**Sur le serveur:**

```bash
# Avec Let's Encrypt (gratuit)
sudo certbot --apache -d votredomaine.com -d www.votredomaine.com

# Suivre les instructions
# Certbot configurera automatiquement Apache
```

### Étape 9: Configurer GitHub Secrets (5 min)

**Sur GitHub:**

1. Aller sur votre repository → **Settings** → **Secrets and variables** → **Actions**

2. Ajouter les secrets:

   **SSH_PRIVATE_KEY:**
   ```bash
   # Sur votre machine locale
   cat ~/.ssh/baiboly_deploy
   # Copier TOUT le contenu (y compris BEGIN/END)
   ```

   **SERVER_HOST:**
   ```
   # IP de votre serveur
   123.45.67.89
   ```

   **SERVER_USER:**
   ```
   # Votre utilisateur SSH
   ubuntu
   ```

   **DOMAIN** (optionnel):
   ```
   votredomaine.com
   ```

### Étape 10: Tester le Workflow (2 min)

**Sur votre machine locale:**

```bash
# Commit et push
git add .
git commit -m "ci: configure CI/CD workflow"
git push origin main

# Aller sur GitHub → Actions
# Vérifier que le workflow s'exécute correctement
```

## ✅ Vérification Finale

### Backend

```bash
curl http://votre-serveur/api/health
# Devrait retourner: {"status": "healthy"}

curl http://votre-serveur/api/fihirana?limit=5
# Devrait retourner les 5 premiers hymnes
```

### Frontend

Ouvrir dans le navigateur:
- `http://votre-serveur` (ou `https://votredomaine.com` si SSL configuré)
- Vérifier que la page charge
- Tester la navigation Fihirana/Bible

### Base de Données

```bash
ssh user@serveur
docker-compose -f /opt/baiboly/deploy/docker-compose.prod.yml exec db \
  psql -U baiboly -d baiboly -c "SELECT COUNT(*) FROM hira;"
# Devrait retourner: 892
```

## 🎉 Déploiement Terminé !

Votre application est maintenant déployée et accessible.

### Prochaines Étapes

1. **Configurer les backups automatiques:**
   ```bash
   # Sur le serveur
   crontab -e
   # Ajouter:
   0 2 * * * cd /opt/baiboly/deploy && bash backup.sh
   ```

2. **Configurer le monitoring:**
   - UptimeRobot pour surveiller la disponibilité
   - Logs centralisés (Papertrail, Loggly)

3. **Optimisations:**
   - Configurer le cache Apache
   - Optimiser les images
   - CDN pour les assets statiques

## 📚 Documentation Complète

- **CI/CD:** `CI_CD.md`
- **Secrets GitHub:** `GITHUB_SECRETS.md`
- **Déploiement:** `deploy/README.md`
- **Architecture:** `DEPLOYMENT.md`

## 🆘 Problèmes Courants

### Le backend ne démarre pas

```bash
# Vérifier les logs
docker-compose -f /opt/baiboly/deploy/docker-compose.prod.yml logs backend

# Redémarrer
docker-compose -f /opt/baiboly/deploy/docker-compose.prod.yml restart backend
```

### Le frontend affiche 404

```bash
# Vérifier les fichiers
ls -la /var/www/baiboly/

# Vérifier Apache
sudo apache2ctl configtest
tail -f /var/log/apache2/baiboly-error.log
```

### La base de données est vide

```bash
# Restaurer le backup
cd /opt/baiboly/deploy
gunzip -c backups/db_backup.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T db \
  psql -U baiboly -d baiboly
```

## 📞 Support

Pour plus d'aide, consultez:
- `GITHUB_SECRETS.md` - Configuration détaillée des secrets
- `CI_CD.md` - Documentation complète du workflow
- `deploy/README.md` - Guide de déploiement détaillé
