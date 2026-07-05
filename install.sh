#!/usr/bin/env bash

set -e

REPO_URL="https://github.com/Bgalea/coding-agent-bootstrap.git"
DEFAULT_INSTALL_DIR="$HOME/.gemini/config/skills/coding-agent-bootstrap"

echo "=================================================="
echo "    CODING AGENT BOOTSTRAP SKILL INSTALLER       "
echo "=================================================="

# Let user customize install directory
read -p "Install directory [default: $DEFAULT_INSTALL_DIR]: " INSTALL_DIR
INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"

# Create parent directories
mkdir -p "$(dirname "$INSTALL_DIR")"

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
    echo "Skill already installed in $INSTALL_DIR. Updating..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "Cloning repository..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Make scripts executable
echo "Configuring permissions..."
chmod +x scripts/bootstrap.py
chmod +x scripts/fetch_rules.py

echo "=================================================="
echo "          INSTALLATION COMPLETED!                 "
echo "=================================================="
echo "Skill installed in: $INSTALL_DIR"
echo ""
echo "To use this skill in your workspace, ask your agent:"
echo "\"Je veux démarrer un nouveau projet. Utilise le skill coding-agent-bootstrap.\""
echo "=================================================="
