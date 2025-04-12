from django.contrib import admin
from .models import Paciente, Laudo, Alerta

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento', 'created_at')
    search_fields = ('nome',)
    list_filter = ('created_at',)

@admin.register(Laudo)
class LaudoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo_exame', 'data_exame', 'status', 'created_at')
    list_filter = ('tipo_exame', 'status', 'created_at')
    search_fields = ('paciente__nome',)
    date_hierarchy = 'data_exame'

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('laudo', 'nivel', 'valor_alterado', 'revisado', 'created_at')
    list_filter = ('nivel', 'revisado', 'created_at')
    search_fields = ('laudo__paciente__nome', 'descricao')
    date_hierarchy = 'created_at'
