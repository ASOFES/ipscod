from django import forms
from .models import Ravitaillement, Station
from core.models import Vehicule, Utilisateur, Etablissement
from django.utils.translation import gettext_lazy as _

class RavitaillementForm(forms.ModelForm):
    """Formulaire pour la création et modification de ravitaillements"""
    
    class Meta:
        model = Ravitaillement
        fields = ['vehicule', 'station', 'nom_station', 'kilometrage_avant', 'kilometrage_apres', 
                'litres', 'cout_unitaire', 'commentaires', 'image', 'chauffeur']
        widgets = {
            'vehicule': forms.Select(attrs={'class': 'form-select'}),
            'station': forms.Select(attrs={'class': 'form-select select2', 'data-placeholder': 'Sélectionnez une station...'}),
            'nom_station': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la station si non répertoriée'}),
            'kilometrage_avant': forms.NumberInput(attrs={'class': 'form-control'}),
            'kilometrage_apres': forms.NumberInput(attrs={'class': 'form-control'}),
            'litres': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cout_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'commentaires': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'chauffeur': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.createur = kwargs.pop('createur', None)
        super().__init__(*args, **kwargs)
        
        # Filtrer les véhicules par établissement
        self.fields['vehicule'].queryset = Vehicule.objects.filter(
            etablissement=self.createur.etablissement
        ).order_by('immatriculation')
        
        # Filtrer les stations par établissement
        self.fields['station'].queryset = Station.objects.filter(
            etablissement=self.createur.etablissement,
            est_active=True
        ).order_by('nom')
        
        # Rendre le champ nom_station conditionnel via JavaScript
        self.fields['nom_station'].widget.attrs.update({
            'class': 'form-control',
            'disabled': 'disabled',
            'style': 'display: none;'
        })
        
        # Ajouter des labels plus descriptifs
        self.fields['vehicule'].label = "Véhicule"
        self.fields['station'].label = "Station de ravitaillement"
        
        # Préremplir par défaut avec l'utilisateur connecté si il est chauffeur
        if self.createur and hasattr(self.createur, 'role'):
            if self.createur.role == 'chauffeur':
                self.fields['chauffeur'].queryset = Utilisateur.objects.filter(pk=self.createur.pk)
                self.fields['chauffeur'].initial = self.createur.pk
                self.fields['chauffeur'].widget.attrs['disabled'] = 'disabled'
            elif self.createur.role in ['admin', 'dispatch'] or self.createur.is_superuser:
                self.fields['chauffeur'].queryset = Utilisateur.objects.filter(role='chauffeur').order_by('first_name')
            else:
                # Pour d'autres rôles, ne montrer aucun chauffeur ou un queryset vide
                self.fields['chauffeur'].queryset = Utilisateur.objects.none()
                self.fields['chauffeur'].widget.attrs['disabled'] = 'disabled'
        else:
            # Si pas de createur (cas rare ou non connecté), aucun chauffeur sélectionnable
            self.fields['chauffeur'].queryset = Utilisateur.objects.none()
            self.fields['chauffeur'].widget.attrs['disabled'] = 'disabled'
        
        # Nous n'utilisons pas de champ calculé dans le formulaire pour éviter les erreurs
        # Le calcul sera fait côté JavaScript dans le template
    
    def clean(self):
        cleaned_data = super().clean()
        station = cleaned_data.get('station')
        nom_station = cleaned_data.get('nom_station')
        
        # Validation : au moins une station doit être sélectionnée ou un nom saisi
        if not station and not nom_station:
            raise forms.ValidationError(
                "Veuillez sélectionner une station ou saisir un nom de station."
            )
            
        # Si une station est sélectionnée, ignorer le champ nom_station
        if station:
            cleaned_data['nom_station'] = station.nom
            
        # Validation des kilométrages
        km_avant = cleaned_data.get('kilometrage_avant')
        km_apres = cleaned_data.get('kilometrage_apres')
        
        if km_avant is not None and km_apres is not None and km_apres <= km_avant:
            raise forms.ValidationError(
                "Le kilométrage après doit être supérieur au kilométrage avant."
            )
            
        # Calcul automatique du coût total
        litres = cleaned_data.get('litres')
        cout_unitaire = cleaned_data.get('cout_unitaire')
        
        if litres is not None and cout_unitaire is not None:
            cleaned_data['cout_total'] = round(litres * cout_unitaire, 2)
            
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.createur:
            instance.createur = self.createur
            if not hasattr(instance, 'etablissement'):
                instance.etablissement = self.createur.etablissement
                
        if commit:
            instance.save()
        return instance


class StationForm(forms.ModelForm):
    """Formulaire pour la création et modification des stations de ravitaillement"""
    
    class Meta:
        model = Station
        fields = ['nom', 'adresse', 'ville', 'code_postal', 'pays', 'telephone', 'email', 'est_active']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nom de la station')
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Adresse complète')
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Ville')
            }),
            'code_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Code postal')
            }),
            'pays': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Pays')
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Téléphone')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Adresse email')
            }),
            'est_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'nom': _('Nom de la station'),
            'adresse': _('Adresse'),
            'ville': _('Ville'),
            'code_postal': _('Code postal'),
            'pays': _('Pays'),
            'telephone': _('Téléphone'),
            'email': _('Email'),
            'est_active': _('Station active'),
        }
        help_texts = {
            'est_active': _('Décochez cette case pour désactiver la station sans la supprimer'),
        }
    
    def __init__(self, *args, **kwargs):
        self.etablissement = kwargs.pop('etablissement', None)
        super().__init__(*args, **kwargs)
        
        # Si c'est une nouvelle station, on la marque comme active par défaut
        if not self.instance.pk:
            self.fields['est_active'].initial = True
            
        # Si un établissement est fourni, on l'utilise
        if self.etablissement and not self.instance.etablissement_id:
            self.instance.etablissement = self.etablissement
    
    def clean_nom(self):
        """Vérifie que le nom de la station est unique pour cet établissement"""
        nom = self.cleaned_data['nom']
        qs = Station.objects.filter(nom__iexact=nom, etablissement=self.etablissement)
        
        # Si on est en mode édition, on exclut l'instance actuelle
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise forms.ValidationError(
                _('Une station avec ce nom existe déjà pour cet établissement.')
            )
            
        return nom
    
    def clean_telephone(self):
        """Nettoie et valide le numéro de téléphone"""
        telephone = self.cleaned_data.get('telephone', '').strip()
        if telephone and not telephone.startswith('+'):
            # Si le numéro ne commence pas par +, on essaie de formater
            telephone = telephone.replace(' ', '').replace('.', '').replace('-', '')
            if telephone.startswith('0'):
                telephone = '+243' + telephone[1:]  # Format pour la RDC
        return telephone
    
    def save(self, commit=True):
        """Sauvegarde la station avec l'établissement si nécessaire"""
        if self.etablissement and not self.instance.etablissement_id:
            self.instance.etablissement = self.etablissement
            
        instance = super().save(commit=commit)
        return instance
