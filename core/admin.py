from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Vehicule, Course, ActionTraceur, Etablissement, ApplicationControl
from django.utils import timezone
from datetime import datetime, time

class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'etablissement', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active', 'etablissement')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'telephone', 'adresse', 'photo')}),
        ('Rôle', {'fields': ('role',)}),
        ('Établissement', {'fields': ('etablissement',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('etablissement', 'username')

class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'marque', 'modele', 'couleur', 'date_expiration_assurance', 'date_expiration_controle_technique')
    list_filter = ('marque', 'modele')
    search_fields = ('immatriculation', 'marque', 'modele', 'numero_chassis')
    date_hierarchy = 'date_creation'

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'demandeur', 'point_embarquement', 'destination', 'chauffeur', 'vehicule', 'statut', 'date_demande')
    list_filter = ('statut', 'date_demande')
    search_fields = ('demandeur__username', 'chauffeur__username', 'vehicule__immatriculation', 'point_embarquement', 'destination')
    date_hierarchy = 'date_demande'
    raw_id_fields = ('demandeur', 'chauffeur', 'vehicule', 'dispatcher')



class ActionTraceurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'action', 'date_action')
    list_filter = ('action', 'date_action')
    search_fields = ('utilisateur__username', 'action', 'details')
    date_hierarchy = 'date_action'
    readonly_fields = ('utilisateur', 'action', 'date_action', 'details')

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Vehicule, VehiculeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ActionTraceur, ActionTraceurAdmin)
admin.site.register(Etablissement)
admin.site.register(ApplicationControl)

# Enregistrement automatique de tous les modèles non déjà enregistrés
for model in [m for m in globals().values() if isinstance(m, type) and hasattr(m, '_meta')]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
