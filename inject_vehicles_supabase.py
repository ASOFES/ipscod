#!/usr/bin/env python3
"""
Script d'injection des véhicules dans Supabase
IPS-CO - Base de données des véhicules
"""

import os
import psycopg2
from datetime import date
from psycopg2.extras import RealDictCursor
import json

# Configuration Supabase
SUPABASE_CONFIG = {
    'host': 'db.xxxxxxxxxxxxx.supabase.co',  # À remplacer par votre host
    'database': 'postgres',
    'user': 'postgres',
    'password': 'ipsco2025secure',
    'port': '5432'
}

def parse_french_date(date_str):
    """Parse les dates françaises en objets date Python."""
    mois_fr = {
        'janv.': 1, 'févr.': 2, 'mars': 3, 'avr.': 4, 'mai': 5, 'juin': 6,
        'juil.': 7, 'août': 8, 'sept.': 9, 'oct.': 10, 'nov.': 11, 'déc.': 12
    }
    
    try:
        parts = date_str.split()
        jour = int(parts[0])
        mois = mois_fr.get(parts[1], 1)
        annee = int(parts[2])
        return date(annee, mois, jour)
    except:
        return date(2025, 12, 31)  # Date par défaut

def get_supabase_connection():
    """Établit la connexion à Supabase."""
    try:
        # Essayer d'abord les variables d'environnement
        host = os.getenv('SUPABASE_URL', SUPABASE_CONFIG['host'])
        password = os.getenv('SUPABASE_DB_PASSWORD', SUPABASE_CONFIG['password'])
        
        conn = psycopg2.connect(
            host=host,
            database=SUPABASE_CONFIG['database'],
            user=SUPABASE_CONFIG['user'],
            password=password,
            port=SUPABASE_CONFIG['port']
        )
        print("✅ Connexion à Supabase établie avec succès")
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à Supabase: {e}")
        return None

