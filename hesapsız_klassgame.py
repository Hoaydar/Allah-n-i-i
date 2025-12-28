from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from aiogram import Bot
import asyncio
from datetime import datetime

# --- AYARLAR ---
url = "https://www.klasgame.com/revenger-online/revenger-online-gold"
my_token = '7453834823:AAHUQNj727_TzXRG4o-ZYCuMM5TmdLTtK5c'
my_chat_ids = [5695472914, 6291821880]

bot = Bot(token=my_token)

async def send_to_all(text):
    for chat_id in my_chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Mesaj hatası: {e}")

async def main():
    options = Options()
    # Bot korumasını aşmak ve VDS kararlılığı için ayarlar
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False) # "add_use_" değil, "add_" olmalı
    
    # VDS ortamında hata almamak için bu 3 satır kritiktir:
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless") # Eğer VDS'de ekran yoksa burayı aktif et

    driver = webdriver.Chrome(options=options)
    last_status = None 

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Takip başlatıldı...")

    try:
        while True:
            try:
                # Siteye gitmeyi dene
                driver.get(url)
                
                # Butonun yüklenmesi için bekle
                wait = WebDriverWait(driver, 15)
                button_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-sell.button-top-animation")))
                
                onclick = button_element.get_attribute("onclick")
                now = datetime.now().strftime('%H:%M:%S')
                
                # Durum tespiti
                if "Şu an için alış aktif görünmüyor" in onclick:
                    current_status = "kapali"
                    status_text = "KAPALI"
                else:
                    current_status = "acik"
                    status_text = "AÇIK"

                print(f"[{now}] Durum: {status_text}")

                # Durum değiştiyse mesaj at
                if current_status != last_status:
                    if current_status == "acik":
                        await send_to_all(f"✅ Buton AÇILDI! {url}")
                    else:
                        await send_to_all("❌ Buton KAPANDI!")
                    last_status = current_status

            except Exception as e:
                # DNS (ERR_NAME_NOT_RESOLVED) veya sayfa hatalarında buraya düşer
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Bağlantı/Buton hatası: {e}")
                # Hata durumunda 10 saniye bekle ve döngünün başına dön
                await asyncio.sleep(10)
                continue 
            
            # Normal döngü beklemesi (Banlanmamak için 20 sn)
            await asyncio.sleep(20) 
            
    except KeyboardInterrupt:
        print("Durduruldu.")
    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
