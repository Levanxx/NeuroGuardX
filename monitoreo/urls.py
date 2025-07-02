from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('agregar/', views.agregar_evento, name='agregar_evento'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('doctor/login/', views.login_doctor, name='login_doctor'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
