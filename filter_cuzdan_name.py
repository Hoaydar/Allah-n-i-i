import json
import os

# Dosya yolları (istediğin gibi değiştir)
INPUT_FILE = "wallets.json"
OUTPUT_FILE = "output.txt"  # tek satır, virgülle ayrılmış adresler

def take_and_remove_addresses(input_file, output_file, take_count=500):
    # Mevcut dosya var mı kontrolü
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' bulunamadı.")

    # JSON dosyasını oku
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON beklenen formatta değil. Beklenen: liste (her öğe bir obje, içinde 'address' alanı).")

    # Adresleri topla (sadece address alanı olanları)
    addresses = [item["address"] for item in data if isinstance(item, dict) and "address" in item]

    # Kaç tane alınacak?
    to_take = addresses[:take_count]
    taken_count = len(to_take)

    if taken_count == 0:
        print("Dosyada 'address' alanı bulunan cüzdan yok.")
        return

    # Tek satır, aralarında sadece virgül olacak şekilde yaz
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(",".join(to_take))

    # Orijinal veriden alınanları çıkar
    # Daha güvenli yaklaşım: ilk taken_count öğeyi sil (orijinal sırayı korur)
    remaining_data = data[taken_count:]

    # Üzerine yaz (orijinali güncelle)
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(remaining_data, f, ensure_ascii=False, indent=4)

    print(f"{taken_count} adet adres '{output_file}' dosyasına yazıldı.")
    print(f"Orijinal dosya '{input_file}' güncellendi. Kalan öğe sayısı: {len(remaining_data)}")

if __name__ == "__main__":
    take_and_remove_addresses(INPUT_FILE, OUTPUT_FILE, take_count=500)