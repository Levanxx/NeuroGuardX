from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Evento
from .forms import EventoForm
import datetime
import json

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('-fecha', '-hora')
    return render(request, 'monitoreo/lista_eventos.html', {'eventos': eventos})

def agregar_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'monitoreo/agregar_evento.html', {'form': form})

def chatbot(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user_message = body.get('message', '').lower().strip()
        except:
            return JsonResponse({'reply': 'Error al procesar el mensaje.'})

        pregunta = user_message \
            .replace('á', 'a').replace('é', 'e') \
            .replace('í', 'i').replace('ó', 'o') \
            .replace('ú', 'u').replace('¿', '').replace('?', '')

        if 'quien eres' in pregunta or 'como te llamas' in pregunta:
            return JsonResponse({'reply': 'Soy Nhyrex, el asistente de Levanx AI creado para ayudarte.'})

        if 'hola' in pregunta or 'buenas' in pregunta:
            return JsonResponse({'reply': '¡Hola! ¿En qué te puedo ayudar?'})

        if 'gracias' in pregunta:
            return JsonResponse({'reply': '¡Con gusto! Estoy aquí para ayudarte cuando quieras.'})

        if 'funcion' in pregunta or 'puedes hacer' in pregunta:
            return JsonResponse({'reply': 'Puedo ayudarte a registrar eventos, mostrar información del sistema y responder preguntas sobre su uso.'})

        if 'registrar' in pregunta or 'registra' in pregunta:
            tipo = None
            if 'anomalia' in pregunta:
                tipo = 'anomalia'
            elif 'ataque' in pregunta:
                tipo = 'ataque'

            if tipo:
                dispositivo = 'Smartwatch'
                if 'almohada' in pregunta:
                    dispositivo = 'Almohada Inteligente'
                elif 'anillo' in pregunta:
                    dispositivo = 'Anillo Inteligente'

                now = datetime.datetime.now()

                evento = Evento.objects.create(
                    tipo=tipo,
                    fecha=now.date(),
                    hora=now.strftime('%H:%M'),
                    dispositivo=dispositivo
                )

                return JsonResponse({
                    'reply': f'Se ha registrado una {tipo} con el {dispositivo}.',
                    'evento_registrado': {
                        'tipo': tipo.capitalize(),
                        'fecha': now.strftime('%B %d, %Y'),
                        'hora': now.strftime('%I:%M %p'),
                        'dispositivo': dispositivo
                    }
                })

        return JsonResponse({'reply': 'No entendí tu mensaje. Intenta con algo como "Registrar una anomalía con el smartwatch".'})

    return JsonResponse({'reply': 'Método no permitido'}, status=405)