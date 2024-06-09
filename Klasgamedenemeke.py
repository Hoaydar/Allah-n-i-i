from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
import asyncio
import time

url = "https://www.klasgame.com/mmorpg-oyunlar/knight-unity/knight-unity-goldbar"
my_token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'
my_chat_id = -1002209424495

async def send(msg, chat_id, token=my_token):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)

async def main():
    while True:
        driver = webdriver.Chrome()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        xpath = driver.find_element(By.CLASS_NAME, " product-sell button-top-animation")
        data = xpath.get_attribute('href')
        onclick = xpath.get_attribute('onclick')
        if onclick == "message('Şu an için alış aktif görünmüyor, lütfen daha sonra tekrar deneyiniz.', 'danger'); return false;":
            print('devam etmeli')
        else:
            await send(msg='data', chat_id=my_chat_id, token=my_token)

        driver.quit()
        await asyncio.sleep(45)

if __name__ == "__main__":
    asyncio.run(main())