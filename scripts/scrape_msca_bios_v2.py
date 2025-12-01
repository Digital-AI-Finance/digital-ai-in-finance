"""
Scrape biographies/CVs from MSCA Digital Finance website - Version 2
Improved extraction targeting actual bio text near person names
"""

import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def scrape_bios():
    """Scrape people with their biographical information"""

    print("Starting Playwright browser...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading MSCA Our People page...")
        page.goto("https://www.digital-finance-msca.com/our-people", wait_until="networkidle")

        # Wait for content to load
        time.sleep(5)

        # Scroll to load all content
        print("Scrolling to load all content...")
        for _ in range(15):
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(0.3)

        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)

        print("Extracting bio data...")

        # Get the structure of person entries
        people_bios = page.evaluate(r'''() => {
            const results = {};

            // Find all rich text or paragraph elements
            const allElements = document.querySelectorAll('p, span, div');
            const textBlocks = [];

            allElements.forEach(el => {
                const text = el.innerText.trim();
                // Look for text blocks that are bio-length (100-600 chars)
                if (text.length > 80 && text.length < 800) {
                    // Check if it contains bio-like keywords
                    const bioKeywords = /professor|phd|research|university|expert|specializ|focus|interests|department|school|institute|doctorate|master|bachelor/i;
                    if (bioKeywords.test(text)) {
                        textBlocks.push({
                            text: text,
                            rect: el.getBoundingClientRect()
                        });
                    }
                }
            });

            // Find name elements and try to match with nearby bios
            const namePattern = /^[A-Z][a-z]+(\s+[A-Z][a-z-]+){1,3}$/;
            const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6, strong, b, [class*="name"], [class*="title"]');

            headings.forEach(h => {
                const name = h.innerText.trim();
                if (namePattern.test(name) && name.length > 5 && name.length < 40) {
                    const nameRect = h.getBoundingClientRect();

                    // Find closest bio text block
                    let closestBio = null;
                    let minDistance = Infinity;

                    textBlocks.forEach(block => {
                        // Calculate distance (prefer text below or to the right of name)
                        const dx = block.rect.left - nameRect.left;
                        const dy = block.rect.top - nameRect.top;

                        // Bio should be below or close to the name
                        if (dy >= -50 && dy < 300) {
                            const distance = Math.abs(dx) + Math.abs(dy);
                            if (distance < minDistance) {
                                minDistance = distance;
                                closestBio = block.text;
                            }
                        }
                    });

                    if (closestBio && !results[name]) {
                        results[name] = closestBio;
                    }
                }
            });

            return results;
        }''')

        print(f"Found {len(people_bios)} direct bio matches")

        # Also get full page text for backup extraction
        full_text = page.evaluate('() => document.body.innerText')

        browser.close()

        return people_bios, full_text

def extract_affiliations_from_text(text):
    """Extract name -> affiliation mappings from page text"""
    affiliations = {}

    # Common institutions
    institutions = [
        ("American University of Sharjah", "AUS, UAE"),
        ("Athena Research Center", "Athena, Greece"),
        ("Babes-Bolyai University", "UBB, Romania"),
        ("Bern University of Applied Sciences", "BFH, Switzerland"),
        ("Bucharest University of Economic Studies", "ASE, Romania"),
        ("Chinese Academy of Sciences", "CAS, China"),
        ("ETH Zurich", "ETH, Switzerland"),
        ("Grisons University of Applied Sciences", "FHGR, Switzerland"),
        ("FH Graubuenden", "FHGR, Switzerland"),
        ("University of Applied Sciences Grisons", "FHGR, Switzerland"),
        ("FHGR", "FHGR, Switzerland"),
        ("Humboldt", "HU Berlin, Germany"),
        ("Kaunas University of Technology", "KTU, Lithuania"),
        ("RPTU Kaiserslautern-Landau", "RPTU, Germany"),
        ("Technical University of Kaiserslautern", "RPTU, Germany"),
        ("UBB", "UBB, Romania"),
        ("University of Manchester", "UoM, UK"),
        ("University of Pavia", "UniPV, Italy"),
        ("University of Pristina", "UP, Kosovo"),
        ("Universita degli Studi di Napoli", "UniNA, Italy"),
        ("WU Vienna", "WU, Austria"),
        ("Renmin University", "RUC, China"),
        ("Queensland University", "UQ, Australia"),
        ("Coimbra", "UC, Portugal"),
        ("Calabria", "UniCal, Italy")
    ]

    lines = text.split('\n')

    for i, line in enumerate(lines):
        line = line.strip()
        # Check if line looks like a name
        if re.match(r'^[A-Z][a-z]+(\s+[A-Z][a-z-]+){1,3}$', line) and 5 < len(line) < 40:
            # Look at surrounding lines for institution
            for j in range(max(0, i-5), min(len(lines), i+5)):
                for inst_full, inst_short in institutions:
                    if inst_full.lower() in lines[j].lower():
                        affiliations[line] = inst_short
                        break

    return affiliations

def main():
    print("Scraping MSCA bios (v2)...")

    # Load known names from scientific committee
    committee_file = DATA_DIR / "scientific_committee.json"
    with open(committee_file, 'r', encoding='utf-8') as f:
        committee = json.load(f)['selected']

    print(f"Looking for bios for {len(committee)} committee members")

    # Scrape the page
    people_bios, full_text = scrape_bios()

    # Match committee members
    bios = {}
    affiliations = {}

    # Get affiliations from text
    all_affiliations = extract_affiliations_from_text(full_text)

    for cm in committee:
        # Try exact match first
        if cm in people_bios:
            bios[cm] = people_bios[cm]
            print(f"  Found bio for: {cm}")

        # Try partial match
        for name, bio in people_bios.items():
            if cm.lower() in name.lower() or name.lower() in cm.lower():
                if cm not in bios:
                    bios[cm] = bio
                    print(f"  Found bio for: {cm} (partial match with {name})")
                break

        # Get affiliation
        if cm in all_affiliations:
            affiliations[cm] = all_affiliations[cm]
        else:
            # Try partial match
            for name, aff in all_affiliations.items():
                if cm.lower() in name.lower() or name.lower() in cm.lower():
                    affiliations[cm] = aff
                    break

    print(f"\nTotal bios found: {len(bios)} / {len(committee)}")
    print(f"Total affiliations found: {len(affiliations)} / {len(committee)}")

    # Save results
    output_file = DATA_DIR / "msca_bios.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'source': 'https://www.digital-finance-msca.com/our-people',
            'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'bios': bios,
            'affiliations': affiliations
        }, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_file}")

    # Print samples
    if bios:
        print("\nSample bios:")
        for name, bio in list(bios.items())[:3]:
            try:
                print(f"  {name}: {bio[:100]}...")
            except:
                print(f"  {name}: [bio text available]")

if __name__ == "__main__":
    main()
