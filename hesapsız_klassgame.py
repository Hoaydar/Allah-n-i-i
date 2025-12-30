from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from aiogram import Bot
import asyncio
from datetime import datetime

# --- AYARLAR ---
CHECK_URL = "https://www.klasgame.com/revenger-online/revenger-online-gold"
MY_TOKEN = '7453834823:AAHUQNj727_TzXRG4o-ZYCuMM5TmdLTtK5c'
USER_IDS = [5695472914, 6291821880]

bot = Bot(token=MY_TOKEN)

# İlk koddaki send_telegram_message fonksiyon yapısı
async def send_telegram_message(uid, text):
    try:
        await bot.send_message(chat_id=uid, text=text)
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Mesaj hatası ({uid}): {e}")

def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

async def main():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # VDS Ayarları
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless") # Ekran yoksa aktif et

    driver = webdriver.Chrome(options=options)
    last_status = None 

    log("Takip başlatıldı...")

    try:
        while True:
            try:
                driver.get(CHECK_URL)
                
                # Butonun yüklenmesini bekle
                wait = WebDriverWait(driver, 15)
                correct_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-sell.button-top-animation")))
                
                if correct_button:
                    onclick = correct_button.get_attribute("onclick")
                    
                    # --- İLK BAŞTA ATTIĞIN KONTROL MANTIĞI ---
                    if onclick == "message('Şu an için alış aktif görünmüyor, lütfen daha sonra tekrar deneyiniz.', 'danger'); return false;":
                        current_status = "kapali"
                        if current_status != last_status:
                            log("❌ Satış aktif değil (buton pasif).")
                            last_status = current_status
                    else:
                        current_status = "acik"
                        if current_status != last_status:
                            log("✅ Satış aktif bulundu! Telegram mesajı gönderiliyor...")
                            for uid in USER_IDS:
                                await send_telegram_message(uid, f"Revenger Online satış aktif: {CHECK_URL}")
                            last_status = current_status
                    # ------------------------------------------

            except Exception as e:
                log(f"Bağlantı/Buton hatası: {e}")
                await asyncio.sleep(10)
                continue 
            
            await asyncio.sleep(20) # Döngü beklemesi
            
    except KeyboardInterrupt:
        print("Durduruldu.")
    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
