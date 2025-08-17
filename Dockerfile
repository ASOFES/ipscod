FROM python:3.11-slim

# Définir les variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV SECRET_KEY=django-insecure-ipsco-deploy-2025-08-17-secret-key-for-production-deployment
ENV DEBUG=False
ENV DJANGO_SETTINGS_MODULE=gestion_vehicules.settings
ENV BUILD_TIMESTAMP=2025-08-17-21-32-migrations-fix

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

# Rendre le script de démarrage exécutable
RUN chmod +x start.sh

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Utiliser le script de démarrage
CMD ["./start.sh"] 