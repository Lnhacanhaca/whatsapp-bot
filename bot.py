import time
import json
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Configuração do Chrome Headless para Railway
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa sem interface gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium"  # Caminho do Chrome no Railway

# Caminho do Chromedriver no Railway
chromedriver_path = "/usr/bin/chromedriver"

# Iniciar o WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ler os casais do arquivo JSON
with open("casais.json", "r", encoding="utf-8") as file:
    casais = json.load(file)

# Função para verificar aniversários e enviar mensagens
def enviar_lembrete():
    hoje = datetime.datetime.now().strftime("%d-%m")  # Formato DD-MM
    for casal in casais:
        if casal["data"] == hoje:
            mensagem = f"🎉 Parabéns {casal['nome1']} e {casal['nome2']} pelo seu aniversário de casamento! 🎊"
            
            try:
                driver.get("https://web.whatsapp.com")  # Acessa o WhatsApp Web
                time.sleep(15)  # Tempo para escanear o QR Code (primeira execução)

                # Buscar o grupo
                search_box = driver.find_element(By.XPATH, "//div[@title='Pesquisar ou começar uma nova conversa']")
                search_box.click()
                search_box.send_keys("Nome do Grupo do WhatsApp")  # Substitua pelo nome do grupo
                time.sleep(2)
                search_box.send_keys(Keys.ENTER)

                # Enviar a mensagem
                message_box = driver.find_element(By.XPATH, "//div[@title='Digite uma mensagem']")
                message_box.click()
                message_box.send_keys(mensagem)
                message_box.send_keys(Keys.ENTER)

                print(f"✅ Mensagem enviada para {casal['nome1']} e {casal['nome2']}")
            
            except Exception as e:
                print(f"❌ Erro ao enviar mensagem para {casal['nome1']} e {casal['nome2']}: {str(e)}")

# Rodar o bot diariamente
while True:
    enviar_lembrete()
    time.sleep(86400)  # Espera 24 horas antes do próximo envio