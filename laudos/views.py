from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Laudo, Alerta, Paciente
from .forms import LaudoUploadForm, PacienteForm
from .utils import extract_text_from_pdf, analyze_laudo_with_gpt4, parse_gpt4_response

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
            try:
                # Save the laudo
                laudo = form.save()
                
                # Extract text from PDF
                pdf_text = extract_text_from_pdf(laudo.arquivo_pdf)
                
                # Analyze with GPT-4
                gpt_response = analyze_laudo_with_gpt4(pdf_text)
                
                # Parse the response
                alerta_data = parse_gpt4_response(gpt_response)
                
                if alerta_data:
                    # Create alert if critical values found
                    Alerta.objects.create(
                        laudo=laudo,
                        nivel=alerta_data['nivel'],
                        descricao=alerta_data['descricao'],
                        valor_alterado=alerta_data['valor_alterado'],
                        valor_referencia=alerta_data['valor_referencia']
                    )
                    messages.warning(request, 'Alerta crítico detectado! Verifique o dashboard.')
                else:
                    messages.success(request, 'Laudo processado com sucesso. Nenhum alerta crítico.')
                
                return redirect('laudos:dashboard')
                
            except Exception as e:
                print(f"Erro ao processar o laudo: {str(e)}")
                messages.error(request, f'Erro ao processar o laudo: {str(e)}')
                return redirect('laudos:upload_laudo')
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
