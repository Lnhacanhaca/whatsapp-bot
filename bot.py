import datetime
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Função para carregar aniversários do JSON
def get_today_anniversaries():
    with open("casais.json", "r", encoding="utf-8") as file:
        casais = json.load(file)

    hoje = datetime.datetime.today().strftime("%d/%m")  # Formato DD/MM
    aniversariantes = [casal["nome"] for casal in casais if casal["data"][:5] == hoje]

    return aniversariantes

# Configuração do ChromeDriver para WhatsApp Web
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Iniciar navegador
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com")
time.sleep(15)  # Tempo para escanear QR Code na primeira vez

# Verificar aniversários e enviar mensagem no WhatsApp
aniversariantes = get_today_anniversaries()

if aniversariantes:
    grupo = "Grupo da Família"  # Substitua pelo nome real do grupo no WhatsApp
    mensagem = f"🎉 Hoje é o aniversário de casamento de {', '.join(aniversariantes)}! Parabéns! ❤️🎊"

    # Buscar o grupo no WhatsApp
    search_box = driver.find_element(By.XPATH, "//div[@title='Pesquisar ou começar uma nova conversa']")
    search_box.send_keys(grupo)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    # Enviar mensagem no grupo
    campo_mensagem = driver.find_element(By.XPATH, "//div[@title='Mensagem']")
    campo_mensagem.send_keys(mensagem)
    campo_mensagem.send_keys(Keys.ENTER)
    time.sleep(2)

# Fechar navegador
driver.quit()
