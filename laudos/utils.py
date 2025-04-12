import os
from openai import OpenAI
from PyPDF2 import PdfReader
from django.conf import settings

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'api-key here'))

def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def analyze_laudo_with_gpt4(text):
    """Analyze laudo text using GPT-4o mini to identify critical values and generate alerts."""
    prompt = f"""
    Você é um assistente médico especializado em análise de laudos. Analise o seguinte laudo e identifique valores críticos ou alterados que necessitem de atenção médica imediata.

    Regras:
    1. Identifique apenas valores realmente críticos ou significativamente alterados
    2. Para cada valor crítico, forneça:
       - O valor encontrado
       - O valor de referência normal
       - Uma descrição clara do problema
    3. Se não houver valores críticos, retorne apenas "NENHUM_ALERTA"

    Formato da resposta:
    NIVEL: [CRITICO/MODERADO/BAIXO]
    VALOR_ALTERADO: [valor encontrado]
    VALOR_REFERENCIA: [valor de referência]
    DESCRICAO: [descrição do problema]

    Laudo:
    {text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente médico especializado em análise de laudos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error analyzing laudo with GPT-4o mini: {str(e)}")

def parse_gpt4_response(response):
    """Parse GPT-4o mini response into structured data."""
    if "NENHUM_ALERTA" in response:
        return None

    try:
        lines = response.split('\n')
        data = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()

        return {
            'nivel': data.get('NIVEL', 'BAIXO'),
            'valor_alterado': data.get('VALOR_ALTERADO', ''),
            'valor_referencia': data.get('VALOR_REFERENCIA', ''),
            'descricao': data.get('DESCRICAO', '')
        }
    except Exception as e:
        raise Exception(f"Error parsing GPT-4o mini response: {str(e)}") 