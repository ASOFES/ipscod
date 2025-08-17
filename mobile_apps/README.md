# Application Demandeur - IPS-CO

## 📱 Vue d'ensemble

Application mobile Flutter pour les demandeurs de courses de transport. Permet aux utilisateurs de demander des courses, suivre leur statut en temps réel, et gérer leur profil.

## 🚀 Fonctionnalités principales

### 🔐 Authentification
- Connexion avec email/mot de passe
- Inscription avec validation des données
- Authentification biométrique (optionnelle)
- Récupération de mot de passe

### 📍 Gestion des courses
- Création de nouvelles demandes de course
- Sélection du point de départ et destination
- Choix du type de véhicule
- Estimation des prix en temps réel
- Historique des courses

### 📊 Suivi en temps réel
- Statut de la course (en attente, acceptée, en cours, terminée)
- Localisation du chauffeur
- Temps d'arrivée estimé
- Notifications push

### 👤 Profil utilisateur
- Gestion des informations personnelles
- Adresses favorites
- Méthodes de paiement
- Historique des courses
- Évaluations et commentaires

## 🛠 Technologies utilisées

- **Framework**: Flutter 3.19+
- **Langage**: Dart 3.3+
- **Gestion d'état**: Riverpod
- **Navigation**: GoRouter
- **HTTP Client**: Dio + Retrofit
- **Stockage local**: Hive + SharedPreferences
- **Authentification**: Local Auth
- **Notifications**: Firebase Messaging
- **Géolocalisation**: Geolocator + Geocoding

## 📁 Structure du projet

```
lib/
├── core/                    # Services et utilitaires
│   ├── router/             # Configuration des routes
│   ├── services/           # Services (notifications, API)
│   └── utils/              # Utilitaires
├── features/               # Fonctionnalités par module
│   ├── auth/              # Authentification
│   ├── courses/           # Gestion des courses
│   └── profile/           # Profil utilisateur
├── shared/                 # Composants partagés
│   ├── themes/            # Thèmes et styles
│   ├── widgets/           # Widgets réutilisables
│   └── constants/         # Constantes
└── main.dart              # Point d'entrée
```

## 🔧 Configuration requise

### Prérequis
- Flutter SDK 3.19+
- Dart SDK 3.3+
- Android Studio / VS Code
- Émulateur Android ou appareil physique

### Dépendances système
- Android API 21+ (Android 5.0+)
- iOS 12.0+

## 📦 Installation

1. **Cloner le projet**
```bash
git clone [URL_DU_REPO]
cd mobile_apps/demandeur_app
```

2. **Installer les dépendances**
```bash
flutter pub get
```

3. **Configuration Firebase** (optionnel)
```bash
# Ajouter google-services.json (Android)
# Ajouter GoogleService-Info.plist (iOS)
```

4. **Lancer l'application**
```bash
flutter run
```

## 🌐 Configuration API

L'application se connecte aux APIs Django déployées sur Render :

- **Base URL**: `https://[VOTRE_APP].onrender.com`
- **Authentification**: JWT Token
- **Format**: JSON REST API

### Endpoints principaux
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/register/` - Inscription
- `GET /api/courses/` - Liste des courses
- `POST /api/courses/` - Créer une course
- `GET /api/courses/{id}/` - Détails d'une course

## 🎨 Thèmes et personnalisation

L'application utilise Material 3 avec des thèmes personnalisés :

- **Thème clair** : Couleurs vives et contrastées
- **Thème sombre** : Palette sombre élégante
- **Couleurs primaires** : Bleu IPS-CO
- **Couleurs d'accent** : Orange et vert

## 📱 Fonctionnalités avancées

### 🔔 Notifications
- Notifications push pour les mises à jour de course
- Notifications locales pour les actions utilisateur
- Gestion des permissions (Android/iOS)

### 📍 Géolocalisation
- Détection automatique de la position
- Recherche d'adresses avec autocomplétion
- Calcul des distances et temps de trajet

### 🔒 Sécurité
- Stockage sécurisé des tokens
- Chiffrement des données sensibles
- Authentification biométrique

## 🧪 Tests

```bash
# Tests unitaires
flutter test

# Tests d'intégration
flutter test integration_test/

# Tests de widgets
flutter test test/widget_test.dart
```

## 📦 Build et déploiement

### Build de développement
```bash
flutter build apk --debug
flutter build ios --debug
```

### Build de production
```bash
flutter build apk --release
flutter build appbundle --release
flutter build ios --release
```

### Génération de l'APK
```bash
# APK complet
flutter build apk --release

# APK divisé par architecture
flutter build apk --split-per-abi --release
```

## 🚀 Déploiement

### Google Play Store
1. Générer un APK signé
2. Créer une version dans la console Google Play
3. Télécharger l'APK
4. Publier en production

### App Store (iOS)
1. Build iOS avec Xcode
2. Archive et upload via Xcode
3. Validation et publication

## 📊 Métriques et analytics

- **Firebase Analytics** : Suivi des utilisateurs
- **Crashlytics** : Rapport d'erreurs
- **Performance Monitoring** : Métriques de performance

## 🔧 Développement

### Code generation
```bash
# Générer le code Riverpod
flutter packages pub run build_runner build

# Générer le code Retrofit
flutter packages pub run build_runner build --delete-conflicting-outputs
```

### Linting
```bash
# Vérifier le code
flutter analyze

# Corriger automatiquement
dart fix --apply
```

## 📚 Documentation

- [Documentation Flutter](https://docs.flutter.dev/)
- [Documentation Riverpod](https://riverpod.dev/)
- [Documentation GoRouter](https://pub.dev/packages/go_router)
- [Documentation Firebase](https://firebase.flutter.dev/)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence [LICENCE_À_DÉFINIR]

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Contacter l'équipe de développement
- Consulter la documentation

---

**Version**: 1.0.0  
**Dernière mise à jour**: Décembre 2024  
**Équipe**: IPS-CO Development Team
