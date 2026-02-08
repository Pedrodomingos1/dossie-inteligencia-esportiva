# Dossiê Inteligência Esportiva - Enterprise & PWA

**Versão 2.0 (Mobile-First)**

Um sistema robusto e modular para análise de futebol, construído com arquitetura profissional em Python/Flask e otimizado como Progressive Web App (PWA) para instalação em dispositivos móveis.

## Funcionalidades Principais

*   **Arquitetura Enterprise:** Código limpo e desacoplado, separando lógica de apresentação (`web/`), serviços de integração (`services/`) e estratégias de cálculo (`strategies/`).
*   **PWA Nativo:** Instale diretamente no Android/iOS. Funciona offline (Service Worker), tem ícone dedicado e design adaptativo.
*   **Análise +EV:** Algoritmos proprietários para cálculo de Valor Esperado positivo em apostas.
*   **Integração IA:** Simulação de analista esportivo com geração de insights automáticos.
*   **Design Responsivo:** Interface "Dark Mode" otimizada para uso com uma mão em telas de smartphones.

## Estrutura do Projeto

*   `run.py`: Ponto único de entrada da aplicação.
*   `web/`: Camada de apresentação (Flask App, Templates, Static, Rotas).
    *   `modelos.py`: Definições do banco de dados (SQLAlchemy).
    *   `rotas.py`: Definição de endpoints e views.
*   `services/`: Integrações externas.
    *   `raspagem.py`: Coleta de dados (SofaScore).
    *   `ia.py`: Inteligência Artificial para análise.
    *   `notificacao.py`: Envio de alertas (Telegram).
*   `strategies/`: Lógica de negócios pura.
    *   `analise.py`: Motor de cálculo estatístico.

## Como Rodar

**Pré-requisitos:** Python 3.10+

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure o ambiente:**
    Crie um arquivo `.env` na raiz (opcional, o sistema usa defaults seguros para dev).

3.  **Execute a aplicação:**
    ```bash
    python run.py
    ```
    Acesse em: `http://127.0.0.1:5000`

## Instalação Mobile (PWA)

1.  Acesse a URL do sistema pelo navegador do celular (Chrome/Safari).
2.  Toque em "Compartilhar" (iOS) ou Menu (Android).
3.  Selecione **"Adicionar à Tela de Início"**.
4.  O Dossiê será instalado como um aplicativo nativo.

---
Desenvolvido por **Pedro Domingos** | Jessé Produções
