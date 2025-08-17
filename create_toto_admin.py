#!/usr/bin/env python
"""
Script de création d'un utilisateur admin 'toto'
Crée un utilisateur avec le rôle administrateur
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_toto_admin():
    """Crée un utilisateur admin 'toto' avec le rôle administrateur"""
    
    print("🔑 Création de l'utilisateur admin 'toto'...")
    
    try:
        User = get_user_model()
        
        # Vérifier si l'utilisateur 'toto' existe déjà
        try:
            toto_user = User.objects.get(username='toto')
            print("⚠️ L'utilisateur 'toto' existe déjà, mise à jour...")
            
            # Mettre à jour le mot de passe et les permissions
            toto_user.set_password('patrick22')
            toto_user.is_staff = True
            toto_user.is_superuser = True
            toto_user.is_active = True
            toto_user.role = 'admin'
            toto_user.save()
            
            print("✅ Utilisateur 'toto' mis à jour avec succès!")
            
        except User.DoesNotExist:
            print("👤 Création d'un nouvel utilisateur 'toto'...")
            
            # Créer un nouvel utilisateur admin
            toto_user = User.objects.create_user(
                username='toto',
                email='toto@ipsco.com',
                password='patrick22',
                first_name='Toto',
                last_name='Admin',
                role='admin',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            print("✅ Utilisateur 'toto' créé avec succès!")
        
        # Afficher les détails de l'utilisateur
        print(f"\n📋 Détails de l'utilisateur:")
        print(f"   Username: {toto_user.username}")
        print(f"   Email: {toto_user.email}")
        print(f"   Prénom: {toto_user.first_name}")
        print(f"   Nom: {toto_user.last_name}")
        print(f"   Rôle: {toto_user.role}")
        print(f"   Staff: {toto_user.is_staff}")
        print(f"   Superuser: {toto_user.is_superuser}")
        print(f"   Actif: {toto_user.is_active}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    success = create_toto_admin()
    if success:
        print("\n🚀 Utilisateur 'toto' prêt!")
        print("🔑 Connectez-vous avec: toto/patrick22")
    else:
        print("\n⚠️ Création échouée.")
