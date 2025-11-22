# Configuration Serveur OVH - Baiboly

## 📋 Informations Serveur

- **IP:** `193.70.0.44`
- **Port SSH:** `22`
- **Utilisateur:** `root`
- **Chemin déploiement:** `/var/www/html/baiboly`

## ✅ Secrets GitHub Configurés

Vous avez déjà configuré les secrets suivants sur GitHub :

- ✅ `SSH_PRIVATE_KEY` - Clé SSH pour accès serveur
- ✅ `SERVER_HOST` - `193.70.0.44`
- ✅ `SERVER_USER` - `root`

**Note:** Le secret `DOMAIN` n'est pas nécessaire car vous configurerez le domaine manuellement dans Apache.

## 🚀 Prochaines Étapes

### 1. Initialiser le Serveur (Première fois uniquement)

```bash
# Copier le script de setup
scp deploy/server-setup.sh root@193.70.0.44:/tmp/

# Se connecter au serveur
ssh root@193.70.0.44

# Exécuter le script de setup
bash /tmp/server-setup.sh
```

Ce script va installer :
- Docker & Docker Compose
- Apache avec modules nécessaires (proxy, ssl, rewrite, headers, deflate, expires)
- Certbot pour SSL
- Créer les répertoires `/opt/baiboly` et `/var/www/html/baiboly`
- Configurer le firewall

### 2. Cloner le Repository sur le Serveur

```bash
# Sur le serveur
cd /opt
git clone https://github.com/votre-username/baiboly.git
cd baiboly
```

### 3. Configurer Apache

```bash
# Copier la configuration
cp deploy/baiboly.conf /etc/apache2/sites-available/

# Éditer avec votre domaine
nano /etc/apache2/sites-available/baiboly.conf
# Remplacer "votredomaine.com" par votre vrai domaine

# Activer le site
a2ensite baiboly.conf
a2dissite 000-default.conf

# Tester la configuration
apache2ctl configtest

# Recharger Apache
systemctl reload apache2
```

### 4. Configurer l'Environnement

```bash
cd /opt/baiboly/deploy

# Créer le fichier .env
cp .env.production.example .env

# Générer les secrets
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)" >> .env

# Éditer le fichier pour vérifier
nano .env
```

### 5. Copier le Backup Initial

```bash
# Depuis votre machine locale
scp backend/db_backup.sql root@193.70.0.44:/opt/baiboly/deploy/backups/
```

### 6. Premier Déploiement Manuel

```bash
# Sur le serveur
cd /opt/baiboly/deploy

# Déployer le backend
bash deploy-backend.sh

# Attendre que tout démarre (~5 min)
# Vérifier
curl http://localhost:5000/api/health
```

```bash
# Sur votre machine locale
cd frontend
npm install
npm run build

# Copier vers le serveur
scp -r dist root@193.70.0.44:/opt/baiboly/deploy/
```

```bash
# Sur le serveur
cd /opt/baiboly/deploy
bash deploy-frontend.sh

# Vérifier
curl http://localhost
```

### 7. Configurer SSL (Optionnel)

```bash
# Sur le serveur
certbot --apache -d votredomaine.com -d www.votredomaine.com
```

### 8. Tester le Workflow GitHub Actions

```bash
# Sur votre machine locale
git push origin master

# Aller sur GitHub → Actions
# Vérifier que le workflow s'exécute correctement
```

## 🔍 Vérifications

### Backend

```bash
curl http://193.70.0.44:5000/api/health
# Devrait retourner: {"status": "healthy"}

curl http://193.70.0.44:5000/api/fihirana?limit=5
# Devrait retourner les 5 premiers hymnes
```

### Frontend

Ouvrir dans le navigateur :
- `http://193.70.0.44` (ou votre domaine si configuré)

### Base de Données

```bash
ssh root@193.70.0.44
docker-compose -f /opt/baiboly/deploy/docker-compose.prod.yml exec db \
  psql -U baiboly -d baiboly -c "SELECT COUNT(*) FROM hira;"
# Devrait retourner: 892
```

