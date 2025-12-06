"""
Download partner university logos using Playwright for dynamic pages
"""

import asyncio
import requests
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    from PIL import Image
    from io import BytesIO
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

BASE_DIR = Path(__file__).parent.parent
LOGOS_DIR = BASE_DIR / "assets" / "logos"
LOGOS_DIR.mkdir(exist_ok=True)

# Direct logo URLs that should work
DIRECT_URLS = {
    "fhgr": "https://www.fhgr.ch/typo3conf/ext/fhgr_template/Resources/Public/Images/Logo/logo-fhgr.svg",
    "bfh": "https://www.bfh.ch/dam/jcr:4e0d4ddb-6c08-4dc3-9f9f-f5c7d5d45f1e/BFH_Logo_A_de_100_4f.png",
}

async def download_with_playwright():
    """Use Playwright to screenshot logos from websites"""
    if not HAS_PLAYWRIGHT:
        print("Playwright not available")
        return

    universities = [
        ("fhgr", "https://www.fhgr.ch", "img[alt*='Logo'], img[alt*='logo'], .logo img"),
        ("aus", "https://www.aus.edu", "img[alt*='Logo'], img[alt*='logo'], .logo img, header img"),
        ("manchester", "https://www.manchester.ac.uk", "img[alt*='Logo'], img[alt*='logo'], .logo img"),
        ("renmin", "https://www.ruc.edu.cn/en", "img[alt*='Logo'], img[alt*='logo'], .logo img"),
        ("babes_bolyai", "https://www.ubbcluj.ro/en/", "img[alt*='Logo'], img[alt*='logo'], .logo img"),
        ("bfh", "https://www.bfh.ch", "img[alt*='Logo'], img[alt*='logo'], .logo img"),
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for name, url, selector in universities:
            print(f"\n{name.upper()}: {url}")
            try:
                page = await browser.new_page()
                await page.goto(url, wait_until='domcontentloaded', timeout=15000)
                await asyncio.sleep(2)

                # Try to find logo
                logo = await page.query_selector(selector)
                if logo:
                    # Take screenshot of just the logo element
                    output = LOGOS_DIR / f"{name}.png"
                    await logo.screenshot(path=str(output))
                    print(f"  Saved: {output.name}")
                else:
                    print(f"  Logo element not found")

                await page.close()
            except Exception as e:
                print(f"  Error: {e}")

        await browser.close()

def create_text_logos():
    """Create simple text-based logos as SVG"""
    print("\nCreating text-based logo placeholders...")

    logos = {
        "fhgr": {"text": "FHGR", "color": "#004B87", "name": "Fachhochschule Graubunden"},
        "aus": {"text": "AUS", "color": "#00205B", "name": "American University of Sharjah"},
        "manchester": {"text": "UoM", "color": "#660099", "name": "University of Manchester"},
        "renmin": {"text": "RUC", "color": "#8B0000", "name": "Renmin University"},
        "babes_bolyai": {"text": "UBB", "color": "#003366", "name": "Babes-Bolyai University"},
        "bfh": {"text": "BFH", "color": "#000000", "name": "Bern University of Applied Sciences"},
    }

    for name, data in logos.items():
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50" viewBox="0 0 100 50">
  <rect width="100" height="50" fill="white" rx="5"/>
  <rect x="2" y="2" width="96" height="46" fill="none" stroke="{data['color']}" stroke-width="2" rx="4"/>
  <text x="50" y="32" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="{data['color']}" text-anchor="middle">{data['text']}</text>
</svg>'''
        output = LOGOS_DIR / f"{name}.svg"
        with open(output, 'w') as f:
            f.write(svg)
        print(f"  Created: {output.name}")

def main():
    print("=" * 50)
    print("Partner University Logos")
    print("=" * 50)

    # Try Playwright first
    if HAS_PLAYWRIGHT:
        print("\nTrying to download logos with Playwright...")
        asyncio.run(download_with_playwright())

    # Check what we got
    existing = list(LOGOS_DIR.glob("*.png")) + list(LOGOS_DIR.glob("*.svg"))
    print(f"\nExisting logos: {len(existing)}")

    # Create text placeholders for any missing
    needed = {"fhgr", "aus", "manchester", "renmin", "babes_bolyai", "bfh"}
    have = {f.stem for f in existing}
    missing = needed - have

    if missing:
        print(f"Missing: {missing}")
        create_text_logos()

    print("\nDone!")
    for f in LOGOS_DIR.glob("*"):
        print(f"  {f.name}")

if __name__ == "__main__":
    main()
