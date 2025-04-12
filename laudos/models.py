from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Laudo(models.Model):
    TIPO_EXAME_CHOICES = [
        ('HEMOGRAMA', 'Hemograma'),
        ('BIOQUIMICA', 'Bioquímica'),
        ('URINA', 'Urina'),
        ('IMAGEM', 'Imagem'),
    ]

    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PROCESSANDO', 'Processando'),
        ('PROCESSADO', 'Processado'),
        ('ERRO', 'Erro'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo_exame = models.CharField(max_length=50, choices=TIPO_EXAME_CHOICES)
    data_exame = models.DateField()
    arquivo_pdf = models.FileField(upload_to='laudos/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_exame} - {self.paciente.nome} - {self.data_exame}"

class Alerta(models.Model):
    NIVEL_CHOICES = [
        ('CRITICO', 'Crítico'),
        ('MODERADO', 'Moderado'),
        ('BAIXO', 'Baixo'),
    ]

    laudo = models.ForeignKey(Laudo, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    descricao = models.TextField()
    valor_alterado = models.CharField(max_length=100)
    valor_referencia = models.CharField(max_length=100)
    revisado = models.BooleanField(default=False)
    revisado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_revisao = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def marcar_como_revisado(self, usuario):
        self.revisado = True
        self.revisado_por = usuario
        self.data_revisao = timezone.now()
        self.save()

    def __str__(self):
        return f"Alerta {self.nivel} - {self.laudo}"
