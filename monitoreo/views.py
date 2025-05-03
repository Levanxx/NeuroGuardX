from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm

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