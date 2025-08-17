# 🚀 Guide de Déploiement de l'API IPS-CO

## 📋 Vue d'ensemble

Ce guide vous explique comment déployer l'API REST pour votre application mobile IPS-CO. L'API est maintenant configurée et prête à être déployée.

## 🔧 Configuration Actuelle

### ✅ Ce qui est déjà configuré :

1. **Endpoints API** dans `core/api.py`
2. **URLs API** dans `core/api_urls.py`
3. **Configuration Django REST Framework** dans `settings.py`
4. **Configuration CORS** pour l'application mobile
5. **Fichier requirements.txt** avec toutes les dépendances

### 📱 Endpoints disponibles :

- **`/api/login/`** - Authentification des utilisateurs
- **`/api/verify-token/`** - Vérification des tokens
- **`/api/chauffeur/missions/`** - Missions des chauffeurs
- **`/api/demandeur/demandes/`** - Demandes des demandeurs
- **`/api/dispatch/demandes/`** - Gestion des dispatchers

## 🚀 Étapes de Déploiement

### 1. **Installation des Dépendances**

```bash
# Installer les nouvelles dépendances
pip install -r requirements.txt
```

### 2. **Exécution des Migrations**

```bash
# Créer les migrations si nécessaire
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 3. **Test Local**

```bash
# Démarrer le serveur de développement
python manage.py runserver

# Tester l'API
python test_api.py
```

### 4. **Déploiement sur Render.com**

1. **Pousser les changements** vers votre dépôt GitHub
2. **Redéployer** automatiquement sur Render.com
3. **Vérifier** que l'API fonctionne en production

## 🧪 Test de l'API

### Test Local
```bash
python test_api.py
```

### Test en Production
```bash
python test_api.py
# L'API sera testée sur https://ipsco.onrender.com
```

## 📱 Configuration de l'Application Mobile

Votre application mobile Flutter est déjà configurée pour se connecter à :

```dart
// lib/utils/constants.dart
class ApiEndpoints {
  static const String baseUrl = 'https://ipsco.onrender.com';
  static const String apiBase = '$baseUrl/api';
  
  // Authentification
  static const String login = '$apiBase/login/';
  static const String refresh = '$apiBase/verify-token/';
  
  // Missions
  static const String missions = '$apiBase/chauffeur/missions/';
  // ... autres endpoints
}
```

## 🔐 Authentification

L'API utilise un système d'authentification simple avec des tokens au format :
```
{role}_{user_id}_{username}
```

Exemple : `chauffeur_123_john_doe`

### Headers requis :
```
Authorization: Bearer {token}
Content-Type: application/json
```

## 🌐 Configuration CORS

L'API accepte les requêtes depuis :
- ✅ `https://ipsco.onrender.com`
- ✅ `http://localhost:3000`
- ✅ `http://127.0.0.1:3000`

## 🐛 Résolution des Problèmes

### Erreur 404 sur les endpoints API
- Vérifiez que `path('api/', include('core.api_urls'))` est dans `gestion_vehicules/urls.py`
- Vérifiez que `rest_framework` est dans `INSTALLED_APPS`

### Erreur CORS
- Vérifiez que `corsheaders.middleware.CorsMiddleware` est dans `MIDDLEWARE`
- Vérifiez la configuration CORS dans `settings.py`

### Erreur d'importation
- Vérifiez que toutes les dépendances sont installées
- Exécutez `pip install -r requirements.txt`

## 📊 Monitoring

### Logs Django
- Les erreurs API sont loggées dans les logs Django
- Vérifiez les logs sur Render.com

### Test de Connexion
- Utilisez `test_api.py` pour vérifier la connectivité
- Testez chaque endpoint individuellement

## 🎯 Prochaines Étapes

1. **Déployer l'API** sur Render.com
2. **Tester la connexion** depuis l'application mobile
3. **Implémenter l'authentification JWT** (optionnel)
4. **Ajouter la validation** des données
5. **Implémenter les notifications** Firebase

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs Django
2. Testez l'API localement
3. Vérifiez la configuration des URLs
4. Consultez la documentation Django REST Framework

---

**🎉 Votre API IPS-CO est maintenant prête pour l'application mobile !**
