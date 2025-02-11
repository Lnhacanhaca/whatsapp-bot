import time
import json
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Configuração do Chrome Headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa sem interface gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Iniciar o WebDriver (Selenium Manager gerencia o ChromeDriver automaticamente)
driver = webdriver.Chrome(options=chrome_options)
print("✅ ChromeDriver iniciado com sucesso!")

# Ler os casais do arquivo JSON
with open("casais.json", "r", encoding="utf-8") as file:
    casais = json.load(file)

# Função para enviar mensagens no WhatsApp
def enviar_mensagem_whatsapp(mensagem, nome_grupo):
    try:
        print("🔍 Acessando o WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        time.sleep(15)  # Tempo para escanear o QR Code

        print(f"🔍 Procurando o grupo: {nome_grupo}")
        search_box = driver.find_element(By.XPATH, "//div[@title='Pesquisar ou começar uma nova conversa']")
        search_box.click()
        search_box.send_keys(nome_grupo)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)

        print("📤 Enviando mensagem...")
        message_box = driver.find_element(By.XPATH, "//div[@title='Digite uma mensagem']")
        message_box.click()
        message_box.send_keys(mensagem)
        message_box.send_keys(Keys.ENTER)

        print("✅ Mensagem enviada com sucesso!")
    except NoSuchElementException as e:
        print(f"❌ Elemento não encontrado: {str(e)}")
    except TimeoutException as e:
        print(f"❌ Timeout ao tentar acessar o WhatsApp Web: {str(e)}")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

# Função principal para verificar aniversários e enviar mensagens
def enviar_lembrete():
    try:
        print("📅 Verificando aniversários de casamento...")
        hoje = datetime.datetime.now().strftime("%d-%m")  # Formato DD-MM

        for casal in casais:
            if casal["data"] == hoje:
                mensagem = f"🎉 Parabéns {casal['nome1']} e {casal['nome2']} pelo seu aniversário de casamento! 🎊"
                print(f"💌 Preparando mensagem para {casal['nome1']} e {casal['nome2']}...")
                enviar_mensagem_whatsapp(mensagem, "Nome do Grupo do WhatsApp")  # Substitua pelo nome do grupo
    except FileNotFoundError:
        print("❌ Arquivo 'casais.json' não encontrado.")
    except json.JSONDecodeError:
        print("❌ Erro ao ler o arquivo 'casais.json'. Verifique o formato do JSON.")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

# Loop principal do bot
def main():
    try:
        while True:
            enviar_lembrete()
            print("⏳ Aguardando 24 horas para a próxima verificação...")
            time.sleep(86400)  # Espera 24 horas
    except KeyboardInterrupt:
        print("🛑 Bot interrompido pelo usuário.")
    finally:
        print("🚪 Fechando o ChromeDriver...")
        driver.quit()

if __name__ == "__main__":
    main()