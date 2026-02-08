# Manual do Soberano: Dossiê Inteligência Esportiva

Este documento serve como o guia definitivo para assumir o controle total do sistema de inteligência esportiva. Siga estas ordens para garantir a estabilidade e o sucesso da operação.

---

## 1. Sincronia com o Trono (Git)

Para eliminar qualquer vestígio de código antigo e garantir que sua máquina local esteja perfeitamente alinhada com a versão final e segura da `main`, execute este comando no terminal do seu VS Code:

```bash
git fetch origin && git reset --hard origin/main
```

> **Atenção:** Este comando sobrescreve quaisquer alterações locais não salvas, garantindo uma cópia limpa e fiel do repositório remoto.

---

## 2. Preparação do Terreno (Ambiente)

Antes de iniciar o sistema, certifique-se de que o ambiente está pronto para a batalha.

**Configuração do Ambiente Virtual (Recomendado):**
*   **Windows:** `python -m venv venv` e depois `venv\Scripts\activate`
*   **Mac/Linux:** `python3 -m venv venv` e depois `source venv/bin/activate`

**Instalação das Armas (Dependências):**
Com o ambiente ativado, instale todas as bibliotecas necessárias com um único comando:

```bash
pip install -r requirements.txt
```

---

## 3. Ativação do Coração (Execução)

Para dar vida ao sistema e iniciar o servidor web, execute:

```bash
python run.py
```

Se tudo estiver correto, você verá uma mensagem indicando que o servidor está rodando em `http://127.0.0.1:5000`.

---

## 4. Manual do Usuário (Navegação VIP)

Uma vez que o sistema esteja operante:

1.  **Acesso:** Abra seu navegador e vá para `http://127.0.0.1:5000`.
2.  **Autenticação:** Faça login com suas credenciais de Soberano (ou crie uma nova conta em "Cadastrar" se for o primeiro acesso).
3.  **Painel de Controle:** Você será direcionado ao **Painel Principal**, onde verá a lista de "Jogos de Hoje" (obtidos em tempo real ou simulados se a API estiver indisponível).
4.  **Ação:** Escolha um jogo e clique no botão **"Gerar Dossiê"**.
5.  **O Dossiê Premium:** O sistema processará os dados e a IA gerará o relatório. Role a página para baixo até encontrar o card dourado **"Agente de Inteligência Especializado"**. Ali reside a análise detalhada e humanizada, exclusiva para a operação Enterprise.

---

## 5. Protocolo de Manutenção

Para perpetuar seu legado e salvar melhorias futuras no código, memorize estes três comandos sagrados:

1.  **Preparar:** Adiciona todas as mudanças ao palco.
    ```bash
    git add .
    ```

2.  **Selar:** Cria um registro permanente (commit) do que foi feito.
    ```bash
    git commit -m "Descreva aqui o que você melhorou"
    ```

3.  **Enviar:** Transmite as alterações para o repositório remoto (GitHub).
    ```bash
    git push origin main
    ```

---
**Vitória e Glória.**
