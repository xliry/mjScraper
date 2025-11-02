# Midjourney Video Scraper

Python scraper için Midjourney.com'dan video indirme aracı.

## Özellikler

- ✅ Otomatik popup kapatma ("Look around a bit")
- ✅ Infinite scroll ile tüm videoları yükleme
- ✅ Network request yakalama ile video URL çıkarma
- ✅ Paralel veya sıralı video indirme
- ✅ İlerleme takibi (progress bars)
- ✅ Tekrar indirmeyi önleme

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

### Basit kullanım (her şeyi otomatik yap):

```bash
python main.py
```

Bu komut:
1. Sayfayı açar
2. Popup'ı kapatır
3. Sayfa sonuna kadar scroll eder
4. Tüm video URL'lerini toplar
5. Videoları indirir

### Sadece URL'leri topla:

```bash
python scraper.py
```

URL'ler `downloads/video_urls.txt` dosyasına kaydedilir.

### Sadece videoları indir (URL'ler zaten toplanmışsa):

```bash
python downloader.py
```

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

**Download hataları:**
- `DOWNLOAD_TIMEOUT` değerini artır
- Sequential download kullan (daha güvenli)

## Gereksinimler

- Python 3.8+
- Windows/Linux/Mac
- İnternet bağlantısı
