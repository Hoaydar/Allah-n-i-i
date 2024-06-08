from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
import time

url = "https://www.klasgame.com/mmorpg-oyunlar/knight-unity/knight-unity-goldbar"
my_token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'
my_chat_id = -1002209424495

def send(msg, chat_id, token=my_token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

service = Service('/path/to/chromedriver')  # Chromedriver yolunu buraya girin
options = Options()
options.headless = True  # Başsız tarayıcı modunu etkinleştirir

while True:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    try:
        # Belirli bir elementi bekle
        wait = WebDriverWait(driver, 10)
        xpath = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='urunler']/div[4]/div[1]/div[3]/div[2]/div[2]/div/div[1]/div[5]/a")))
        href = xpath.get_attribute('href')

        # Href kontrolü ve mesaj gönderme
        if href:
            send(msg=href, chat_id=my_chat_id, token=my_token)
        else:
            print("Href değeri 'false' veya 'a' etiketi bulunamadı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

    driver.quit()
    time.sleep(5)
