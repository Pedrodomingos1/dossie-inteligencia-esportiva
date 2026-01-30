import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class AnalistaIA:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def gerar_veredito(self, tema):
        prompt = f"Gere um dossiê estatístico curto sobre {tema}. Inclua: últimos 5 jogos, média de gols e escanteios. Não use IA para inventar, busque dados reais."
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            return response.text if response.text else "🛡️ Sem dados disponíveis."
        except Exception as e:
            return f"🛡️ Erro de conexão: {e}"