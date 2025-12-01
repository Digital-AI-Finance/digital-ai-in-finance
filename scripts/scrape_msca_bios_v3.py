"""
Scrape affiliations and try to get bios from MSCA Digital Finance website - Version 3
Improved extraction based on page structure (people grouped under institutions)
"""

import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Known affiliations for committee members (from MSCA network)
KNOWN_AFFILIATIONS = {
    "Stephen Chan": "American University of Sharjah, UAE",
    "Codruta Mare": "Babes-Bolyai University, Romania",
    "Liana Stanca": "Babes-Bolyai University, Romania",
    "Monica Violeta Achim": "Babes-Bolyai University, Romania",
    "Stefana Belbe": "Babes-Bolyai University, Romania",
    "Joerg Osterrieder": "FHGR, Switzerland",
    "Alexandra-Ioana Conda": "Bucharest University of Economic Studies, Romania",
    "Daniel Traian Pele": "Bucharest University of Economic Studies, Romania",
    "Rui Ren": "Renmin University of China, China",
    "Vasile Strat": "Bucharest University of Economic Studies, Romania",
    "Wolfgang Hardle": "Humboldt University Berlin, Germany",
    "Ruting Wang": "Renmin University of China, China",
    "Ralf Korn": "RPTU Kaiserslautern-Landau, Germany",
    "Audrius Kabasinskas": "Kaunas University of Technology, Lithuania",
    "Kristina Sutiene": "Kaunas University of Technology, Lithuania",
    "Axel Gross-Klussmann": "Bern University of Applied Sciences, Switzerland",
    "Stefan Theussl": "WU Vienna, Austria",
    "Jeffrey Chu": "University of Manchester, UK",
    "Anastas Dzurovski": "University of Pristina, Kosovo",
    "Sabrina Giordano": "University of Calabria, Italy",
    "Catarina Silva": "University of Coimbra, Portugal",
    "Claudia Tarantola": "University of Pavia, Italy",
    "Maria Iannario": "University of Naples Federico II, Italy",
    "Ioana Coita": "University of Oradea, Romania",
    "Alessandra Tanda": "University of Pavia, Italy",
    "Albulena Shala": "University of Pristina, Kosovo",
    "Rezarta Perri": "University of Pristina, Kosovo",
    "Kurt Hornik": "WU Vienna, Austria",
    "Ronald Hochreiter": "WU Vienna, Austria"
}

def scrape_bios():
    """Try to scrape actual bios from individual profile pages or main page"""

    print("Starting Playwright browser...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading MSCA Our People page...")
        page.goto("https://www.digital-finance-msca.com/our-people", wait_until="networkidle")
        time.sleep(5)

        # Scroll to load all content
        for _ in range(15):
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(0.3)
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)

        # Try to find clickable person cards/links
        person_links = page.evaluate('''() => {
            const links = [];
            const anchors = document.querySelectorAll('a[href*="people"], a[href*="team"], a[href*="member"]');
            anchors.forEach(a => {
                links.push({href: a.href, text: a.innerText.trim()});
            });
            return links;
        }''')

        print(f"Found {len(person_links)} potential profile links")

        # Get text content near person names for bio extraction
        bios = {}
        full_text = page.evaluate('() => document.body.innerText')

        browser.close()

        # Try to extract bios from page text
        lines = full_text.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()
            # Check if line is a known committee member name
            for name in KNOWN_AFFILIATIONS.keys():
                if name.lower() == line.lower() or name.lower() in line.lower():
                    # Look for bio-like text in next few lines
                    bio_parts = []
                    for j in range(i+1, min(i+10, len(lines))):
                        next_line = lines[j].strip()
                        # Skip empty lines, short lines, or lines that look like another name
                        if not next_line or len(next_line) < 20:
                            continue
                        if re.match(r'^[A-Z][a-z]+(\s+[A-Z][a-z-]+){1,3}$', next_line):
                            break  # Hit another name
                        # Check if it looks like bio content
                        if any(kw in next_line.lower() for kw in ['professor', 'phd', 'research', 'university', 'department', 'interests', 'focus', 'specializ', 'expertise']):
                            bio_parts.append(next_line)
                            if len(' '.join(bio_parts)) > 200:
                                break

                    if bio_parts:
                        bios[name] = ' '.join(bio_parts)
                    break

        return bios

def main():
    print("Scraping MSCA data (v3)...")

    # Load known names from scientific committee
    committee_file = DATA_DIR / "scientific_committee.json"
    with open(committee_file, 'r', encoding='utf-8') as f:
        committee = json.load(f)['selected']

    print(f"Processing {len(committee)} committee members")

    # Try to scrape bios
    scraped_bios = scrape_bios()

    # Build final data with known affiliations
    affiliations = {}
    bios = {}

    for member in committee:
        # Get affiliation (from known data)
        if member in KNOWN_AFFILIATIONS:
            affiliations[member] = KNOWN_AFFILIATIONS[member]

        # Get bio if scraped
        if member in scraped_bios:
            bios[member] = scraped_bios[member]

    print(f"\nAffiliations: {len(affiliations)} / {len(committee)}")
    print(f"Bios found: {len(bios)} / {len(committee)}")

    # Save results
    output_file = DATA_DIR / "msca_bios.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'source': 'https://www.digital-finance-msca.com/our-people',
            'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'affiliations': affiliations,
            'bios': bios
        }, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_file}")

    # List members without bios (for manual addition)
    missing_bios = [m for m in committee if m not in bios]
    if missing_bios:
        print(f"\nMembers without scraped bios ({len(missing_bios)}):")
        for m in missing_bios:
            try:
                print(f"  - {m}")
            except:
                print(f"  - [name with special chars]")

if __name__ == "__main__":
    main()
