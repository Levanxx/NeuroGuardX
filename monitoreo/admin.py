from django.contrib import admin
from .models import Evento, Doctor

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'criticidad', 'fecha', 'hora', 'dispositivo')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad', 'turno', 'numero_colegiatura')