## 📁 Structure des Répertoires sur le Serveur

```
/opt/baiboly/                           # Code de l'application
├── backend/                            # Code backend
├── frontend/                           # Code frontend
├── deploy/                             # Scripts de déploiement
│   ├── docker-compose.prod.yml
│   ├── .env                            # Configuration (à créer)
│   ├── backups/                        # Backups SQL
│   └── logs/                           # Logs application
└── ...

/var/www/html/baiboly/                  # Frontend déployé (servi par Apache)
├── index.html
├── assets/
└── ...

/var/www/html/baiboly-backups/          # Backups frontend (garde 5 derniers)
├── baiboly-20251122_103000/
├── baiboly-20251122_104500/
└── ...

/etc/apache2/sites-available/           # Configuration Apache
└── baiboly.conf                        # VirtualHost configuration
```

## 🔄 Workflow de Déploiement Automatique

Une fois tout configuré :

1. **Développer localement**
   ```bash
   git checkout -b feature/ma-fonctionnalite
   # ... modifications ...
   git commit -m "feat: ma fonctionnalité"
   git push origin feature/ma-fonctionnalite
   ```

2. **Créer Pull Request**
   - Tests s'exécutent automatiquement

3. **Merge dans master**
   ```bash
   git checkout master
   git merge feature/ma-fonctionnalite
   git push origin master
   ```

4. **Déploiement automatique**
   - GitHub Actions détecte le push sur `master`
   - Exécute les tests
   - Build le frontend
   - Déploie sur `193.70.0.44`
   - Health checks

## 🆘 Dépannage

### Le backend ne démarre pas

```bash
ssh root@193.70.0.44
cd /opt/baiboly/deploy
docker-compose -f docker-compose.prod.yml logs backend
```

### Le frontend affiche 404

```bash
ssh root@193.70.0.44
ls -la /var/www/html/baiboly/
apache2ctl configtest
tail -f /var/log/apache2/baiboly-error.log
```

### Workflow GitHub Actions échoue

1. Vérifier les logs dans GitHub → Actions
2. Vérifier que les secrets sont bien configurés
3. Tester la connexion SSH manuellement :
   ```bash
   ssh -i ~/.ssh/baiboly_deploy root@193.70.0.44
   ```

## 📞 Commandes Utiles

```bash
# Redémarrer backend
ssh root@193.70.0.44 "cd /opt/baiboly/deploy && docker-compose -f docker-compose.prod.yml restart backend"

# Voir les logs backend
ssh root@193.70.0.44 "cd /opt/baiboly/deploy && docker-compose -f docker-compose.prod.yml logs -f backend"

# Voir les logs Apache
ssh root@193.70.0.44 "tail -f /var/log/apache2/baiboly-access.log"

# Redémarrer Apache
ssh root@193.70.0.44 "systemctl restart apache2"

# Backup manuel
ssh root@193.70.0.44 "cd /opt/baiboly/deploy && bash backup.sh"
```

## ✅ Checklist Déploiement

- [ ] Script `server-setup.sh` exécuté
- [ ] Repository cloné dans `/opt/baiboly`
- [ ] Apache configuré (`baiboly.conf`)
- [ ] `.env` créé et configuré
- [ ] Backup SQL copié
- [ ] Premier déploiement backend réussi
- [ ] Premier déploiement frontend réussi
- [ ] SSL configuré (optionnel)
- [ ] Workflow GitHub Actions testé
- [ ] Application accessible via IP/domaine

## 🎉 C'est Prêt !

Une fois toutes ces étapes complétées, votre application sera :
- ✅ Déployée sur `http://193.70.0.44` (ou votre domaine)
- ✅ Déploiement automatique sur chaque push `master`
- ✅ Backups automatiques
- ✅ Rollback possible en cas de problème

**Bon déploiement !** 🚀
