#!/usr/bin/env python
"""
Script pour ajouter les véhicules de l'image à la base de données IPS-CO
"""
import os
import sys
import django
from datetime import datetime, date
from dateutil import parser

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from core.models import Vehicule, Etablissement, Utilisateur
from django.utils import timezone

def parse_french_date(date_str):
    """Parse les dates françaises du format '18 juin 2021'"""
    if not date_str or date_str.strip() == '':
        return None
    
    # Mapping des mois français
    mois_fr = {
        'janv': '01', 'févr': '02', 'mars': '03', 'avr': '04',
        'mai': '05', 'juin': '06', 'juil': '07', 'août': '08',
        'sept': '09', 'oct': '10', 'nov': '11', 'déc': '12'
    }
    
    try:
        # Nettoyer la chaîne
        date_str = date_str.strip()
        
        # Gérer les cas spéciaux
        if date_str in ['??', 'NON', '#VALEUR!']:
            return None
        
        # Parser la date française
        parts = date_str.split()
        if len(parts) == 3:
            jour = int(parts[0])
            mois_fr_abbr = parts[1]
            annee = int(parts[2])
            
            if mois_fr_abbr in mois_fr:
                mois = int(mois_fr[mois_fr_abbr])
                return date(annee, mois, jour)
        
        # Essayer de parser avec dateutil si le format français échoue
        return parser.parse(date_str, dayfirst=True).date()
    except:
        print(f"Impossible de parser la date: {date_str}")
        return None

def get_or_create_etablissement(nom):
    """Récupère ou crée un établissement"""
    etablissement, created = Etablissement.objects.get_or_create(
        nom=nom,
        defaults={
            'type': 'departement',
            'actif': True
        }
    )
    if created:
        print(f"✅ Établissement créé: {nom}")
    return etablissement

