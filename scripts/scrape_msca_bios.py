"""
Scrape biographies/CVs from MSCA Digital Finance website
Uses Playwright to handle JavaScript-rendered content
"""

import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def scrape_people_with_bios():
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
        for _ in range(10):
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(0.5)

        # Scroll back to top
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)

        print("Extracting people data...")

        # Get all text content that looks like a person entry
        # The MSCA site typically shows: Name, Title/Role, Institution, Bio

        # Try to find person containers
        people_data = page.evaluate('''() => {
            const people = [];

            // Find all elements that might contain person info
            // Look for containers with images and text nearby
            const allText = document.body.innerText;

            // Get all potential name elements (usually bold or heading)
            const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6, strong, b');
            const processedNames = new Set();

            headings.forEach(h => {
                const text = h.innerText.trim();
                // Check if it looks like a name (2-4 words, proper case)
                if (text && text.split(/\\s+/).length >= 2 && text.split(/\\s+/).length <= 5) {
                    // Check if it starts with a capital letter and has reasonable length
                    if (/^[A-Z]/.test(text) && text.length > 5 && text.length < 50) {
                        // Try to find associated description
                        let parent = h.parentElement;
                        let bio = '';
                        let affiliation = '';

                        // Look for nearby text content
                        for (let i = 0; i < 5 && parent; i++) {
                            const siblings = parent.querySelectorAll('p, span, div');
                            siblings.forEach(s => {
                                const sibText = s.innerText.trim();
                                if (sibText.length > 50 && sibText.length < 1000 && !sibText.includes(text)) {
                                    if (!bio || sibText.length > bio.length) {
                                        bio = sibText;
                                    }
                                }
                                // Look for affiliation (shorter text, may contain University, Institute, etc.)
                                if (sibText.length > 10 && sibText.length < 100) {
                                    if (/University|Institute|School|College|Department|Professor|Dr\.|PhD/.test(sibText)) {
                                        affiliation = sibText;
                                    }
                                }
                            });
                            parent = parent.parentElement;
                        }

                        if (!processedNames.has(text.toLowerCase())) {
                            processedNames.add(text.toLowerCase());
                            people.push({
                                name: text,
                                affiliation: affiliation,
                                bio: bio
                            });
                        }
                    }
                }
            });

            return people;
        }''')

        print(f"Found {len(people_data)} potential person entries")

        # Also try to get structured data from any data attributes or JSON
        structured_data = page.evaluate('''() => {
            // Look for any script tags with JSON-LD or embedded data
            const scripts = document.querySelectorAll('script[type="application/ld+json"]');
            const data = [];
            scripts.forEach(s => {
                try {
                    const json = JSON.parse(s.textContent);
                    data.push(json);
                } catch (e) {}
            });
            return data;
        }''')

        if structured_data:
            print(f"Found {len(structured_data)} structured data blocks")

        # Get the full page text for analysis
        full_text = page.evaluate('() => document.body.innerText')

        browser.close()

        return {
            'people': people_data,
            'structured': structured_data,
            'full_text': full_text[:50000]  # First 50k chars
        }

def extract_bios_from_text(text, known_names):
    """Extract bio information for known names from page text"""
    bios = {}

    # Split text into paragraphs
    paragraphs = text.split('\n\n')

    for name in known_names:
        name_lower = name.lower()
        # Find paragraphs mentioning this name
        for i, para in enumerate(paragraphs):
            if name_lower in para.lower() or name.split()[0].lower() in para.lower():
                # Check surrounding paragraphs for bio-like content
                bio_candidates = []
                for j in range(max(0, i-2), min(len(paragraphs), i+3)):
                    p = paragraphs[j].strip()
                    # Bio-like: longer text, contains words like "research", "PhD", "Professor"
                    if len(p) > 100 and len(p) < 800:
                        if any(kw in p.lower() for kw in ['research', 'phd', 'professor', 'university', 'specializes', 'focuses', 'interests']):
                            bio_candidates.append(p)

                if bio_candidates:
                    bios[name] = max(bio_candidates, key=len)
                    break

    return bios

def main():
    print("Scraping MSCA bios...")

    # Load known names from scientific committee
    committee_file = DATA_DIR / "scientific_committee.json"
    with open(committee_file, 'r', encoding='utf-8') as f:
        committee = json.load(f)['selected']

    print(f"Looking for bios for {len(committee)} committee members")

    # Scrape the page
    data = scrape_people_with_bios()

    # Try to match with known names
    bios = {}

    # First check extracted people data
    for person in data.get('people', []):
        name = person.get('name', '')
        bio = person.get('bio', '')
        if bio and len(bio) > 50:
            # Try to match with committee members
            for cm in committee:
                if cm.lower() in name.lower() or name.lower() in cm.lower():
                    bios[cm] = bio
                    print(f"  Found bio for: {cm}")
                    break

    # Also try to extract from full text
    text_bios = extract_bios_from_text(data.get('full_text', ''), committee)
    for name, bio in text_bios.items():
        if name not in bios:
            bios[name] = bio
            print(f"  Found bio from text for: {name}")

    print(f"\nTotal bios found: {len(bios)} / {len(committee)}")

    # Save results
    output_file = DATA_DIR / "msca_bios.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'source': 'https://www.digital-finance-msca.com/our-people',
            'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'bios': bios,
            'raw_people': data.get('people', [])[:50]  # First 50 for reference
        }, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_file}")

    # Print sample
    if bios:
        print("\nSample bio:")
        name = list(bios.keys())[0]
        print(f"  {name}: {bios[name][:200]}...")

if __name__ == "__main__":
    main()
