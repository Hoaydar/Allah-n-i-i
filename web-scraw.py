import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Telegram Bot Bilgileri (Buraya kendi bilgilerini eklemelisin)
TELEGRAM_BOT_TOKEN = "6463031187:AAGAVe5K6yWqH9vTSz5sGLGL2LKWmEodzjw"
TELEGRAM_CHAT_ID = "-1002209424495"

def send_telegram_message(message):
    """Telegram grubuna mesaj gönderir."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("✅ Mesaj başarıyla gönderildi!")
    else:
        print(f"❌ Telegram Hata: {response.status_code}, {response.text}")

def check_buttons_and_send_message(url):
    """Sayfadaki tüm butonları kontrol eder ve Telegram mesajı gönderir."""
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Tüm butonları seç
        buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-sell.button-top-animation")))

        print(f"🔎 {len(buttons)} buton bulundu, kontrol ediliyor...")

        blocked_message = "message('Şu an için alış aktif görünmüyor, lütfen daha sonra tekrar deneyiniz.', 'danger'); return false;"
        alış_var = False  # En az bir tane aktif alış bulunursa True olacak

        for index, button in enumerate(buttons, start=1):
            onclick_value = button.get_attribute("onclick")
            print(f"🔹 Buton {index} Onclick: {onclick_value}")

            if onclick_value and blocked_message not in onclick_value: #
                alış_var = True
                send_telegram_message(f"🔥 Nowa Online World Gold alımı aktif! ({index}. buton) Hemen kontrol et: {url}")

        if not alış_var:
            print("❌ Alış aktif değil, mesaj gönderilmeyecek.")

    except Exception as e:
        print(f"⚠️ Hata oluştu: {e}")

    finally:
        driver.quit()

# Sürekli çalışan döngü
url = "https://www.klasgame.com/mmorpg-oyunlar/nowa-online-world/nowa-online-world-gold"

while True:
    print("\n🔄 Yeni kontrol başlatılıyor...")
    check_buttons_and_send_message(url)
    print("⏳ 7 saniye bekleniyor...\n")
    time.sleep(7)  # 7 saniye bekle ve tekrar çalıştır