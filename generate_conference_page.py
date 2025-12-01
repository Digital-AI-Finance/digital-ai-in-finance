"""
Compact conference webpage with sidebar navigation
"""

import base64
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "images"
PEOPLE_ASSETS_DIR = BASE_DIR / "assets" / "people"
OUTPUT_FILE = BASE_DIR / "index.html"

def load_json(filepath):
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_image_base64(filepath):
    """Load image only if it's a real photo (>2KB), not placeholder"""
    if filepath.exists():
        size = filepath.stat().st_size
        if size > 2000:  # Real photos are larger than 2KB
            with open(filepath, 'rb') as f:
                ext = filepath.suffix.lower()
                mime = 'image/png' if ext == '.png' else 'image/jpeg'
                return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return None

DATES = [
    ("Submission", "Feb 15, 2026"),
    ("Notification", "Mar 1, 2026"),
    ("Registration", "Mar 15, 2026"),
    ("Workshop", "Apr 21-23, 2026")
]

TOPICS = [
    "LLMs in Finance", "Explainable AI", "Blockchain Security",
    "Risk Management", "Digital Banking", "Alternative Data"
]

PROGRAM = [
    ("Day 1", "Apr 21", [("09:00", "Opening & Keynote"), ("11:00", "Panel: LLMs"), ("14:00", "Research"), ("16:00", "Workshop"), ("18:00", "Reception")]),
    ("Day 2", "Apr 22", [("09:00", "Keynote: XAI"), ("10:30", "Panel: Blockchain"), ("13:30", "Research"), ("15:30", "Workshop")]),
    ("Day 3", "Apr 23", [("09:00", "Keynote: MENA Banking"), ("10:30", "Collaboration"), ("13:30", "Panel"), ("15:30", "Signing"), ("19:00", "Gala")])
]

