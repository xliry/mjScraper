"""Video downloader with progress tracking"""

import asyncio
import aiohttp
import requests
from pathlib import Path
from typing import List
from tqdm import tqdm
import hashlib
import config


class VideoDownloader:
    def __init__(self, output_folder: str = config.DOWNLOAD_FOLDER):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        self.downloaded_count = 0
        self.failed_count = 0

    def sanitize_filename(self, url: str) -> str:
        """Create a safe filename from URL"""
        # Use hash of URL to create unique filename
        url_hash = hashlib.md5(url.encode()).hexdigest()[:10]

        # Try to get extension from URL
        if '.mp4' in url.lower():
            ext = '.mp4'
        elif '.webm' in url.lower():
            ext = '.webm'
        elif '.mov' in url.lower():
            ext = '.mov'
        else:
            ext = '.mp4'  # default

        return f"midjourney_video_{self.downloaded_count + 1}_{url_hash}{ext}"

    def download_video_sync(self, url: str, filename: str) -> bool:
        """Download a single video synchronously with progress bar"""
        try:
            filepath = self.output_folder / filename

            # Skip if already downloaded
            if filepath.exists():
                print(f"⏭️  Skipping (already exists): {filename}")
                return True

            print(f"⬇️  Downloading: {filename}")

            response = requests.get(url, stream=True, timeout=config.DOWNLOAD_TIMEOUT)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            with open(filepath, 'wb') as f, tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=filename[:30]
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

            self.downloaded_count += 1
            print(f"✅ Downloaded: {filename}")
            return True

        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            self.failed_count += 1
            return False

    async def download_video_async(self, session: aiohttp.ClientSession, url: str, filename: str) -> bool:
        """Download a single video asynchronously"""
        try:
            filepath = self.output_folder / filename

            # Skip if already downloaded
            if filepath.exists():
                print(f"⏭️  Skipping (already exists): {filename}")
                return True

            print(f"⬇️  Downloading: {filename}")

            async with session.get(url, timeout=aiohttp.ClientTimeout(total=config.DOWNLOAD_TIMEOUT)) as response:
                response.raise_for_status()

                with open(filepath, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)

            self.downloaded_count += 1
            print(f"✅ Downloaded: {filename}")
            return True

        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            self.failed_count += 1
            return False

    def download_all_sync(self, video_urls: List[str]) -> None:
        """Download all videos synchronously (one at a time)"""
        print(f"\n🎬 Starting download of {len(video_urls)} videos...")
        print(f"📁 Saving to: {self.output_folder.absolute()}\n")

        for i, url in enumerate(video_urls, 1):
            print(f"\n[{i}/{len(video_urls)}]")
            filename = self.sanitize_filename(url)
            self.download_video_sync(url, filename)

        print(f"\n{'='*60}")
        print(f"📊 Download Summary:")
        print(f"   ✅ Successfully downloaded: {self.downloaded_count}")
        print(f"   ❌ Failed: {self.failed_count}")
        print(f"   📁 Location: {self.output_folder.absolute()}")
        print(f"{'='*60}\n")

    async def download_all_async(self, video_urls: List[str]) -> None:
        """Download all videos asynchronously (parallel downloads)"""
        print(f"\n🎬 Starting parallel download of {len(video_urls)} videos...")
        print(f"📁 Saving to: {self.output_folder.absolute()}\n")

        async with aiohttp.ClientSession() as session:
            # Create semaphore to limit concurrent downloads
            semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_DOWNLOADS)

            async def download_with_semaphore(url: str):
                async with semaphore:
                    filename = self.sanitize_filename(url)
                    return await self.download_video_async(session, url, filename)

            # Download all videos
            tasks = [download_with_semaphore(url) for url in video_urls]
            await asyncio.gather(*tasks)

        print(f"\n{'='*60}")
        print(f"📊 Download Summary:")
        print(f"   ✅ Successfully downloaded: {self.downloaded_count}")
        print(f"   ❌ Failed: {self.failed_count}")
        print(f"   📁 Location: {self.output_folder.absolute()}")
        print(f"{'='*60}\n")


async def main():
    """Test downloader with sample URLs"""
    # Example usage
    downloader = VideoDownloader()

    # Read URLs from file if exists
    urls_file = Path(config.DOWNLOAD_FOLDER) / "video_urls.txt"
    if urls_file.exists():
        with open(urls_file, 'r') as f:
            video_urls = [line.strip() for line in f if line.strip()]

        if video_urls:
            # Choose download method
            print("Choose download method:")
            print("1. Sequential (one at a time, with progress bars)")
            print("2. Parallel (multiple at once, faster)")
            choice = input("Enter choice (1 or 2): ").strip()

            if choice == "2":
                await downloader.download_all_async(video_urls)
            else:
                downloader.download_all_sync(video_urls)
        else:
            print("❌ No video URLs found in video_urls.txt")
    else:
        print("❌ video_urls.txt not found. Run scraper.py first.")


if __name__ == "__main__":
    asyncio.run(main())
