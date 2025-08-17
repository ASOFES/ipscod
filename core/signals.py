from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import logging

from .models import Course, Vehicule, Utilisateur, Etablissement # Assurez-vous d'importer tous les modèles nécessaires

logger = logging.getLogger(__name__)

# Fonction utilitaire pour envoyer des SMS (à implémenter avec un service tiers)
def send_sms_notification(phone_number, message):
    # Ici, vous intégreriez votre API de fournisseur SMS (ex: Twilio, Nexmo)
    # Pour l'instant, nous allons juste logger l'action
    logger.info(f"SMS envoyé à {phone_number}: {message}")
    print(f"SMS envoyé à {phone_number}: {message}") # Pour le débogage

@receiver(post_save, sender=Course)
def check_maintenance_and_notify(sender, instance, created, **kwargs):
    if not instance.vehicule or not instance.kilometrage_fin:
        return # Ne rien faire si pas de véhicule ou de kilométrage de fin

    # Récupérer le véhicule associé à la course
    vehicule = instance.vehicule

    # Mettre à jour le kilométrage actuel du véhicule s'il est plus élevé
    if instance.kilometrage_fin > (vehicule.kilometrage_actuel or 0):
        vehicule.kilometrage_actuel = instance.kilometrage_fin
        vehicule.save(update_fields=['kilometrage_actuel']) # Sauvegarder juste ce champ

    # Calculer la distance depuis le dernier entretien
    distance_depuis_dernier_entretien = (vehicule.kilometrage_actuel or 0) - (vehicule.kilometrage_dernier_entretien or 0)

    # Seuil de 4200 km pour la notification
    SEUIL_KM_ENTRETIEN = 4200

    if distance_depuis_dernier_entretien >= SEUIL_KM_ENTRETIEN:
        # Préparer le message
        subject = f"Alerte Entretien Véhicule: {vehicule.immatriculation}"
        message = (
            f"Le véhicule {vehicule.immatriculation} ({vehicule.marque} {vehicule.modele}) "
            f"a parcouru {distance_depuis_dernier_entretien} km depuis le dernier entretien ({vehicule.kilometrage_dernier_entretien} km). "
            f"Un entretien est recommandé. Kilométrage actuel: {vehicule.kilometrage_actuel} km."
        )

        # Récupérer les administrateurs et dispatchers du département concerné
        recipients_emails = []
        recipients_phone_numbers = []

        # Administrateurs
        admins = Utilisateur.objects.filter(role='admin', is_active=True)
        for admin in admins:
            if admin.email:
                recipients_emails.append(admin.email)
            if admin.telephone:
                recipients_phone_numbers.append(admin.telephone)

        # Dispatchers du département du véhicule
        if vehicule.etablissement:
            dispatchers = Utilisateur.objects.filter(
                role='dispatch',
                etablissement=vehicule.etablissement,
                is_active=True
            )
            for dispatcher in dispatchers:
                if dispatcher.email and dispatcher.email not in recipients_emails:
                    recipients_emails.append(dispatcher.email)
                if dispatcher.telephone and dispatcher.telephone not in recipients_phone_numbers:
                    recipients_phone_numbers.append(dispatcher.telephone)
        
        # Envoyer les emails
        if recipients_emails:
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients_emails, fail_silently=False)
                logger.info(f"Email de notification d'entretien envoyé à: {recipients_emails}")
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi de l'email d'entretien: {e}")

        # Envoyer les SMS
        if recipients_phone_numbers:
            for phone in recipients_phone_numbers:
                send_sms_notification(phone, message)
                
        # Réinitialiser le kilométrage du dernier entretien pour le prochain cycle
        # Il est crucial de s'assurer que cette sauvegarde ne déclenche pas un autre signal en boucle.
        # Pour éviter cela, on utilise update_fields ou on déconnecte/reconnecte le signal si nécessaire.
        vehicule.kilometrage_dernier_entretien = vehicule.kilometrage_actuel
        vehicule.save(update_fields=['kilometrage_dernier_entretien'])
        logger.info(f"Kilométrage du dernier entretien réinitialisé pour {vehicule.immatriculation} à {vehicule.kilometrage_dernier_entretien} km.") 