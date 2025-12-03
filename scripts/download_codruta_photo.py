"""
Download Codruta Mare's correct photo from MSCA website
"""

import asyncio
import requests
import re
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "people"

async def download_photo():
    if not HAS_PLAYWRIGHT:
        print("Playwright required")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Loading MSCA website...")
        await page.goto("https://www.digital-finance-msca.com/our-people", wait_until="networkidle")
        await asyncio.sleep(5)

        # Find all text elements
        text_elements = await page.query_selector_all('span, p, div')

        codruta_img_url = None

        for elem in text_elements:
            try:
                text = await elem.inner_text()
                if text.strip() == "Codruta Mare":
                    print(f"Found exact match: '{text}'")

                    # Get the parent container and look for nearby image
                    # Navigate up to find the container with the image
                    container = await elem.evaluate('''el => {
                        let parent = el.parentElement;
                        for (let i = 0; i < 10; i++) {
                            if (!parent) break;
                            const img = parent.querySelector('img');
                            if (img && img.src) {
                                return img.src;
                            }
                            parent = parent.parentElement;
                        }
                        return null;
                    }''')

                    if container:
                        codruta_img_url = container
                        print(f"Found image URL: {codruta_img_url[:100]}...")
                        break
            except:
                continue

        if not codruta_img_url:
            # Alternative: find by looking at all images and their nearby text
            print("Trying alternative method...")
            images = await page.query_selector_all('img')

            for img in images:
                try:
                    src = await img.get_attribute('src')
                    if not src or 'wixstatic' not in src:
                        continue

                    # Get text near this image
                    nearby_text = await img.evaluate('''el => {
                        let parent = el.parentElement;
                        for (let i = 0; i < 5; i++) {
                            if (!parent) break;
                            const text = parent.textContent || '';
                            if (text.includes('Codruta')) {
                                return text;
                            }
                            parent = parent.parentElement;
                        }
                        return '';
                    }''')

                    if 'Codruta' in nearby_text:
                        codruta_img_url = src
                        print(f"Found via nearby text: {nearby_text[:50]}")
                        print(f"Image URL: {src[:100]}...")
                        break
                except:
                    continue

        if codruta_img_url:
            # Download the image
            print("Downloading image...")

            # Clean URL (remove Wix transformations to get full size)
            clean_url = re.sub(r'/v1/fill/[^/]+/', '/v1/fill/w_300,h_300/', codruta_img_url)

            response = requests.get(clean_url, timeout=30)
            if response.status_code == 200:
                # Save as jpg
                output_path = ASSETS_DIR / "codruta_mare_correct.jpg"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Saved to: {output_path} ({len(response.content)} bytes)")

                # Also replace the wrong file
                wrong_path = ASSETS_DIR / "codruta_mare.jpg"
                with open(wrong_path, 'wb') as f:
                    f.write(response.content)
                print(f"Updated: {wrong_path}")
            else:
                print(f"Download failed: {response.status_code}")
        else:
            print("Could not find Codruta Mare's photo")

        await browser.close()

def main():
    asyncio.run(download_photo())

if __name__ == "__main__":
    main()
