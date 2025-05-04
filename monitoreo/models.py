from django.db import models

TIPO_EVENTO_CHOICES = [
    ('ataque', 'Ataque'),
    ('anomalia', 'Anomalía'),
]

DISPOSITIVOS_CHOICES = [
    ('', '---------'),  # <- valor vacío por defecto
    ('Almohada', 'Almohada Inteligente'),
    ('Anillo', 'Anillo Inteligente'),
    ('Watch', 'Smartwatch'),
]

class Evento(models.Model):
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES)
    fecha = models.DateField()
    hora = models.TimeField()
    dispositivo = models.CharField(max_length=50, choices=DISPOSITIVOS_CHOICES, blank=False)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha} - {self.hora}"