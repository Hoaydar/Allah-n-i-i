from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import telegram
import time

url = "https://www.klasgame.com/mmorpg-oyunlar/knight-unity/knight-unity-goldbar"
my_token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'
my_chat_id = -1002209424495

def send(msg, chat_id, token=my_token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

a = 1

while a > 0:
    driver = webdriver.Chrome()
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    a_tag = soup.find('a', class_='product-sell')

    # 'a' etiketinin href özelliğini alarak kontrol etme
    if a_tag.get('onclick') != "message('Şu an için alış aktif görünmüyor, lütfen daha sonra tekrar deneyiniz.', 'danger'); return false;":
        send(msg=a_tag['href'], chat_id=my_chat_id, token=my_token)
    else:
        print("Href değeri 'false' veya 'a' etiketi bulunamadı.")

    driver.quit()
    time.sleep(5)