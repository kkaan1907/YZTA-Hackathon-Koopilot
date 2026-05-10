# 🔧 Muhammed Köseoğlu — Backend & AI Geliştirici

## Rol: Backend Mimarisi + Gemini AI Agent + API Geliştirme

**Sorumluluk Alanı:** FastAPI backend, Gemini AI entegrasyonu, veritabanı tasarımı, API endpoint'leri, iş mantığı.

---

## 📅 Gün Gün Plan

### 🟢 GÜN 1 — 10 Mayıs Pazar (BUGÜN)

**Tema: Backend İskeleti Sağlamlaştırma + AI Agent İyileştirme**

- [x] Mevcut backend kodu gözden geçirme
- [ ] `main.py`'ı modülerleştir — route'ları ayrı dosyalara taşı:
  - `routers/inventory.py` — Stok endpoint'leri
  - `routers/orders.py` — Sipariş endpoint'leri
  - `routers/shipping.py` — Kargo endpoint'leri
  - `routers/ai.py` — AI analiz endpoint'leri
- [ ] `/ai/daily-summary` endpoint'ini oluştur:
  - Bugünkü toplam mesaj sayısı
  - Intent dağılımı (sipariş, kargo, şikayet, soru)
  - En çok sorulan ürünler
  - Stok uyarıları (stokta 0 olup çok sorulan ürünler)
- [ ] AI agent prompt'unu iyileştir:
  - Ürün adı eşleştirme için fuzzy matching mantığı
  - Cevap tonunu kooperatif kimliğine uygun tut
- [ ] `.env.example` dosyasını güncelle
- [ ] Backend'i test et: `uvicorn main:app --reload`

**Teslim:** Modüler backend çalışır halde, `/ai/daily-summary` endpoint'i hazır.

---

### 🟡 GÜN 2 — 11 Mayıs Pazartesi

**Tema: AI Agent Geliştirme + Frontend API Desteği**

- [ ] Sipariş onaylama akışını geliştir:
  - Onay sonrası stok düşme → kargo durumu güncelleme
  - Sipariş reddetme endpoint'i ekle: `PUT /orders/{id}/reject`
- [ ] Mesaj sınıflandırma iyileştirmesi:
  - `complaint` (şikayet) intent'i için özel cevap şablonu
  - `return_request` (iade) intent'i ekle
- [ ] Kargo mock API'sini zenginleştir:
  - Tutarlı kargo durumları (sipariş durumuna göre)
  - Tahmini teslimat tarihi ekleme
- [ ] Stok uyarı sistemi:
  - Stok 5'in altına düşünce uyarı flag'i
  - `/inventory/alerts` endpoint'i
- [ ] Frontend'in ihtiyaç duyduğu API response'larını Kaan ile koordine et
- [ ] CORS ve hata yönetimini gözden geçir

**Teslim:** Tüm API endpoint'leri çalışır, stok uyarı sistemi aktif.

---

### 🔴 GÜN 3 — 12 Mayıs Salı

**Tema: Entegrasyon + Son Düzeltmeler + Demo Hazırlığı**

- [ ] Frontend-Backend entegrasyon testi:
  - Mesaj gönderme → AI analiz → sipariş oluşturma akışı
  - Sipariş onaylama → stok düşme akışı
  - Kargo sorgulama akışı
  - Günlük özet verisi
- [ ] Edge case'leri düzelt:
  - Boş mesaj, çok uzun mesaj
  - Aynı ürünü farklı isimlerle sipariş etme
  - Stokta olmayan ürün siparişi
- [ ] AI prompt'unu son kez fine-tune et
- [ ] `db_init.py`'ı demo senaryosuna göre güncelle:
  - Demo'da gösterilecek ürünleri ekle
  - Geçmiş sipariş verilerini zenginleştir
- [ ] API dokümantasyonunu kontrol et (`/docs` ekranı)
- [ ] Demo sırasında sorun çıkmaması için backend'i stabilize et

**Teslim:** Tam entegre, demo-ready backend.

---

### ⚫ GÜN 4 — 13 Mayıs Çarşamba (TESLİM GÜNÜ)

**Tema: Son Kontroller + Teslim**

- [ ] Son entegrasyon testi (uçtan uca)
- [ ] GitHub repo'yu temizle:
  - Gereksiz dosyaları sil
  - `.env` dosyasının gitignore'da olduğunu doğrula
  - Branch'leri birleştir
- [ ] README'nin güncel olduğunu kontrol et
- [ ] Backend'in `db_init.py` ile temiz başlangıç yapabildiğini doğrula
- [ ] Demo videosu için backend'i hazırla
- [ ] **23:59'a kadar teslim formunu doldur** (Zeynep ile koordineli)

**Teslim:** Her şey GitHub'da, repo public, backend sorunsuz çalışıyor.

---

## 🔑 Kritik Notlar

1. **Gemini API key'ini .env'den oku, kodda hardcode'lama**
2. **Her endpoint'te hata yönetimi olsun** — demo sırasında patlamamalı
3. **Rate limiting'i koru** — Gemini API kotasını aşma
4. **db_init.py çalıştırınca demo-ready data yüklensin**
5. **Kaan ile sürekli API format'ı konuş** — frontend'in beklediği response yapısı net olsun

---

## 📦 Oluşturulacak/Güncellenecek Dosyalar

```
backend/
├── main.py                  # Sadeleştirilmiş, router import'ları
├── routers/
│   ├── __init__.py
│   ├── inventory.py         # Stok endpoint'leri
│   ├── orders.py            # Sipariş endpoint'leri
│   ├── shipping.py          # Kargo endpoint'leri
│   └── ai.py                # AI analiz + günlük özet
├── ai_agent.py              # Gemini AI mantığı (iyileştirilmiş)
├── models.py                # DB modelleri (gerekirse güncelle)
├── schemas.py               # API şemaları (gerekirse güncelle)
├── database.py              # DB bağlantı
├── db_init.py               # Demo data (zenginleştirilmiş)
├── requirements.txt
├── .env.example
└── .gitignore
```
