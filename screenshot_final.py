import os
import uuid
from playwright.sync_api import sync_playwright

def gerar_screenshots_finais():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        # 1. Login
        pagina.goto("http://127.0.0.1:5000/cadastro")
        nome_usuario = f"pro_{str(uuid.uuid4())[:6]}"
        pagina.fill("input[name='username']", nome_usuario)
        pagina.fill("input[name='password']", "senha123")
        pagina.click("button[type='submit']")
        pagina.fill("input[name='username']", nome_usuario)
        pagina.fill("input[name='password']", "senha123")
        pagina.click("button[type='submit']")

        # 2. Dashboard (Dark Mode)
        pagina.wait_for_selector(".container-jogos", timeout=5000)
        pagina.screenshot(path="final_dashboard.png")

        # 3. Dossiê (Simulado)
        # Vamos gerar um dossiê simulado diretamente
        pagina.goto("http://127.0.0.1:5000/dossie/gerar/123/Flamengo_vs_Palmeiras")
        pagina.wait_for_selector(".card", timeout=10000)
        pagina.screenshot(path="final_dossie.png")

        navegador.close()

if __name__ == "__main__":
    gerar_screenshots_finais()
