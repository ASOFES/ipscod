#!/bin/bash

echo "🚀 Démarrage de l'application IPSCO..."

# Vérifier les variables d'environnement
echo "📋 Configuration:"
echo "  - SECRET_KEY: ${SECRET_KEY:-django-insecure-ipsco-deploy-2025-08-17-secret-key-for-production-deployment}"
echo "  - DEBUG: ${DEBUG:-False}"
echo "  - DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE:-gestion_vehicules.settings}"

# Attendre que la base de données soit prête (pour PostgreSQL)
if [ -n "$DATABASE_URL" ]; then
    echo "⏳ Attente de la base de données PostgreSQL..."
    # Attendre 30 secondes maximum
    for i in {1..30}; do
        if python manage.py check --database default 2>/dev/null; then
            echo "✅ Base de données PostgreSQL prête!"
            break
        fi
        echo "⏳ Tentative $i/30..."
        sleep 1
    done
fi

# Appliquer les migrations
echo "🔄 Application des migrations Django..."
python manage.py migrate --noinput

# Collecter les fichiers statiques si nécessaire
if [ ! -d "staticfiles" ]; then
    echo "📁 Collecte des fichiers statiques..."
    python manage.py collectstatic --noinput
fi

# Créer un superutilisateur par défaut si la base est vide
echo "👤 Vérification du superutilisateur..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Création du superutilisateur par défaut...')
    User.objects.create_superuser('admin', 'admin@ipsco.com', 'admin123')
    print('Superutilisateur créé: admin/admin123')
else:
    print('Superutilisateur existe déjà')
"

# Démarrer l'application
echo "🚀 Démarrage de Gunicorn..."
exec gunicorn gestion_vehicules.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
