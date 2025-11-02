"""Configuration settings for Midjourney video scraper"""

# URL to scrape
TARGET_URL = "https://www.midjourney.com/explore?tab=video_top"

# Download settings
DOWNLOAD_FOLDER = "downloads"
MAX_CONCURRENT_DOWNLOADS = 5

# Scraping settings
SCROLL_PAUSE_TIME = 2  # seconds to wait after each scroll
SCROLL_ATTEMPTS = 100  # maximum scroll attempts (adjust based on need)

# Timeouts
PAGE_LOAD_TIMEOUT = 30000  # milliseconds
DOWNLOAD_TIMEOUT = 60  # seconds per video

# User agent (optional, Playwright handles this)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
