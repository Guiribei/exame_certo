# Generated by Django 5.0.2 on 2025-04-12 13:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Laudo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_exame', models.CharField(choices=[('HEMOGRAMA', 'Hemograma'), ('BIOQUIMICA', 'Bioquímica'), ('URINA', 'Urina'), ('IMAGEM', 'Imagem')], max_length=50)),
                ('data_exame', models.DateField()),
                ('arquivo_pdf', models.FileField(upload_to='laudos/')),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('PROCESSANDO', 'Processando'), ('PROCESSADO', 'Processado'), ('ERRO', 'Erro')], default='PENDENTE', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('data_nascimento', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(choices=[('CRITICO', 'Crítico'), ('MODERADO', 'Moderado'), ('BAIXO', 'Baixo')], max_length=20)),
                ('descricao', models.TextField()),
                ('valor_alterado', models.CharField(max_length=100)),
                ('valor_referencia', models.CharField(max_length=100)),
                ('revisado', models.BooleanField(default=False)),
                ('data_revisao', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('revisado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('laudo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laudos.laudo')),
            ],
        ),
        migrations.AddField(
            model_name='laudo',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laudos.paciente'),
        ),
    ]
