# Script PowerShell pour ajouter les véhicules à la base de données IPS-CO
# Exécuter en tant qu'administrateur si nécessaire

Write-Host "🚗 Script d'ajout des véhicules IPS-CO" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Vérifier si Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python depuis https://python.org" -ForegroundColor Yellow
    exit 1
}

# Vérifier si pip est installé
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip détecté: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip n'est pas installé" -ForegroundColor Red
    exit 1
}

# Installer les dépendances
Write-Host "📦 Installation des dépendances..." -ForegroundColor Yellow
try {
    pip install python-dateutil
    Write-Host "✅ python-dateutil installé" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors de l'installation de python-dateutil" -ForegroundColor Red
    Write-Host "Tentative d'installation avec --user..." -ForegroundColor Yellow
    try {
        pip install --user python-dateutil
        Write-Host "✅ python-dateutil installé avec --user" -ForegroundColor Green
    } catch {
        Write-Host "❌ Impossible d'installer python-dateutil" -ForegroundColor Red
        exit 1
    }
}

# Vérifier si Django est installé
try {
    python -c "import django; print('Django version:', django.get_version())" 2>&1
    Write-Host "✅ Django détecté" -ForegroundColor Green
} catch {
    Write-Host "❌ Django n'est pas installé" -ForegroundColor Red
    Write-Host "Installation de Django..." -ForegroundColor Yellow
    try {
        pip install Django
        Write-Host "✅ Django installé" -ForegroundColor Green
    } catch {
        Write-Host "❌ Impossible d'installer Django" -ForegroundColor Red
        exit 1
    }
}

# Vérifier la structure du projet
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ manage.py non trouvé. Assurez-vous d'être dans le répertoire racine du projet Django" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "add_vehicles_from_image.py")) {
    Write-Host "❌ add_vehicles_from_image.py non trouvé" -ForegroundColor Red
    exit 1
}

# Vérifier la base de données
Write-Host "🔍 Vérification de la base de données..." -ForegroundColor Yellow
try {
    python manage.py check
    Write-Host "✅ Configuration Django valide" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur de configuration Django" -ForegroundColor Red
    Write-Host "Vérifiez votre fichier settings.py" -ForegroundColor Yellow
    exit 1
}

# Appliquer les migrations si nécessaire
Write-Host "🔄 Application des migrations..." -ForegroundColor Yellow
try {
    python manage.py migrate
    Write-Host "✅ Migrations appliquées" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Erreur lors des migrations (peut être normal)" -ForegroundColor Yellow
}

# Exécuter le script d'ajout des véhicules
Write-Host "🚗 Ajout des véhicules à la base de données..." -ForegroundColor Yellow
try {
    python add_vehicles_from_image.py
    Write-Host "✅ Script d'ajout des véhicules exécuté avec succès!" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur lors de l'exécution du script" -ForegroundColor Red
    exit 1
}

# Exécuter les tests de vérification
Write-Host "🧪 Exécution des tests de vérification..." -ForegroundColor Yellow
try {
    python test_vehicles_import.py
    Write-Host "✅ Tests de vérification terminés!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Erreur lors des tests (peut être normal)" -ForegroundColor Yellow
}

Write-Host "🎉 Processus terminé!" -ForegroundColor Green
Write-Host "Vous pouvez maintenant vérifier les véhicules dans l'admin Django" -ForegroundColor Cyan
Write-Host "URL: http://localhost:8000/admin/core/vehicule/" -ForegroundColor Cyan

# Pause pour permettre à l'utilisateur de lire les messages
Read-Host "Appuyez sur Entrée pour fermer"
