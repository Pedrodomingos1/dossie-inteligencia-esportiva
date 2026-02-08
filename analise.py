import math
import random
import json
import os
import requests

def calcular_valor_esperado(probabilidade_estimada, odd_casa, valor_apostado=1.0):
    """
    Calcula o Valor Esperado (EV) de uma aposta.

    Fórmula: EV = (Probabilidade * Lucro) - (Probabilidade de Perda * Valor Apostado)

    Args:
        probabilidade_estimada (float): Probabilidade de vencer (0.0 a 1.0).
        odd_casa (float): Odd oferecida pela casa de apostas (decimal).
        valor_apostado (float): Valor da aposta (padrão 1.0 unidade).

    Returns:
        float: O valor esperado da aposta.
    """
    lucro_potencial = (odd_casa - 1) * valor_apostado
    probabilidade_perda = 1.0 - probabilidade_estimada

    ev = (probabilidade_estimada * lucro_potencial) - (probabilidade_perda * valor_apostado)
    return ev

class AnalistaIA:
    def __init__(self):
        # Aqui você configuraria a API Key de um LLM real (OpenAI, Anthropic, etc.)
        self.api_key = os.getenv('LLM_API_KEY')
        self.api_url = os.getenv('LLM_API_URL', 'https://api.openai.com/v1/chat/completions') # Exemplo

    def analisar_partida(self, dados_partida):
        """
        Envia os dados da partida para uma IA e retorna uma análise estruturada.

        Args:
            dados_partida (dict): Estatísticas e informações do jogo.

        Returns:
            dict: JSON contendo grau_de_confianca, justificativa e placar_provavel.
        """
        prompt = self._construir_prompt(dados_partida)

        # Simulação para desenvolvimento sem custo de API
        if not self.api_key:
            return self._simular_analise(dados_partida)

        # Implementação real (exemplo genérico)
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo", # Ou o modelo de sua preferência
                "messages": [
                    {"role": "system", "content": "Você é um especialista em estatística esportiva. Responda apenas com JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            resposta = requests.post(self.api_url, json=payload, headers=headers)
            resposta.raise_for_status()
            resultado = resposta.json()['choices'][0]['message']['content']
            return json.loads(resultado)
        except Exception as e:
            print(f"Erro na análise de IA: {e}")
            return self._simular_analise(dados_partida)

    def _construir_prompt(self, dados):
        return f"""
        Analise a seguinte partida de futebol com base nas estatísticas fornecidas:
        {json.dumps(dados, indent=2)}

        Retorne um JSON com os seguintes campos:
        - grau_de_confianca (0 a 100, inteiro)
        - justificativa (string, breve explicação em português)
        - placar_provavel (string, ex: "2-1")
        - probabilidade_vitoria_casa (0.0 a 1.0, float)
        """

    def _simular_analise(self, dados):
        """Simula uma resposta da IA para fins de teste e desenvolvimento."""
        # Lógica simples baseada em quem tem mais posse de bola ou chutes, apenas para variar o resultado
        stats = dados.get('estatisticas', {})
        posse = stats.get('Ball possession', {'casa': '50%', 'fora': '50%'})

        try:
            posse_casa = int(posse['casa'].replace('%', ''))
        except:
            posse_casa = 50

        confianca = random.randint(60, 90)
        prob_vitoria = posse_casa / 100.0

        placar_casa = random.randint(0, 3)
        placar_fora = random.randint(0, 2)

        if posse_casa > 60:
            justificativa = "O time da casa domina a posse de bola e cria mais oportunidades, indicando forte favoritismo."
            placar_casa = max(placar_casa, placar_fora + 1)
        elif posse_casa < 40:
            justificativa = "O time visitante tem controlado o jogo, explorando bem os contra-ataques."
            placar_fora = max(placar_fora, placar_casa + 1)
        else:
            justificativa = "Partida equilibrada com chances para ambos os lados, tendência de empate ou vitória apertada."

        return {
            "grau_de_confianca": confianca,
            "justificativa": justificativa,
            "placar_provavel": f"{placar_casa}-{placar_fora}",
            "probabilidade_vitoria_casa": round(prob_vitoria, 2)
        }
