from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F, Count, Case, When, Value, IntegerField
from django.contrib.auth import get_user_model
from core.models import Message  # Import du modèle Message pour le chat interne
from django.utils import timezone
from django.http import HttpResponse
from core.models import Course, ActionTraceur, Utilisateur, Vehicule
from .forms import TraiterDemandeForm
from .utils import export_courses_to_excel, export_course_detail_to_excel
from core.utils import render_to_pdf
from notifications.utils import notify_user, send_sms, send_whatsapp, notify_course_participants, notify_multiple_users
import datetime

# Récupérer l'utilisateur système pour les messages système
def get_system_user():
    """
    Récupère l'utilisateur système ou le premier administrateur trouvé.
    Crée un utilisateur système si aucun n'existe.
    """
    User = get_user_model()
    # Essayer de récupérer l'utilisateur système
    system_user = User.objects.filter(username='system').first()
    
    if not system_user:
        # Si aucun utilisateur système n'existe, utiliser le premier superutilisateur
        system_user = User.objects.filter(is_superuser=True).first()
        
        if not system_user:
            # Si aucun superutilisateur n'existe, créer un utilisateur système
            system_user = User.objects.create_user(
                username='system',
                email='system@example.com',
                password=User.objects.make_random_password(),
                first_name='Système',
                last_name='MAMO',
                role='admin',
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
    
    return system_user


@login_required
def suivi_kilometrage(request):
    """
    Vue pour le suivi kilométrique des véhicules
    """
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    # Récupérer les filtres
    vehicule_id = request.GET.get('vehicule')
    chauffeur_id = request.GET.get('chauffeur')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    # Filtrer les courses avec kilométrage renseigné
    courses = Course.objects.filter(
        Q(kilometrage_depart__isnull=False) | Q(kilometrage_fin__isnull=False),
        statut__in=['en_cours', 'terminee']
    ).select_related('vehicule', 'chauffeur', 'demandeur')
    
    # Appliquer les filtres supplémentaires
    if vehicule_id:
        courses = courses.filter(vehicule_id=vehicule_id)
    
    if chauffeur_id:
        courses = courses.filter(chauffeur_id=chauffeur_id)
    
    if date_debut:
        date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d')
        courses = courses.filter(date_depart__date__gte=date_debut)
    
    if date_fin:
        date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d')
        courses = courses.filter(date_depart__date__lte=date_fin)
    
    # Récupérer le paramètre de tri
    sort_by = request.GET.get('sort_by', '-date_depart')  # Tri par défaut : date décroissante
    
    # Valider le paramètre de tri pour éviter les injections SQL
    valid_sort_fields = ['date_depart', '-date_depart', 'date_depart__month', '-date_depart__month',
                         'chauffeur__last_name', '-chauffeur__last_name', 
                         'vehicule__immatriculation', '-vehicule__immatriculation', 
                         'distance_parcourue', '-distance_parcourue']
    
    if sort_by not in valid_sort_fields:
        sort_by = '-date_depart'  # Valeur par défaut sécurisée
    
    # Trier les courses selon le paramètre de tri
    courses = courses.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(courses, 12)  # 12 courses par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiques par véhicule
    stats_vehicules = courses.values(
        'vehicule__immatriculation', 'vehicule__marque', 'vehicule__modele'
    ).annotate(
        count=Count('id'),
        distance_totale=Sum(Case(
            When(kilometrage_fin__isnull=False, kilometrage_depart__isnull=False, 
                 then=F('kilometrage_fin') - F('kilometrage_depart')),
            default=Value(0),
            output_field=IntegerField()
        ))
    ).filter(vehicule__isnull=False).order_by('-distance_totale')
    
    # Statistiques par chauffeur
    stats_chauffeurs = courses.values('chauffeur').annotate(
        chauffeur_name=F('chauffeur__first_name'),
        count=Count('id'),
        distance_totale=Sum(Case(
            When(kilometrage_fin__isnull=False, kilometrage_depart__isnull=False, 
                 then=F('kilometrage_fin') - F('kilometrage_depart')),
            default=Value(0),
            output_field=IntegerField()
        ))
    ).filter(chauffeur__isnull=False).order_by('-distance_totale')
    
    # Récupérer la liste des véhicules et chauffeurs pour les filtres
    vehicules = Vehicule.objects.all().order_by('immatriculation')
    chauffeurs = Utilisateur.objects.filter(role='chauffeur').order_by('first_name')
    
    context = {
        'courses': page_obj,
        'vehicules': vehicules,
        'chauffeurs': chauffeurs,
        'stats_vehicules': stats_vehicules,
        'stats_chauffeurs': stats_chauffeurs,
        'active_tab': 'suivi'
    }
    
    return render(request, 'dispatch/suivi_kilometrage.html', context)


@login_required
def export_suivi_kilometrage_excel(request):
    """
    Exporte les données de suivi kilométrique au format Excel
    """
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    # Récupérer les filtres
    vehicule_id = request.GET.get('vehicule')
    chauffeur_id = request.GET.get('chauffeur')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    # Filtrer les courses avec kilométrage renseigné
    courses = Course.objects.filter(
        Q(kilometrage_depart__isnull=False) | Q(kilometrage_fin__isnull=False),
        statut__in=['en_cours', 'terminee']
    ).select_related('vehicule', 'chauffeur', 'demandeur')
    
    # Appliquer les filtres supplémentaires
    if vehicule_id:
        courses = courses.filter(vehicule_id=vehicule_id)
    
    if chauffeur_id:
        courses = courses.filter(chauffeur_id=chauffeur_id)
    
    if date_debut:
        date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d')
        courses = courses.filter(date_depart__date__gte=date_debut)
    
    if date_fin:
        date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d')
        courses = courses.filter(date_depart__date__lte=date_fin)
    
    # Créer le nom du fichier avec la date
    filename = f'suivi_kilometrage_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    # Utiliser la fonction d'exportation Excel
    return export_courses_to_excel(courses, filename=filename)

@login_required
def dashboard(request):
    """Vue pour le tableau de bord du dispatcher"""
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    # Récupérer toutes les demandes avec les relations
    demandes = Course.objects.select_related('demandeur', 'chauffeur', 'vehicule').all().order_by('-date_demande')
    
    # Filtres
    statut = request.GET.get('statut')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    recherche = request.GET.get('recherche')
    tri = request.GET.get('tri', '-date_demande')  # Tri par défaut : date décroissante
    
    # Appliquer les filtres
    if statut:
        demandes = demandes.filter(statut=statut)
    
    if date_debut:
        date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
        demandes = demandes.filter(date_demande__date__gte=date_debut)
    
    if date_fin:
        date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
        demandes = demandes.filter(date_demande__date__lte=date_fin)
    
    # Recherche par nom de demandeur ou autres champs
    if recherche:
        demandes = demandes.filter(
            Q(demandeur__first_name__icontains=recherche) | 
            Q(demandeur__last_name__icontains=recherche) |
            Q(demandeur__username__icontains=recherche) |
            Q(point_embarquement__icontains=recherche) |
            Q(destination__icontains=recherche) |
            Q(motif__icontains=recherche)
        )
    
    # Valider et appliquer le tri
    valid_sort_fields = [
        'date_demande', '-date_demande', 
        'date_souhaitee', '-date_souhaitee',
        'demandeur__last_name', '-demandeur__last_name',
        'statut', '-statut',
        'chauffeur__last_name', '-chauffeur__last_name',
        'vehicule__immatriculation', '-vehicule__immatriculation'
    ]
    
    if tri not in valid_sort_fields:
        tri = '-date_demande'  # Valeur par défaut sécurisée
        
    demandes = demandes.order_by(tri)
    
    # Pagination
    paginator = Paginator(demandes, 12)  # 12 demandes par page
    page_number = request.GET.get('page')
    demandes_page = paginator.get_page(page_number)
    
    # Statistiques
    total = Course.objects.count()
    en_attente = Course.objects.filter(statut='en_attente').count()
    validee = Course.objects.filter(statut='validee').count()
    en_cours = Course.objects.filter(statut='en_cours').count()
    terminee = Course.objects.filter(statut='terminee').count()
    refusee = Course.objects.filter(statut='refusee').count()
    
    # Calculer les pourcentages
    stats = {
        'total': total,
        'en_attente': en_attente,
        'validee': validee,
        'en_cours': en_cours,
        'terminee': terminee,
        'refusee': refusee,
        'en_attente_percent': (en_attente / total * 100) if total > 0 else 0,
        'validee_percent': (validee / total * 100) if total > 0 else 0,
        'en_cours_percent': (en_cours / total * 100) if total > 0 else 0,
        'terminee_percent': (terminee / total * 100) if total > 0 else 0,
        'refusee_percent': (refusee / total * 100) if total > 0 else 0
    }
    
    context = {
        'demandes': demandes_page,
        'stats': stats,
        'tri_actuel': tri,
    }
    
    return render(request, 'dispatch/dashboard.html', context)

@login_required
def detail_demande(request, demande_id):
    """Vue pour afficher les détails d'une demande de mission"""
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    demande = get_object_or_404(Course, id=demande_id)
    
    # Récupérer l'historique des actions liées à cette demande
    historique = ActionTraceur.objects.filter(
        Q(details__icontains=f"Demande #{demande.id}") |
        Q(details__icontains=f"Course {demande.id}")
    ).order_by('-date_action')
    
    context = {
        'demande': demande,
        'historique': historique,
    }
    
    return render(request, 'dispatch/detail_demande.html', context)

@login_required
def traiter_demande(request, demande_id):
    """Vue pour traiter une demande de mission"""
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    # D'abord, récupérer la demande sans filtre de statut
    demande = get_object_or_404(Course, id=demande_id)
    
    # Si la demande n'est pas en attente, rediriger vers la page de détails avec un message
    if demande.statut != 'en_attente':
        messages.warning(request, f"Cette demande a déjà été traitée et est actuellement '{demande.get_statut_display()}'.")
        return redirect('dispatch:detail_demande', demande_id=demande_id)
    
    # Récupérer les chauffeurs disponibles
    chauffeurs = Utilisateur.objects.filter(role='chauffeur', is_active=True)
    
    # Récupérer tous les véhicules
    tous_vehicules = Vehicule.objects.all()
    
    # Filtrer les véhicules disponibles en utilisant la méthode est_disponible
    vehicules = [v for v in tous_vehicules if v.est_disponible()]
    
    if request.method == 'POST':
        form = TraiterDemandeForm(request.POST)
        if form.is_valid():
            decision = form.cleaned_data['decision']
            commentaire = form.cleaned_data['commentaire']
            
            if decision == 'valider':
                # Mettre à jour la demande
                demande.statut = 'validee'
                demande.chauffeur = form.cleaned_data['chauffeur']
                demande.vehicule = form.cleaned_data['vehicule']
                demande.dispatcher = request.user
                demande.date_validation = timezone.now()
                demande.save()
                
                # Le véhicule est maintenant assigné à cette course
                # Pas besoin de mettre à jour un champ de disponibilité car nous filtrons
                # les véhicules disponibles en fonction des courses en cours
                
                # Créer une entrée dans l'historique des actions
                action_details = f"Demande #{demande.id} validée - Chauffeur: {demande.chauffeur.get_full_name()}, Véhicule: {demande.vehicule.immatriculation}"
                if commentaire:
                    action_details += f" - Commentaire: {commentaire}"
                
                ActionTraceur.objects.create(
                    utilisateur=request.user,
                    action="Validation de demande de mission",
                    details=action_details
                )
                
                # Notification individuelle au demandeur (message personnalisé)
                demandeur_title = f"Votre demande de course #{demande.id} a été validée"
                demandeur_message = f"Votre demande de course de {demande.point_embarquement} à {demande.destination} a été validée. Chauffeur assigné: {demande.chauffeur.get_full_name()}."
                
                # Notification interne au demandeur
                notify_user(
                    demande.demandeur,
                    demandeur_title,
                    demandeur_message,
                    notification_type='all',
                    course=demande
                )
                
                # Notification individuelle au chauffeur (message personnalisé)
                chauffeur_title = f"Nouvelle course assignée #{demande.id}"
                chauffeur_message = f"Une nouvelle course vous a été assignée de {demande.point_embarquement} à {demande.destination} pour le {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}."
                
                # Notification interne au chauffeur
                notify_user(
                    demande.chauffeur,
                    chauffeur_title,
                    chauffeur_message,
                    notification_type='all',
                    course=demande
                )
                
                # Notification de groupe à tous les participants (message général)
                participants = [demande.demandeur, demande.chauffeur, demande.dispatcher]
                groupe_message = f"""Course #{demande.id} validée:\n- Trajet: {demande.point_embarquement} → {demande.destination}\n- Date: {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}\n- Demandeur: {demande.demandeur.get_full_name()}\n- Chauffeur: {demande.chauffeur.get_full_name()}\n- Véhicule: {demande.vehicule.marque} {demande.vehicule.modele} ({demande.vehicule.immatriculation})\n- Nombre de passagers: {demande.nombre_passagers}\n"""
                notify_course_participants(
                    participants,
                    groupe_message,
                    notification_type='whatsapp'
                )
                
                # Notification SMS/WhatsApp au demandeur
                if demande.demandeur.telephone:
                    send_sms(demande.demandeur.telephone, demandeur_message)
                    send_whatsapp(demande.demandeur.telephone, demandeur_message)
                # Notification SMS/WhatsApp au chauffeur
                if demande.chauffeur and demande.chauffeur.telephone:
                    send_sms(demande.chauffeur.telephone, chauffeur_message)
                    send_whatsapp(demande.chauffeur.telephone, chauffeur_message)
                
                # Notification dans le chat interne pour le demandeur
                chat_message_demandeur = f"""Votre demande de mission a été validée ✅
- Trajet: {demande.point_embarquement} → {demande.destination}
- Date: {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}
- Chauffeur: {demande.chauffeur.get_full_name()}
- Véhicule: {demande.vehicule}"""
                
                # Notification dans le chat interne pour le chauffeur
                chat_message_chauffeur = f"""Nouvelle mission assignée 🚗
- Trajet: {demande.point_embarquement} → {demande.destination}
- Date: {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}
- Demandeur: {demande.demandeur.get_full_name()}
- Véhicule: {demande.vehicule}"""
                
                # Création des messages dans le chat interne
                # Utiliser l'utilisateur système comme expéditeur pour les messages système
                system_user = get_system_user()
                
                # Message pour le demandeur
                Message.objects.create(
                    sender=system_user,
                    recipient=demande.demandeur,
                    content=chat_message_demandeur,
                    is_system_message=True
                )
                
                # Message pour le chauffeur
                Message.objects.create(
                    sender=system_user,
                    recipient=demande.chauffeur,
                    content=chat_message_chauffeur,
                    is_system_message=True
                )
                
                # Message pour l'admin/dispatcher
                chat_message_admin = f"""Nouvelle mission planifiée 📋
- Trajet: {demande.point_embarquement} → {demande.destination}
- Date: {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}
- Demandeur: {demande.demandeur.get_full_name()}
- Chauffeur: {demande.chauffeur.get_full_name()}
- Véhicule: {demande.vehicule}
- Statut: Validée"""
                
                Message.objects.create(
                    sender=system_user,
                    recipient=request.user,  # L'admin/dispatcher qui a validé
                    content=chat_message_admin,
                    is_system_message=True
                )
                
                messages.success(request, f'La demande #{demande.id} a été validée avec succès.')
                return redirect('dispatch:liste_courses')
            
            elif decision == 'refuser':
                # Mettre à jour la demande
                demande.statut = 'refusee'
                demande.dispatcher = request.user
                demande.save()
                
                # Créer une entrée dans l'historique des actions
                action_details = f"Demande #{demande.id} refusée"
                if commentaire:
                    action_details += f" - Motif: {commentaire}"
                
                ActionTraceur.objects.create(
                    utilisateur=request.user,
                    action="Refus de demande de mission",
                    details=action_details
                )
                
                # Notification individuelle au demandeur (message personnalisé)
                demandeur_title = f"Votre demande de course #{demande.id} a été refusée"
                demandeur_message = f"Votre demande de course de {demande.point_embarquement} à {demande.destination} a été refusée."
                if commentaire:
                    demandeur_message += f" Motif: {commentaire}"
                
                # Notification interne au demandeur
                notify_user(
                    demande.demandeur,
                    demandeur_title,
                    demandeur_message,
                    notification_type='all',
                    course=demande
                )
                
                # Notification dans le chat interne pour le refus
                chat_message_refus = f"""Votre demande de mission a été refusée ❌
- Trajet: {demande.point_embarquement} → {demande.destination}
- Date: {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}"""
                
                if commentaire:
                    chat_message_refus += f"\n- Motif: {commentaire}"
                
                # Récupérer l'utilisateur système pour les messages système
                system_user = get_system_user()
                
                # Message de refus pour le demandeur
                Message.objects.create(
                    sender=system_user,
                    recipient=demande.demandeur,
                    content=chat_message_refus,
                    is_system_message=True
                )
                
                # Message de refus pour l'admin/dispatcher
                chat_message_admin_refus = f"""Demande refusée ❌
- Trajet: {demande.point_embarquement} → {demande.destination}
- Date: {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}
- Demandeur: {demande.demandeur.get_full_name()}
- Motif: {commentaire or 'Aucun motif fourni'}"""
                
                Message.objects.create(
                    sender=system_user,
                    recipient=request.user,  # L'admin/dispatcher qui a refusé
                    content=chat_message_admin_refus,
                    is_system_message=True
                )
                
                # Notification de groupe (au demandeur et au dispatcher uniquement)
                groupe_title = f"Demande de course #{demande.id} refusée"
                groupe_message = f"""Demande #{demande.id} refusée:
- Trajet: {demande.point_embarquement} → {demande.destination}
- Demandeur: {demande.demandeur.get_full_name()}
- Date demandée: {demande.date_souhaitee.strftime('%d/%m/%Y à %H:%M')}
"""
                if commentaire:
                    groupe_message += f"- Motif: {commentaire}"
                
                # Créer une liste avec seulement le demandeur et le dispatcher
                participants = [demande.demandeur, demande.dispatcher]
                
                # Envoyer la notification WhatsApp
                notify_multiple_users(
                    participants,
                    groupe_title,
                    groupe_message,
                    notification_type='whatsapp',
                    course=demande
                )
                
                # Notification SMS/WhatsApp au demandeur
                if demande.demandeur.telephone:
                    send_sms(demande.demandeur.telephone, demandeur_message)
                    send_whatsapp(demande.demandeur.telephone, demandeur_message)
                
                messages.success(request, f'La demande #{demande.id} a été refusée.')
                return redirect('dispatch:liste_courses')
    else:
        form = TraiterDemandeForm()
    
    return render(request, 'dispatch/traiter_demande.html', {
        'form': form,
        'demande': demande,
        'chauffeurs': chauffeurs,
        'vehicules': vehicules
    })


@login_required
def course_detail_pdf(request, course_id):
    """Vue pour générer un PDF des détails d'une course"""
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id)
    
    # Préparer le contexte pour le template PDF
    context = {
        'course': course,
        'date_impression': timezone.now().strftime('%d/%m/%Y %H:%M'),
        'year': timezone.now().year,
        'nombre_passagers': course.nombre_passagers,
    }
    
    # Générer le PDF
    pdf = render_to_pdf('dispatch/pdf/course_detail_pdf.html', context)
    if pdf:
        response = pdf
        filename = f"course_{course_id}_details_{timezone.now().strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse("Une erreur s'est produite lors de la génération du PDF.")


