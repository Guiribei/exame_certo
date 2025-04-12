# ExameCerto - IA Clínica Sentinela

Sistema inteligente de gestão e processamento de laudos de exames complementares.

## Setup do Ambiente

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações:
```bash
python manage.py migrate
```

4. Crie um superusuário:
```bash
python manage.py createsuperuser
```

5. Execute o servidor:
```bash
python manage.py runserver
```

## Funcionalidades Principais

- Upload de laudos em PDF
- Processamento inteligente de laudos
- Dashboard médico com alertas críticos
- Visualização detalhada de alertas com explicabilidade
- Sistema de marcação de alertas como revisados
