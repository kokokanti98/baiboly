# Configuration des Secrets GitHub - Baiboly

Ce document explique comment configurer les secrets nécessaires pour le workflow CI/CD GitHub Actions.

## Secrets Requis

Le workflow nécessite les secrets suivants dans votre repository GitHub :

| Secret | Description | Exemple | Obligatoire |
|--------|-------------|---------|-------------|
| `SSH_PRIVATE_KEY` | Clé SSH privée pour accès au serveur | `-----BEGIN OPENSSH PRIVATE KEY-----...` | ✅ Oui |
| `SERVER_HOST` | IP ou domaine du serveur VPS OVH | `193.70.0.44` | ✅ Oui |
| `SERVER_USER` | Utilisateur SSH sur le serveur | `root` | ✅ Oui |

**Note:** Le domaine sera configuré manuellement dans Apache (`/etc/apache2/sites-available/baiboly.conf`), donc pas besoin du secret `DOMAIN`.

## Étape 1 : Créer une Clé SSH pour CI/CD

Sur votre **machine locale** :

```bash
# Générer une nouvelle clé SSH dédiée au CI/CD
ssh-keygen -t ed25519 -C "github-actions-baiboly" -f ~/.ssh/baiboly_deploy

# Afficher la clé PRIVÉE (à copier dans GitHub Secrets)
cat ~/.ssh/baiboly_deploy

# Afficher la clé PUBLIQUE (à copier sur le serveur)
cat ~/.ssh/baiboly_deploy.pub
```

## Étape 2 : Configurer le Serveur VPS OVH

### 2.1 Copier la Clé Publique sur le Serveur

```bash
# Option 1: Avec ssh-copy-id (recommandé)
ssh-copy-id -i ~/.ssh/baiboly_deploy.pub user@votre-serveur-ovh

# Option 2: Manuellement
ssh user@votre-serveur-ovh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Coller la clé publique, sauvegarder
chmod 600 ~/.ssh/authorized_keys
exit
```

### 2.2 Tester la Connexion SSH

```bash
ssh -i ~/.ssh/baiboly_deploy user@votre-serveur-ovh
# Si ça fonctionne, vous êtes connecté sans mot de passe ✅
```

### 2.3 Préparer le Serveur

```bash
# Se connecter au serveur
ssh user@votre-serveur-ovh

# Créer le répertoire de l'application
sudo mkdir -p /opt/baiboly
sudo chown $USER:$USER /opt/baiboly

# Cloner le repository (première fois)
cd /opt
git clone https://github.com/votre-username/baiboly.git

# Ou si déjà cloné, mettre à jour
cd /opt/baiboly
git pull origin main
```

## Étape 3 : Configurer les Secrets GitHub

### 3.1 Accéder aux Secrets

1. Aller sur votre repository GitHub
2. Cliquer sur **Settings** (Paramètres)
3. Dans le menu de gauche, cliquer sur **Secrets and variables** → **Actions**
4. Cliquer sur **New repository secret**

### 3.2 Ajouter les Secrets

#### Secret 1: `SSH_PRIVATE_KEY`

```bash
# Sur votre machine locale, copier la clé PRIVÉE
cat ~/.ssh/baiboly_deploy
```

