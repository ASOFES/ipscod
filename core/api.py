from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
import json
from .models import Utilisateur, Course, Vehicule
from suivi.models import SuiviVehicule

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Endpoint API pour la connexion des applications mobiles"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': 'Nom d\'utilisateur et mot de passe requis'
            }, status=400)
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            # Autoriser les rôles mobiles: chauffeur, dispatch, demandeur
            if user.role in ['chauffeur', 'dispatch', 'demandeur']:
                role = user.role
                return JsonResponse({
                    'success': True,
                    'token': f'{role}_{user.id}_{user.username}',  # Token simple pour la démo
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'role': user.role,
                        'telephone': user.telephone,
                        'etablissement': user.etablissement.nom if user.etablissement else None,
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': "Accès non autorisé. Rôle requis: chauffeur, dispatch ou demandeur"
                }, status=403)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Nom d\'utilisateur ou mot de passe incorrect'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Format JSON invalide'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)

# -------------------- DEMANDEUR --------------------

def _get_user_from_token(request, expected_roles=None):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, JsonResponse({'success': False, 'error': "Token d'authentification requis"}, status=401)
    token = auth_header.split(' ')[1]
    parts = token.split('_')
    if len(parts) != 3:
        return None, JsonResponse({'success': False, 'error': 'Token invalide'}, status=401)
    role_prefix, user_id_str, username = parts
    try:
        user_id = int(user_id_str)
    except ValueError:
        return None, JsonResponse({'success': False, 'error': 'Token invalide'}, status=401)
    try:
        user = Utilisateur.objects.get(id=user_id, username=username, is_active=True)
    except Utilisateur.DoesNotExist:
        return None, JsonResponse({'success': False, 'error': 'Token invalide ou expiré'}, status=401)
    if expected_roles and (user.role not in expected_roles or user.role != role_prefix):
        return None, JsonResponse({'success': False, 'error': 'Accès non autorisé'}, status=403)
    return user, None

@csrf_exempt
@require_http_methods(["POST"]) 
def api_demandeur_demandes_create(request):
    """Créer une demande de mission (Course) par un demandeur"""
    user, err = _get_user_from_token(request, expected_roles=['demandeur'])
    if err:
        return err
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)

    required = ['point_embarquement', 'destination', 'motif', 'nombre_passagers']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return JsonResponse({'success': False, 'error': f"Champs manquants: {', '.join(missing)}"}, status=400)

    course = Course.objects.create(
        demandeur=user,
        etablissement=user.etablissement,
        point_embarquement=data['point_embarquement'],
        destination=data['destination'],
        motif=data['motif'],
        nombre_passagers=int(data.get('nombre_passagers', 1)),
        date_souhaitee=timezone.datetime.fromisoformat(data['date_souhaitee']) if data.get('date_souhaitee') else None,
        priorite=data.get('priorite', 'important'),
        statut='en_attente',
    )
    return JsonResponse({'success': True, 'demande_id': course.id})

@csrf_exempt
@require_http_methods(["GET"]) 
def api_demandeur_demandes_list(request):
    """Lister les demandes d'un demandeur"""
    user, err = _get_user_from_token(request, expected_roles=['demandeur'])
    if err:
        return err
    qs = Course.objects.filter(demandeur=user).order_by('-date_demande')
    result = [{
        'id': c.id,
        'point_embarquement': c.point_embarquement,
        'destination': c.destination,
        'motif': c.motif,
        'nombre_passagers': c.nombre_passagers,
        'date_demande': c.date_demande.isoformat() if c.date_demande else None,
        'date_souhaitee': c.date_souhaitee.isoformat() if c.date_souhaitee else None,
        'statut': c.statut,
        'priorite': c.priorite,
        'chauffeur': c.chauffeur.username if c.chauffeur_id else None,
        'vehicule': c.vehicule.immatriculation if c.vehicule_id else None,
    } for c in qs]
    return JsonResponse({'success': True, 'demandes': result})

# -------------------- DISPATCH --------------------

@csrf_exempt
@require_http_methods(["GET"]) 
def api_dispatch_demandes_list(request):
    """Liste des demandes filtrables par statut pour le dispatcher"""
    user, err = _get_user_from_token(request, expected_roles=['dispatch'])
    if err:
        return err
    statut = request.GET.get('statut')
    qs = Course.objects.all().order_by('-date_demande')
    if statut:
        qs = qs.filter(statut=statut)
    data = [{
        'id': c.id,
        'demandeur': c.demandeur.username if c.demandeur_id else None,
        'point_embarquement': c.point_embarquement,
        'destination': c.destination,
        'motif': c.motif,
        'nombre_passagers': c.nombre_passagers,
        'date_demande': c.date_demande.isoformat() if c.date_demande else None,
        'date_souhaitee': c.date_souhaitee.isoformat() if c.date_souhaitee else None,
        'statut': c.statut,
        'priorite': c.priorite,
        'chauffeur': c.chauffeur.username if c.chauffeur_id else None,
        'vehicule': c.vehicule.immatriculation if c.vehicule_id else None,
    } for c in qs]
    return JsonResponse({'success': True, 'demandes': data})

