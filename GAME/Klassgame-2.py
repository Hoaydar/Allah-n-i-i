from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
import asyncio
import time

url = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold"
my_token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'
my_chat_id = -1002209424495

async def send(msg, chat_id, token=my_token):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)

async def main():
    while True:
        driver = webdriver.Chrome()
        driver.get(url)

        # Find all elements matching the class name
        buttons = driver.find_elements(By.CLASS_NAME, "product-sell.button-top-animation")
        correct_button = None

        # Loop through the buttons to find the correct one
        for button in buttons:
            href = button.get_attribute('href')
            if href == 'https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-10-gb':
                correct_button = button
                break  # Exit the loop once the correct button is found

        # Ensure correct_button is not None before accessing its attributes
        if correct_button:
            onclick = correct_button.get_attribute('onclick')
            if onclick == "message('Şu an için alış aktif görünmüyor, lütfen daha sonra tekrar deneyiniz.', 'danger'); return false;":
                print('devam etmeli')
            else:
                await send(msg='data', chat_id=my_chat_id, token=my_token)
        else:
            print('10-gb buton bulunamadı')

        driver.quit()
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())