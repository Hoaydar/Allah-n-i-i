import asyncio
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from aiogram import Bot
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram API bilgileri
TELEGRAM_API_ID = '25380560'
TELEGRAM_API_HASH = '6e554fabcb17b2072f2b1242dfb7bdc6'
PHONE_NUMBER = '+905432240619'
TARGET_GROUPS = ["NowaOnlineBOT"]  # Takip edilecek gruplar
DESTINATION_GROUP = -1002209424495  # Mesajların gönderileceği grup
BLOCKED_KEYWORDS = ["DUYURU", "BİLDİRİM", "SATIN AL", "SONTEKLİF", "EPİN", "/SERVER", "/EPİN"]

# Aiogram API bilgileri
AIOGRAM_TOKEN = '7453834823:AAHUQNj727_TzXRG4o-ZYCuMM5TmdLTtK5c'
AIOGRAM_CHAT_ID = -1002609153844  # Mesajların gönderileceği chat ID

# Fiyat takibi için bilgiler
BUTTON_NAMES = ["Aura", "Fenix", "Tera", "World Ares 10M", "World Ares 10GB"]
PREVIOUS_PRICES = {name: None for name in BUTTON_NAMES}

# Windows için asyncio event loop düzeltmesi
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# last_message_ids tanımlanması
last_message_ids = {group: 0 for group in TARGET_GROUPS}  # Global last_message_ids

def start_driver():
    """Selenium sürücüsünü başlatır."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f"Selenium sürücüsü başlatma hatası: {e}")
        return None


async def send_telegram_message(message, chat_id, token=AIOGRAM_TOKEN):
    """Telegram'a mesaj gönderir."""
    try:
        async with Bot(token=token) as bot:
            await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error(f"Telegram mesaj gönderme hatası: {e}")


async def check_price_changes(driver, price_changes_counter):
    """Web sitesinden fiyat değişikliklerini kontrol eder."""
    if driver is None:
        return

    try:
        driver.get("https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold")
        buttons = driver.find_elements(By.CLASS_NAME, "product-price")

        if len(buttons) != len(BUTTON_NAMES):
            logging.warning(f"Beklenen {len(BUTTON_NAMES)} buton, ancak {len(buttons)} bulundu!")

        price_changes = []
        all_prices = []

        for index, button in enumerate(buttons):
            price_text = button.text.strip()
            if price_text:
                button_name = BUTTON_NAMES[index] if index < len(BUTTON_NAMES) else f"Bilinmeyen {index + 1}"
                if PREVIOUS_PRICES[button_name] and PREVIOUS_PRICES[button_name] != price_text:
                    price_changes.append(f"⚠️ {button_name} Yeni Fiyat: {price_text} (Önceki: {PREVIOUS_PRICES[button_name]})")
                PREVIOUS_PRICES[button_name] = price_text
                all_prices.append(f" {button_name}: {price_text}")

        if price_changes:
            await send_telegram_message("\n".join(price_changes), chat_id=AIOGRAM_CHAT_ID)

        # Her 150 döngüde bir tüm fiyatları gönder
        if price_changes_counter % 80 == 0:
            await send_telegram_message("\n".join(all_prices), chat_id=AIOGRAM_CHAT_ID)

    except Exception as e:
        logging.error(f"Fiyat kontrolü sırasında hata oluştu: {e}")


async def check_telegram_messages(client):
    """Telegram gruplarındaki mesajları kontrol eder."""
    try:
        await client.start(phone=PHONE_NUMBER)
    except SessionPasswordNeededError:
        logging.error("Telegram oturumu için şifre gerekiyor.")
        return

    for group in TARGET_GROUPS:
        try:
            async for message in client.iter_messages(group, limit=10):
                if message.id > last_message_ids.get(group, 0):
                    if message.text and not any(keyword in message.text.upper() for keyword in BLOCKED_KEYWORDS):
                        try:
                            await client.send_message(DESTINATION_GROUP, message.text)
                            logging.info(f'Gönderildi: {message.text[:30]}...')
                        except Exception as e:
                            logging.error(f"Telegram mesajı gönderme hatası: {e}")
                    last_message_ids[group] = message.id
        except Exception as e:
            logging.error(f"Telegram mesajları alma hatası: {e}")