def generate_html():
    committee_data = load_json(DATA_DIR / "scientific_committee.json")
    committee = committee_data.get('selected', [])

    photo_data = load_json(DATA_DIR / "msca_people_named.json")
    photo_map = {p['name'].lower(): p['filename'] for p in photo_data.get('people', [])}

    affiliations_data = load_json(DATA_DIR / "msca_bios.json")
    affiliations = affiliations_data.get('affiliations', {})
    bios = affiliations_data.get('bios', {})

    network_map = load_image_base64(IMAGES_DIR / "network_map.png")

    css = '''
    :root { --blue: #2E5090; --gold: #D4AF37; --dark: #1a1a2e; --light: #f0f0f0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, -apple-system, sans-serif; font-size: 13px; line-height: 1.4; color: #333; display: flex; min-height: 100vh; }

    /* Sidebar */
    .sidebar { width: 200px; background: var(--dark); color: white; position: fixed; height: 100vh; padding: 15px; overflow-y: auto; }
    .sidebar h1 { font-size: 0.95rem; color: var(--gold); margin-bottom: 5px; }
    .sidebar .subtitle { font-size: 0.7rem; opacity: 0.7; margin-bottom: 15px; border-bottom: 1px solid #444; padding-bottom: 10px; }
    .sidebar nav a { display: block; color: white; text-decoration: none; padding: 6px 10px; font-size: 0.8rem; border-radius: 4px; margin-bottom: 2px; opacity: 0.8; }
    .sidebar nav a:hover { background: rgba(255,255,255,0.1); opacity: 1; }
    .sidebar .register-btn { display: block; background: var(--gold); color: var(--dark); text-align: center; padding: 8px; border-radius: 4px; font-weight: 700; font-size: 0.8rem; margin-top: 15px; text-decoration: none; }
    .sidebar .info { margin-top: 20px; padding-top: 15px; border-top: 1px solid #444; font-size: 0.7rem; opacity: 0.6; }

    /* Main */
    main { margin-left: 200px; flex: 1; background: white; }

    /* Hero */
    .hero { background: linear-gradient(135deg, var(--blue), #1a3a6e); color: white; padding: 25px 20px; }
    .hero h1 { font-size: 1.4rem; color: white; }
    .hero p { opacity: 0.9; font-size: 0.85rem; margin-top: 3px; }
    .hero-info { display: flex; gap: 25px; margin-top: 12px; flex-wrap: wrap; }
    .hero-info div span:first-child { font-size: 0.65rem; text-transform: uppercase; opacity: 0.7; }
    .hero-info div span:last-child { display: block; font-weight: 600; font-size: 0.9rem; }

    /* Sections */
    section { padding: 20px; border-bottom: 1px solid #eee; }
    h2 { font-size: 1rem; color: var(--blue); margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
    h2::before { content: ''; width: 3px; height: 16px; background: var(--gold); }

    /* Dates */
    .dates { display: flex; gap: 8px; flex-wrap: wrap; }
    .date-item { background: var(--light); padding: 8px 12px; border-radius: 4px; text-align: center; flex: 1; min-width: 100px; }
    .date-item .label { font-size: 0.65rem; color: #666; text-transform: uppercase; }
    .date-item .value { font-size: 0.85rem; font-weight: 700; color: var(--blue); }

    /* Topics */
    .topics { display: flex; gap: 6px; flex-wrap: wrap; }
    .topic { background: var(--blue); color: white; padding: 5px 10px; border-radius: 3px; font-size: 0.75rem; }

    /* Program */
    .program { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
    .day { background: var(--light); border-radius: 5px; overflow: hidden; }
    .day-header { background: var(--blue); color: white; padding: 6px 10px; font-size: 0.8rem; font-weight: 600; }
    .day-header span { opacity: 0.8; font-weight: 400; }
    .session { padding: 4px 10px; font-size: 0.75rem; border-bottom: 1px solid #ddd; display: flex; }
    .session:last-child { border: none; }
    .session-time { width: 40px; font-weight: 600; color: var(--blue); }

    /* Committee */
    .committee { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 8px; }
    .member { text-align: center; padding: 8px 4px; }
    .member img { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; border: 2px solid var(--blue); }
    .member .initials { width: 45px; height: 45px; border-radius: 50%; background: linear-gradient(135deg, var(--blue), #1a3a6e); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin: 0 auto; }
    .member .name { font-size: 0.7rem; font-weight: 600; margin-top: 4px; line-height: 1.2; }
    .member .aff { font-size: 0.6rem; color: #888; }
    .member { position: relative; cursor: pointer; }
    .member .bio { display: none; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); background: var(--dark); color: white; padding: 8px 10px; border-radius: 5px; font-size: 0.65rem; width: 180px; text-align: left; z-index: 100; line-height: 1.3; }
    .member:hover .bio { display: block; }

    /* Venue */
    .venue-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
    .venue-info h3 { font-size: 0.9rem; color: var(--blue); margin-bottom: 3px; }
    .venue-info p { font-size: 0.75rem; color: #666; }
    .venue-info ul { list-style: none; font-size: 0.7rem; margin-top: 8px; }
    .venue-info li { padding: 2px 0 2px 12px; position: relative; }
    .venue-info li::before { content: "-"; position: absolute; left: 0; color: var(--gold); }
    .venue-map iframe { width: 100%; height: 150px; border: none; border-radius: 4px; }

    /* Network */
    .network-img { max-width: 100%; height: auto; border-radius: 5px; margin-top: 10px; }

    /* Chairs */
    .chairs { font-size: 0.8rem; color: #555; margin-bottom: 8px; }

    @media (max-width: 900px) {
        .sidebar { width: 160px; }
        main { margin-left: 160px; }
        .program { grid-template-columns: 1fr; }
        .venue-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 600px) {
        .sidebar { display: none; }
        main { margin-left: 0; }
    }
    '''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI for Digital Finance 2026</title>
    <style>{css}</style>
