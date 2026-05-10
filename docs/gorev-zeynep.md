# 🎥 Zeynep — Demo, Test & Sunum Sorumlusu

## Rol: Demo Video + Pitch Deck + Test + Dokümantasyon + Teslim

**Sorumluluk Alanı:** 1 dakikalık YouTube videosu, 10 sayfalık pitch deck, uçtan uca test senaryoları, demo verileri, proje dokümantasyonu, teslim formu.

---

## 📅 Gün Gün Plan

### 🟢 GÜN 1 — 10 Mayıs Pazar (BUGÜN)

**Tema: Sunum Stratejisi + Demo Senaryosu + Test Planı**

- [ ] Hackathon kurallarını tekrar oku ve teslim edileceklerin listesini çıkar:
  - [ ] 1 dakikalık YouTube videosu
  - [ ] GitHub repo linki (public)
  - [ ] Pitch Deck (10 sayfa PDF)
  - [ ] Teslim formu
  - [ ] (Opsiyonel) Canlı link
- [ ] **1 dakikalık video senaryosunu yaz** (saniye saniye):
  - `0-7 sn:` Problem tanımı — "Kooperatiflerde sipariş ve stok takibi hâlâ WhatsApp + Excel ile yürütülüyor."
  - `7-25 sn:` Demo — Müşteri mesajı gelir, AI analiz eder, siparişe dönüştürür
  - `25-40 sn:` Demo — Stok kontrolü + AI cevap önerisi + insan onayı
  - `40-52 sn:` Demo — Kargo sorgulama akışı
  - `52-60 sn:` Dashboard özet — "Bugün X sipariş, Y stok uyarısı" + kapanış
- [ ] **Pitch Deck iskeletini oluştur** (Google Slides veya Canva):
  1. Kapak — Koopilot logo + tagline + takım
  2. Problem — Manuel iş yükü, kayıp siparişler
  3. Çözüm — AI operasyon ajanı
  4. Demo Akışı — Ekran görüntüleri ile
  5. Yapay Zeka Kullanımı — Gemini, intent extraction, function calling
  6. Mimari — Sistem diyagramı
  7. Teknoloji Yığını — FastAPI, React, Gemini, SQLite
  8. Gelecek Vizyonu — Gerçek API entegrasyonları
  9. Etki — Kadın kooperatifleri için somut fayda
  10. Kapanış — Takım + İletişim
- [ ] **Test senaryolarını belirle**:
  - Senaryo 1: Yeni sipariş mesajı → sipariş taslağı → onay
  - Senaryo 2: Eksik bilgili mesaj → AI eksik bilgi tespit → takip mesajı
  - Senaryo 3: Kargo sorgulama mesajı → kargo durumu
  - Senaryo 4: Stokta olmayan ürün siparişi → uyarı
  - Senaryo 5: Şikayet mesajı → şikayet sınıflandırma
- [ ] **Demo için örnek mesaj listesi hazırla** (en az 10 farklı mesaj)

**Teslim:** Video senaryosu yazıldı, pitch deck iskeleti hazır, test senaryoları belirlendi.

---

### 🟡 GÜN 2 — 11 Mayıs Pazartesi

**Tema: Pitch Deck İçerik + Test Çalışması**

- [ ] Pitch deck'i doldur:
  - Problem slide'ına istatistik/kaynak ekle
  - Çözüm slide'ına UI mockup/screenshot koy
  - Mimari diyagramını koy (README'deki diagramdan)
  - Etki slide'ına kooperatif bilgilerini ekle
- [ ] Backend'i test et:
  - Muhammed'den backend'i al, lokal çalıştır
  - Test senaryolarını `/docs` üzerinden dene
  - Bulduğun bug'ları Muhammed'e raporla
- [ ] Frontend'i test et (Kaan'dan aldıkça):
  - UI'da kırık bir şey var mı?
  - Akış mantıklı mı?
  - Kullanıcı gözünden değerlendir
- [ ] Demo verileri hazırla:
  - Kooperatif ürünleri (gerçekçi isimler, fiyatlar)
  - Örnek müşteri mesajları (Türkçe, doğal dilde)
  - Geçmiş sipariş verileri
- [ ] `db_init.py` için Muhammed'e demo data listesi gönder

**Teslim:** Pitch deck %80 hazır, test senaryoları çalıştırılmış, demo verileri hazır.

---

### 🔴 GÜN 3 — 12 Mayıs Salı

**Tema: Entegrasyon Testi + Video Hazırlık**

- [ ] **Uçtan uca test yap:**
  - Backend başlat → Frontend başlat → Tam akış testi
  - Her paneli test et: Mesajlar, Siparişler, Stok, Kargo, Özet
  - Mobil/tablet görünümü kontrol et
