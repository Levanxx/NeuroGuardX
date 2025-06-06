from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'title': 'Selecciona el tipo de evento: ataque, anomalía o chequeo general.'
            }),
            'criticidad': forms.Select(attrs={
                'class': 'form-select',
                'title': 'Selecciona el nivel de criticidad del evento.'
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'title': 'Indica la fecha exacta del evento.'
            }),
            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'title': 'Especifica la hora exacta del evento.'
            }),
            'dispositivo': forms.Select(attrs={
                'class': 'form-select',
                'title': 'Selecciona el dispositivo desde el cual se detectó el evento.'
            }),
        }