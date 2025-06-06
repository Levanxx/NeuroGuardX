from django.db import models

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

    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO)
    criticidad = models.CharField(max_length=10, choices=CRITICIDAD, default='moderado')
    fecha = models.DateField()
    hora = models.TimeField()
    dispositivo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.get_tipo_display()} ({self.fecha})"