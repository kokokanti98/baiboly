# Configuration DNS et Apache - baiboly-fihirana.mnsite.ovh

## ✅ Configuration DNS (Déjà Fait)

Vous avez configuré :
- **Domaine:** `baiboly-fihirana.mnsite.ovh`
- **Type:** A
- **Cible:** `193.70.0.44` (IP du serveur)

**Propagation DNS:** Peut prendre 15 minutes à 48 heures (généralement ~1 heure)

### Vérifier la Propagation DNS

```bash
# Depuis votre machine locale
nslookup baiboly-fihirana.mnsite.ovh

# Ou
ping baiboly-fihirana.mnsite.ovh
# Devrait répondre depuis 193.70.0.44
```

## 📋 Configuration Apache sur le Serveur

### Étape 1: Copier la Configuration

Le fichier `deploy/baiboly.conf` est déjà configuré avec votre domaine.

```bash
# Se connecter au serveur
ssh root@193.70.0.44

# Copier la configuration Apache
cp /opt/baiboly/deploy/baiboly.conf /etc/apache2/sites-available/

# Vérifier le contenu
cat /etc/apache2/sites-available/baiboly.conf
```

### Étape 2: Activer le Site

```bash
# Activer le site Baiboly
a2ensite baiboly.conf

# Désactiver le site par défaut
a2dissite 000-default.conf

# Tester la configuration
apache2ctl configtest
# Devrait afficher: Syntax OK

# Recharger Apache
systemctl reload apache2
```

### Étape 3: Vérifier (Sans SSL d'abord)

```bash
# Tester l'accès HTTP (sera redirigé vers HTTPS mais échouera sans certificat)
curl -I http://baiboly-fihirana.mnsite.ovh
# Devrait retourner une redirection 301
```

### Étape 4: Configurer SSL avec Let's Encrypt

**Important:** Attendez que le DNS soit propagé avant de configurer SSL !

```bash
# Installer Certbot (si pas déjà fait par server-setup.sh)
apt-get update
apt-get install certbot python3-certbot-apache

# Obtenir le certificat SSL
certbot --apache -d baiboly-fihirana.mnsite.ovh -d www.baiboly-fihirana.mnsite.ovh

# Suivre les instructions:
# 1. Entrer votre email
# 2. Accepter les termes
# 3. Choisir de rediriger HTTP vers HTTPS (option 2)
```

Certbot va automatiquement :
- ✅ Obtenir le certificat SSL
- ✅ Modifier la configuration Apache
- ✅ Configurer le renouvellement automatique

### Étape 5: Vérifier SSL

```bash
# Tester HTTPS
curl -I https://baiboly-fihirana.mnsite.ovh
# Devrait retourner 200 OK

# Vérifier le certificat
openssl s_client -connect baiboly-fihirana.mnsite.ovh:443 -servername baiboly-fihirana.mnsite.ovh
```

### Étape 6: Configurer le Renouvellement Automatique

```bash
# Tester le renouvellement (dry-run)
certbot renew --dry-run

# Le renouvellement automatique est déjà configuré par Certbot
# Vérifier le timer systemd
systemctl status certbot.timer
```

## 🔍 Configuration Finale Apache

Votre fichier `/etc/apache2/sites-available/baiboly.conf` contient :

```apache
<VirtualHost *:80>
    ServerName baiboly-fihirana.mnsite.ovh
    ServerAlias www.baiboly-fihirana.mnsite.ovh
    
    # Redirect HTTP to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
</VirtualHost>

<VirtualHost *:443>
    ServerName baiboly-fihirana.mnsite.ovh
    ServerAlias www.baiboly-fihirana.mnsite.ovh
    
    # SSL Configuration (Certbot ajoutera les certificats)
    SSLEngine on
    
    # Document Root
    DocumentRoot /var/www/html/baiboly
    
    # Proxy API vers Backend Docker
    ProxyPass /api http://localhost:5000/api
    ProxyPassReverse /api http://localhost:5000/api
    
    # ... (headers de sécurité, cache, etc.)
</VirtualHost>
```

## ✅ Checklist Complète

### Avant SSL

- [ ] DNS configuré (A record → 193.70.0.44)
- [ ] DNS propagé (vérifier avec `nslookup`)
- [ ] Apache configuré (`baiboly.conf` copié)
- [ ] Site activé (`a2ensite baiboly.conf`)
- [ ] Site par défaut désactivé (`a2dissite 000-default.conf`)
- [ ] Configuration testée (`apache2ctl configtest`)
- [ ] Apache rechargé (`systemctl reload apache2`)

### Avec SSL

- [ ] Certbot installé
- [ ] Certificat SSL obtenu (`certbot --apache`)
- [ ] HTTPS fonctionne
- [ ] Redirection HTTP → HTTPS active
- [ ] Renouvellement automatique configuré

## 🌐 URLs Finales

Une fois tout configuré :

- **HTTP:** `http://baiboly-fihirana.mnsite.ovh` → Redirige vers HTTPS
- **HTTPS:** `https://baiboly-fihirana.mnsite.ovh` → Application
- **API:** `https://baiboly-fihirana.mnsite.ovh/api/health`

## 🔧 Commandes Utiles

```bash
# Vérifier les sites activés
ls -la /etc/apache2/sites-enabled/

# Voir les logs Apache
tail -f /var/log/apache2/baiboly-access.log
tail -f /var/log/apache2/baiboly-error.log

# Recharger Apache après modification config
systemctl reload apache2

# Redémarrer Apache
systemctl restart apache2

# Vérifier le statut Apache
systemctl status apache2

# Tester la configuration
apache2ctl configtest

# Voir les certificats SSL
certbot certificates

# Renouveler manuellement
certbot renew
```

## 🆘 Dépannage

### DNS ne se propage pas

```bash
# Vérifier depuis différents DNS
nslookup baiboly-fihirana.mnsite.ovh 8.8.8.8
nslookup baiboly-fihirana.mnsite.ovh 1.1.1.1

# Attendre et réessayer (peut prendre jusqu'à 48h)
```

### Erreur "Name or service not known"

Le DNS n'est pas encore propagé. Attendez et réessayez.

### Erreur SSL "Certificate not found"

```bash
# Vérifier que Certbot a bien créé les certificats
ls -la /etc/letsencrypt/live/baiboly-fihirana.mnsite.ovh/

# Relancer Certbot si nécessaire
certbot --apache -d baiboly-fihirana.mnsite.ovh
```

### Site inaccessible

```bash
# Vérifier qu'Apache écoute sur les bons ports
netstat -tlnp | grep :80
netstat -tlnp | grep :443

# Vérifier le firewall
ufw status
# Ports 80 et 443 doivent être ouverts
```

## 📝 Notes Importantes

1. **Attendez la propagation DNS** avant de configurer SSL
2. **Certbot modifiera automatiquement** votre configuration Apache
3. **Le renouvellement SSL est automatique** (tous les 60 jours)
4. **Les logs sont dans** `/var/log/apache2/`
5. **Le certificat est valide 90 jours** et se renouvelle automatiquement

## 🎉 Résultat Final

Une fois tout configuré, votre application sera accessible sur :

**https://baiboly-fihirana.mnsite.ovh**

Avec :
- ✅ SSL/HTTPS automatique
- ✅ Redirection HTTP → HTTPS
- ✅ Headers de sécurité
- ✅ Compression et cache
- ✅ API proxy vers backend Docker
- ✅ Renouvellement SSL automatique