async def main():
    """Asenkron ana fonksiyon."""
    driver = start_driver()
    client = TelegramClient('session_name', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    price_changes_counter = 0

    while True:
        await asyncio.gather(
            check_telegram_messages(client),
            check_price_changes(driver, price_changes_counter)
        )
        price_changes_counter += 1
        await asyncio.sleep(10)  # 10 saniye bekle

if __name__ == "__main__":
    asyncio.run(main())import asyncio
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from aiogram import Bot
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram API bilgileri
TELEGRAM_API_ID = '25380560'
TELEGRAM_API_HASH = '6e554fabcb17b2072f2b1242dfb7bdc6'
PHONE_NUMBER = '+905432240619'
TARGET_GROUPS = ["NowaOnlineBOT"]  # Takip edilecek gruplar
DESTINATION_GROUP = -1002209424495  # Mesajların gönderileceği grup
BLOCKED_KEYWORDS = ["DUYURU", "BİLDİRİM", "SATIN AL", "SONTEKLİF", "EPİN", "/SERVER", "/EPİN"]

# Aiogram API bilgileri
AIOGRAM_TOKEN = '7453834823:AAHUQNj727_TzXRG4o-ZYCuMM5TmdLTtK5c'
AIOGRAM_CHAT_ID = -1002609153844  # Mesajların gönderileceği chat ID

# Fiyat takibi için bilgiler
BUTTON_NAMES = ["Aura", "Fenix", "Tera", "World Ares 10M", "World Ares 10GB"]
PREVIOUS_PRICES = {name: None for name in BUTTON_NAMES}

# Windows için asyncio event loop düzeltmesi
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# last_message_ids tanımlanması
last_message_ids = {group: 0 for group in TARGET_GROUPS}  # Global last_message_ids

def start_driver():
    """Selenium sürücüsünü başlatır."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    try:
        return webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f"Selenium sürücüsü başlatma hatası: {e}")
        return None


async def send_telegram_message(message, chat_id, token=AIOGRAM_TOKEN):
    """Telegram'a mesaj gönderir."""
    try:
        async with Bot(token=token) as bot:
            await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error(f"Telegram mesaj gönderme hatası: {e}")


async def check_price_changes(driver, price_changes_counter):
    """Web sitesinden fiyat değişikliklerini kontrol eder."""
    if driver is None:
        return

    try:
        driver.get("https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold")
        buttons = driver.find_elements(By.CLASS_NAME, "product-price")

        if len(buttons) != len(BUTTON_NAMES):
            logging.warning(f"Beklenen {len(BUTTON_NAMES)} buton, ancak {len(buttons)} bulundu!")

        price_changes = []
        all_prices = []

        for index, button in enumerate(buttons):
            price_text = button.text.strip()
            if price_text:
                button_name = BUTTON_NAMES[index] if index < len(BUTTON_NAMES) else f"Bilinmeyen {index + 1}"
                if PREVIOUS_PRICES[button_name] and PREVIOUS_PRICES[button_name] != price_text:
                    price_changes.append(f"⚠️ {button_name} Yeni Fiyat: {price_text} (Önceki: {PREVIOUS_PRICES[button_name]})")
                PREVIOUS_PRICES[button_name] = price_text
                all_prices.append(f" {button_name}: {price_text}")

        if price_changes:
            await send_telegram_message("\n".join(price_changes), chat_id=AIOGRAM_CHAT_ID)

        # Her 150 döngüde bir tüm fiyatları gönder
        if price_changes_counter % 80 == 0:
            await send_telegram_message("\n".join(all_prices), chat_id=AIOGRAM_CHAT_ID)

    except Exception as e:
        logging.error(f"Fiyat kontrolü sırasında hata oluştu: {e}")


async def check_telegram_messages(client):
    """Telegram gruplarındaki mesajları kontrol eder."""
    try:
        await client.start(phone=PHONE_NUMBER)
    except SessionPasswordNeededError:
        logging.error("Telegram oturumu için şifre gerekiyor.")
        return

    for group in TARGET_GROUPS:
        try:
            async for message in client.iter_messages(group, limit=10):
                if message.id > last_message_ids.get(group, 0):
                    if message.text and not any(keyword in message.text.upper() for keyword in BLOCKED_KEYWORDS):
                        try:
                            await client.send_message(DESTINATION_GROUP, message.text)
                            logging.info(f'Gönderildi: {message.text[:30]}...')
                        except Exception as e:
                            logging.error(f"Telegram mesajı gönderme hatası: {e}")
                    last_message_ids[group] = message.id
        except Exception as e:
            logging.error(f"Telegram mesajları alma hatası: {e}")


async def main():
    """Asenkron ana fonksiyon."""
    driver = start_driver()
    client = TelegramClient('session_name', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    price_changes_counter = 0

    while True:
        await asyncio.gather(
            check_telegram_messages(client),
            check_price_changes(driver, price_changes_counter)
        )
        price_changes_counter += 1
        await asyncio.sleep(10)  # 10 saniye bekle

if __name__ == "__main__":
    asyncio.run(main())
