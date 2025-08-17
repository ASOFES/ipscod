#!/usr/bin/env bash
# Script de build personnalisé pour Render

echo "🚀 Démarrage du build IPSCO..."

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances système nécessaires
apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Build terminé avec succès!"
