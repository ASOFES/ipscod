# IPS-CO - Gestion de Parc Automobile

## 📋 Description

IPS-CO (International People Solutions) est une application web Django complète pour la gestion de parc automobile. Elle permet de gérer les véhicules, les chauffeurs, les missions, les entretiens, les ravitaillements et les rapports de manière centralisée.

## 🚀 Fonctionnalités principales

### 👥 Gestion des utilisateurs
- **Demandeurs** : Création et suivi des demandes de transport
- **Chauffeurs** : Gestion des missions et rapports de conduite
- **Dispatchers** : Attribution des missions et suivi des courses
- **Administrateurs** : Gestion complète du système

### 🚗 Gestion des véhicules
- Enregistrement des véhicules avec photos
- Suivi du kilométrage
- Historique des entretiens
- Gestion des documents

### 📋 Missions et courses
- Création de demandes de transport
- Attribution automatique des chauffeurs et véhicules
- Suivi en temps réel des missions
- Rapports détaillés

### 🔧 Entretien et maintenance
- Planification des entretiens
- Suivi des coûts
- Historique complet
- Alertes de maintenance

### ⛽ Ravitaillement
- Enregistrement des ravitaillements
- Calcul des consommations
- Rapports de carburant
- Optimisation des coûts

### 📊 Rapports avancés
- Rapports de chauffeurs avec scoring
- Rapports de véhicules avec classification
- Rapports de missions avec évaluation
- Rapports de carburant détaillés
- Export PDF et Excel

### 🔒 Sécurité
- Checklists de sécurité
- Suivi des incidents
- Notifications push
- Contrôle d'accès

## 🛠️ Technologies utilisées

- **Backend** : Django 4.2.23
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap
- **PDF** : xhtml2pdf, WeasyPrint
- **Excel** : xlwt, openpyxl
- **Notifications** : Service Workers, Push API
- **Charts** : Chart.js

## 📦 Installation

### Prérequis
- Python 3.9+
- pip
- Git

### Installation locale

1. **Cloner le repository**
```bash
git clone <url-du-repo>
cd mamo1
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : http://127.0.0.1:8000/

## 🏗️ Structure du projet

```
mamo1/
├── core/                    # Application principale
├── chauffeur/              # Gestion des chauffeurs
├── demandeur/              # Gestion des demandeurs
├── dispatch/               # Gestion des dispatchers
├── entretien/              # Gestion des entretiens
├── rapport/                # Rapports et analyses
├── ravitaillement/         # Gestion du carburant
├── securite/               # Sécurité et checklists
├── suivi/                  # Suivi des véhicules
├── notifications/          # Système de notifications
├── gestion_vehicules/      # Configuration Django
├── static/                 # Fichiers statiques
├── media/                  # Fichiers uploadés
└── templates/              # Templates HTML
```

## 👤 Utilisateurs par défaut

Après l'installation, vous pouvez utiliser :
- **Utilisateur** : `toto`
- **Mot de passe** : `admin123`

## 📱 Modules principaux

### 🚗 Gestion des véhicules
- Ajout/modification/suppression de véhicules
- Upload de photos
- Suivi du kilométrage
- Historique complet

### 👨‍💼 Gestion des chauffeurs
- Profils détaillés
- Missions assignées
- Rapports de conduite
- Évaluations

### 📋 Demandes de transport
- Création de demandes
- Attribution automatique
- Suivi des statuts
- Notifications

### 🔧 Entretien
- Planification
- Coûts
- Historique
- Alertes

### ⛽ Ravitaillement
- Enregistrement
- Calculs
- Rapports
- Optimisation

### 📊 Rapports
- Chauffeurs (scoring avancé)
- Véhicules (classification)
- Missions (évaluation)
- Carburant (détails)

## 🔧 Configuration

### Variables d'environnement
Créez un fichier `.env` à la racine du projet :

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Base de données
Le projet utilise SQLite par défaut. Pour PostgreSQL :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Déploiement

### Production avec Gunicorn

1. **Installer Gunicorn**
```bash
pip install gunicorn
```

2. **Configurer le serveur**
```bash
gunicorn gestion_vehicules.wsgi:application --bind 0.0.0.0:8000
```

### Docker (optionnel)

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "gestion_vehicules.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📈 Fonctionnalités avancées

### 🎯 Système de scoring
- **Chauffeurs** : Productivité, Efficacité énergétique, Rentabilité, Régularité
- **Véhicules** : Fiabilité, Efficacité énergétique, Rentabilité, Utilisation
- **Missions** : Ponctualité, Efficacité, Rentabilité, Qualité

### 📊 Rapports interactifs
- Graphiques Chart.js
- Filtres avancés
- Export PDF/Excel
- Tableaux de bord

### 🔔 Notifications
- Push notifications
- Notifications en temps réel
- Emails automatiques
- Alertes système

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Toto Mulumba** - Développeur Full Stack

## 🙏 Remerciements

- Django Framework
- Bootstrap pour l'interface
- Chart.js pour les graphiques
- Tous les contributeurs

---

**IPS-CO - International People Solutions**  
*Gestion de Parc Automobile Professionnelle* 