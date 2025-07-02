from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Evento, Doctor
from .forms import EventoForm
import datetime
import json

# VISTA: Listar eventos
def lista_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha', '-hora')
    return render(request, 'monitoreo/lista_eventos.html', {'eventos': eventos})

# VISTA: Agregar evento manualmente
def agregar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('agregar_evento')}?success=1")
    else:
        form = EventoForm()
    return render(request, 'monitoreo/agregar_evento.html', {'form': form})

# VISTA: Chatbot con IA simple
def chatbot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user_message = body.get('message', '').lower().strip()
        except:
            return JsonResponse({'reply': 'Error al procesar el mensaje.'})

        pregunta = user_message \
            .replace('á', 'a').replace('é', 'e') \
            .replace('í', 'i').replace('ó', 'o').replace('ú', 'u') \
            .replace('¿', '').replace('?', '')

        sesion = request.session

        if sesion.get('esperando_criticidad'):
            criticidad = None
            if 'leve' in pregunta:
                criticidad = 'leve'
            elif 'moderado' in pregunta:
                criticidad = 'moderado'
            elif 'grave' in pregunta:
                criticidad = 'grave'

            if criticidad:
                tipo = sesion.get('tipo')
                dispositivo = sesion.get('dispositivo', 'Smartwatch')
                now = datetime.datetime.now()

                evento = Evento.objects.create(
                    tipo=tipo,
                    criticidad=criticidad,
                    fecha=now.date(),
                    hora=now.strftime('%H:%M'),
                    dispositivo=dispositivo
                )

                sesion.pop('esperando_criticidad', None)
                sesion.pop('tipo', None)
                sesion.pop('dispositivo', None)

                return JsonResponse({
                    'reply': f'✅ Evento registrado como {criticidad} con tipo {tipo.capitalize()} y dispositivo {dispositivo}.',
                    'evento_registrado': {
                        'tipo': tipo.capitalize(),
                        'criticidad': criticidad.capitalize(),
                        'fecha': now.strftime('%d de %B de %Y'),
                        'hora': now.strftime('%I:%M %p'),
                        'dispositivo': dispositivo
                    }
                })
            else:
                return JsonResponse({'reply': 'Por favor indica si es leve, moderado o grave.'})

        if 'hola' in pregunta or 'buenas' in pregunta:
            return JsonResponse({'reply': '¡Hola! ¿Quieres registrar un evento o saber el estado del sistema?'})

        if 'gracias' in pregunta:
            return JsonResponse({'reply': '¡Con gusto! Estoy aquí para ayudarte cuando quieras.'})

        if 'quien eres' in pregunta or 'como te llamas' in pregunta:
            return JsonResponse({'reply': 'Soy Nhyrex, el asistente de Levanx AI creado para ayudarte.'})

        if 'funcion' in pregunta or 'puedes hacer' in pregunta or 'reporte' in pregunta:
            return JsonResponse({'reply': 'Puedo registrar eventos, darte reportes y ayudarte con tu monitoreo. Prueba con "Registrar un ataque con el anillo".'})

        if 'registrar' in pregunta or 'registra' in pregunta or 'añadir' in pregunta or 'agrega' in pregunta:
            tipo = None
            if 'anomalia' in pregunta:
                tipo = 'anomalia'
            elif 'ataque' in pregunta:
                tipo = 'ataque'
            elif 'chequeo' in pregunta or 'normal' in pregunta:
                tipo = 'normal'

            if tipo:
                dispositivo = 'Smartwatch'
                if 'almohada' in pregunta:
                    dispositivo = 'Almohada Inteligente'
                elif 'anillo' in pregunta:
                    dispositivo = 'Anillo Inteligente'

                sesion['tipo'] = tipo
                sesion['dispositivo'] = dispositivo
                sesion['esperando_criticidad'] = True

                return JsonResponse({'reply': f'¿Qué nivel de criticidad tiene el evento de tipo {tipo}? (leve, moderado o grave)'})

        return JsonResponse({'reply': '¿Quieres registrar un evento? Dime cosas como "Registrar anomalía con el smartwatch".'})

    return JsonResponse({'reply': 'Método no permitido'}, status=405)

# VISTA: Login exclusivo para doctores
def login_doctor(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                doctor = Doctor.objects.get(user=user)
                login(request, user)
                return redirect('/doctor/dashboard/?success=1')
            except Doctor.DoesNotExist:
                error = 'Este usuario no tiene perfil de doctor.'
        else:
            error = 'Usuario o contraseña incorrectos.'

    return render(request, 'monitoreo/login_doctor.html', {'error': error})

# VISTA: Panel del doctor (estilo index, con filtros y opción de exportar)
@login_required
def doctor_dashboard(request):
    eventos = Evento.objects.all().order_by('-fecha', '-hora')
    return render(request, 'monitoreo/doctor_dashboard.html', {'eventos': eventos})

# VISTA: Cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('login_doctor')
