from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('agregar/', views.agregar_evento, name='agregar_evento'),
    path('chatbot/', views.chatbot, name='chatbot'),  # Ruta para el chatbot
]