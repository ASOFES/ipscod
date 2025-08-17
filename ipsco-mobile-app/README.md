# 🚗 IPS-CO Mobile App

## 📱 Application Mobile Flutter pour IPS-CO

### 🎯 Modules Disponibles

#### 1. **Chauffeur** 🚙
- **Voir les courses assignées**
- **Démarrer une course** (kilométrage avant)
- **Terminer une course** (kilométrage après)
- **Historique des courses**
- **Gestion de session**

#### 2. **Dispatcher** 📋
- **Voir les demandes de missions**
- **Assigner les missions aux chauffeurs**
- **Historique d'assignation**
- **Suivi des courses**

#### 3. **Demandeur de Mission** 📝
- **Nouvelle demande de mission**
- **Historique des demandes**
- **Suivi du statut**

### 🔧 Technologies Utilisées

- **Frontend** : Flutter (Dart)
- **Backend** : Django REST API (IPS-CO)
- **Authentification** : JWT Token
- **Notifications** : Push Notifications
- **Base de données** : SQLite (local) + API REST

### 📱 Fonctionnalités

- ✅ **Authentification par rôle**
- ✅ **Interface adaptée au rôle**
- ✅ **Notifications en temps réel**
- ✅ **Mode hors ligne**
- ✅ **Synchronisation automatique**
- ✅ **Gestion des sessions**

### 🚀 Installation

```bash
# Installer Flutter
flutter doctor

# Cloner le projet
git clone [URL_DU_REPO]

# Installer les dépendances
flutter pub get

# Lancer l'application
flutter run
```

### 📊 Architecture

```
ipsco-mobile-app/
├── lib/
│   ├── main.dart
│   ├── models/
│   ├── services/
│   ├── screens/
│   ├── widgets/
│   └── utils/
├── assets/
├── android/
├── ios/
└── pubspec.yaml
```

### 🔐 Configuration

1. **URL de l'API** : Modifier `lib/config/api_config.dart`
2. **Clés de notification** : Configurer dans `android/app/` et `ios/Runner/`
3. **Variables d'environnement** : Créer `.env` file

---

*Application mobile IPS-CO - Gestion des véhicules et missions*
