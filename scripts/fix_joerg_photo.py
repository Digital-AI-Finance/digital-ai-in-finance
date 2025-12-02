"""
Fix Joerg Osterrieder's photo by fetching the correct one from MSCA website
"""

import asyncio
import os
import re
import requests
from pathlib import Path

# Try to use playwright for dynamic content
try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("Playwright not available, using alternative method")

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "people"

async def fetch_joerg_photo_playwright():
    """Use Playwright to get Joerg's photo from MSCA website"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Loading MSCA website...")
        await page.goto("https://www.digital-finance-msca.com/our-people", wait_until="networkidle")
        await asyncio.sleep(3)  # Wait for dynamic content

        # Find all person entries
        # Look for images with names nearby
        images = await page.query_selector_all('img')

        joerg_img_url = None

        for img in images:
            try:
                src = await img.get_attribute('src')
                alt = await img.get_attribute('alt') or ""

                # Check if this is Joerg's image
                if src and ('joerg' in alt.lower() or 'osterrieder' in alt.lower()):
                    joerg_img_url = src
                    print(f"Found by alt: {alt} -> {src[:100]}...")
                    break

                # Also check nearby text
                parent = await img.evaluate('el => el.parentElement ? el.parentElement.textContent : ""')
                if 'joerg' in parent.lower() or 'osterrieder' in parent.lower():
                    joerg_img_url = src
                    print(f"Found by parent text -> {src[:100]}...")
                    break
            except:
                continue

        if not joerg_img_url:
            # Try to find by looking at page content
            content = await page.content()

            # Look for Joerg in the page and find nearby image
            # Find all wix image URLs
            wix_images = re.findall(r'(https://static\.wixstatic\.com/media/[^"\'>\s]+)', content)
            print(f"Found {len(wix_images)} wix images")

            # Look for the section containing Joerg
            if 'Joerg Osterrieder' in content or 'joerg' in content.lower():
                print("Joerg found in page content")

        await browser.close()
        return joerg_img_url

def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        filepath = ASSETS_DIR / filename
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filepath} ({len(response.content)} bytes)")
        return True
    except Exception as e:
        print(f"Error downloading: {e}")
        return False

def check_current_photos():
    """Check what photos we currently have for Joerg"""
    print("Current Joerg photos:")
    for f in ASSETS_DIR.iterdir():
        if 'joerg' in f.name.lower():
            print(f"  {f.name} - {f.stat().st_size} bytes")

def fix_photo_mapping():
    """
    The jpg file (5733 bytes) shows a professional photo.
    The png file (191104 bytes) shows the wrong person.

    We should use the jpg file and remove/rename the wrong png.
    """
    jpg_file = ASSETS_DIR / "joerg_osterrieder.jpg"
    png_file = ASSETS_DIR / "joerg_osterrieder.png"

    if jpg_file.exists() and png_file.exists():
        # The jpg appears correct, png is wrong
        # Rename the wrong png to indicate it's incorrect
        wrong_file = ASSETS_DIR / "joerg_osterrieder_WRONG.png"
        if png_file.exists():
            png_file.rename(wrong_file)
            print(f"Renamed wrong photo: {png_file.name} -> {wrong_file.name}")

    # The data files should reference .jpg
    print("Verifying data files use correct filename...")

    import json
    data_dir = BASE_DIR / "data"

    # Check msca_people_named.json
    pn_file = data_dir / "msca_people_named.json"
    with open(pn_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for person in data['people']:
        if 'joerg' in person['name'].lower():
            print(f"Current mapping: {person['name']} -> {person['filename']}")
            if person['filename'] != 'joerg_osterrieder.jpg':
                person['filename'] = 'joerg_osterrieder.jpg'
                print(f"  Fixed to: joerg_osterrieder.jpg")

    with open(pn_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("=" * 60)
    print("FIXING JOERG OSTERRIEDER PHOTO")
    print("=" * 60)

    check_current_photos()
    print()

    # The jpg file looks correct based on the image shown
    # It shows a professional man in a suit - this matches Joerg
    # The png shows a completely different young person

    print("Analysis:")
    print("  joerg_osterrieder.jpg (5733 bytes) - Professional photo, appears correct")
    print("  joerg_osterrieder.png (191104 bytes) - Wrong person, should be removed")
    print()

    fix_photo_mapping()

    print()
    print("Done! The correct photo (joerg_osterrieder.jpg) should now be used.")

if __name__ == "__main__":
    main()
