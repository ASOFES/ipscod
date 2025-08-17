#!/usr/bin/env python
"""
Script pour configurer la base de données sur Render
Exécute les migrations et crée les objets nécessaires
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from core.models import ApplicationControl, Etablissement

def run_migrations():
    """Exécute les migrations Django"""
    print("🔄 Exécution des migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations exécutées avec succès")
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False
    return True

def create_default_etablissement():
    """Crée un établissement par défaut"""
    print("🏢 Création d'un établissement par défaut...")
    try:
        if Etablissement.objects.count() == 0:
            etablissement = Etablissement.objects.create(
                nom="Établissement Principal"
            )
            print(f"✅ Établissement créé: {etablissement}")
        else:
            print("✅ Établissement déjà existant")
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'établissement: {e}")

def create_application_control():
    """Crée l'objet ApplicationControl"""
    print("🔐 Création de l'ApplicationControl...")
    try:
        if ApplicationControl.objects.count() == 0:
            control = ApplicationControl.objects.create(
                is_open=True,
                start_datetime=django.utils.timezone.now(),
                end_datetime=django.utils.timezone.now() + django.utils.timezone.timedelta(days=365),
                message="Application ouverte par défaut"
            )
            print(f"✅ ApplicationControl créé: {control}")
        else:
            print("✅ ApplicationControl déjà existant")
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'ApplicationControl: {e}")

def create_superuser():
    """Crée un superutilisateur par défaut"""
    print("👑 Création d'un superutilisateur...")
    try:
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            # Créer un superutilisateur
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print(f"✅ Superutilisateur créé: {user.username}")
            print("🔑 Identifiants: admin / admin123")
        else:
            print("✅ Superutilisateur déjà existant")
    except Exception as e:
        print(f"❌ Erreur lors de la création du superutilisateur: {e}")

def main():
    """Fonction principale"""
    print("🚀 Configuration de la base de données sur Render")
    print("=" * 60)
    
    # Exécuter les migrations
    if not run_migrations():
        print("❌ Impossible de continuer sans migrations")
        return
    
    # Créer les objets nécessaires
    create_default_etablissement()
    create_application_control()
    create_superuser()
    
    print("\n🎯 Configuration terminée avec succès!")
    print("🌐 L'application devrait maintenant fonctionner sur Render")

if __name__ == '__main__':
    main()
