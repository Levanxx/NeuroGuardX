from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    TIPO_EVENTO = [
        ('ataque', 'Ataque'),
        ('anomalia', 'Anomalía'),
        ('normal', 'Chequeo General'),
    ]

    CRITICIDAD = [
        ('leve', 'Leve'),
        ('moderado', 'Moderado'),
        ('grave', 'Grave'),
    ]

    DISPOSITIVO_CHOICES = [
        ('smartwatch', 'Smartwatch'),
        ('anillo', 'Anillo Inteligente'),
        ('almohada', 'Almohada Inteligente'),
    ]

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_EVENTO,
        verbose_name='Tipo de Evento'
    )

    criticidad = models.CharField(
        max_length=10,
        choices=CRITICIDAD,
        default='moderado',
        verbose_name='Nivel de Criticidad'
    )

    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')

    dispositivo = models.CharField(
        max_length=50,
        choices=DISPOSITIVO_CHOICES,
        verbose_name='Dispositivo'
    )

    def __str__(self):
        return f"{self.get_tipo_display()} ({self.fecha})"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    turno = models.CharField(max_length=50, choices=[('mañana', 'Mañana'), ('tarde', 'Tarde'), ('noche', 'Noche')])
    numero_colegiatura = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.especialidad}"
