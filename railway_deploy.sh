#!/bin/bash

echo "🚀 Déploiement Railway - IPS-CO"
echo "=================================="

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur: manage.py non trouvé. Assurez-vous d'être dans le répertoire du projet Django."
    exit 1
fi

echo "✅ Projet Django détecté"

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "🗄️ Application des migrations..."
python manage.py migrate

# Créer un superutilisateur si nécessaire
echo "👤 Création du superutilisateur..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@ipsco.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo "✅ Déploiement Railway terminé avec succès!"
echo "🌐 Votre application sera disponible sur: https://ipsco-production.up.railway.app" 