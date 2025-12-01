"""
Scrape bios for committee members from MSCA website
"""

from playwright.sync_api import sync_playwright
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def main():
    print("Scraping bios from MSCA...")

    with open(DATA_DIR / 'scientific_committee.json') as f:
        committee = json.load(f)['selected']

    bios = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.digital-finance-msca.com/our-people', wait_until='networkidle')
        time.sleep(5)

        # Scroll to load all
        for i in range(40):
            page.evaluate(f'window.scrollTo(0, {i*350})')
            time.sleep(0.2)

        for name in committee:
            print(f"\nSearching bio for: {name}")

            try:
                # Find the name element
                name_el = page.locator(f'text="{name}"').first
                name_el.scroll_into_view_if_needed()
                time.sleep(0.3)

                box = name_el.bounding_box()
                if not box:
                    print(f"  Could not find")
                    continue

                # Look for bio text near the name
                bio = page.evaluate('''(params) => {
                    const nameY = params.y;
                    const nameX = params.x;

                    // Find all text elements
                    const allText = [];
                    document.querySelectorAll('p, span, div').forEach(el => {
                        const rect = el.getBoundingClientRect();
                        const text = el.innerText?.trim();

                        if (!text || text.length < 50 || text.length > 800) return;

                        // Should be below or near the name
                        const vDist = rect.top - nameY;
                        const hDist = Math.abs(rect.left - nameX);

                        if (vDist > -20 && vDist < 200 && hDist < 300) {
                            // Skip if it's an institution name or contains common non-bio patterns
                            if (/^(University|Institute|School|European|Funded|Views|Grant)/i.test(text)) return;
                            if (/Marie Sk.*odowska|Horizon Europe|European Union/i.test(text)) return;

                            allText.push({text, dist: vDist + hDist});
                        }
                    });

                    // Sort by distance and get the best candidate
                    allText.sort((a, b) => a.dist - b.dist);

                    for (const item of allText) {
                        // Check if it looks like a bio (contains bio-like words)
                        if (/research|professor|PhD|interests|focus|expertise|works|studies|specializ/i.test(item.text)) {
                            return item.text;
                        }
                    }

                    return allText.length > 0 ? allText[0].text : null;
                }''', {'x': box['x'], 'y': box['y']})

                if bio:
                    bios[name] = bio
                    print(f"  Found: {bio[:60]}...")
                else:
                    print(f"  No bio found")

            except Exception as e:
                print(f"  Error: {e}")

        browser.close()

    # Save bios
    with open(DATA_DIR / 'msca_bios.json') as f:
        existing = json.load(f)

    existing['bios'] = bios

    with open(DATA_DIR / 'msca_bios.json', 'w') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    print(f"\n\nSaved {len(bios)} bios")

if __name__ == "__main__":
    main()
