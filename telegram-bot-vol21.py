import re
from telethon import TelegramClient
import asyncio

# API Bilgileri
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

async def main():
    await client.start(phone=phone_number)

    for target_group in target_groups:
        # **Son 10 mesajı getir**
        messages = []
        async for message in client.iter_messages(target_group, limit=10):
            messages.append(message)

        # **Eski mesajları atlayıp, yalnızca yeni olanları işle**
        for message in reversed(messages):  # Eski mesajlardan yeniye doğru sırala
            if message.id <= last_message_ids[target_group]:
                continue  # Eğer mesaj zaten işlendi ise atla

            if message.text:
                # **"DUYURU" kelimesi içeren mesajları atla**
                if "DUYURU" in message.text.upper():
                    print(f'Atlandı (DUYURU içeriyor): {message.text[:30]}...')
                    continue
            
                # **Mesajı hedef gruba gönder**
                await client.send_message(destination_group, message.text)
                print(f'Gönderildi: {message.text[:30]}...')

            # **Son mesaj ID’sini güncelle**
            last_message_ids[target_group] = message.id

async def run_bot():
    while True:
        await main()
        await asyncio.sleep(20)  # **Her 20 saniyede bir yeni mesajları kontrol et**

with client:
    client.loop.run_until_complete(run_bot())