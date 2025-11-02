# Midjourney Video Scraper

A Python-based web scraper for downloading videos from Midjourney.com.

## Features

- ✅ Automatic popup handling ("Look around a bit" dialog)
- ✅ Infinite scroll to load all videos
- ✅ Network request interception for video URL extraction
- ✅ Browser context video downloads (no 403 Forbidden errors!)
- ✅ JavaScript fetch API for authenticated downloads
- ✅ Skip already downloaded videos
- ✅ File size reporting

## Installation

### 1. Create Python virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browser

```bash
playwright install chromium
```

## Usage

### Simple usage (recommended):

```bash
python main.py
```

The program will present 2 options:
- **1. Scrape URLs and download videos** - Collect URLs and download videos
- **2. Only scrape URLs** - Only collect URLs without downloading

This command will:
1. Open the page in browser
2. Close the popup automatically
3. Scroll to the bottom to load all videos
4. Extract all video URLs
5. Download videos using browser context (no 403 errors!)

### Only scrape URLs:

```bash
python scraper.py
```

URLs will be saved to `downloads/video_urls.txt`.

**NOTE:** `downloader.py` is no longer used. All operations are handled in `scraper.py` to maintain browser context.

## Configuration

You can modify settings in `config.py`:

- `SCROLL_PAUSE_TIME`: Wait time after each scroll (seconds)
- `SCROLL_ATTEMPTS`: Maximum number of scroll attempts
- `MAX_CONCURRENT_DOWNLOADS`: Number of parallel downloads
- `DOWNLOAD_TIMEOUT`: Timeout per video (seconds)

## Project Structure

```
mjScraper/
├── main.py              # Main script
├── scraper.py           # Web scraping logic
├── downloader.py        # Video download logic (deprecated)
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── downloads/           # Downloaded videos and URL list
└── README.md           # This file
```

## Tips

- Browser runs in visible mode by default (`headless=False`). Change this in `scraper.py:158` if needed.
- For many videos, parallel downloads may be faster (but watch for rate limiting)
- Increase `config.SCROLL_ATTEMPTS` if you want to scroll more

## Troubleshooting

**Popup not found:**
- Update popup selectors in `scraper.py:24-29`

**Videos not loading:**
- Increase `SCROLL_PAUSE_TIME` value (for slow internet connections)

**403 Forbidden error:**
- ✅ Fixed! Now using JavaScript fetch API with browser context
- If still experiencing issues, ensure browser runs in headless=False mode

**Download too slow:**
- Normal! Each video downloads through browser context
- Large videos may take time

## Requirements

- Python 3.8+
- Windows/Linux/Mac
- Internet connection

## How It Works

The scraper uses Playwright to:
1. Launch a Chromium browser instance
2. Navigate to Midjourney's video explore page
3. Handle authentication and popups automatically
4. Scroll to load all video content dynamically
5. Extract video URLs from network requests and DOM elements
6. Download videos using JavaScript's fetch API within the browser context to maintain authentication

This approach bypasses CDN restrictions by utilizing the browser's native authentication state.
