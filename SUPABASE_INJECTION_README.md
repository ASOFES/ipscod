# 🚗 Injection Directe des Véhicules dans Supabase

## 📅 Date de Création
**14 Août 2025**

## 🎯 Objectif
Injecter directement les **9 véhicules IPS-CO** dans votre base de données Supabase, sans passer par Git.

## 🚀 Avantages de l'Injection Directe

- ✅ **Plus rapide** que le déploiement Git
- ✅ **Contrôle total** sur la base de données
- ✅ **Pas de conflits** de déploiement
- ✅ **Mise à jour immédiate** de la base
- ✅ **Facile à déboguer** et modifier

## 📋 Prérequis

### 1. **Base de données Supabase active**
- Projet créé sur [supabase.com](https://supabase.com)
- Informations de connexion disponibles

### 2. **Dépendances Python installées**
```bash
pip install psycopg2-binary
```

### 3. **Fichiers de configuration**
- `inject_vehicles_supabase.py` ✅ Créé
- `supabase_config.py` ✅ Créé

## 🔧 Configuration

### **Étape 1 : Obtenir votre host Supabase**
1. Allez sur [supabase.com](https://supabase.com)
2. Connectez-vous à votre projet
3. **Settings** → **Database** → **Connection string**
4. Copiez la partie **host** (ex: `db.abcdefghijkl.supabase.co`)

### **Étape 2 : Modifier la configuration**
Dans `supabase_config.py`, remplacez :
```python
'host': 'db.xxxxxxxxxxxxx.supabase.co'  # Votre vrai host
'password': 'ipsco2025secure'           # Votre vrai mot de passe
```

### **Étape 3 : Variables d'environnement (optionnel)**
```bash
export SUPABASE_URL="db.votrehost.supabase.co"
export SUPABASE_DB_PASSWORD="votre_mot_de_passe"
```

## 🚀 Exécution

### **Lancement du script**
```bash
python inject_vehicles_supabase.py
```

### **Processus automatique**
1. **Connexion** à Supabase
2. **Création des tables** si nécessaire
3. **Création de l'établissement** IPS-CO
4. **Création de l'utilisateur** admin
5. **Injection des 9 véhicules**
6. **Vérification** et rapport

## 📊 Véhicules à Injecter

### **TOYOTA PRADO JEEP (3 véhicules)**
- 9133 AQ05 - OB DG
- 0595 AV05 - GM DG  
- 0595 AV05-B - CB ASSOCIE

### **MITSUBISHI FUSO CAMION (2 véhicules)**
- 1815 AV05 - OB DG
- 1815 AV05-B - GM DG

### **HYUNDAI PICK-UP (1 véhicule)**
- 0595 AV05-C - IPS-CO CREC07

### **TATA BUS et MINI BUS (3 véhicules)**
- 6690 AB14 - IPS-CO CREC07
- 6690 AB14-B - IPS-CO LSHI
- 6690 AB14-C - IPS-CO KAMOA

## 🔍 Structure des Tables

### **core_etablissement**
- id, nom, type, code, date_creation

### **core_utilisateur**
- id, username, email, first_name, last_name, is_staff, is_superuser

### **core_vehicule**
- Tous les champs du modèle Django Vehicule
- Relations avec etablissement et utilisateur

## ✅ Vérification

### **Après l'injection**
1. **Vérifiez dans Supabase** :
   - Table `core_vehicule` : 9 véhicules
   - Table `core_etablissement` : 1 établissement IPS-CO
   - Table `core_utilisateur` : 1 utilisateur admin

2. **Testez votre application** :
   - Les véhicules devraient être visibles
   - Les exports PDF devraient fonctionner
   - Les rapports devraient inclure les véhicules

## 🚨 Gestion des Erreurs

### **Erreur de connexion**
- Vérifiez l'host et le mot de passe
- Vérifiez que Supabase est actif

### **Erreur de table**
- Le script crée automatiquement les tables
- Vérifiez les permissions de l'utilisateur postgres

### **Véhicule en double**
- Le script ignore automatiquement les doublons
- Vérifiez les immatriculations

## 🔄 Réinjection

### **Si vous voulez tout refaire**
```bash
# Supprimez d'abord les tables dans Supabase
# Puis relancez le script
python inject_vehicles_supabase.py
```

### **Ajout de nouveaux véhicules**
- Modifiez le tableau `vehicles_data` dans le script
- Relancez l'injection

## 📞 Support

### **En cas de problème**
1. Vérifiez les logs du script
2. Vérifiez la connexion Supabase
3. Vérifiez les permissions de base de données

### **Logs utiles**
- Connexion réussie : ✅ Connexion à Supabase établie
- Tables créées : ✅ Tables créées/vérifiées
- Véhicules ajoutés : ✅ Véhicule X ajouté
- Total final : 📊 Total des véhicules dans la base

---
*Document généré automatiquement pour l'injection Supabase*
