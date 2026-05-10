# 🎨 Kaan — Frontend & UI/UX Geliştirici

## Rol: React Dashboard + Kullanıcı Deneyimi + Görsel Tasarım

**Sorumluluk Alanı:** React frontend, dashboard arayüzü, API entegrasyonu, responsive tasarım, kullanıcı akışları.

---

## 📅 Gün Gün Plan

### 🟢 GÜN 1 — 10 Mayıs Pazar (BUGÜN)

**Tema: Frontend Projesi Kurulumu + Tasarım Sistemi + İskelet**

- [ ] Vite + React projesi oluştur:
  ```bash
  cd frontend
  npm create vite@latest ./ -- --template react
  npm install
  npm install axios react-icons
  ```
- [ ] Tasarım sistemi oluştur (`src/index.css`):
  - Renk paleti (kooperatif teması — toprak tonları, yeşiller)
  - Tipografi (Google Fonts: Inter veya Outfit)
  - Spacing, border-radius, shadow token'ları
  - Dark/light tema hazırlığı (opsiyonel)
- [ ] Ana layout'u oluştur:
  - **Sidebar** (sol menü): Mesajlar, Siparişler, Stok, Kargo, Özet
  - **Main Content** alanı
  - **Header** (Koopilot logosu + kooperatif adı)
- [ ] API servis katmanını oluştur (`src/services/api.js`):
  - `analyzeMessage(message, sessionId)`
  - `getInventory()`
  - `getOrders()`
  - `approveOrder(orderId)`
  - `getShippingStatus(orderId)`
  - `getDailySummary()`
- [ ] `MessagePanel` bileşeninin iskeletini oluştur:
  - Mesaj giriş alanı
  - AI yanıt gösterim alanı
  - Sohbet baloncukları (müşteri + AI)

**Teslim:** Frontend projesi çalışıyor, layout hazır, API servisi bağlanmaya hazır.

---

### 🟡 GÜN 2 — 11 Mayıs Pazartesi

**Tema: Dashboard Panelleri + Backend Entegrasyonu**

- [ ] `MessagePanel` bileşenini tamamla:
  - Mesaj gönder → AI yanıtı göster akışı
  - Session ID ile sohbet hafızası
  - Sipariş taslağı kartı (AI çıktısından)
  - Stok uyarısı gösterimi
  - "Sipariş oluşturuldu" bildirimi
- [ ] `OrderPanel` bileşeni:
  - Sipariş listesi (durum badge'leri: Taslak, Onaylandı, Kargoda)
  - Sipariş detay görünümü (ürünler, müşteri bilgileri)
  - **Onayla butonu** (human-in-the-loop)
  - Sipariş reddetme butonu
- [ ] `InventoryPanel` bileşeni:
  - Ürün tablosu (ad, kategori, stok, fiyat)
  - Stok düşük uyarısı (kırmızı highlight)
  - Stok güncelleme (inline edit veya modal)
- [ ] Backend API'sine bağlan ve gerçek veri çek
- [ ] Muhammed ile API response formatlarını doğrula

**Teslim:** 3 ana panel çalışıyor, backend'den veri geliyor.

---

### 🔴 GÜN 3 — 12 Mayıs Salı

**Tema: Kalan Paneller + Polish + Demo UI**

- [ ] `ShippingPanel` bileşeni:
  - Sipariş no ile kargo sorgulama
  - Kargo durumu kartı
- [ ] `DailySummary` bileşeni:
  - Bugünün istatistikleri (mesaj, sipariş, stok uyarısı)
  - En çok sorulan ürünler listesi
  - Basit bar/pie chart (opsiyonel — Chart.js veya sadece CSS bar)
- [ ] UI Polish:
  - Hover efektleri ve geçiş animasyonları
  - Loading spinner'ları
  - Boş durum (empty state) görselleri
  - Hata durumu UI'ları
  - Toast bildirimleri (sipariş onaylandı, stok uyarısı)
- [ ] Responsive kontrol (tablet ve mobil)
- [ ] Demo akışını test et:
  1. Mesaj gönder → AI analiz → sipariş oluştur → onayla
  2. Kargo sorgula
  3. Stok kontrol
  4. Günlük özet

**Teslim:** Tüm paneller çalışıyor, UI profesyonel, demo akışı sorunsuz.

---

### ⚫ GÜN 4 — 13 Mayıs Çarşamba (TESLİM GÜNÜ)

**Tema: Son Dokunuşlar + Demo Desteği + Teslim**

- [ ] Son UI bugfix'leri
- [ ] Demo senaryosu için özel UI düzenlemeleri:
  - Demo sırasında gösterilecek mock veriler frontend'de hazır
  - Animasyonlar düzgün çalışıyor
- [ ] Screenshot'lar al → README'ye ekle
- [ ] Video çekimi için frontend'i hazırla
- [ ] Muhammed ile son entegrasyon testi
- [ ] GitHub'a son push
- [ ] **23:59'a kadar teslim**

**Teslim:** Frontend production-ready, screenshot'lar alınmış.

---

## 🔑 Kritik Notlar

1. **API base URL'yi env variable yap** — `VITE_API_URL=http://localhost:8000`
2. **Loading ve error state'lerini atla** — Her API çağrısında göster
3. **Muhammed'in API response'ları değişebilir** — `api.js` katmanını kullan, component'larda doğrudan axios çağırma
4. **Demo'da en güzel görünecek paneli öne çıkar** — MessagePanel en etkileyici olacak
5. **Font ve renkleri baştan belirle** — Sonradan değiştirmek zor
6. **Favicon ve sayfa başlığını unutma** — `Koopilot | Kooperatif Operasyon Ajanı`

---

## 📦 Oluşturulacak Dosyalar

```
frontend/
├── index.html                    # Favicon, title, font import
├── vite.config.js
├── package.json
├── public/
│   └── favicon.svg               # Koopilot favicon
├── src/
│   ├── main.jsx                  # React giriş noktası
│   ├── App.jsx                   # Ana uygulama + routing
│   ├── App.css                   # App-specific stiller
│   ├── index.css                 # Global tasarım sistemi
│   ├── components/
│   │   ├── Sidebar.jsx           # Sol navigasyon menüsü
│   │   ├── Header.jsx            # Üst bar
│   │   ├── MessagePanel.jsx      # AI mesaj analiz paneli
│   │   ├── OrderPanel.jsx        # Sipariş yönetim paneli
│   │   ├── InventoryPanel.jsx    # Stok yönetim paneli
│   │   ├── ShippingPanel.jsx     # Kargo takip paneli
│   │   └── DailySummary.jsx      # Günlük özet dashboard
│   └── services/
│       └── api.js                # Backend API iletişim katmanı
```

---

## 🎨 Tasarım Referansları

### Renk Paleti (Önerilen)

| Renk | Hex | Kullanım |
|------|-----|----------|
| Koyu Yeşil | `#1B4332` | Sidebar, başlıklar |
| Orta Yeşil | `#2D6A4F` | Aktif menü, primary buton |
| Açık Yeşil | `#52B788` | Accent, hover |
| Toprak | `#8B7355` | Secondary, border |
| Krem | `#FAF3E0` | Arka plan |
| Beyaz | `#FFFFFF` | Kart arka planı |
| Kırmızı | `#E63946` | Hata, stok uyarısı |
| Turuncu | `#F4A261` | Dikkat, pending durumu |

### Tipografi

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
font-family: 'Inter', sans-serif;
```
