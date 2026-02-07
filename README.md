# Dossiê Inteligência Esportiva

Um aplicativo web desenvolvido em Flask que permite a analistas esportivos gerarem dossiês e relatórios detalhados sobre partidas de futebol, utilizando dados extraídos em tempo real.

## Funcionalidades

*   **Autenticação de Usuários:** Sistema seguro de registro e login para usuários.
*   **Visualização de Jogos do Dia:** Exibe uma lista dos principais jogos de futebol que ocorrerão no dia.
*   **Geração de Dossiês:** Com um clique, gere um dossiê detalhado com estatísticas de uma partida específica (ex: posse de bola, chutes a gol, etc.).
*   **Histórico de Dossiês:** Os dossiês gerados ficam salvos e associados à conta do usuário para consulta futura.
*   **Coleta de Dados:** Utiliza web scraping para buscar informações do [SofaScore](https://www.sofascore.com/).

## Tecnologia Utilizada

*   **Backend:**
    *   [Flask](https://flask.palletsprojects.com/): Microframework web em Python.
    *   [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/): ORM para interação com o banco de dados.
    *   [Flask-Login](https://flask-login.readthedocs.io/): Gerenciamento de sessões de usuário.
    *   [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/): Hashing de senhas.
    *   [Requests](https://requests.readthedocs.io/): Para realizar as requisições HTTP no scraper.
*   **Frontend:**
    *   HTML5 / CSS3
    *   [Templates Jinja2](https://jinja.palletsprojects.com/)
*   **Banco de Dados:**
    *   SQLite (padrão em desenvolvimento)

## Configuração e Instalação

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

**Pré-requisitos:**
*   Python 3.8+
*   Git

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Pedrodomingos1/dossie-inteligencia-esportiva.git
    cd dossie-inteligencia-esportiva
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv venv
    venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione a seguinte variável. Use uma chave secreta forte.
    ```
    SECRET_KEY='sua_chave_secreta_aqui'
    ```

5.  **Inicie a aplicação:**
    ```bash
    python app.py
    ```
    O aplicativo estará disponível em `http://127.0.0.1:5000`.

## Como Usar

1.  Acesse a página e crie uma conta de usuário.
2.  Faça o login com suas credenciais.
3.  Na dashboard, você verá a lista de jogos do dia.
4.  Clique em "Gerar Dossiê" em um dos jogos para criar e visualizar as estatísticas detalhadas.
5.  Você pode revisitar seus dossiês gerados a qualquer momento a partir da dashboard.