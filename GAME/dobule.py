from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from aiogram import Bot
import asyncio
import traceback

# İkinci site bilgileri
url2 = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold"
chat_id2 = -1002254160124

# Telegram bot token
token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'

async def send_message(msg, chat_id, token):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)
    await bot.close()

async def check_klasgame():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-sell.button-top-animation"))
        )

        buttons = driver.find_elements(By.CSS_SELECTOR, ".product-sell.button-top-animation")
        print(f"Bulunan buton sayısı: {len(buttons)}")

        if len(buttons) < 5:
            print("Klasgame: Beklenen 5 buton bulunamadı")
            return

        button_names = ["AURA", "FENIX", "TERA", "ARES", "ARES"]
        for index, button in enumerate(buttons[:5]):
            onclick = button.get_attribute('onclick')
            print(f"Button {button_names[index]} onclick değeri: {onclick}")

            if onclick and "Şu an için alış aktif görünmüyor" not in onclick:
                msg = f"Klasgame - {button_names[index]}\n\nhttps://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold"
                await send_message(msg=msg, chat_id=chat_id2, token=token)
                break
        else:
            print("Klasgame: Tüm butonlar pasif durumda.")

    except Exception as e:
        print(f"Klasgame için bir hata oluştu: {traceback.format_exc()}")
    finally:
        driver.quit()

async def main():
    while True:
        await asyncio.gather(
            check_klasgame()
        )
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())