@csrf_exempt
@require_http_methods(["POST"]) 
def api_dispatch_assigner(request, course_id):
    """Valider/refuser et assigner une demande: chauffeur + véhicule"""
    user, err = _get_user_from_token(request, expected_roles=['dispatch'])
    if err:
        return err
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Demande introuvable'}, status=404)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)

    action = data.get('action', 'valider')  # valider | refuser
    if action == 'refuser':
        course.statut = 'refusee'
        course.dispatcher = user
        course.save()
        return JsonResponse({'success': True, 'statut': course.statut})

    chauffeur_id = data.get('chauffeur_id')
    vehicule_id = data.get('vehicule_id')
    if not chauffeur_id or not vehicule_id:
        return JsonResponse({'success': False, 'error': 'chauffeur_id et vehicule_id requis'}, status=400)
    try:
        chauffeur = Utilisateur.objects.get(id=chauffeur_id, role='chauffeur')
        vehicule = Vehicule.objects.get(id=vehicule_id)
    except Utilisateur.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Chauffeur invalide'}, status=400)
    except Vehicule.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Véhicule invalide'}, status=400)

    # Validation + assignation
    course.chauffeur = chauffeur
    course.vehicule = vehicule
    course.dispatcher = user
    course.statut = 'validee'
    course.date_validation = timezone.now()
    course.save()
    return JsonResponse({'success': True, 'statut': course.statut})

# -------------------- CHAUFFEUR actions --------------------

@csrf_exempt
@require_http_methods(["POST"]) 
def api_chauffeur_demarrer(request, course_id):
    user, err = _get_user_from_token(request, expected_roles=['chauffeur'])
    if err:
        return err
    try:
        course = Course.objects.get(id=course_id, chauffeur=user)
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mission introuvable'}, status=404)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)
    km_depart = data.get('kilometrage_depart')
    if km_depart is None:
        return JsonResponse({'success': False, 'error': 'kilometrage_depart requis'}, status=400)
    course.kilometrage_depart = int(km_depart)
    course.statut = 'en_cours'
    course.date_depart = timezone.now()
    course.save()
    return JsonResponse({'success': True, 'statut': course.statut})

@csrf_exempt
@require_http_methods(["POST"]) 
def api_chauffeur_terminer(request, course_id):
    user, err = _get_user_from_token(request, expected_roles=['chauffeur'])
    if err:
        return err
    try:
        course = Course.objects.get(id=course_id, chauffeur=user)
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mission introuvable'}, status=404)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)
    km_fin = data.get('kilometrage_fin')
    if km_fin is None:
        return JsonResponse({'success': False, 'error': 'kilometrage_fin requis'}, status=400)

    course.kilometrage_fin = int(km_fin)
    course.statut = 'terminee'
    course.date_fin = timezone.now()
    # Distance sera recalculée dans save()
    course.save()

    # Mettre à jour le kilométrage centralisé du véhicule et le suivi journalier
    if course.vehicule_id and course.distance_parcourue:
        veh = course.vehicule
        veh.kilometrage_actuel = max(veh.kilometrage_actuel or 0, course.kilometrage_fin)
        veh.save()
        SuiviVehicule.mettre_a_jour_suivi(veh, timezone.now().date(), course.distance_parcourue)

    return JsonResponse({'success': True, 'statut': course.statut, 'distance_parcourue': course.distance_parcourue})

@csrf_exempt
@require_http_methods(["GET"])
def api_verify_token(request):
    """Endpoint API pour vérifier la validité d'un token"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({
                'success': False,
                'error': 'Token d\'authentification requis'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        
        # Décoder le token simple (format: role_id_username)
        parts = token.split('_')
        if len(parts) == 3:
            role_prefix = parts[0]
            try:
                user_id = int(parts[1])
            except ValueError:
                user_id = None
            username = parts[2]
            if user_id is not None:
                try:
                    user = Utilisateur.objects.get(id=user_id, username=username, is_active=True)
                    if user.role in ['chauffeur', 'dispatch', 'demandeur'] and user.role == role_prefix:
                        return JsonResponse({
                            'success': True,
                            'user': {
                                'id': user.id,
                                'username': user.username,
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'email': user.email,
                                'role': user.role,
                                'telephone': user.telephone,
                                'etablissement': user.etablissement.nom if user.etablissement else None,
                            }
                        })
                except Utilisateur.DoesNotExist:
                    pass
        
        return JsonResponse({
            'success': False,
            'error': 'Token invalide ou expiré'
        }, status=401)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def api_chauffeur_missions(request):
    """Endpoint API pour récupérer les missions d'un chauffeur (assignées)"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({
                'success': False,
                'error': 'Token d\'authentification requis'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        parts = token.split('_')
        if len(parts) == 3 and parts[0] == 'chauffeur':
            user_id = int(parts[1])
            username = parts[2]
            try:
                user = Utilisateur.objects.get(id=user_id, username=username, is_active=True, role='chauffeur')
                # Missions réellement assignées
                courses = Course.objects.filter(chauffeur=user).order_by('-date_demande')
                missions = []
                for c in courses:
                    missions.append({
                        'id': c.id,
                        'demandeur': f"{c.demandeur.first_name} {c.demandeur.last_name}" if c.demandeur_id else None,
                        'point_embarquement': c.point_embarquement,
                        'destination': c.destination,
                        'motif': c.motif,
                        'nombre_passagers': c.nombre_passagers,
                        'date_demande': c.date_demande.isoformat() if c.date_demande else None,
                        'date_souhaitee': c.date_souhaitee.isoformat() if c.date_souhaitee else None,
                        'statut': c.statut,
                        'priorite': c.priorite,
                        'vehicule_immatriculation': c.vehicule.immatriculation if c.vehicule_id else None,
                        'vehicule_marque': c.vehicule.marque if c.vehicule_id else None,
                        'vehicule_modele': c.vehicule.modele if c.vehicule_id else None,
                        'kilometrage_depart': c.kilometrage_depart,
                        'kilometrage_fin': c.kilometrage_fin,
                        'distance_parcourue': c.distance_parcourue,
                    })
                return JsonResponse({'success': True, 'missions': missions})
            except Utilisateur.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': False,
            'error': 'Token invalide ou expiré'
        }, status=401)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        }, status=500)
