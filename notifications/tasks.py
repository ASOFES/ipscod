from django.utils import timezone
from datetime import timedelta
from .models import DocumentNotification, EntretienNotification
from core.models import Vehicule, Message, Utilisateur
from django.db.models import Q

def check_documents_and_send_notifications():
    """
    Vérifie les documents de bord et les entretiens, et envoie des notifications si nécessaire.
    Cette fonction est conçue pour être exécutée périodiquement via une tâche planifiée.
    
    Returns:
        tuple: (bool, str) - Statut de l'opération et message descriptif
    """
    try:
        today = timezone.now().date()
        system_user = get_system_user()
        
        if not system_user:
            error_msg = "Aucun utilisateur système trouvé pour envoyer les notifications"
            print(error_msg)
            return False, error_msg
        
        # 1. Vérifier les documents de bord
        check_documents(today, system_user)
        
        # 2. Vérifier les entretiens
        check_entretiens(today, system_user)
        
        return True, "Vérification des documents et entretiens terminée avec succès"
        
    except Exception as e:
        error_msg = f"Erreur lors de la vérification des documents et entretiens: {e}"
        print(error_msg)
        return False, error_msg

def get_system_user():
    """
    Récupère l'utilisateur système pour les notifications.
    
    Returns:
        Utilisateur: L'utilisateur système ou le premier superutilisateur trouvé.
        Retourne None si aucun utilisateur n'est trouvé.
    """
    try:
        # Essayer de récupérer l'utilisateur système
        system_user = Utilisateur.objects.filter(username='system').first()
        
        # Si aucun utilisateur système n'existe, utiliser le premier superutilisateur
        if not system_user:
            system_user = Utilisateur.objects.filter(is_superuser=True).first()
            
            # Si aucun superutilisateur n'existe, essayer de créer un utilisateur système
            if not system_user:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                system_user = User.objects.create_user(
                    username='system',
                    email='system@example.com',
                    password=User.objects.make_random_password(),
                    is_active=False
                )
                system_user.save()
                
        return system_user
        
    except Exception as e:
        print(f"Erreur lors de la récupération/création de l'utilisateur système: {e}")
        return None

def check_documents(today, system_user):
    """
    Vérifie les documents de bord et envoie des notifications si nécessaire.
    
    Args:
        today (date): Date du jour pour la vérification
        system_user (Utilisateur): Utilisateur système pour l'envoi des notifications
    """
    try:
        # Vérifier les documents expirés ou sur le point d'expirer
        for vehicule in Vehicule.objects.all():
            try:
                # Vérifier l'assurance
                if vehicule.date_expiration_assurance:
                    jours_restants = (vehicule.date_expiration_assurance - today).days
                    if jours_restants <= 30:  # Alerte 30 jours avant l'expiration
                        send_document_notification(
                            vehicule=vehicule,
                            document_type='assurance',
                            date_expiration=vehicule.date_expiration_assurance,
                            jours_restants=jours_restants,
                            system_user=system_user
                        )
                
                # Vérifier le contrôle technique
                if vehicule.date_expiration_controle_technique:
                    jours_restants = (vehicule.date_expiration_controle_technique - today).days
                    if jours_restants <= 30:  # Alerte 30 jours avant l'expiration
                        send_document_notification(
                            vehicule=vehicule,
                            document_type='contrôle technique',
                            date_expiration=vehicule.date_expiration_controle_technique,
                            jours_restants=jours_restants,
                            system_user=system_user
                        )
                
                # Vérifier la vignette
                if vehicule.date_expiration_vignette:
                    jours_restants = (vehicule.date_expiration_vignette - today).days
                    if jours_restants <= 30:  # Alerte 30 jours avant l'expiration
                        send_document_notification(
                            vehicule=vehicule,
                            document_type='vignette',
                            date_expiration=vehicule.date_expiration_vignette,
                            jours_restants=jours_restants,
                            system_user=system_user
                        )
                        
            except Exception as e:
                print(f"Erreur lors de la vérification des documents pour le véhicule {vehicule.immatriculation}: {e}")
                continue  # Continuer avec le véhicule suivant en cas d'erreur
                
    except Exception as e:
        print(f"Erreur critique lors de la vérification des documents: {e}")
        raise  # Relancer l'exception pour la gestion des erreurs de niveau supérieur

