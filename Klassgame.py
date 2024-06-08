from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import telegram
import time
import asyncio

url = "https://www.klasgame.com/mmorpg-oyunlar/knight-unity/knight-unity-goldbar"
my_token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'
my_chat_id = -1002209424495

def send(msg, chat_id, token=my_token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

while True:
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    xpath = driver.find_element(By.XPATH, "//*[@id='urunler']/div[4]/div[1]/div[3]/div[2]/div[2]/div/div[1]/div[5]/a")
    data = xpath.get_attribute('href')
    onclick = xpath.get_attribute('onclick')
    if onclick == None:
        asyncio.run(send(msg='data', chat_id=my_chat_id, token=my_token))

    driver.quit()
    time.sleep(5)