- **Name**: `SSH_PRIVATE_KEY`
- **Value**: Coller TOUT le contenu (y compris les lignes `-----BEGIN` et `-----END`)

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
...
(toute la clé)
...
-----END OPENSSH PRIVATE KEY-----
```

#### Secret 2: `SERVER_HOST`

- **Name**: `SERVER_HOST`
- **Value**: L'IP ou le domaine de votre VPS OVH

Exemples :
```
123.45.67.89
```
ou
```
vps-12345678.vps.ovh.net
```

Pour trouver votre IP :
```bash
# Sur le serveur
curl ifconfig.me
```

#### Secret 3: `SERVER_USER`

- **Name**: `SERVER_USER`
- **Value**: Votre nom d'utilisateur SSH

Exemples courants :
- `ubuntu` (pour Ubuntu)
- `debian` (pour Debian)
- `root` (⚠️ non recommandé)

Pour vérifier :
```bash
# Sur le serveur
whoami
```

#### Secret 4: `DOMAIN` (Optionnel pour l'instant)

- **Name**: `DOMAIN`
- **Value**: Votre nom de domaine (si vous en avez un)

Exemple :
```
baiboly.mg
```

**Note**: Vous pouvez laisser ce secret vide pour l'instant. Il sera utilisé plus tard pour les health checks HTTPS.

## Étape 4 : Tester le Workflow

### 4.1 Commit et Push

```bash
# Sur votre machine locale
cd c:\Dev\baiboly
git add .github/workflows/ci-cd.yml
git commit -m "ci: add GitHub Actions CI/CD workflow"
git push origin main
```

### 4.2 Vérifier l'Exécution

1. Aller sur GitHub → votre repository
2. Cliquer sur l'onglet **Actions**
3. Vous devriez voir le workflow "CI/CD Pipeline - Baiboly" en cours d'exécution

### 4.3 Interpréter les Résultats

- ✅ **Vert** : Tout s'est bien passé
- ❌ **Rouge** : Une erreur s'est produite
  - Cliquer sur le workflow pour voir les logs
  - Vérifier les secrets
  - Vérifier la connexion SSH

## Étape 5 : Secrets Supplémentaires (Plus Tard)

Ces secrets seront nécessaires quand vous configurerez l'environnement de production sur le serveur :

### `POSTGRES_PASSWORD`

```bash
# Générer un mot de passe sécurisé
openssl rand -base64 32
```

### `SECRET_KEY`

```bash
# Générer une clé secrète Flask
openssl rand -hex 32
```

Ces secrets seront utilisés dans le fichier `.env` sur le serveur.

## Troubleshooting

### Erreur: "Permission denied (publickey)"

**Cause**: La clé SSH n'est pas correctement configurée

**Solution**:
```bash
# Vérifier que la clé publique est sur le serveur
ssh user@serveur "cat ~/.ssh/authorized_keys"

# Vérifier les permissions
ssh user@serveur "ls -la ~/.ssh/"
# authorized_keys doit être 600
# .ssh doit être 700
```

### Erreur: "Host key verification failed"

**Cause**: Le serveur n'est pas dans les known_hosts

**Solution**: Le workflow utilise `ssh-keyscan` pour ajouter automatiquement le serveur. Si le problème persiste :
```bash
# Sur votre machine locale
ssh-keyscan -H votre-serveur-ovh >> ~/.ssh/known_hosts
```

### Erreur: "No such file or directory: /opt/baiboly"

**Cause**: Le répertoire n'existe pas sur le serveur

**Solution**:
```bash
ssh user@serveur
sudo mkdir -p /opt/baiboly
sudo chown $USER:$USER /opt/baiboly
cd /opt
git clone https://github.com/votre-username/baiboly.git
```

### Erreur: "docker-compose: command not found"

**Cause**: Docker Compose n'est pas installé sur le serveur

**Solution**:
```bash
ssh user@serveur
cd /opt/baiboly/deploy
sudo bash server-setup.sh
```

## Sécurité

### ✅ Bonnes Pratiques

- ✅ Utiliser une clé SSH dédiée pour CI/CD (pas votre clé personnelle)
- ✅ Ne jamais commiter les clés privées dans le repository
- ✅ Utiliser des secrets GitHub pour toutes les informations sensibles
- ✅ Limiter les permissions de l'utilisateur SSH (pas root)
- ✅ Activer l'authentification à deux facteurs sur GitHub

### ❌ À Éviter

- ❌ Utiliser `root` comme utilisateur SSH
- ❌ Mettre des secrets dans le code ou les fichiers de configuration
- ❌ Partager les clés SSH
- ❌ Utiliser des mots de passe faibles

## Workflow de Déploiement

Une fois les secrets configurés, le workflow fonctionne ainsi :

1. **Push sur `main`** → Déclenche le workflow
2. **Tests Backend** → Pytest + couverture ≥80%
3. **Tests Frontend** → Jest + couverture ≥75%
4. **Build Frontend** → `npm run build`
5. **Déploiement Backend** → Docker sur serveur
6. **Déploiement Frontend** → Copie vers `/var/www/html/baiboly`
7. **Health Checks** → Vérification API + Frontend
8. **Nettoyage** → Suppression anciens backups

## Support

- Documentation CI/CD complète: `CI_CD.md`
- Guide déploiement: `deploy/README.md`
- Plan d'implémentation: `.gemini/antigravity/brain/.../implementation_plan.md`
