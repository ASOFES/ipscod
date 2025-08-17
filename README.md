# IPSCO - Système de Gestion de Véhicules

## Description

IPSCO est une application Django complète pour la gestion de flotte de véhicules, incluant :
- Gestion des chauffeurs et missions
- Suivi des demandes de transport
- Gestion de l'entretien des véhicules
- Rapports et statistiques
- Applications mobiles Flutter
- Système de notifications

## 🚀 Déploiement sur Render

### Prérequis
- Compte Render.com
- Repository GitHub connecté

### Étapes de déploiement

1. **Connecter le repository GitHub**
   - Allez sur [Render.com](https://render.com)
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre compte GitHub
   - Sélectionnez le repository `ASOFES/ipscod`

2. **Configuration automatique**
   - Le fichier `render.yaml` configure automatiquement :
     - Service web Python
     - Base de données PostgreSQL
     - Variables d'environnement

3. **Variables d'environnement**
   - `DATABASE_URL` : Configurée automatiquement
   - `SECRET_KEY` : Générée automatiquement
   - `DEBUG` : `false` en production
   - `ALLOWED_HOSTS` : `.onrender.com`

4. **Déploiement**
   - Render détecte automatiquement la configuration
   - Le build se fait avec `pip install -r requirements.txt`
   - L'application démarre avec `gunicorn gestion_vehicules.wsgi:application`

## 🏗️ Structure du projet

```
ipsco-deploy-clean/
├── gestion_vehicules/          # Configuration Django principale
├── core/                       # Modèles et vues principales
├── chauffeur/                  # Gestion des chauffeurs
├── demandeur/                  # Demandes de transport
├── dispatch/                   # Dispatch des missions
├── entretien/                  # Gestion de l'entretien
├── ravitaillement/             # Suivi du carburant
├── rapport/                    # Génération de rapports
├── securite/                   # Sécurité et checklists
├── notifications/              # Système de notifications
├── mobile_apps/                # Applications Flutter
├── static/                     # Fichiers statiques
└── media/                      # Fichiers uploadés
```

## 🛠️ Technologies utilisées

- **Backend** : Django 4.2.7
- **Base de données** : PostgreSQL
- **Serveur** : Gunicorn
- **Frontend** : HTML/CSS/JavaScript
- **Mobile** : Flutter
- **Déploiement** : Render.com

## 📱 Applications mobiles

Le projet inclut plusieurs applications Flutter :
- `ipsco-mobile-app/` : Application principale
- `ipsco_test_web/` : Application de test
- `mobile_apps/demandeur_app_new/` : Application demandeur

## 🔧 Configuration locale

1. **Cloner le repository**
   ```bash
   git clone https://github.com/ASOFES/ipscod.git
   cd ipscod
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer la base de données**
   - Créer une base PostgreSQL
   - Configurer `DATABASE_URL` dans `.env`

4. **Lancer l'application**
   ```bash
   python manage.py runserver
   ```

## 📊 Fonctionnalités principales

- **Gestion des véhicules** : Suivi, entretien, kilométrage
- **Gestion des chauffeurs** : Missions, rapports, évaluations
- **Demandes de transport** : Création, suivi, dispatch
- **Rapports** : Statistiques, exports PDF, analyses
- **Sécurité** : Checklists, contrôles, historique
- **Notifications** : Système de rappels et alertes

## 🌐 Déploiement

L'application est configurée pour un déploiement automatique sur Render avec :
- Configuration PostgreSQL automatique
- Variables d'environnement sécurisées
- Build et déploiement automatisés
- Monitoring et logs intégrés

## 📞 Support

Pour toute question ou problème :
- Créez une issue sur GitHub
- Consultez la documentation des applications mobiles
- Vérifiez les logs de déploiement sur Render

---

**IPSCO** - Système de gestion de flotte professionnel 