#!/usr/bin/env python3
"""
Configuration Supabase pour IPS-CO
"""

import os

# Configuration Supabase
SUPABASE_CONFIG = {
    'host': os.getenv('SUPABASE_URL', 'db.xxxxxxxxxxxxx.supabase.co'),  # À remplacer par votre host
    'database': 'postgres',
    'user': 'postgres',
    'password': os.getenv('SUPABASE_DB_PASSWORD', 'ipsco2025secure'),
    'port': '5432'
}

# Variables d'environnement pour Supabase
SUPABASE_ENV_VARS = {
    'SUPABASE_URL': 'db.xxxxxxxxxxxxx.supabase.co',  # Votre host Supabase
    'SUPABASE_DB_PASSWORD': 'ipsco2025secure',       # Votre mot de passe
    'SUPABASE_API_KEY': 'your-api-key-here',         # Votre clé API (optionnel)
    'SUPABASE_ANON_KEY': 'your-anon-key-here'       # Votre clé anonyme (optionnel)
}

# Instructions pour configurer
SETUP_INSTRUCTIONS = """
🚀 Configuration Supabase pour IPS-CO

1. Remplacez 'db.xxxxxxxxxxxxx.supabase.co' par votre vrai host Supabase
2. Vérifiez que le mot de passe est correct
3. Exécutez le script d'injection

Pour obtenir votre host Supabase :
1. Allez sur https://supabase.com
2. Connectez-vous à votre projet
3. Settings → Database → Connection string
4. Copiez la partie host (sans le port)
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
    print("\nConfiguration actuelle :")
    for key, value in SUPABASE_CONFIG.items():
        if key == 'password':
            print(f"{key}: {'*' * len(value)}")
        else:
            print(f"{key}: {value}")
