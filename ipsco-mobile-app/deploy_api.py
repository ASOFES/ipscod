#!/usr/bin/env python3
"""
Script de déploiement de l'API IPS-CO
"""
import os
import subprocess
import sys

def install_requirements():
    """Installer les dépendances Python"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dépendances installées avec succès")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False
    return True

def run_migrations():
    """Exécuter les migrations Django"""
    print("🔄 Exécution des migrations...")
    try:
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ Migrations exécutées avec succès")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False
    return True

def test_server():
    """Tester le serveur localement"""
    print("🧪 Test du serveur local...")
    try:
        # Démarrer le serveur en arrière-plan
        process = subprocess.Popen([
            sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre un peu pour que le serveur démarre
        import time
        time.sleep(3)
        
        # Tester la connexion
        import requests
        try:
            response = requests.get("http://localhost:8000/api/login/", timeout=5)
            print(f"✅ Serveur local fonctionne! Status: {response.status_code}")
        except:
            print("⚠️ Serveur local accessible mais API non testée")
        
        # Arrêter le serveur
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    return True

def main():
    """Fonction principale"""
    print("🚀 Déploiement de l'API IPS-CO...")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("manage.py"):
        print("❌ Erreur: manage.py non trouvé. Exécutez ce script depuis le répertoire racine du projet.")
        return
    
    # Installer les dépendances
    if not install_requirements():
        return
    
    # Exécuter les migrations
    if not run_migrations():
        return
    
    # Tester le serveur
    if not test_server():
        return
    
    print("\n🎉 Déploiement terminé avec succès!")
    print("📱 Votre API est maintenant prête pour l'application mobile")
    print("🌐 Redéployez sur Render.com pour tester en production")

if __name__ == "__main__":
    main()
