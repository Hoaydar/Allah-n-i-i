import re
import asyncio
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from aiogram import Bot
from telethon import TelegramClient

# API Bilgileri (Telethon için)
api_id = '25380560'
api_hash = '6e554fabcb17b2072f2b1242dfb7bdc6'
phone_number = '+905432240619'
client = TelegramClient('session_name', api_id, api_hash)

# Kaynak gruplar (Takip edilecek gruplar)
target_groups = ["NowaOnlineBOT"]

# Mesajların gönderileceği özel grup (ID formatında)
destination_group = -1002209424495

# Son mesaj ID'lerini takip etmek için
last_message_ids = {group_id: 0 for group_id in target_groups}

# **İstenmeyen mesajları filtrelemek için anahtar kelimeler**
blocked_keywords = [
    "DUYURU",
    "BİLDİRİM", 
    "SATIN AL", 
    "SONTEKLİF", 
    "EPİN", 
    "/SERVER", 
    "/EPİN"
]

# Telegram mesaj gönderme fonksiyonu (Aiogram)
my_token = '7453834823:AAHUQNj727_TzXRG4o-ZYCuMM5TmdLTtK5c'
my_chat_id = -1002609153844  # Geçerli bir chat_id gir

button_names = ["Aura", "Fenix", "Tera", "World Ares 10M", "World Ares 10GB"]
previous_prices = {name: None for name in button_names}

# Windows için asyncio event loop düzeltmesi
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Selenium başlatma fonksiyonu
def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı görünmez çalıştır
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Telegram mesaj gönderme fonksiyonu
async def send(msg, chat_id, token=my_token):
    try:
        async with Bot(token=token) as bot:
            await bot.send_message(chat_id=chat_id, text=msg)
    except Exception as e:
        print(f"Telegram mesaj gönderme hatası: {e}")

# Fiyat değişimlerini kontrol eden fonksiyon
async def check_price_changes(driver, iteration_count):
    driver.get("https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold")
    buttons = driver.find_elements(By.CLASS_NAME, "product-price")

    if len(buttons) != len(button_names):
        print(f"Uyarı: Beklenen {len(button_names)} buton, ancak {len(buttons)} bulundu!")

    price_changes = []
    all_prices = []

    for index, button in enumerate(buttons):
        price_text = button.text.strip()
        if price_text:
            button_name = button_names[index] if index < len(button_names) else f"Bilinmeyen {index+1}"

            if previous_prices[button_name] and previous_prices[button_name] != price_text:
                price_changes.append(f"⚠️ {button_name} Yeni Fiyat: {price_text} (Önceki: {previous_prices[button_name]})")

            previous_prices[button_name] = price_text
            all_prices.append(f"💰 {button_name}: {price_text}")

    if price_changes:
        await send("\n".join(price_changes), chat_id=my_chat_id)

    iteration_count += 1
    if iteration_count >= 150:
        await send("\n".join(all_prices), chat_id=my_chat_id)
        iteration_count = 0

    return iteration_count

# Telegram'dan mesajları kontrol etme fonksiyonu
async def check_telegram_messages():
    await client.start(phone=phone_number)

    for target_group in target_groups:
        messages = []
        async for message in client.iter_messages(target_group, limit=10):
            messages.append(message)

        for message in reversed(messages):
            if message.id <= last_message_ids[target_group]:
                continue

            if message.text:
                if any(keyword in message.text.upper() for keyword in blocked_keywords):
                    print(f'Atlandı (Filtreye takıldı): {message.text[:30]}...')
                    continue

                await client.send_message(destination_group, message.text)
                print(f'Gönderildi: {message.text[:30]}...')
            last_message_ids[target_group] = message.id

# Asenkron ana fonksiyon
async def main():
    driver = start_driver()
    iteration_count = 0  # 10 dk'lık mesajı takip etmek için sayaç
    while True:
        # İki farklı işlemi sırayla çalıştır
        await asyncio.gather(
            check_telegram_messages(),
            check_price_changes(driver, iteration_count)
        )
        await asyncio.sleep(10)  # 10 saniye bekle

if __name__ == "__main__":
    asyncio.run(main())