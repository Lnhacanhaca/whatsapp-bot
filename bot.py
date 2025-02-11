import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do Chrome Headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa sem interface gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium"  # Caminho para o Chromium no Railway

# Carregar lista de casais e aniversários do arquivo JSON
with open("casais.json", "r", encoding="utf-8") as file:
    casais = json.load(file)

# Nome do grupo do WhatsApp onde a mensagem será enviada
WHATSAPP_GROUP = "Grupo da Família"  # 🔴 ALTERE para o nome exato do grupo no WhatsApp

# Função para enviar mensagem no WhatsApp Web
def enviar_mensagem(mensagem):
    try:
        # Inicia o navegador
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://web.whatsapp.com")

        # Aguarda o usuário escanear o QR Code
        input("🔹 Escaneie o QR Code e pressione Enter para continuar...")

        # Buscar o grupo no WhatsApp
        search_box = driver.find_element(By.XPATH, "//div[@title='Pesquisar ou começar uma nova conversa']")
        search_box.click()
        search_box.send_keys(WHATSAPP_GROUP)
        time.sleep(2)  # Aguarde o carregamento

        # Seleciona o grupo
        group = driver.find_element(By.XPATH, f"//span[@title='{WHATSAPP_GROUP}']")
        group.click()

        # Envia a mensagem
        message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
        message_box.send_keys(mensagem)
        message_box.send_keys(Keys.RETURN)  # Pressiona "Enter"
        print(f"✅ Mensagem enviada para o grupo: {WHATSAPP_GROUP}")

    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
    finally:
        driver.quit()

# Função para verificar aniversários e enviar mensagens
def verificar_aniversarios():
    hoje = datetime.today().strftime("%d-%m")  # Formato "dia-mês"
    for casal in casais:
        if casal["data"] == hoje:
            mensagem = f"🎉 Parabéns {casal['nomes']} pelo aniversário de casamento! 🥂🎊"
            enviar_mensagem(mensagem)

# Loop diário para verificar aniversários e enviar mensagens
while True:
    verificar_aniversarios()
    time.sleep(86400)  # Espera 24 horas antes de verificar novamente
