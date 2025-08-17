from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Utilisateur, ApplicationControl, Etablissement
from django import forms

class UtilisateurCreationForm(UserCreationForm):
    """Formulaire de création d'utilisateur personnalisé"""
    etablissement = forms.ModelChoiceField(queryset=Etablissement.objects.all(), required=True, label="Département", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'telephone', 'adresse', 'photo', 'etablissement')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['etablissement'].queryset = Etablissement.objects.filter(pk=user.etablissement.pk)
            self.fields['etablissement'].initial = user.etablissement
            self.fields['etablissement'].disabled = True
        # Rendre les champs obligatoires plus visibles
        for field_name in ['username', 'email', 'role', 'password1', 'password2']:
            self.fields[field_name].widget.attrs['class'] = 'form-control is-required'
        
        # Ajouter des classes Bootstrap aux autres champs
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                
        # S'assurer que les champs de mot de passe sont bien présents
        if 'password1' not in self.fields or 'password2' not in self.fields:
            raise ValueError("Les champs de mot de passe sont manquants dans le formulaire")

class UtilisateurChangeForm(UserChangeForm):
    """Formulaire de modification d'utilisateur personnalisé"""
    password = None  # Supprimer le champ de mot de passe du formulaire de modification
    
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'telephone', 'adresse', 'photo', 'is_active', 'etablissement')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes Bootstrap à tous les champs
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ApplicationControlForm(forms.ModelForm):
    class Meta:
        model = ApplicationControl
        fields = ['is_open', 'start_datetime', 'end_datetime', 'message']

class AdminPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe administrateur")

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Etablissement
        fields = ['nom', 'type', 'code', 'parent', 'adresse', 'telephone', 'email', 'responsable', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les responsables possibles (admin et dispatch uniquement)
        self.fields['responsable'].queryset = Utilisateur.objects.filter(
            role__in=['admin', 'dispatch']
        )
        # Filtrer les parents possibles (exclure le département actuel et ses enfants)
        if self.instance.pk:
            self.fields['parent'].queryset = Etablissement.objects.exclude(
                pk__in=[self.instance.pk] + [d.pk for d in self.instance.get_all_enfants()]
            )
        else:
            self.fields['parent'].queryset = Etablissement.objects.all()

    def clean_code(self):
        code = self.cleaned_data['code']
        if Etablissement.objects.filter(code=code).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("Ce code est déjà utilisé par un autre département.")
        return code
