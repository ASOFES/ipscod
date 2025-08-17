from django import forms
from core.models import Utilisateur, Vehicule

class TraiterDemandeForm(forms.Form):
    """Formulaire pour le traitement des demandes de mission par le dispatcher"""
    DECISION_CHOICES = (
        ('', 'Sélectionnez une décision'),
        ('valider', 'Valider la demande'),
        ('refuser', 'Refuser la demande'),
    )
    
    decision = forms.ChoiceField(
        label="Décision",
        choices=DECISION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    chauffeur = forms.ModelChoiceField(
        label="Chauffeur",
        queryset=Utilisateur.objects.filter(role='chauffeur', is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    vehicule = forms.ModelChoiceField(
        label="Véhicule",
        queryset=Vehicule.objects.all(),  # Ce queryset sera remplacé dynamiquement dans la vue
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    commentaire = forms.CharField(
        label="Commentaire",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        decision = cleaned_data.get('decision')
        chauffeur = cleaned_data.get('chauffeur')
        vehicule = cleaned_data.get('vehicule')
        
        if decision == 'valider':
            if not chauffeur:
                self.add_error('chauffeur', 'Vous devez sélectionner un chauffeur pour valider la demande.')
            
            if not vehicule:
                self.add_error('vehicule', 'Vous devez sélectionner un véhicule pour valider la demande.')
        
        return cleaned_data