- [ ] **Demo akışını prova et:**
  - Hangi mesajları sırayla göndereceğini belirle
  - Hangi ekranlarda ne gösterilecek planla
  - Zamanlama yap (60 saniye sınırı!)
- [ ] **Video çekim hazırlığı:**
  - Ekran kayıt programı hazırla (OBS, veya basit ekran kaydı)
  - Eğer sesli olacaksa ses metnini hazırla
  - Arka plan temizliği (tarayıcı tab'ları, masaüstü)
- [ ] Pitch deck'i sonlandır:
  - Screenshot'ları güncelle (son UI'dan)
  - Son kontrol ve düzeltmeler
  - PDF olarak export et
- [ ] README'deki screenshot'ları güncelle (Kaan'la birlikte)
- [ ] Teslim formu linkini ve gereksinimlerini kontrol et

**Teslim:** Tam test tamamlandı, video çekime hazır, pitch deck bitti.

---

### ⚫ GÜN 4 — 13 Mayıs Çarşamba (TESLİM GÜNÜ)

**Tema: Video Çekimi + Son Teslim**

- [ ] **Sabah: Demo videosu çek**
  - Temiz bir ortamda çek (tam ekran, gereksiz tab yok)
  - 1 dakikayı geçme (59 saniye ideal)
  - En az 2-3 kez çek, en iyisini seç
  - Gerekirse altyazı ekle (Türkçe)
- [ ] **Videoyu YouTube'a yükle:**
  - Başlık: "Koopilot — AI Destekli Kooperatif Operasyon Ajanı | YZTA Hackathon 2026"
  - Açıklama: Kısa proje tanıtımı + GitHub linki
  - Etiketler: YZTA, Hackathon, AI, Kooperatif, Gemini
  - Erişim: Public veya Unlisted
- [ ] **GitHub repo son kontrol:**
  - README güncel mi?
  - Gereksiz dosya var mı?
  - Public mı?
- [ ] **Teslim formunu doldur** (tüm linkleri eksiksiz):
  - YouTube video linki
  - GitHub repo linki
  - (Varsa) Canlı uygulama linki
  - Pitch Deck PDF
- [ ] Takım arkadaşlarına son kontrol ettir
- [ ] **23:59'DAN ÖNCE GÖNDER** — Son dakikaya bırakma!

**Teslim:** Video YouTube'da, form gönderildi, her şey tamam.

---

## 🔑 Kritik Notlar

1. **Video 1 dakikayı geçmemeli** — Fazla olan kısım izlenmeyecek
2. **Videoda sunum yapmayın, ürünü gösterin** — Jüri çalışan demo görmek istiyor
3. **Pitch deck kapağı ve kapanışı dahil 10 sayfa** — Fazla yapmayın
4. **Teslim formunu eksik bırakmayın** — Eksik form = değerlendirmeye alınmama
5. **Son güne bırakmayın** — Mutlaka Salı akşamı prova çekin
6. **Demo verilerini gerçekçi yapın** — "test1", "ürün2" gibi isimler kullanmayın

---

## 📦 Oluşturulacak Dosyalar

```
docs/
├── pitch-deck.pdf              # 10 sayfalık sunum
├── video-script.md             # Video senaryosu (saniye saniye)
├── test-scenarios.md           # Test senaryoları ve sonuçları
├── demo-messages.md            # Demo mesaj listesi
└── assets/
    ├── koopilot-banner.png     # README banner
    ├── screenshot-messages.png # Mesaj paneli screenshot
    ├── screenshot-orders.png   # Sipariş paneli screenshot
    ├── screenshot-stock.png    # Stok paneli screenshot
    └── screenshot-summary.png  # Günlük özet screenshot
```

---

## 🎬 Demo Mesaj Örnekleri (Video İçin)

Bu mesajları sırayla göndererek demo akışını oluşturabilirsin:

```
1. "Merhaba, 2 kavanoz domates salçası ve 1 şişe nar ekşisi almak istiyorum. 
    Ankara'ya kargo olur mu?"

2. "İsmim Fatma Yıldız, telefon numaram 0532 111 2233"

3. "Adresim: Çankaya Mah. Atatürk Cad. No:15 Çankaya/Ankara"

4. "Kargom nerede? Ayşe Yılmaz'ın siparişini soruyorum."

5. "Zeytinyağınız kaç lira? Stokta var mı?"

6. "Geçen siparişimde salça kavanozunun kapağı açılmıştı, 
    değişim yapılabilir mi?"
```
