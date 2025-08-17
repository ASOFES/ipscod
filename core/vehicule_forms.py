from django import forms
from django.utils import timezone
from .models import Vehicule, Etablissement

class VehiculeForm(forms.ModelForm):
    """Formulaire pour la création et modification de véhicules"""
    etablissement = forms.ModelChoiceField(queryset=Etablissement.objects.all(), required=True, label="Département", widget=forms.Select(attrs={'class': 'form-control'}))
    date_expiration_assurance = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date
    )
    date_expiration_controle_technique = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date
    )
    date_expiration_vignette = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date
    )
    date_expiration_stationnement = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date
    )
    
    class Meta:
        model = Vehicule
        fields = [
            'etablissement',
            'immatriculation', 'marque', 'modele', 'couleur', 'numero_chassis', 'image',
            'date_expiration_assurance', 'date_expiration_controle_technique',
            'date_expiration_vignette', 'date_expiration_stationnement'
        ]
        widgets = {
            'immatriculation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: AB-123-CD'}),
            'marque': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Toyota'}),
            'modele': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Corolla'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Bleu'}),
            'numero_chassis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: VF1234567890'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.createur = kwargs.pop('createur', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['etablissement'].queryset = Etablissement.objects.filter(pk=user.etablissement.pk)
            self.fields['etablissement'].initial = user.etablissement
            self.fields['etablissement'].disabled = True
        
        # Ajouter des labels plus descriptifs
        self.fields['immatriculation'].label = "Immatriculation"
        self.fields['marque'].label = "Marque"
        self.fields['modele'].label = "Modèle"
        self.fields['couleur'].label = "Couleur"
        self.fields['numero_chassis'].label = "Numéro de châssis"
        self.fields['image'].label = "Image du véhicule"
        self.fields['date_expiration_assurance'].label = "Date d'expiration de l'assurance"
        self.fields['date_expiration_controle_technique'].label = "Date d'expiration du contrôle technique"
        self.fields['date_expiration_vignette'].label = "Date d'expiration de la vignette"
        self.fields['date_expiration_stationnement'].label = "Date d'expiration du stationnement"
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.createur:
            instance.createur = self.createur
        if commit:
            instance.save()
        return instance

class VehiculeChangeEtablissementForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['etablissement']
