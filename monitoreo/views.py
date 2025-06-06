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

        sesion = request.session

        # Paso 2: Si estamos esperando criticidad
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

                # Limpiar sesión
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

        # Paso 1: Saludos y ayuda
        if 'hola' in pregunta or 'buenas' in pregunta:
            return JsonResponse({'reply': '¡Hola! ¿Quieres registrar un evento o saber el estado del sistema?'})

        if 'gracias' in pregunta:
            return JsonResponse({'reply': '¡Con gusto! Estoy aquí para ayudarte cuando quieras.'})

        if 'quien eres' in pregunta or 'como te llamas' in pregunta:
            return JsonResponse({'reply': 'Soy Nhyrex, el asistente de Levanx AI creado para ayudarte.'})

        if 'funcion' in pregunta or 'puedes hacer' in pregunta or 'reporte' in pregunta:
            return JsonResponse({'reply': 'Puedo registrar eventos, darte reportes y ayudarte con tu monitoreo. Prueba con "Registrar un ataque con el anillo".'})

        # Paso 3: Intento de detección de registro de evento
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

                # Guardar en sesión y esperar criticidad
                sesion['tipo'] = tipo
                sesion['dispositivo'] = dispositivo
                sesion['esperando_criticidad'] = True

                return JsonResponse({'reply': f'¿Qué nivel de criticidad tiene el evento de tipo {tipo}? (leve, moderado o grave)'})

        return JsonResponse({'reply': '¿Quieres registrar un evento? Dime cosas como "Registrar anomalía con el smartwatch".'})

    return JsonResponse({'reply': 'Método no permitido'}, status=405)