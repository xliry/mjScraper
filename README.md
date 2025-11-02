# Midjourney Video Scraper

Python scraper için Midjourney.com'dan video indirme aracı.

## Özellikler

- ✅ Otomatik popup kapatma ("Look around a bit")
- ✅ Infinite scroll ile tüm videoları yükleme
- ✅ Network request yakalama ile video URL çıkarma
- ✅ Browser context ile video indirme (403 Forbidden hatası yok!)
- ✅ Playwright authentication ile CDN erişimi
- ✅ Tekrar indirmeyi önleme
- ✅ Dosya boyutu gösterimi

## Kurulum

### 1. Python virtual environment oluştur (önerilen)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Paketleri yükle

```bash
pip install -r requirements.txt
```

### 3. Playwright browser'ı yükle

```bash
playwright install chromium
```

## Kullanım

### Basit kullanım (önerilen):

```bash
python main.py
```

Program açılınca 2 seçenek sunulur:
- **1. Scrape URLs and download videos** - URL'leri topla ve videoları indir
- **2. Only scrape URLs** - Sadece URL'leri topla

Bu komut:
1. Sayfayı açar
2. Popup'ı kapatır
3. Sayfa sonuna kadar scroll eder
4. Tüm video URL'lerini toplar
5. Videoları browser context ile indirir (403 hatası yok!)

### Sadece URL'leri topla:

```bash
python scraper.py
```

URL'ler `downloads/video_urls.txt` dosyasına kaydedilir.

**NOT:** `downloader.py` artık kullanılmıyor. Browser context gerektirdiği için tüm işlem `scraper.py` içinde yapılıyor.

## Ayarlar

`config.py` dosyasından ayarları değiştirebilirsin:

- `SCROLL_PAUSE_TIME`: Scroll sonrası bekleme süresi (saniye)
- `SCROLL_ATTEMPTS`: Maksimum scroll sayısı
- `MAX_CONCURRENT_DOWNLOADS`: Paralel indirme sayısı
- `DOWNLOAD_TIMEOUT`: Video başına timeout (saniye)

## Proje Yapısı

```
mjScraper/
├── main.py              # Ana script
├── scraper.py           # Web scraping logic
├── downloader.py        # Video indirme logic
├── config.py            # Ayarlar
├── requirements.txt     # Python paketleri
├── downloads/           # İndirilen videolar ve URL listesi
└── README.md           # Bu dosya
```

## İpuçları

- İlk kez çalıştırırken browser açık görünür (`headless=False`). Bunu `scraper.py:95`'te değiştirebilirsin.
- Çok fazla video varsa paralel indirme kullan (ama dikkat et, sunucu rate limit yapabilir)
- Scroll sayısını artırmak istersen `config.SCROLL_ATTEMPTS` değerini yükselt

## Sorun Giderme

**Popup bulunamıyor:**
- Popup selector'ları `scraper.py:24-29` satırlarında güncelle

**Videolar yüklenmiyor:**
- `SCROLL_PAUSE_TIME` değerini artır (yavaş internet için)

**403 Forbidden hatası:**
- ✅ Artık düzeltildi! Browser context kullanılarak çözüldü.
- Eğer hala sorun yaşıyorsan, browser'ı headless=False modda çalıştır

**Download çok yavaş:**
- Normal! Her video browser context üzerinden indiriliyor
- Büyük videolar için zaman alabilir

## Gereksinimler

- Python 3.8+
- Windows/Linux/Mac
- İnternet bağlantısı
