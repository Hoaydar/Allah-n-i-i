from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from aiogram import Bot, Dispatcher, types
import asyncio
import traceback

url = "https://oyuneks.com/nowa-online-world/nowa-online-world-gold"
my_token = '6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw'
my_chat_id = -1002209424495

async def send(msg, chat_id, token=my_token):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=msg)
    await bot.close()  # Bot bağlantısını kapatmayı unutmayın

async def main():
    while True:
        # Tarayıcıyı başlatıyoruz
        options = Options()
        # Tarayıcıyı arka planda çalıştırmak için
        # options.add_argument("--headless") 

        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            
            # Sayfa öğelerinin yüklendiğinden emin olmak için bekliyoruz
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.pageInner > div > div > div.col-sm-7.col-md-9.order-md-2.order-1 > div > div > div > div > div:nth-child(1) > div > div.info > div.buttons > div > div > div.detailBasketNavigateArea > a.basketNavigatePlus.quantityPlusGB"))
            )
            # 'quantityPlus' butonunu buluyoruz
            buttonsinteger = driver.find_element(By.CSS_SELECTOR, "body > div.pageInner > div > div > div.col-sm-7.col-md-9.order-md-2.order-1 > div > div > div > div > div:nth-child(1) > div > div.info > div.buttons > div > div > div.detailBasketNavigateArea > a.basketNavigatePlus.quantityPlusGB")
            buttonsinteger.click()
            await asyncio.sleep(1)  # Bekleme süresi için await kullanıyoruz

            # 'leftBasketButton' butonunu buluyoruz
            buttons = driver.find_element(By.CSS_SELECTOR, "body > div.pageInner > div > div > div.col-sm-7.col-md-9.order-md-2.order-1 > div > div > div > div > div:nth-child(3) > div > div.info > div.buttons > div > div > div.verticalButtonLeftBox > a")

            # Butonun onclick olayını alıyoruz
            onclick = buttons.get_attribute('onclick')
            if onclick != "requireBasket(1,1,1548,1,1,this,2);":
                print("Devam etmeli...")
            else:
                await send(msg='Oyuneks\n\nhttps://oyuneks.com/nowa-online-world/nowa-online-world-gold', chat_id=my_chat_id, token=my_token)

        except Exception as e:
            print(f"Bir hata oluştu: {traceback.format_exc()}")

        finally:
            # Tarayıcıyı kapatıyoruz
            driver.quit()

        # 10 saniye bekliyoruz
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())