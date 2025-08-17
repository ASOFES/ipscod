FROM python:3.11-slim

# Définir les variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV SECRET_KEY=django-insecure-ipsco-deploy-2025-08-17-secret-key-for-production-deployment
ENV DEBUG=False
ENV DJANGO_SETTINGS_MODULE=gestion_vehicules.settings
ENV BUILD_TIMESTAMP=2025-08-17-21-24-force-rebuild

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le code de l'application
COPY . .

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Commande de démarrage avec variables d'environnement forcées
CMD ["sh", "-c", "echo 'Build timestamp: $BUILD_TIMESTAMP' && echo 'SECRET_KEY: $SECRET_KEY' && export SECRET_KEY=${SECRET_KEY:-django-insecure-ipsco-deploy-2025-08-17-secret-key-for-production-deployment} && export DEBUG=${DEBUG:-False} && gunicorn gestion_vehicules.wsgi:application --bind 0.0.0.0:8000"] 