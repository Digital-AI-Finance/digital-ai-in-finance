"""
Correctly scrape and match committee member data from MSCA website
- Name, Photo, University, Bio must all match correctly
"""

from playwright.sync_api import sync_playwright
import json
import time
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets" / "people"

# Ensure directories exist
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def clean_filename(name):
    """Create safe filename from name"""
    return re.sub(r'[^a-zA-Z0-9]', '_', name.lower()) + '.jpg'

def main():
    print("Scraping MSCA Digital Finance website for correct member data...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible for debugging
        page = browser.new_page()

        print("Loading page...")
        page.goto('https://www.digital-finance-msca.com/our-people', wait_until='networkidle')
        time.sleep(5)

        # Scroll to load all content
        print("Scrolling to load all members...")
        for i in range(50):
            page.evaluate(f'window.scrollTo(0, {i * 400})')
            time.sleep(0.15)

        # Go back to top
        page.evaluate('window.scrollTo(0, 0)')
        time.sleep(2)

        # Get all member cards - look for the structure with image + name + bio
        print("\nExtracting member data...")

        members_data = page.evaluate('''() => {
            const members = [];

            // Find all elements that look like member cards
            // Wix sites often have repeating structures
            const allImages = document.querySelectorAll('img');

            allImages.forEach(img => {
                const src = img.src;
                // Skip non-person images (logos, icons, etc.)
                if (!src || src.includes('logo') || src.includes('icon') ||
                    src.includes('static.wixstatic.com/media/11062b') ||
                    img.width < 50 || img.height < 50) return;

                // Look for nearby text elements (name, role, bio)
                const parent = img.closest('div[data-testid]') || img.parentElement?.parentElement?.parentElement;
                if (!parent) return;

                // Get all text in the vicinity
                const textElements = parent.querySelectorAll('p, span, h1, h2, h3, h4, h5, h6');
                const texts = [];
                textElements.forEach(el => {
                    const text = el.innerText?.trim();
                    if (text && text.length > 2 && text.length < 500) {
                        texts.push(text);
                    }
                });

                // Try to identify name (usually short, capitalized)
                let name = null;
                let affiliation = null;
                let bio = null;

                for (const text of texts) {
                    // Name pattern: typically 2-4 words, capitalized
                    if (!name && text.length < 50 && /^[A-Z][a-z]+ [A-Z]/.test(text)) {
                        // Check it's not a common non-name phrase
                        if (!text.includes('University') && !text.includes('Research') &&
                            !text.includes('Member') && !text.includes('Digital')) {
                            name = text;
                        }
                    }
                    // Affiliation: contains University, Institute, etc.
                    if (!affiliation && (text.includes('University') || text.includes('Institute') ||
                        text.includes('School') || text.includes('Bank'))) {
                        affiliation = text;
                    }
                    // Bio: longer text with research-related words
                    if (!bio && text.length > 100 &&
                        (text.includes('research') || text.includes('focus') ||
                         text.includes('PhD') || text.includes('Professor'))) {
                        bio = text;
                    }
                }

                if (name && src.includes('wixstatic.com')) {
                    members.push({
                        name: name,
                        affiliation: affiliation || '',
                        bio: bio || '',
                        imageUrl: src,
                        imgWidth: img.naturalWidth || img.width,
                        imgHeight: img.naturalHeight || img.height
                    });
                }
            });

            return members;
        }''')

        print(f"Found {len(members_data)} potential members")

        # Deduplicate by name
        seen_names = set()
        unique_members = []
        for m in members_data:
            if m['name'] not in seen_names:
                seen_names.add(m['name'])
                unique_members.append(m)

        print(f"Unique members: {len(unique_members)}")

        # Download photos and save data
        final_members = []
        for member in unique_members:
            name_safe = member['name'].encode('ascii', 'replace').decode()
            print(f"\n{name_safe}")
            aff_safe = member['affiliation'][:60].encode('ascii', 'replace').decode() if member['affiliation'] else "No affiliation"
            print(f"  Affiliation: {aff_safe}")

            # Download photo
            filename = clean_filename(member['name'])
            filepath = ASSETS_DIR / filename

            try:
                response = page.request.get(member['imageUrl'])
                if response.ok:
                    with open(filepath, 'wb') as f:
                        f.write(response.body())
                    size = filepath.stat().st_size
                    print(f"  Photo: {filename} ({size} bytes)")

                    if size > 2000:  # Real photo
                        final_members.append({
                            'name': member['name'],
                            'affiliation': member['affiliation'],
                            'bio': member['bio'],
                            'filename': filename
                        })
            except Exception as e:
                print(f"  Photo error: {e}")

        browser.close()

    # Save to JSON
    output = {
        'source': 'https://www.digital-finance-msca.com/our-people',
        'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'members': final_members
    }

    with open(DATA_DIR / 'msca_members_correct.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n\nSaved {len(final_members)} members to msca_members_correct.json")

if __name__ == "__main__":
    main()