</head>
<body>
    <aside class="sidebar">
        <h1>AI for Digital Finance</h1>
        <div class="subtitle">Swiss-MENA Workshop 2026</div>
        <nav>
            <a href="#dates">Important Dates</a>
            <a href="#topics">Topics</a>
            <a href="#program">Program</a>
            <a href="#committee">Committee</a>
            <a href="#venue">Venue</a>
            <a href="#network">Network</a>
        </nav>
        <a href="#" class="register-btn" onclick="alert('Opens Jan 2026'); return false;">Register</a>
        <div class="info">
            Apr 21-23, 2026<br>
            AUS, Sharjah, UAE<br><br>
            80-100 participants
        </div>
    </aside>

    <main>
        <section class="hero">
            <h1>AI for Digital Finance Workshop</h1>
            <p>Swiss-MENA Research Network</p>
            <div class="hero-info">
                <div><span>Date</span><span>April 21-23, 2026</span></div>
                <div><span>Venue</span><span>American University of Sharjah</span></div>
                <div><span>Participants</span><span>80-100 expected</span></div>
            </div>
        </section>

        <section id="dates">
            <h2>Important Dates</h2>
            <div class="dates">'''

    for label, date in DATES:
        html += f'<div class="date-item"><div class="label">{label}</div><div class="value">{date}</div></div>'

    html += '''
            </div>
        </section>

        <section id="topics">
            <h2>Topics</h2>
            <div class="topics">'''

    for topic in TOPICS:
        html += f'<span class="topic">{topic}</span>'

    html += '''
            </div>
        </section>

        <section id="program">
            <h2>Program</h2>
            <div class="program">'''

    for day, date, sessions in PROGRAM:
        html += f'<div class="day"><div class="day-header">{day} <span>({date})</span></div>'
        for time, title in sessions:
            html += f'<div class="session"><span class="session-time">{time}</span><span>{title}</span></div>'
        html += '</div>'

    html += '''
            </div>
        </section>

        <section id="committee">
            <h2>Scientific Committee</h2>
            <div class="chairs"><strong>Chairs:</strong> J. Osterrieder (FHGR) & S. Chan (AUS)</div>
            <div class="committee">'''

    for member in committee:
        photo_file = photo_map.get(member.lower())
        aff = affiliations.get(member, '')
        aff_short = aff.split(',')[0].replace("University of ", "U.").replace("University", "U.")[:25]
        bio = bios.get(member, '')

        photo_b64 = None
        if photo_file:
            photo_b64 = load_image_base64(PEOPLE_ASSETS_DIR / photo_file)

        bio_html = f'<div class="bio">{bio}</div>' if bio else ''

        if photo_b64:
            html += f'<div class="member"><img src="{photo_b64}" alt="{member}"><div class="name">{member}</div><div class="aff">{aff_short}</div>{bio_html}</div>'
        else:
            initials = ''.join(n[0].upper() for n in member.split()[:2] if n)
            html += f'<div class="member"><div class="initials">{initials}</div><div class="name">{member}</div><div class="aff">{aff_short}</div>{bio_html}</div>'

    html += '''
            </div>
        </section>

        <section id="venue">
            <h2>Venue</h2>
            <div class="venue-grid">
                <div class="venue-info">
                    <h3>American University of Sharjah</h3>
                    <p>University City, Sharjah, UAE</p>
                    <ul>
                        <li>Conference center (200+ capacity)</li>
                        <li>Full AV & WiFi</li>
                        <li>On-campus accommodation</li>
                        <li>25 min from Dubai Airport</li>
                    </ul>
                </div>
                <div class="venue-map">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3607!2d55.505!3d25.286!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5f5f!2sAmerican%20University%20of%20Sharjah!5e0!3m2!1sen!2sae" loading="lazy"></iframe>
                </div>
            </div>
        </section>

        <section id="network">
            <h2>Partner Network</h2>
            <p style="font-size:0.8rem;color:#666;">Core: FHGR (CH) & AUS (UAE) | Partners: Manchester, Renmin, Babes-Bolyai, BFH</p>'''

    if network_map:
        html += f'<img src="{network_map}" alt="Network" class="network-img">'

    html += '''
        </section>
    </main>
</body>
</html>'''

    return html

def main():
    print("Generating compact conference page...")
    html = generate_html()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
