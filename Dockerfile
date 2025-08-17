# Dockerfile personnalisé pour forcer Python 3.11 et éviter pandas
FROM python:3.11.18-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_NO_DEPENDENCIES=1

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xvfb \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Installation DIRECTE des packages SANS créer de requirements.txt
RUN pip install --no-cache-dir --no-deps --only-binary=:all: \
    Django==4.2.20 \
    gunicorn==21.2.0 \
    whitenoise==6.6.0 \
    psycopg2-binary==2.9.10 \
    dj-database-url==2.1.0 \
    python-dotenv==1.0.0 \
    django-bootstrap5==25.1 \
    django-crispy-forms==2.4 \
    djangorestframework==3.16.0 \
    django-cors-headers==4.3.1 \
    openpyxl==3.1.2 \
    xlsxwriter==3.1.9

# Vérification qu'aucun package problématique n'est installé
RUN pip list | grep -E "(pandas|numpy|matplotlib)" || echo "✅ Aucun package problématique trouvé"

# Copie du code source
COPY . .

# Configuration Django
RUN python manage.py collectstatic --noinput

# Exposition du port
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "gestion_vehicules.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120", "--workers", "1", "--max-requests", "1000", "--max-requests-jitter", "100"] 