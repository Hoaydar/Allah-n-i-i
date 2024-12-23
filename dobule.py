from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from aiogram import Bot
import asyncio
import traceback

# İlk site bilgileri
url1 = "https://oyuneks.com/nowa-online-world/nowa-online-world-gold"
chat_id1 = -1002254160124
# İkinci site bilgileri
url2 = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold"
chat_id2 = -1002209424495

# Telegram bot token
token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'

async def send_message(msg, chat_id, token):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)
    await bot.close()

async def check_oyuneks():
    options = Options()
    # options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştırmak için

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url1)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.pageInner > div > div > div.col-sm-7.col-md-9.order-md-2.order-1 > div > div > div > div > div:nth-child(1) > div > div.info > div.buttons > div > div > div.detailBasketNavigateArea > a.basketNavigatePlus.quantityPlusGB"))
        )
        buttonsinteger = driver.find_element(By.CSS_SELECTOR, "body > div.pageInner > div > div > div.col-sm-7.col-md-9.order-md-2.order-1 > div > div > div > div > div:nth-child(1) > div > div.info > div.buttons > div > div > div.detailBasketNavigateArea > a.basketNavigatePlus.quantityPlusGB")
        buttonsinteger.click()
        await asyncio.sleep(1)

        buttons = driver.find_element(By.CSS_SELECTOR, "body > div.pageInner > div > div > div.col-sm-7.col-md-9.order-md-2.order-1 > div > div > div > div > div:nth-child(3) > div > div.info > div.buttons > div > div > div.verticalButtonLeftBox > a")
        onclick = buttons.get_attribute('onclick')

        if onclick != "requireBasket(1,1,1548,1,1,this,2);":
            print("Oyuneks: Devam etmeli...")
        else:
            await send_message(msg='Oyuneks\n\nhttps://oyuneks.com/nowa-online-world/nowa-online-world-gold', chat_id=chat_id1, token=token)
    except Exception as e:
        print(f"Oyuneks için bir hata oluştu: {traceback.format_exc()}")
    finally:
        driver.quit()
'''
async def check_klasgame():
    driver = webdriver.Chrome()
    try:
        driver.get(url2)
        buttons = driver.find_elements(By.CLASS_NAME, "product-sell.button-top-animation")
        correct_button = None

        for button in buttons:
            href = button.get_attribute('href')
            if href == 'https://www.klasgame.com/satis-yap/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold/nowa-online-world-10-gb':
                correct_button = button
                break

        if correct_button:
            onclick = correct_button.get_attribute('onclick')
            if onclick == "message('Şu an için alış aktif görünmüyor, lütfen daha sonra tekrar deneyiniz.', 'danger'); return false;":
                print("Klasgame: Devam etmeli...")
            else:
                await send_message(msg='Klasgame\n\nhttps://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold', chat_id=chat_id2, token=token)
        else:
            print("Klasgame: 10-gb buton bulunamadı")
    except Exception as e:
        print(f"Klasgame için bir hata oluştu: {traceback.format_exc()}")
    finally:
        driver.quit()
'''
async def check_klasgame():
    driver = webdriver.Chrome()
    try:
        driver.get(url2)
        buttons = driver.find_elements(By.CLASS_NAME, "product-sell.button-top-animation")

        if len(buttons) < 5:
            print("Klasgame: Beklenen 5 buton bulunamadı")
            return

        button_names = ["AURA", "FENIX", "TERA", "ARES", "ARES"]
        for index, button in enumerate(buttons[:5]):
            onclick = button.get_attribute('onclick')

            if onclick != "message('Şu an için alış aktif görünmüyor, lütfen daha sonra tekrar deneyiniz.', 'danger'); return false;":
                msg = f"Klasgame - {button_names[index]}\n\nhttps://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold"
                await send_message(msg=msg, chat_id=chat_id2, token=token)
                break
        else:
            print("Klasgame: Devam etmeli...")

    except Exception as e:
        print(f"Klasgame için bir hata oluştu: {traceback.format_exc()}")
    finally:
        driver.quit()

async def main():
    while True:
        await asyncio.gather(
            check_oyuneks(),
            check_klasgame()
        )
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