def check_entretiens(today, system_user):
    """
    Vérifie les véhicules nécessitant un entretien et envoie des notifications si nécessaire.
    
    Args:
        today (date): Date du jour pour la vérification (non utilisé actuellement mais conservé pour compatibilité)
        system_user (Utilisateur): Utilisateur système pour l'envoi des notifications
    """
    try:
        for vehicule in Vehicule.objects.all():
            try:
                # Vérifier si les données nécessaires sont disponibles
                if vehicule.kilometrage_actuel is None or vehicule.kilometrage_dernier_entretien is None:
                    print(f"Données manquantes pour le véhicule {vehicule.immatriculation}: kilométrage actuel ou dernier entretien non renseigné")
                    continue
                
                # Calculer les kilomètres parcourus depuis le dernier entretien
                kilometres_parcourus = vehicule.kilometrage_actuel - vehicule.kilometrage_dernier_entretien
                kilometres_restants = max(0, 4500 - kilometres_parcourus)
                
                # Vérifier si une notification doit être envoyée
                # - Si le kilométrage d'entretien est dépassé (4500 km)
                # - Ou s'il reste moins de 500 km avant l'entretien
                if kilometres_parcourus >= 4500 or kilometres_restants <= 500:
                    print(f"Envoi d'une notification d'entretien pour le véhicule {vehicule.immatriculation} - {kilometres_parcourus} km parcourus")
                    send_entretien_notification(
                        vehicule=vehicule,
                        kilometres_parcourus=kilometres_parcourus,
                        kilometres_restants=kilometres_restants,
                        system_user=system_user
                    )
                    
            except Exception as e:
                print(f"Erreur lors de la vérification de l'entretien pour le véhicule {vehicule.immatriculation}: {e}")
                continue  # Continuer avec le véhicule suivant en cas d'erreur
                
    except Exception as e:
        print(f"Erreur critique lors de la vérification des entretiens: {e}")
        raise  # Relancer l'exception pour la gestion des erreurs de niveau supérieur

def send_document_notification(vehicule, document_type, date_expiration, jours_restants, system_user):
    """
    Envoie une notification pour un document sur le point d'expirer ou ayant expiré.
    
    Args:
        vehicule (Vehicule): Le véhicule concerné
        document_type (str): Type de document (assurance, contrôle technique, vignette)
        date_expiration (date): Date d'expiration du document
        jours_restants (int): Nombre de jours restants avant expiration (négatif si expiré)
        system_user (Utilisateur): Utilisateur système pour l'envoi des notifications
    """
    try:
        # Vérifier si une notification similaire a déjà été envoyée récemment (dans les 7 derniers jours)
        recent_notification = DocumentNotification.objects.filter(
            vehicule=vehicule,
            document_type=document_type,
            date_creation__gte=timezone.now() - timedelta(days=7)
        ).exists()
        
        if not recent_notification:
            # Créer un message système
            message = f"Le document {document_type} du véhicule {vehicule.immatriculation} "
            if jours_restants <= 0:
                message += f"a expiré le {date_expiration.strftime('%d/%m/%Y')}"
            else:
                message += f"expire dans {jours_restants} jour(s) (le {date_expiration.strftime('%d/%m/%Y')})"
            
            # Récupérer les utilisateurs administrateurs
            admin_users = Utilisateur.objects.filter(Q(is_superuser=True) | Q(role='admin'))
            
            if not admin_users.exists():
                print("Aucun administrateur trouvé pour l'envoi des notifications")
                return False
            
            # Envoyer la notification à chaque administrateur
            for user in admin_users.distinct():
                try:
                    Message.objects.create(
                        sender=system_user,
                        recipient=user,
                        content=message,
                        is_system_message=True
                    )
                    print(f"Notification envoyée à {user.username}: {message}")
                except Exception as e:
                    print(f"Erreur lors de l'envoi de la notification à {user.username}: {e}")
            
            # Enregistrer la notification dans la base de données
            try:
                DocumentNotification.objects.create(
                    vehicule=vehicule,
                    document_type=document_type,
                    date_expiration=date_expiration,
                    is_active=True
                )
                print(f"Notification enregistrée pour le véhicule {vehicule.immatriculation}, document: {document_type}")
                return True
                
            except Exception as e:
                print(f"Erreur lors de l'enregistrement de la notification: {e}")
                return False
        else:
            print(f"Une notification récente existe déjà pour ce document ({document_type}) du véhicule {vehicule.immatriculation}")
            return False
            
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification pour le document {document_type} du véhicule {vehicule.immatriculation}: {e}")
        return False

