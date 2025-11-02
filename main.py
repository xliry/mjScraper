"""
Midjourney Video Scraper - Main Script

This script orchestrates the scraping and downloading of videos from midjourney.com/explore
"""

import asyncio
from scraper import MidjourneyVideoScraper


async def main():
    print("="*60)
    print("🎨 MIDJOURNEY VIDEO SCRAPER")
    print("="*60)
    print()

    # Ask user for download preference upfront
    print("Choose action:")
    print("  1. Scrape URLs and download videos (Recommended)")
    print("  2. Only scrape URLs (no download)")
    print()

    choice = input("Enter choice (1/2) [default: 1]: ").strip() or "1"
    download_videos = (choice == "1")

    print()
    print("📍 Starting scraper...")
    print()

    scraper = MidjourneyVideoScraper()
    video_urls = await scraper.scrape(download_videos=download_videos)

    if not video_urls:
        print("❌ No videos found. Exiting...")
        return

    print()
    print("="*60)
    print("🎉 ALL DONE!")
    print(f"📊 Total videos: {len(video_urls)}")
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
