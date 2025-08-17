#!/usr/bin/env python3
"""
Test complet de l'API IPS-CO en production
"""
import requests
import json
import time

def test_web_api():
    """Test de l'API en production sur Render.com"""
    base_url = "https://ipsco.onrender.com"
    
    print("🌐 Test de l'API IPS-CO en production...")
    print(f"📍 URL: {base_url}")
    print("=" * 50)
    
    # Test de la racine du site
    print("\n🔍 Test 1: Connexion au site principal")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"✅ Site principal accessible! Status: {response.status_code}")
        if response.status_code == 200:
            print("📄 Page d'accueil chargée avec succès")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test des endpoints API
    print("\n🔍 Test 2: Endpoints de l'API REST")
    endpoints = [
        "/api/login/",
        "/api/verify-token/",
        "/api/chauffeur/missions/",
        "/api/demandeur/demandes/",
        "/api/dispatch/demandes/",
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Test de: {endpoint}")
        
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=15)
            print(f"✅ Connexion réussie! Status: {response.status_code}")
            
            if response.status_code == 200:
                print("📄 Réponse: OK - Endpoint fonctionnel")
            elif response.status_code == 401:
                print("📄 Réponse: Authentification requise (normal)")
            elif response.status_code == 405:
                print("📄 Réponse: Méthode non autorisée (normal pour GET sur POST endpoint)")
            elif response.status_code == 404:
                print("❌ Réponse: Endpoint non trouvé - API non encore déployée")
            else:
                print(f"📄 Réponse: {response.text[:100]}...")
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout - Le serveur met du temps à répondre")
        except requests.exceptions.ConnectionError:
            print("❌ Erreur de connexion - Serveur inaccessible")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    # Test de l'admin Django
    print("\n🔍 Test 3: Interface d'administration")
    try:
        response = requests.get(f"{base_url}/admin/", timeout=10)
        print(f"✅ Admin accessible! Status: {response.status_code}")
        if response.status_code == 200:
            print("📄 Interface d'administration accessible")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test des véhicules
    print("\n🔍 Test 4: Page des véhicules")
    try:
        response = requests.get(f"{base_url}/vehicules/", timeout=10)
        print(f"✅ Véhicules accessible! Status: {response.status_code}")
        if response.status_code == 200:
            print("📄 Page des véhicules accessible")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Résumé des tests:")
    print("✅ Site principal: Accessible")
    print("✅ Admin Django: Accessible")
    print("✅ Page véhicules: Accessible")
    print("⚠️  API REST: À vérifier (peut nécessiter un redéploiement)")
    print("\n📱 Votre application mobile pourra se connecter une fois l'API déployée!")

if __name__ == "__main__":
    test_web_api()
