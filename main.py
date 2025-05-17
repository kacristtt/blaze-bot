import time
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = "8047337853:AAGizHiBxQSrrUl8IQw-TX9Zjz86PcJGhlU"
CHAT_ID = "6821521589"

def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Erro ao enviar alerta: {e}")

def analisar_resultados(cores):
    if 'white' not in cores[-7:]:
        return "⚪ Apostar no BRANCO"
    if cores[-3:] == ['red', 'red', 'red']:
        return "⚫ Apostar no PRETO"
    if cores[-3:] == ['black', 'black', 'black']:
        return "🔴 Apostar no VERMELHO"
    return "🔄 Sem sinal agora"

def coletar_cores():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()
        pagina.goto("https://blaze.bet.br/pt/games/double", timeout=60000)
        pagina.wait_for_timeout(5000)
        try:
            bolas = pagina.query_selector_all(".entries .entry")
            cores = []
            for bola in bolas[-8:]:
                cor = bola.get_attribute("class")
                if "white" in cor:
                    cores.append("white")
                elif "red" in cor:
                    cores.append("red")
                elif "black" in cor:
                    cores.append("black")
            navegador.close()
            return cores
        except Exception as e:
            navegador.close()
            print(f"Erro ao coletar cores: {e}")
            return []

def run():
    cores = coletar_cores()
    if cores:
        print("Últimas cores:", cores)
        sinal = analisar_resultados(cores)
        print("Sinal:", sinal)
        enviar_alerta(f"SINAL DO BLAZE DOUBLE\n\nÚltimas: {cores}\n➡️ {sinal}")
    else:
        print("Não foi possível coletar as cores.")

while True:
    try:
        run()
    except Exception as e:
        print(f"Erro inesperado: {e}")
    time.sleep(20)
