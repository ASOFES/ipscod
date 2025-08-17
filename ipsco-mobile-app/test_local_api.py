#!/usr/bin/env python3
"""
Test de l'API IPS-CO locale
"""
import requests
import json

def test_local_api():
    """Test de l'API locale"""
    base_url = "http://localhost:8000"
    
    print("🔍 Test de l'API IPS-CO locale...")
    print(f"📍 URL: {base_url}")
    
    # Test des endpoints API
    endpoints = [
        "/api/login/",
        "/api/verify-token/",
        "/api/chauffeur/missions/",
        "/api/demandeur/demandes/",
        "/api/dispatch/demandes/",
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Test de l'endpoint: {endpoint}")
        
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ Connexion réussie!")
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("📄 Réponse: OK")
            elif response.status_code == 401:
                print("📄 Réponse: Authentification requise (normal)")
            elif response.status_code == 405:
                print("📄 Réponse: Méthode non autorisée (normal pour GET sur POST endpoint)")
            else:
                print(f"📄 Réponse: {response.text[:100]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
        except Exception as e:
            print(f"❌ Erreur inconnue: {e}")
    
    print("\n🔍 Test terminé.")

if __name__ == "__main__":
    test_local_api()
