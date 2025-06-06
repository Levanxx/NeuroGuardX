from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['tipo', 'criticidad', 'fecha', 'hora', 'dispositivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'criticidad': forms.Select(attrs={'class': 'form-select'}),
            'dispositivo': forms.TextInput(attrs={'class': 'form-control'}),
        }