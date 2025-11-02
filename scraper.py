"""Midjourney video scraper using Playwright"""

import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright, Page
from typing import List, Set
import config


class MidjourneyVideoScraper:
    def __init__(self):
        self.video_urls: Set[str] = set()
        self.download_folder = Path(config.DOWNLOAD_FOLDER)
        self.download_folder.mkdir(exist_ok=True)

    async def handle_popup(self, page: Page) -> bool:
        """Handle the 'Look around a bit' popup"""
        try:
            print("🔍 Checking for popup...")
            # Wait for popup and click "Look around a bit" button
            # Try multiple possible selectors
            selectors = [
                "text=Look around a bit",
                "button:has-text('Look around a bit')",
                "[aria-label*='Look around']",
                "button:has-text('look around')"
            ]

            for selector in selectors:
                try:
                    button = page.locator(selector)
                    if await button.count() > 0:
                        await button.first.click(timeout=5000)
                        print("✅ Popup closed successfully")
                        await page.wait_for_timeout(2000)  # Wait for popup to close
                        return True
                except Exception:
                    continue

            print("ℹ️  No popup found or already closed")
            return False

        except Exception as e:
            print(f"⚠️  Popup handling error (might be ok): {e}")
            return False

    async def scroll_to_bottom(self, page: Page) -> None:
        """Scroll to the bottom of the page to load all videos"""
        print("📜 Starting infinite scroll...")

        previous_height = 0
        no_change_count = 0
        scroll_count = 0

        while scroll_count < config.SCROLL_ATTEMPTS:
            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # Wait for new content to load
            await page.wait_for_timeout(config.SCROLL_PAUSE_TIME * 1000)

            # Get new height
            current_height = await page.evaluate("document.body.scrollHeight")

            # Check if we've reached the bottom
            if current_height == previous_height:
                no_change_count += 1
                if no_change_count >= 3:
                    print("✅ Reached bottom of page (no new content after 3 attempts)")
                    break
            else:
                no_change_count = 0
                scroll_count += 1
                print(f"📊 Scroll {scroll_count}: Height {previous_height} -> {current_height}")

            previous_height = current_height

        print(f"✅ Scrolling complete. Total scrolls: {scroll_count}")

    async def extract_video_urls(self, page: Page) -> List[str]:
        """Extract all video URLs from the page"""
        print("🎬 Extracting video URLs...")

        # Method 1: Find video elements
        video_elements = await page.locator("video").all()
        print(f"Found {len(video_elements)} video elements")

        for video in video_elements:
            # Try to get src attribute
            src = await video.get_attribute("src")
            if src:
                self.video_urls.add(src)

            # Try to get source children
            sources = await video.locator("source").all()
            for source in sources:
                src = await source.get_attribute("src")
                if src:
                    self.video_urls.add(src)

        # Method 2: Intercept network requests for video files
        # This is handled by the page.on("response") listener in scrape()

        print(f"✅ Found {len(self.video_urls)} unique video URLs")
        return list(self.video_urls)

    async def scrape(self) -> List[str]:
        """Main scraping method"""
        async with async_playwright() as p:
            print("🚀 Launching browser...")
            browser = await p.chromium.launch(
                headless=False,  # Set to True for production
                args=['--disable-blink-features=AutomationControlled']
            )

            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=config.USER_AGENT
            )

            page = await context.new_page()

            # Intercept video requests
            async def handle_response(response):
                url = response.url
                # Check if response is a video
                if any(ext in url.lower() for ext in ['.mp4', '.webm', '.mov', '.m3u8']):
                    self.video_urls.add(url)
                # Also check content-type
                try:
                    content_type = response.headers.get('content-type', '')
                    if 'video' in content_type:
                        self.video_urls.add(url)
                except:
                    pass

            page.on("response", handle_response)

            print(f"🌐 Navigating to {config.TARGET_URL}")
            await page.goto(config.TARGET_URL, wait_until="networkidle", timeout=config.PAGE_LOAD_TIMEOUT)

            # Wait for page to load
            await page.wait_for_timeout(3000)

            # Handle popup
            await self.handle_popup(page)

            # Wait a bit more
            await page.wait_for_timeout(2000)

            # Scroll to load all videos
            await self.scroll_to_bottom(page)

            # Extract video URLs
            video_urls = await self.extract_video_urls(page)

            print(f"🎯 Total videos found: {len(video_urls)}")

            # Save URLs to file
            urls_file = self.download_folder / "video_urls.txt"
            with open(urls_file, "w") as f:
                for url in video_urls:
                    f.write(f"{url}\n")
            print(f"💾 Video URLs saved to {urls_file}")

            await browser.close()

            return video_urls


async def main():
    scraper = MidjourneyVideoScraper()
    video_urls = await scraper.scrape()
    return video_urls


if __name__ == "__main__":
    asyncio.run(main())