@login_required
def course_detail_excel(request, course_id):
    """Vue pour générer un fichier Excel des détails d'une course"""
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id)
    
    # Générer le fichier Excel
    filename = f"course_{course_id}_details_{timezone.now().strftime('%Y%m%d')}.xlsx"
    # Ajouter le nombre de passagers dans le contexte si besoin
    return export_course_detail_to_excel(course, filename)


@login_required
def courses_list_pdf(request):
    """Vue pour générer un PDF de la liste des courses avec filtrage"""
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    # Récupérer toutes les demandes avec leurs relations
    courses = Course.objects.select_related('demandeur', 'chauffeur', 'vehicule').all().order_by('-date_demande')
    
    # Appliquer les filtres
    statut = request.GET.get('statut')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    filters = {}
    
    if statut:
        courses = courses.filter(statut=statut)
        filters['statut'] = statut
        # Obtenir l'affichage lisible du statut
        for choice in Course.STATUS_CHOICES:
            if choice[0] == statut:
                filters['statut_display'] = choice[1]
                break
    
    if date_debut:
        date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
        courses = courses.filter(date_demande__date__gte=date_debut)
        filters['date_debut'] = date_debut
    
    if date_fin:
        date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
        courses = courses.filter(date_demande__date__lte=date_fin)
        filters['date_fin'] = date_fin
    
    # Préparer le contexte pour le template PDF
    context = {
        'courses': courses,
        'filters': filters if filters else None,
        'date_impression': timezone.now().strftime('%d/%m/%Y %H:%M'),
        'year': timezone.now().year
    }
    
    # Générer le PDF
    pdf = render_to_pdf('dispatch/pdf/courses_list_pdf.html', context)
    if pdf:
        response = pdf
        filename = f"courses_list_{timezone.now().strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
    return HttpResponse("Une erreur s'est produite lors de la génération du PDF.")


@login_required
def courses_list_excel(request):
    """Vue pour générer un fichier Excel de la liste des courses avec filtrage"""
    # Vérifier que l'utilisateur est bien un dispatcher, un admin ou un superuser
    if request.user.role != 'dispatch' and request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page.")
        return redirect('home')
    
    # Récupérer toutes les demandes avec leurs relations
    courses = Course.objects.select_related('demandeur', 'chauffeur', 'vehicule').all().order_by('-date_demande')
    
    # Appliquer les filtres
    statut = request.GET.get('statut')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    if statut:
        courses = courses.filter(statut=statut)
    
    if date_debut:
        date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
        courses = courses.filter(date_demande__date__gte=date_debut)
    
    if date_fin:
        date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
        courses = courses.filter(date_demande__date__lte=date_fin)
    
    # Générer le fichier Excel
    filename = f"courses_list_{timezone.now().strftime('%Y%m%d')}.xlsx"
    return export_courses_to_excel(courses, filename)