def create_tables_if_not_exist(conn):
    """Crée les tables nécessaires si elles n'existent pas."""
    try:
        cursor = conn.cursor()
        
        # Table Etablissement
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS core_etablissement (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                type VARCHAR(50) DEFAULT 'departement',
                code VARCHAR(20),
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Table Utilisateur
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS core_utilisateur (
                id SERIAL PRIMARY KEY,
                username VARCHAR(150) UNIQUE NOT NULL,
                email VARCHAR(254) UNIQUE NOT NULL,
                first_name VARCHAR(150),
                last_name VARCHAR(150),
                is_staff BOOLEAN DEFAULT FALSE,
                is_superuser BOOLEAN DEFAULT FALSE,
                date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Table Vehicule
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS core_vehicule (
                id SERIAL PRIMARY KEY,
                etablissement_id INTEGER REFERENCES core_etablissement(id),
                immatriculation VARCHAR(20) UNIQUE NOT NULL,
                marque VARCHAR(50) NOT NULL,
                modele VARCHAR(50) NOT NULL,
                couleur VARCHAR(30) DEFAULT 'Non spécifiée',
                numero_chassis VARCHAR(50) UNIQUE NOT NULL,
                image VARCHAR(255),
                date_immatriculation DATE,
                date_expiration_assurance DATE NOT NULL,
                date_expiration_controle_technique DATE NOT NULL,
                date_expiration_vignette DATE NOT NULL,
                date_expiration_stationnement DATE NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                createur_id INTEGER REFERENCES core_utilisateur(id),
                kilometrage_dernier_entretien INTEGER DEFAULT 0,
                kilometrage_actuel INTEGER DEFAULT 0
            );
        """)
        
        conn.commit()
        print("✅ Tables créées/vérifiées avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()

def inject_vehicles_to_supabase():
    """Injecte les véhicules dans Supabase."""
    
    # Données des véhicules
    vehicles_data = [
        {
            "marque": "TOYOTA",
            "modele": "PRADO JEEP",
            "immatriculation": "9133 AQ05",
            "statut_affectation": "OB DG",
            "carte_rose": "18 juin 2021",
            "assurance_fin": "1 mars 2025",
            "controle_technique_fin": "7 avr. 2026",
            "stationnement_fin": "15 avr. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "TOYOTA",
            "modele": "PRADO JEEP",
            "immatriculation": "0595 AV05",
            "statut_affectation": "GM DG",
            "carte_rose": "22 janv. 2016",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "4 mars 2023",
            "stationnement_fin": "31 déc. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "TOYOTA",
            "modele": "PRADO JEEP",
            "immatriculation": "0595 AV05-B",
            "statut_affectation": "CB ASSOCIE",
            "carte_rose": "22 janv. 2016",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "4 mars 2023",
            "stationnement_fin": "31 déc. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "MITSUBISHI",
            "modele": "FUSO CAMION",
            "immatriculation": "1815 AV05",
            "statut_affectation": "OB DG",
            "carte_rose": "20 juin 2023",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "7 avr. 2026",
            "stationnement_fin": "15 avr. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "MITSUBISHI",
            "modele": "FUSO CAMION",
            "immatriculation": "1815 AV05-B",
            "statut_affectation": "GM DG",
            "carte_rose": "20 juin 2023",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "7 avr. 2026",
            "stationnement_fin": "15 avr. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "HYUNDAI",
            "modele": "PICK-UP",
            "immatriculation": "0595 AV05-C",
            "statut_affectation": "IPS-CO CREC07",
            "carte_rose": "22 janv. 2016",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "4 mars 2023",
            "stationnement_fin": "31 déc. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "TATA",
            "modele": "BUS",
            "immatriculation": "6690 AB14",
            "statut_affectation": "IPS-CO CREC07",
            "carte_rose": "10 mars 2023",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "13 janv. 2026",
            "stationnement_fin": "31 déc. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "TATA",
            "modele": "MINI BUS",
            "immatriculation": "6690 AB14-B",
            "statut_affectation": "IPS-CO LSHI",
            "carte_rose": "10 mars 2023",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "13 janv. 2026",
            "stationnement_fin": "31 déc. 2025",
            "vignette_fin": "31 déc. 2025"
        },
        {
            "marque": "TATA",
            "modele": "MINI BUS",
            "immatriculation": "6690 AB14-C",
            "statut_affectation": "IPS-CO KAMOA",
            "carte_rose": "10 mars 2023",
            "assurance_fin": "31 déc. 2024",
            "controle_technique_fin": "13 janv. 2026",
            "stationnement_fin": "31 déc. 2025",
            "vignette_fin": "31 déc. 2025"
        }
    ]
    
    # Connexion à Supabase
    conn = get_supabase_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Créer les tables si nécessaire
        create_tables_if_not_exist(conn)
        
        # Créer l'établissement IPS-CO
        cursor.execute("""
            INSERT INTO core_etablissement (nom, type, code)
            VALUES ('IPS-CO', 'departement', 'IPS')
            ON CONFLICT (nom) DO NOTHING
            RETURNING id;
        """)
        
        etablissement_result = cursor.fetchone()
        if etablissement_result:
            etablissement_id = etablissement_result[0]
        else:
            cursor.execute("SELECT id FROM core_etablissement WHERE nom = 'IPS-CO';")
            etablissement_id = cursor.fetchone()[0]
        
        print(f"🏢 Établissement IPS-CO créé/récupéré avec l'ID: {etablissement_id}")
        
        # Créer un utilisateur admin par défaut
        cursor.execute("""
            INSERT INTO core_utilisateur (username, email, first_name, last_name, is_staff, is_superuser)
            VALUES ('admin', 'admin@ipsco.com', 'Admin', 'IPS-CO', TRUE, TRUE)
            ON CONFLICT (username) DO NOTHING
            RETURNING id;
        """)
        
        admin_result = cursor.fetchone()
        if admin_result:
            admin_id = admin_result[0]
        else:
            cursor.execute("SELECT id FROM core_utilisateur WHERE username = 'admin';")
            admin_id = cursor.fetchone()[0]
        
        print(f"👤 Utilisateur admin créé/récupéré avec l'ID: {admin_id}")
        
        # Injecter les véhicules
        vehicles_added = 0
        for i, vehicle_data in enumerate(vehicles_data, 1):
            try:
                # Vérifier si le véhicule existe déjà
                cursor.execute("""
                    SELECT id FROM core_vehicule WHERE immatriculation = %s;
                """, (vehicle_data['immatriculation'],))
                
                if cursor.fetchone():
                    print(f"⚠️  Véhicule {vehicle_data['immatriculation']} existe déjà, ignoré.")
                    continue
                
                # Parser les dates
                carte_rose = parse_french_date(vehicle_data['carte_rose'])
                assurance_fin = parse_french_date(vehicle_data['assurance_fin'])
                controle_fin = parse_french_date(vehicle_data['controle_technique_fin'])
                vignette_fin = parse_french_date(vehicle_data['vignette_fin'])
                stationnement_fin = parse_french_date(vehicle_data['stationnement_fin'])
                
                # Insérer le véhicule
                cursor.execute("""
                    INSERT INTO core_vehicule (
                        etablissement_id, immatriculation, marque, modele, couleur,
                        numero_chassis, date_immatriculation, date_expiration_assurance,
                        date_expiration_controle_technique, date_expiration_vignette,
                        date_expiration_stationnement, createur_id, kilometrage_dernier_entretien,
                        kilometrage_actuel
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    etablissement_id,
                    vehicle_data['immatriculation'],
                    vehicle_data['marque'],
                    vehicle_data['modele'],
                    'Non spécifiée',
                    f"CHASSIS_{vehicle_data['immatriculation'].replace(' ', '').replace('-', '')}",
                    carte_rose,
                    assurance_fin,
                    controle_fin,
                    vignette_fin,
                    stationnement_fin,
                    admin_id,
                    0,  # kilometrage_dernier_entretien
                    0   # kilometrage_actuel
                ))
                
                vehicles_added += 1
                print(f"✅ Véhicule {i}: {vehicle_data['marque']} {vehicle_data['modele']} - {vehicle_data['immatriculation']} ajouté")
                
            except Exception as e:
                print(f"❌ Erreur lors de l'ajout du véhicule {i}: {e}")
        
        conn.commit()
        print(f"\n🎉 {vehicles_added} véhicules ajoutés avec succès dans Supabase !")
        
        # Vérifier le total
        cursor.execute("SELECT COUNT(*) FROM core_vehicule;")
        total_vehicles = cursor.fetchone()[0]
        print(f"📊 Total des véhicules dans la base : {total_vehicles}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'injection des véhicules: {e}")
        conn.rollback()
        return False
    
    finally:
        if conn:
            conn.close()
            print("🔌 Connexion à Supabase fermée")

if __name__ == "__main__":
    print("🚗 Injection des véhicules IPS-CO dans Supabase")
    print("=" * 50)
    
    # Demander confirmation
    response = input("Voulez-vous continuer avec l'injection des véhicules ? (y/N): ")
    if response.lower() in ['y', 'yes', 'oui']:
        success = inject_vehicles_to_supabase()
        if success:
            print("\n🎯 Injection terminée avec succès !")
        else:
            print("\n💥 Échec de l'injection")
    else:
        print("❌ Injection annulée")
