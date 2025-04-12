from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_laudo, name='upload_laudo'),
    path('alerta/<int:alerta_id>/', views.detalhe_alerta, name='detalhe_alerta'),
    path('paciente/novo/', views.cadastrar_paciente, name='cadastrar_paciente'),
] 