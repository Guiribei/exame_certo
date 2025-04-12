from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Laudo, Alerta, Paciente
from .forms import LaudoUploadForm, PacienteForm
import random

# Create your views here.

@login_required
def dashboard(request):
    alertas = Alerta.objects.filter(revisado=False).order_by('-created_at')
    context = {
        'alertas': alertas,
    }
    return render(request, 'laudos/dashboard.html', context)

@login_required
def upload_laudo(request):
    if request.method == 'POST':
        form = LaudoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            laudo = form.save()
            
            # Simulação do processamento de IA
            if random.random() < 0.8:  # 80% de chance de gerar alerta crítico
                Alerta.objects.create(
                    laudo=laudo,
                    nivel='CRITICO',
                    descricao='Valor Crítico Detectado',
                    valor_alterado='Potássio 6.8 mEq/L',
                    valor_referencia='3.5-5.1 mEq/L'
                )
                messages.warning(request, 'Alerta crítico detectado! Verifique o dashboard.')
            else:
                messages.success(request, 'Laudo processado com sucesso. Nenhum alerta crítico.')
            
            return redirect('laudos:dashboard')
    else:
        form = LaudoUploadForm()
    
    return render(request, 'laudos/upload_laudo.html', {'form': form})

@login_required
def detalhe_alerta(request, alerta_id):
    alerta = get_object_or_404(Alerta, id=alerta_id)
    
    if request.method == 'POST' and 'marcar_revisado' in request.POST:
        alerta.marcar_como_revisado(request.user)
        messages.success(request, 'Alerta marcado como revisado com sucesso.')
        return redirect('laudos:dashboard')
    
    context = {
        'alerta': alerta,
    }
    return render(request, 'laudos/detalhe_alerta.html', context)

@login_required
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('laudos:upload_laudo')
    else:
        form = PacienteForm()
    
    return render(request, 'laudos/cadastrar_paciente.html', {'form': form})
