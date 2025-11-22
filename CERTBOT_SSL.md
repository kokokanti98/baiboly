# 🔒 Configuration SSL avec Certbot - Guide Rapide

## ✅ Prérequis

- [ ] DNS propagé (baiboly-fihirana.mnsite.ovh → 193.70.0.44)
- [ ] Apache configuré et en cours d'exécution
- [ ] Site accessible en HTTP
- [ ] Ports 80 et 443 ouverts dans le firewall

## 🚀 Commandes Certbot

### 1. Installer Certbot (si pas déjà fait)

```bash
# Sur le serveur (root@193.70.0.44)
apt-get update
apt-get install certbot python3-certbot-apache -y
```

### 2. Obtenir le Certificat SSL

**Commande simple (recommandée) :**

```bash
certbot --apache -d baiboly-fihirana.mnsite.ovh -d www.baiboly-fihirana.mnsite.ovh
```

**Ce que Certbot va faire automatiquement :**
1. ✅ Vérifier que le domaine pointe vers le serveur
2. ✅ Obtenir le certificat SSL de Let's Encrypt
3. ✅ Modifier `/etc/apache2/sites-available/baiboly.conf`
4. ✅ Ajouter la configuration HTTPS (VirtualHost *:443)
5. ✅ Ajouter la redirection HTTP → HTTPS
6. ✅ Ajouter les headers de sécurité
7. ✅ Recharger Apache
8. ✅ Configurer le renouvellement automatique

**Pendant l'exécution, Certbot vous demandera :**

