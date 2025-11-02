"""
Midjourney Video Scraper - Main Script

This script orchestrates the scraping and downloading of videos from midjourney.com/explore
"""

import asyncio
from scraper import MidjourneyVideoScraper
from downloader import VideoDownloader


async def main():
    print("="*60)
    print("🎨 MIDJOURNEY VIDEO SCRAPER")
    print("="*60)
    print()

    # Step 1: Scrape video URLs
    print("📍 STEP 1: Scraping video URLs from Midjourney...")
    print()

    scraper = MidjourneyVideoScraper()
    video_urls = await scraper.scrape()

    if not video_urls:
        print("❌ No videos found. Exiting...")
        return

    print()
    print(f"✅ Found {len(video_urls)} videos!")
    print()

    # Step 2: Download videos
    print("📍 STEP 2: Downloading videos...")
    print()

    # Ask user for download method
    print("Choose download method:")
    print("  1. Sequential (one at a time, with progress bars) - Recommended")
    print("  2. Parallel (multiple at once, faster but less detailed progress)")
    print("  3. Skip downloads (only scrape URLs)")
    print()

    choice = input("Enter choice (1/2/3) [default: 1]: ").strip() or "1"

    if choice == "3":
        print("⏭️  Skipping downloads. URLs saved to downloads/video_urls.txt")
        return

    downloader = VideoDownloader()

    if choice == "2":
        await downloader.download_all_async(video_urls)
    else:
        downloader.download_all_sync(video_urls)

    print()
    print("="*60)
    print("🎉 ALL DONE!")
    print("="*60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
