#!/usr/bin/env python
"""
Script de déploiement sur Render et test des vues de département
"""

import os
import subprocess
import sys
import time
import requests

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    print(f"Commande: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} réussi")
        if result.stdout:
            print("Sortie:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} échoué")
        print("Erreur:", e.stderr)
        return False

def check_git_status():
    """Vérifie le statut Git et commit les changements si nécessaire"""
    print("\n📋 Vérification du statut Git...")
    
    # Vérifier s'il y a des changements
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    
    if result.stdout.strip():
        print("📝 Changements détectés, commit en cours...")
        
        # Ajouter tous les fichiers
        if not run_command("git add .", "Ajout des fichiers"):
            return False
        
        # Commit des changements
        if not run_command('git commit -m "Ajout des vues de département manquantes"', "Commit des changements"):
            return False
        
        print("✅ Changements commités")
    else:
        print("✅ Aucun changement à commiter")
    
    return True

def push_to_render():
    """Pousse les changements vers Render"""
    print("\n🚀 Déploiement sur Render...")
    
    # Pousser vers le remote principal
    if not run_command("git push", "Push vers le remote principal"):
        return False
    
    print("✅ Code poussé vers Render")
    print("⏳ Déploiement en cours... (peut prendre 5-10 minutes)")
    
    return True

def test_departement_views():
    """Test des vues de département après déploiement"""
    print("\n🧪 Test des vues de département après déploiement...")
    
    # URL de base de l'application sur Render
    base_url = "https://ipsco.onrender.com"
    
    # URLs à tester
    urls_to_test = [
        "/departements/",
        "/departements/create/",
    ]
    
    print("⏳ Attente de 2 minutes pour que le déploiement se termine...")
    time.sleep(120)
    
    for url in urls_to_test:
        full_url = base_url + url
        print(f"\n🔍 Test de {full_url}")
        
        try:
            response = requests.get(full_url, timeout=30)
            if response.status_code == 200:
                print(f"✅ {url} - OK (200)")
            elif response.status_code == 302:  # Redirection vers login
                print(f"⚠️ {url} - Redirection (302) - probablement vers login")
            else:
                print(f"❌ {url} - Erreur ({response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} - Erreur de connexion: {e}")
    
    print("\n🎯 Test de la page de création de département...")
    try:
        response = requests.get(f"{base_url}/departements/create/", timeout=30)
        if response.status_code == 200:
            print("✅ Page de création accessible")
            if "Créer un Département" in response.text:
                print("✅ Contenu de la page correct")
            else:
                print("⚠️ Contenu de la page incorrect")
        else:
            print(f"❌ Page de création non accessible ({response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors du test de la page de création: {e}")

def main():
    """Fonction principale"""
    print("🚀 Script de déploiement et test des vues de département")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("manage.py"):
        print("❌ Erreur: Ce script doit être exécuté depuis le répertoire racine du projet Django")
        sys.exit(1)
    
    # Vérifier le statut Git
    if not check_git_status():
        print("❌ Échec de la vérification Git")
        sys.exit(1)
    
    # Demander confirmation pour le déploiement
    print("\n⚠️ ATTENTION: Ce script va déployer l'application sur Render.")
    response = input("Voulez-vous continuer ? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Déploiement annulé")
        sys.exit(0)
    
    # Déployer sur Render
    if not push_to_render():
        print("❌ Échec du déploiement")
        sys.exit(1)
    
    # Tester les vues après déploiement
    test_departement_views()
    
    print("\n🎉 Déploiement et tests terminés !")
    print("📱 Votre application est disponible sur: https://ipsco.onrender.com")

if __name__ == '__main__':
    main()
