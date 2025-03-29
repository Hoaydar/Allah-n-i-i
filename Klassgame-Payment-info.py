import asyncio
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from aiogram import Bot

# Windows için asyncio event loop düzeltmesi
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

url = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold"
my_token = '7453834823:AAHUQNj727_TzXRG4o-ZYCuMM5TmdLTtK5c'
my_chat_id = -1002609153844  # Geçerli bir chat_id gir

# Buton isimleri sıralı olarak tanımlandı
button_names = ["Aura", "Fenix", "Tera", "World Ares 10M", "World Ares 10GB"]

# Önceki fiyatları saklayacak sözlük
previous_prices = {name: None for name in button_names}

# Telegram mesaj gönderme fonksiyonu
async def send(msg, chat_id, token=my_token):
    try:
        async with Bot(token=token) as bot:
            await bot.send_message(chat_id=chat_id, text=msg)
    except Exception as e:
        print(f"Telegram mesaj gönderme hatası: {e}")

# Selenium başlatma fonksiyonu
def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı görünmez çalıştır
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

async def main():
    driver = start_driver()  # Tek seferlik driver başlat
    iteration_count = 0  # 10 dk'lık mesajı takip etmek için sayaç
    while True:
        driver.get(url)

        # Butonları al
        buttons = driver.find_elements(By.CLASS_NAME, "product-price")

        # Eğer buton sayısı beklenenden farklıysa hata verdirme
        if len(buttons) != len(button_names):
            print(f"Uyarı: Beklenen {len(button_names)} buton, ancak {len(buttons)} bulundu!")

        price_changes = []  # Değişen fiyatları saklar
        all_prices = []  # Tüm fiyatları saklar

        # Butonları sırayla işleyerek fiyatları al
        for index, button in enumerate(buttons):
            price_text = button.text.strip()  # Buton içindeki metni al
            if price_text:  # Eğer boş değilse işle
                button_name = button_names[index] if index < len(button_names) else f"Bilinmeyen {index+1}"

                # Eğer fiyat değiştiyse listeye ekle
                if previous_prices[button_name] and previous_prices[button_name] != price_text:
                    price_changes.append(f"⚠️ {button_name} Yeni Fiyat: {price_text} (Önceki: {previous_prices[button_name]})")

                # Önceki fiyatı güncelle
                previous_prices[button_name] = price_text
                all_prices.append(f"💰 {button_name}: {price_text}")

        # Eğer fiyat değişimi varsa, sadece değişenleri gönder
        if price_changes:
            await send("\n".join(price_changes), chat_id=my_chat_id)

        # Her 6 döngüde bir (10 dk) tüm fiyatları gönder
        iteration_count += 1
        if iteration_count >= 60:
            await send("\n".join(all_prices), chat_id=my_chat_id)
            iteration_count = 0  # Sayaç sıfırla

        await asyncio.sleep(10)  # 10 saniye bekle

if __name__ == "__main__":
    asyncio.run(main())