def get_or_create_admin_user():
    """Récupère ou crée un utilisateur admin pour être le créateur des véhicules"""
    try:
        # Essayer de récupérer un admin existant
        admin_user = Utilisateur.objects.filter(role='admin').first()
        if admin_user:
            return admin_user
        
        # Créer un admin par défaut si aucun n'existe
        admin_user = Utilisateur.objects.create_user(
            username='admin_vehicules',
            email='admin@ipsco.com',
            password='admin123456',
            first_name='Admin',
            last_name='Véhicules',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Utilisateur admin créé: {admin_user}")
        return admin_user
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'admin: {e}")
        return None

def add_vehicles_from_image():
    """Ajoute les véhicules de l'image à la base de données"""
    
    # Récupérer ou créer l'utilisateur admin
    admin_user = get_or_create_admin_user()
    if not admin_user:
        print("❌ Impossible de créer un utilisateur admin")
        return
    
    # Données des véhicules extraites de l'image
    vehicles_data = [
        {
            'marque': 'TOYOTA',
            'modele': 'PRADO',
            'immatriculation': '9133 AQ05',
            'statut_affectation': 'OB DG',
            'carte_rose': '18 juin 2021',
            'vignette': 'OK',
            'assurance_debut': '1 mars 2024',
            'assurance_fin': '1 mars 2025',
            'controle_technique_debut': '7 avr. 2025',
            'controle_technique_fin': '7 avr. 2026',
            'stationnement_debut': '17 oct. 2024',
            'stationnement_fin': '15 avr. 2025',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': 'NON',
            'entretien_fin': '#VALEUR!'
        },
        {
            'marque': 'TOYOTA',
            'modele': 'HILUX',
            'immatriculation': '0595 AV05',
            'statut_affectation': 'OB DG',
            'carte_rose': '',
            'vignette': 'OK',
            'assurance_debut': '2 mars 2024',
            'assurance_fin': '2 mars 2025',
            'controle_technique_debut': '7 avr. 2025',
            'controle_technique_fin': '7 avr. 2026',
            'stationnement_debut': '4 déc. 2024',
            'stationnement_fin': '2 juin 2025',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': 'NON',
            'entretien_fin': '#VALEUR!'
        },
        {
            'marque': 'TOYOTA',
            'modele': 'HILUX',
            'immatriculation': '3425 AT05',
            'statut_affectation': 'OB DG',
            'carte_rose': '??',
            'vignette': '',
            'assurance_debut': '3 mars 2024',
            'assurance_fin': '3 mars 2025',
            'controle_technique_debut': '4 mars 2022',
            'controle_technique_fin': '4 mars 2023',
            'stationnement_debut': '6 sept. 2024',
            'stationnement_fin': '5 mars 2025',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': 'NON',
            'entretien_fin': '#VALEUR!'
        },
        {
            'marque': 'MITSUBISHI',
            'modele': 'PAJERO',
            'immatriculation': '5791 AH05',
            'statut_affectation': 'OB DG',
            'carte_rose': '22 janv. 2016',
            'vignette': 'OK',
            'assurance_debut': '4 mars 2024',
            'assurance_fin': '4 mars 2025',
            'controle_technique_debut': '7 avr. 2025',
            'controle_technique_fin': '7 avr. 2026',
            'stationnement_debut': '28 juin 1900',
            'stationnement_fin': '',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': 'NON',
            'entretien_fin': '#VALEUR!'
        },
        {
            'marque': 'MITSUBISHI',
            'modele': 'FUSO',
            'immatriculation': '1815 AV05',
            'statut_affectation': 'OB DG',
            'carte_rose': '20 juin 2023',
            'vignette': 'OK',
            'assurance_debut': '1 janv. 2024',
            'assurance_fin': '31 déc. 2024',
            'controle_technique_debut': '7 avr. 2025',
            'controle_technique_fin': '7 avr. 2026',
            'stationnement_debut': '17 oct. 2024',
            'stationnement_fin': '15 avr. 2025',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': '1 janv. 2023',
            'entretien_fin': '1 janv. 2024'
        },
        {
            'marque': 'HYUNDAI',
            'modele': 'ELANTRA',
            'immatriculation': '4787 AS05',
            'statut_affectation': 'GM DG',
            'carte_rose': '4 nov. 2021',
            'vignette': 'OK',
            'assurance_debut': '1 janv. 2024',
            'assurance_fin': '31 déc. 2024',
            'controle_technique_debut': '7 avr. 2025',
            'controle_technique_fin': '7 avr. 2026',
            'stationnement_debut': '28 juin 1900',
            'stationnement_fin': '',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': 'NON',
            'entretien_fin': '#VALEUR!'
        },
        {
            'marque': 'TOYOTA',
            'modele': 'FORTUNER',
            'immatriculation': '',
            'statut_affectation': 'CB ASSOCIE',
            'carte_rose': '',
            'vignette': '',
            'assurance_debut': '1 janv. 2024',
            'assurance_fin': '31 déc. 2024',
            'controle_technique_debut': '5 sept. 2024',
            'controle_technique_fin': '5 sept. 2025',
            'stationnement_debut': '28 juin 1900',
            'stationnement_fin': '',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': 'NON',
            'entretien_fin': '#VALEUR!'
        },
        {
            'marque': 'TATA',
            'modele': 'BUS',
            'immatriculation': '6690 AB14',
            'statut_affectation': 'IPS-CO CREC07',
            'carte_rose': '10 mars 2023',
            'vignette': 'VJ',
            'assurance_debut': '1 janv. 2024',
            'assurance_fin': '31 déc. 2024',
            'controle_technique_debut': '13 janv. 2025',
            'controle_technique_fin': '13 janv. 2026',
            'stationnement_debut': '28 juin 1900',
            'stationnement_fin': '',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': '27 févr. 2024',
            'entretien_fin': '26 févr. 2025'
        },
        {
            'marque': 'TATA',
            'modele': 'BUS',
            'immatriculation': '6901 AB14',
            'statut_affectation': 'IPS-CO LSHI',
            'carte_rose': '10 mars 2023',
            'vignette': 'VJ',
            'assurance_debut': '1 janv. 2024',
            'assurance_fin': '31 déc. 2024',
            'controle_technique_debut': '13 janv. 2025',
            'controle_technique_fin': '13 janv. 2026',
            'stationnement_debut': '28 juin 1900',
            'stationnement_fin': '',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': '30 déc. 1900',
            'entretien_fin': ''
        },
        {
            'marque': 'TOYOTA',
            'modele': 'COASTER',
            'immatriculation': '7528 AB14',
            'statut_affectation': 'IPS-CO KAMOA',
            'carte_rose': '31 août 2023',
            'vignette': 'OK',
            'assurance_debut': '1 janv. 2024',
            'assurance_fin': '31 déc. 2024',
            'controle_technique_debut': '30 déc. 1900',
            'controle_technique_fin': '28 juin 1900',
            'stationnement_debut': '',
            'stationnement_fin': '',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': '30 déc. 1900',
            'entretien_fin': ''
        },
        {
            'marque': 'TOYOTA',
            'modele': 'HIACE',
            'immatriculation': '9326 AN05',
            'statut_affectation': 'IPS-CO KAMOA',
            'carte_rose': '21 août 2018',
            'vignette': 'VJ',
            'assurance_debut': '1 janv. 2024',
            'assurance_fin': '31 déc. 2024',
            'controle_technique_debut': '7 avr. 2025',
            'controle_technique_fin': '7 avr. 2026',
            'stationnement_debut': '28 juin 1900',
            'stationnement_fin': '',
            'autorisation_transport_debut': '1 janv. 2024',
            'autorisation_transport_fin': '31 déc. 2024',
            'entretien_debut': '30 déc. 1900',
            'entretien_fin': ''
        }
    ]
    
    vehicles_added = 0
    vehicles_skipped = 0
    
    for vehicle_data in vehicles_data:
        try:
            # Vérifier si le véhicule existe déjà
            if vehicle_data['immatriculation'] and Vehicule.objects.filter(immatriculation=vehicle_data['immatriculation']).exists():
                print(f"⚠️  Véhicule déjà existant: {vehicle_data['immatriculation']}")
                vehicles_skipped += 1
                continue
            
            # Créer l'établissement basé sur le statut d'affectation
            etablissement_nom = vehicle_data['statut_affectation']
            if etablissement_nom.startswith('IPS-CO'):
                etablissement_nom = 'IPS-CO'
            elif etablissement_nom in ['OB DG', 'GM DG']:
                etablissement_nom = 'Direction Générale'
            elif etablissement_nom == 'CB ASSOCIE':
                etablissement_nom = 'Cabinet Associé'
            
            etablissement = get_or_create_etablissement(etablissement_nom)
            
            # Parser les dates
            date_expiration_assurance = parse_french_date(vehicle_data['assurance_fin'])
            date_expiration_controle_technique = parse_french_date(vehicle_data['controle_technique_fin'])
            date_expiration_vignette = parse_french_date(vehicle_data['vignette_fin']) if 'vignette_fin' in vehicle_data else None
            date_expiration_stationnement = parse_french_date(vehicle_data['stationnement_fin'])
            date_immatriculation = parse_french_date(vehicle_data['carte_rose'])
            
            # Vérifier que les dates obligatoires sont présentes
            if not date_expiration_assurance or not date_expiration_controle_technique:
                print(f"⚠️  Dates manquantes pour {vehicle_data['immatriculation'] or 'Sans plaque'}")
                vehicles_skipped += 1
                continue
            
            # Créer le véhicule
            vehicule = Vehicule.objects.create(
                etablissement=etablissement,
                immatriculation=vehicle_data['immatriculation'] or f"TEMP_{vehicles_added + 1}",
                marque=vehicle_data['marque'],
                modele=vehicle_data['modele'],
                couleur='Non spécifiée',
                numero_chassis=f"CHASSIS_{vehicle_data['marque']}_{vehicle_data['modele']}_{vehicles_added + 1}",
                date_immatriculation=date_immatriculation,
                date_expiration_assurance=date_expiration_assurance,
                date_expiration_controle_technique=date_expiration_controle_technique,
                date_expiration_vignette=date_expiration_vignette or date_expiration_assurance,
                date_expiration_stationnement=date_expiration_stationnement or date_expiration_assurance,
                createur=admin_user,
                kilometrage_dernier_entretien=0,
                kilometrage_actuel=0
            )
            
            print(f"✅ Véhicule ajouté: {vehicule}")
            vehicles_added += 1
            
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout du véhicule {vehicle_data.get('immatriculation', 'Sans plaque')}: {e}")
            vehicles_skipped += 1
    
    print(f"\n📊 Résumé:")
    print(f"✅ Véhicules ajoutés: {vehicles_added}")
    print(f"⚠️  Véhicules ignorés: {vehicles_skipped}")
    print(f"📝 Total traité: {len(vehicles_data)}")

if __name__ == '__main__':
    print("🚗 Ajout des véhicules de l'image à la base de données IPS-CO")
    print("=" * 60)
    
    try:
        add_vehicles_from_image()
        print("\n✅ Script terminé avec succès!")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'exécution du script: {e}")
        import traceback
        traceback.print_exc()
