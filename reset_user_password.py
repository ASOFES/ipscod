import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'toto'
password = 'patrick22'

user, created = User.objects.get_or_create(username=username)
user.set_password(password)
user.is_active = True
user.save()

if created:
    print(f"Utilisateur '{username}' créé avec succès et mot de passe réinitialisé.")
else:
    print(f"Mot de passe de l'utilisateur '{username}' réinitialisé avec succès.") 