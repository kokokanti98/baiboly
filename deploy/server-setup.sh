#!/bin/bash

set -e

echo "=========================================="
echo "Baiboly - Server Initial Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: This script must be run as root${NC}"
    echo "Please run: sudo $0"
    exit 1
fi

echo "This script will:"
echo "  1. Install Docker and Docker Compose"
echo "  2. Configure Apache for Baiboly"
echo "  3. Create necessary directories"
echo "  4. Set up firewall rules"
echo ""
read -p "Continue? [y/N]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

# Update system
echo ""
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Docker
echo ""
echo "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo -e "${GREEN}✓${NC} Docker installed"
else
    echo -e "${GREEN}✓${NC} Docker already installed"
fi

# Install Docker Compose
echo ""
echo "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓${NC} Docker Compose installed"
else
    echo -e "${GREEN}✓${NC} Docker Compose already installed"
fi

# Enable and start Docker
systemctl enable docker
systemctl start docker

# Install Apache (if not already installed)
echo ""
echo "Checking Apache installation..."
if ! command -v apache2 &> /dev/null; then
    echo "Installing Apache..."
    apt-get install -y apache2
    echo -e "${GREEN}✓${NC} Apache installed"
else
    echo -e "${GREEN}✓${NC} Apache already installed"
fi

# Enable required Apache modules
echo ""
echo "Enabling Apache modules..."
a2enmod rewrite
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel
a2enmod ssl
a2enmod headers
a2enmod deflate
a2enmod expires
echo -e "${GREEN}✓${NC} Apache modules enabled"

# Install Certbot for SSL
echo ""
echo "Installing Certbot for SSL certificates..."
if ! command -v certbot &> /dev/null; then
    apt-get install -y certbot python3-certbot-apache
    echo -e "${GREEN}✓${NC} Certbot installed"
else
    echo -e "${GREEN}✓${NC} Certbot already installed"
fi

# Create application directories
echo ""
echo "Creating application directories..."
mkdir -p /opt/baiboly/deploy
mkdir -p /opt/baiboly/deploy/backups
mkdir -p /opt/baiboly/deploy/logs
mkdir -p /var/www/html/baiboly
echo -e "${GREEN}✓${NC} Directories created"

# Set permissions
echo ""
echo "Setting permissions..."
chown -R www-data:www-data /var/www/html/baiboly
chmod -R 755 /var/www/html/baiboly
echo -e "${GREEN}✓${NC} Permissions set"

# Configure firewall
echo ""
echo "Configuring firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 22/tcp   # SSH
    ufw allow 80/tcp   # HTTP
    ufw allow 443/tcp  # HTTPS
    ufw --force enable
    echo -e "${GREEN}✓${NC} Firewall configured"
else
    echo -e "${YELLOW}Warning: UFW not installed, skipping firewall configuration${NC}"
fi

# Create a deployment user (optional but recommended)
echo ""
read -p "Create a deployment user? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter username: " DEPLOY_USER
    if id "$DEPLOY_USER" &>/dev/null; then
        echo -e "${YELLOW}User $DEPLOY_USER already exists${NC}"
    else
        useradd -m -s /bin/bash "$DEPLOY_USER"
        usermod -aG docker "$DEPLOY_USER"
        echo -e "${GREEN}✓${NC} User $DEPLOY_USER created and added to docker group"
        
        # Set up SSH key
        echo ""
        echo "To enable SSH key authentication for CI/CD:"
        echo "1. On your local machine, generate SSH key (if not exists):"
        echo "   ssh-keygen -t ed25519 -C 'ci-cd-baiboly'"
        echo "2. Copy the public key to the server:"
        echo "   ssh-copy-id -i ~/.ssh/id_ed25519.pub $DEPLOY_USER@$(hostname -I | awk '{print $1}')"
        echo "3. Add the private key to GitHub Secrets as SSH_PRIVATE_KEY"
    fi
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Server Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy your application code to /opt/baiboly/"
echo "2. Copy Apache config: cp deploy/baiboly.conf /etc/apache2/sites-available/"
echo "3. Enable the site: sudo a2ensite baiboly.conf"
echo "4. Disable default site: sudo a2dissite 000-default.conf"
echo "5. Test Apache config: sudo apache2ctl configtest"
echo "6. Reload Apache: sudo systemctl reload apache2"
echo "7. Set up SSL: sudo certbot --apache -d yourdomain.com"
echo "8. Configure .env file in /opt/baiboly/deploy/"
echo "9. Run first deployment: cd /opt/baiboly/deploy && ./deploy-backend.sh"
echo ""
echo "Useful commands:"
echo "  Check Docker: docker --version"
echo "  Check Apache: apache2 -v"
echo "  Apache status: systemctl status apache2"
echo "  Docker status: systemctl status docker"
echo ""
