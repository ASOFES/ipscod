#!/usr/bin/env python
import os
import django

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

# Importer le modèle utilisateur (peut être personnalisé dans ton projet)
from django.contrib.auth import get_user_model
User = get_user_model()

# Définir les informations du superutilisateur
username = 'admin'
email = 'admin@asofes.com'
password = 'AdminAsofes2024'  # Remplace par un mot de passe sécurisé en production

# Vérifie si un superutilisateur existe déjà
if not User.objects.filter(username=username).exists():
    print(f"Création du superutilisateur {username}...")
    User.objects.create_superuser(username, email, password)
    print(f"Superutilisateur {username} créé avec succès!")
    print(f"Email: {email}")
    print(f"Mot de passe: {password}")
    print("Conservez ces informations dans un endroit sûr.")
else:
    print(f"Un utilisateur avec le nom {username} existe déjà.")
    print("Aucune modification n'a été effectuée.")

print("\nVous pouvez maintenant vous connecter à l'interface d'administration:")
print("https://asofes.onrender.com/admin/")