def send_entretien_notification(vehicule, kilometres_parcourus, kilometres_restants, system_user):
    """
    Envoie une notification pour un entretien nécessaire.
    
    Args:
        vehicule (Vehicule): Le véhicule concerné
        kilometres_parcourus (int): Nombre de kilomètres parcourus depuis le dernier entretien
        kilometres_restants (int): Nombre de kilomètres restants avant l'entretien
        system_user (Utilisateur): Utilisateur système pour l'envoi des notifications
        
    Returns:
        bool: True si la notification a été envoyée avec succès, False sinon
    """
    try:
        # Vérifier si une notification similaire a déjà été envoyée récemment (dans les 7 derniers jours)
        recent_notification = EntretienNotification.objects.filter(
            vehicule=vehicule,
            date_creation__gte=timezone.now() - timedelta(days=7)
        ).exists()
        
        if not recent_notification:
            # Créer un message système
            message = f"Le véhicule {vehicule.immatriculation} a parcouru {kilometres_parcourus} km "
            if kilometres_parcourus >= 4500:
                message += f"et a dépassé l'intervalle d'entretien de {kilometres_parcourus - 4500} km"
            else:
                message += f"et nécessitera un entretien dans {kilometres_restants} km"
            
            # Récupérer les utilisateurs administrateurs
            admin_users = Utilisateur.objects.filter(Q(is_superuser=True) | Q(role='admin'))
            
            if not admin_users.exists():
                print("Aucun administrateur trouvé pour l'envoi des notifications d'entretien")
                return False
            
            # Envoyer la notification à chaque administrateur
            for user in admin_users.distinct():
                try:
                    Message.objects.create(
                        sender=system_user,
                        recipient=user,
                        content=message,
                        is_system_message=True
                    )
                    print(f"Notification d'entretien envoyée à {user.username}: {message}")
                except Exception as e:
                    print(f"Erreur lors de l'envoi de la notification d'entretien à {user.username}: {e}")
            
            # Enregistrer la notification dans la base de données
            try:
                EntretienNotification.objects.create(
                    vehicule=vehicule,
                    kilometrage_actuel=vehicule.kilometrage_actuel or 0,
                    kilometrage_prochain=(vehicule.kilometrage_dernier_entretien or 0) + 4500,
                    is_active=True
                )
                print(f"Notification d'entretien enregistrée pour le véhicule {vehicule.immatriculation}")
                return True
                
            except Exception as e:
                print(f"Erreur lors de l'enregistrement de la notification d'entretien: {e}")
                return False
                
        else:
            print(f"Une notification d'entretien récente existe déjà pour le véhicule {vehicule.immatriculation}")
            return False
            
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification d'entretien pour le véhicule {vehicule.immatriculation}: {e}")
        return False
