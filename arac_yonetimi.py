# --- ÜST SINIF (SUPERCLASS) ---
class Arac:
    def __init__(self, arac_id, marka, model, yil):
        self.arac_id = arac_id
        self.marka = marka.upper()
        self.model = model.capitalize()
        self.yil = yil

    def bilgileri_goster(self):
        return f"[ID: {self.arac_id}] {self.yil} {self.marka} {self.model}"

    def deger_hesapla(self):
        pass 

# --- ALT SINIF 1: Klasik Araç ---
class KlasikArac(Arac):
    def __init__(self, arac_id, marka, model, yil, restorasyon_yuzdesi):
        super().__init__(arac_id, marka, model, yil)
        self.restorasyon_yuzdesi = restorasyon_yuzdesi

    def deger_hesapla(self):
        taban_fiyat = 450000
        ek_deger = (self.restorasyon_yuzdesi * 12000)
        return taban_fiyat + ek_deger

    def bilgileri_goster(self):
        return super().bilgileri_goster() + f" | Tipi: Klasik | Restorasyon: %{self.restorasyon_yuzdesi}"

# --- ALT SINIF 2: Modern Araç ---
class ModernArac(Arac):
    def __init__(self, arac_id, marka, model, yil, kilometre):
        super().__init__(arac_id, marka, model, yil)
        self.kilometre = kilometre

    def deger_hesapla(self):
        taban_fiyat = 1200000
        deger_kaybi = self.kilometre * 2.5
        guncel_deger = taban_fiyat - deger_kaybi
        return guncel_deger if guncel_deger > 80000 else 80000

    def bilgileri_goster(self):
        return super().bilgileri_goster() + f" | Tipi: Modern | Kilometre: {self.kilometre:,} km"


# --- SİSTEM KONTROL MERKEZİ ---
def ana_program():
    galeri = []

    # Sisteme test için varsayılan 3 araç yükleyelim
    galeri.append(KlasikArac(1, "CHEVROLET", "Impala", 1967, 85))
    galeri.append(ModernArac(2, "PEUGEOT", "508", 2024, 12500))
    galeri.append(ModernArac(3, "TESLA", "Model Y", 2025, 4000))

    while True:
        print("\n" + "="*45)
        print("   ARAÇ DEĞERLEME & OTOMASYON   ")
        print("="*45)
        print("1. Envanteri Listele ve Değerleri Gör")
        print("2. Sisteme Yeni Araç Ekle")
        print("3. Sistemden Araç Çıkar (ID ile)")
        print("4. Markaya Göre Araç Filtrele")
        print("5. Toplam Portföy Değerini Hesapla")
        print("6. Çıkış")
        
        secim = input("\nİşlem Seçiniz (1-6): ")

        # 1. LİSTELEME
        if secim == '1':
            if not galeri:
                print("\n[!] Galeri şu an tamamen boş.")
            else:
                print("\n--- MEVCUT ARAÇ ENVANTERİ ---")
                for a in galeri:
                    print(f"{a.bilgileri_goster()}  ---> Tahmini Değer: {a.deger_hesapla():,.2f} TL")

        # 2. ARAÇ EKLEME (Klasik mi Modern mi?)
        elif secim == '2':
            try:
                # Otomatik benzersiz ID üretme (Mevcut en yüksek ID'nin 1 fazlası)
                yeni_id = max([arac.arac_id for arac in galeri], default=0) + 1
                
                print("\nEkleyeceğiniz araç tipi nedir?")
                tip_sec = input("Klasik için 'K', Modern için 'M' tuşlayın: ").upper()
                
                if tip_sec not in ['K', 'M']:
                    print("[HATA] Sadece K veya M girebilirsiniz!")
                    continue

                marka = input("Markası: ")
                model = input("Modeli: ")
                yil = int(input("Üretim Yılı (Örn: 2021): "))

                if tip_sec == 'K':
                    rest = int(input("Restorasyon Yüzdesi (0-100 arası): "))
                    galeri.append(KlasikArac(yeni_id, marka, model, yil, rest))
                else:
                    km = int(input("Kilometresi: "))
                    galeri.append(ModernArac(yeni_id, marka, model, yil, km))
                
                print(f"\n[BAŞARILI] Araç ID:{yeni_id} koduyla sisteme kaydedildi.")
            
            except ValueError:
                print("\n[CRITICAL ERROR] Sayı girmeniz gereken yere harf girdiniz. İşlem iptal edildi!")

        # 3. ARAÇ SİLME (ID Kontrollü)
        elif secim == '3':
            try:
                sil_id = int(input("\nSilmek istediğiniz aracın ID numarasını girin: "))
                arac_bulundu = False

                for arac in galeri:
                    if arac.arac_id == sil_id:
                        galeri.remove(arac)
                        print(f"\n[SİLİNDİ] {arac.marka} {arac.model} (ID:{sil_id}) envanterden çıkarıldı.")
                        arac_bulundu = True
                        break
                
                if not arac_bulundu:
                    print(f"\n[!] Sistemde '{sil_id}' ID numarasına sahip bir araç bulunamadı.")
            
            except ValueError:
                print("\n[HATA] ID numarası bir tam sayı olmalıdır!")

        # 4. ARAMA / FİLTRELEME
        elif secim == '4':
            arama_kelimesi = input("\nAradığınız Markayı yazın (Örn: Peugeot): ").upper()
            
            # List Comprehension ile tek satırda filtreleme
            sonuclar = [a for a in galeri if arama_kelimesi in a.marka]
            
            if sonuclar:
                print(f"\n--- '{arama_kelimesi}' İÇİN BULUNAN ARAÇLAR ---")
                for s in sonuclar:
                    print(s.bilgileri_goster())
            else:
                print(f"\n[!] Envanterde '{arama_kelimesi}' markasına ait araç yok.")

        # 5. FİNANSAL RAPOR
        elif secim == '5':
            toplam_para = sum([a.deger_hesapla() for a in galeri])
            print(f"\n>>> Galerideki Toplam {len(galeri)} Aracın Güncel Portföy Değeri: {toplam_para:,.2f} TL <<<")

        # 6. ÇIKIŞ
        elif secim == '6':
            print("\nSistem kapatılıyor. İyi çalışmalar dileriz.")
            break

        else:
            print("\n[!] Geçersiz bir menü kodu tuşladınız.")

# Dosya doğrudan çalıştırıldığında tetikle
if __name__ == "__main__":
    ana_program()