1. **Email :** Entrez votre email (pour notifications d'expiration)
   ```
   Enter email address: votre-email@example.com
   ```

2. **Accepter les termes :** Tapez `Y`
   ```
   Please read the Terms of Service at https://letsencrypt.org/documents/LE-SA-v1.3-September-21-2022.pdf
   (A)gree/(C)ancel: A
   ```

3. **Partager l'email avec EFF :** Tapez `N` (optionnel)
   ```
   Would you be willing to share your email address with EFF? (Y)es/(N)o: N
   ```

4. **Redirection HTTPS :** Tapez `2` (rediriger automatiquement)
   ```
   Please choose whether or not to redirect HTTP traffic to HTTPS:
   1: No redirect
   2: Redirect - Make all requests redirect to secure HTTPS access
   Select the appropriate number [1-2]: 2
   ```

### 3. Vérifier le Certificat

```bash
# Vérifier que le certificat est installé
certbot certificates

# Devrait afficher:
# Certificate Name: baiboly-fihirana.mnsite.ovh
#   Domains: baiboly-fihirana.mnsite.ovh www.baiboly-fihirana.mnsite.ovh
#   Expiry Date: ... (90 jours)
#   Certificate Path: /etc/letsencrypt/live/baiboly-fihirana.mnsite.ovh/fullchain.pem
#   Private Key Path: /etc/letsencrypt/live/baiboly-fihirana.mnsite.ovh/privkey.pem
```

### 4. Tester HTTPS

```bash
# Tester depuis le serveur
curl -I https://baiboly-fihirana.mnsite.ovh
# Devrait retourner: HTTP/2 200

# Tester la redirection HTTP → HTTPS
curl -I http://baiboly-fihirana.mnsite.ovh
# Devrait retourner: HTTP/1.1 301 Moved Permanently
# Location: https://baiboly-fihirana.mnsite.ovh/
```

### 5. Vérifier le Renouvellement Automatique

```bash
# Tester le renouvellement (dry-run, ne fait rien)
certbot renew --dry-run

# Devrait afficher:
# Congratulations, all simulated renewals succeeded
```

Le renouvellement automatique est déjà configuré via systemd timer :

```bash
# Vérifier le timer
systemctl status certbot.timer

# Devrait afficher: Active: active (waiting)
```

## 📋 Configuration Finale Apache

Après Certbot, votre fichier `/etc/apache2/sites-available/baiboly.conf` contiendra :

```apache
# HTTP - Redirection vers HTTPS
<VirtualHost *:80>
    ServerName baiboly-fihirana.mnsite.ovh
    ServerAlias www.baiboly-fihirana.mnsite.ovh
    
    RewriteEngine on
    RewriteCond %{SERVER_NAME} =baiboly-fihirana.mnsite.ovh [OR]
    RewriteCond %{SERVER_NAME} =www.baiboly-fihirana.mnsite.ovh
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

# HTTPS - Configuration complète
<VirtualHost *:443>
    ServerName baiboly-fihirana.mnsite.ovh
    ServerAlias www.baiboly-fihirana.mnsite.ovh
    
    # SSL Certificates (ajoutés par Certbot)
    SSLCertificateFile /etc/letsencrypt/live/baiboly-fihirana.mnsite.ovh/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/baiboly-fihirana.mnsite.ovh/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
    
    # Votre configuration originale (DocumentRoot, Proxy, etc.)
    DocumentRoot /var/www/html/baiboly
    ProxyPass /api http://localhost:5000/api
    # ...
</VirtualHost>
```

## 🔄 Renouvellement du Certificat

Les certificats Let's Encrypt sont valides **90 jours**.

**Renouvellement automatique :** Certbot renouvelle automatiquement tous les 60 jours.

**Renouvellement manuel (si nécessaire) :**

```bash
# Renouveler tous les certificats
certbot renew

# Renouveler un certificat spécifique
certbot renew --cert-name baiboly-fihirana.mnsite.ovh

# Forcer le renouvellement (même si pas expiré)
certbot renew --force-renewal
```

## 🆘 Dépannage

### Erreur: "DNS problem: NXDOMAIN"

Le DNS n'est pas encore propagé. Attendez et réessayez.

```bash
# Vérifier le DNS
nslookup baiboly-fihirana.mnsite.ovh
dig baiboly-fihirana.mnsite.ovh
```

### Erreur: "Connection refused"

Apache n'est pas en cours d'exécution ou le port 80 est bloqué.

```bash
# Vérifier Apache
systemctl status apache2

# Vérifier le firewall
ufw status
ufw allow 80/tcp
ufw allow 443/tcp
```

### Erreur: "Unable to find a virtual host"

Le site n'est pas activé dans Apache.

```bash
# Activer le site
a2ensite baiboly.conf
systemctl reload apache2
```

### Certificat expiré

```bash
# Renouveler manuellement
certbot renew --force-renewal

# Vérifier la date d'expiration
certbot certificates
```

## ✅ Checklist SSL

- [ ] DNS propagé et vérifié
- [ ] Apache en cours d'exécution
- [ ] Site accessible en HTTP
- [ ] Certbot installé
- [ ] Certificat SSL obtenu
- [ ] HTTPS fonctionne
- [ ] Redirection HTTP → HTTPS active
- [ ] Renouvellement automatique configuré
- [ ] Test de renouvellement réussi (`certbot renew --dry-run`)

## 🎉 Résultat Final

Votre site sera accessible sur :

- **HTTP:** `http://baiboly-fihirana.mnsite.ovh` → Redirige vers HTTPS
- **HTTPS:** `https://baiboly-fihirana.mnsite.ovh` ✅
- **API:** `https://baiboly-fihirana.mnsite.ovh/api/health` ✅

Avec :
- ✅ Certificat SSL valide (Let's Encrypt)
- ✅ Grade A+ sur SSL Labs
- ✅ Renouvellement automatique tous les 60 jours
- ✅ Headers de sécurité configurés
- ✅ Redirection HTTP → HTTPS

## 📞 Commandes Utiles

```bash
# Voir tous les certificats
certbot certificates

# Supprimer un certificat
certbot delete --cert-name baiboly-fihirana.mnsite.ovh

# Voir les logs Certbot
tail -f /var/log/letsencrypt/letsencrypt.log

# Tester le site SSL
openssl s_client -connect baiboly-fihirana.mnsite.ovh:443 -servername baiboly-fihirana.mnsite.ovh

# Vérifier le grade SSL (depuis votre machine)
# https://www.ssllabs.com/ssltest/analyze.html?d=baiboly-fihirana.mnsite.ovh
```

---

**C'est tout !** Une seule commande Certbot et votre site est sécurisé en HTTPS. 🔒
