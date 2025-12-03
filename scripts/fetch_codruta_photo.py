"""
Fetch Codruta Mare's correct photo from MSCA website
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
    print("Playwright not available")

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "people"

async def fetch_photo():
    if not HAS_PLAYWRIGHT:
        print("Playwright required for this script")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Loading MSCA website...")
        await page.goto("https://www.digital-finance-msca.com/our-people", wait_until="networkidle")
        await asyncio.sleep(5)

        # Get page content
        content = await page.content()

        # Find all image URLs
        wix_images = re.findall(r'(https://static\.wixstatic\.com/media/[^"\'>\s]+)', content)
        print(f"Found {len(wix_images)} images")

        # Look for text containing "Codruta"
        codruta_found = 'codruta' in content.lower() or 'mare' in content.lower()
        print(f"Codruta/Mare found in page: {codruta_found}")

        # Try to find elements with names
        elements = await page.query_selector_all('[data-testid*="richTextElement"]')
        print(f"Found {len(elements)} rich text elements")

        for elem in elements:
            text = await elem.inner_text()
            if 'codruta' in text.lower():
                print(f"Found Codruta in element: {text[:100]}")

                # Try to find nearby image
                parent = await elem.evaluate('el => el.closest("div").parentElement')

        # Screenshot for debugging
        await page.screenshot(path=str(BASE_DIR / "debug_codruta_search.png"), full_page=True)
        print(f"Saved debug screenshot")

        await browser.close()

def main():
    print("Searching for Codruta Mare's photo on MSCA website...")
    asyncio.run(fetch_photo())

if __name__ == "__main__":
    main()
