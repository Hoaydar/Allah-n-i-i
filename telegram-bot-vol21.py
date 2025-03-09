import re
from telethon import TelegramClient
import asyncio

# API bilgileri
api_id = '25380560'
api_hash = '6e554fabcb17b2072f2b1242dfb7bdc6'
phone_number = '+905432240619'
client = TelegramClient('session_name', api_id, api_hash)

target_groups = [
    "NowaOnlineBOT",
   #"knight_mobile"
]

destination_group = 'denemeliksahmara'

last_message_ids = {group_id: 0 for group_id in target_groups}

async def main():
    await client.start(phone=phone_number)

    for target_group in target_groups:
        async for message in client.iter_messages(target_group, min_id=last_message_ids[target_group]):
            if message.text:
                # Amazon linklerini bul ve ?tag= kısmını güncelle
                modified_text = re.sub(
                    r'(https?://(www\.)?amazon\.\w{2,3}/[^\s]+?)\?tag=[^&]+',
                    r'\1?tag=indirimalarmitr_4895-21',
                    message.text
                )
                
                # Güncellenmiş bağlantıyı mesajın sonunda yeniden ekle
                modified_message = re.sub(
                    r'(https?://(www\.)?amazon\.\w{2,3}/[^\s]+)',
                    modified_text,
                    message.text
                )
                
                # Güncellenmiş metni hedef gruba gönder
                await client.send_message(destination_group, modified_message)
                
                # Son mesaj kimliğini güncelle
                last_message_ids[target_group] = max(last_message_ids[target_group], message.id)

async def run_bot():
    while True:
        await main()
        await asyncio.sleep(60)

with client:
    client.loop.run_until_complete(run_bot())