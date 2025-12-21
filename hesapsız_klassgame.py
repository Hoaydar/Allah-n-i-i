from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from aiogram import Bot
import asyncio
from datetime import datetime

# --- AYARLAR ---
url = "https://www.klasgame.com/revenger-online/revenger-online-gold"
my_token = '7453834823:AAHUQNj727_TzXRG4o-ZYCuMM5TmdLTtK5c'
my_chat_ids = [5695472914, 6291821880]  # Listeye eklediğin herkese gider

bot = Bot(token=my_token)

async def send_to_all(text):
    """Listedeki tüm ID'lere mesaj gönderir ve terminale yazar."""
    for chat_id in my_chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {chat_id} ID'sine mesaj gönderilemedi: {e}")

async def main():
    options = Options()
    # options.add_argument("--headless") # Tarayıcıyı gizlemek istersen aktif et
    
    driver = webdriver.Chrome(options=options)
    last_status = None 

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Takip başlatıldı... (Her 10 saniyede bir kontrol)")

    try:
        while True:
            now = datetime.now().strftime('%H:%M:%S')
            driver.get(url)
            await asyncio.sleep(3) # Sayfanın tam yüklenmesi için 3 sn idealdir
            
            try:
                xpath = driver.find_element(By.CLASS_NAME, "product-sell.button-top-animation")
                onclick = xpath.get_attribute("onclick")
                
                # Durum tespiti
                if "Şu an için alış aktif görünmüyor" in onclick:
                    current_status = "kapali"
                    status_text = "KAPALI (Alış pasif)"
                else:
                    current_status = "acik"
                    status_text = "AÇIK (Alış aktif!)"
                
                # Terminale her sorguda durumu yaz
                print(f"[{now}] Kontrol yapıldı: Buton şu an {status_text}")

                # Durum değişikliği kontrolü
                if current_status != last_status:
                    if current_status == "acik":
                        msg = "✅ Buton AÇILDI! Alış aktif."
                        await send_to_all(msg)
                        print(f"[{now}] BİLGİ: Durum değişti -> Mesaj gönderildi (AÇIK)")
                    else:
                        msg = "❌ Buton KAPANDI! Alış pasif."
                        await send_to_all(msg)
                        print(f"[{now}] BİLGİ: Durum değişti -> Mesaj gönderildi (KAPALI)")
                    
                    last_status = current_status
                
            except Exception as e:
                print(f"[{now}] HATA: Buton elementine ulaşılamadı veya sayfa yüklenemedi.")

            await asyncio.sleep(10) # 10 saniye bekle
            
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Program kullanıcı tarafından durduruldu.")
    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())