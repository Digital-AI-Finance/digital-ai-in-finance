"""
Generate compact conference webpage for AI Digital Finance Workshop
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

# Load data functions
def load_json(filepath):
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_image_base64(filepath):
    if filepath.exists():
        with open(filepath, 'rb') as f:
            ext = filepath.suffix.lower()
            mime = 'image/png' if ext == '.png' else 'image/jpeg'
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return None

# Conference data
DATES = [
    ("Submission Deadline", "Feb 15, 2026"),
    ("Notification", "Mar 1, 2026"),
    ("Registration", "Mar 15, 2026"),
    ("Workshop", "Apr 21-23, 2026")
]

TOPICS = [
    "Large Language Models in Finance",
    "Explainable AI for Compliance",
    "Blockchain & Fraud Detection",
    "ML for Risk Management",
    "Digital Banking Innovation",
    "Alternative Data in Finance"
]

PROGRAM = [
    {
        "day": "Day 1: Research Frontiers",
        "date": "April 21, 2026",
        "sessions": [
            ("09:00", "Opening & Keynote: AI Transformation in Finance"),
            ("11:00", "Panel: Large Language Models in Finance"),
            ("14:00", "Research Presentations"),
            ("16:00", "Workshop: Hands-on LLM Applications"),
            ("18:00", "Welcome Reception")
        ]
    },
    {
        "day": "Day 2: Industry Applications",
        "date": "April 22, 2026",
        "sessions": [
            ("09:00", "Keynote: Explainable AI for Compliance"),
            ("10:30", "Panel: Blockchain Security & Fraud Detection"),
            ("13:30", "Research Presentations"),
            ("15:30", "Workshop: Anomaly Detection")
        ]
    },
    {
        "day": "Day 3: Network Launch",
        "date": "April 23, 2026",
        "sessions": [
            ("09:00", "Keynote: Digital Banking in MENA"),
            ("10:30", "Research Collaboration Planning"),
            ("13:30", "Panel: Future of Swiss-MENA Collaboration"),
            ("15:30", "Bilateral Agreement Signing"),
            ("19:00", "Gala Dinner")
        ]
    }
]

def generate_html():
    # Load data
    committee_data = load_json(DATA_DIR / "scientific_committee.json")
    committee = committee_data.get('selected', [])

    photo_data = load_json(DATA_DIR / "msca_people_named.json")
    photo_map = {p['name'].lower(): p['filename'] for p in photo_data.get('people', [])}

    affiliations_data = load_json(DATA_DIR / "msca_bios.json")
    affiliations = affiliations_data.get('affiliations', {})

    network_map = load_image_base64(IMAGES_DIR / "network_map.png")

    # CSS
    css = '''
    :root { --blue: #2E5090; --gold: #D4AF37; --dark: #333; --light: #f5f5f5; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.5; color: var(--dark); font-size: 14px; }
    .container { max-width: 1100px; margin: 0 auto; padding: 0 15px; }

    /* Nav */
    nav { background: var(--blue); padding: 10px 0; position: sticky; top: 0; z-index: 100; }
    nav .container { display: flex; justify-content: space-between; align-items: center; }
    nav .logo { color: white; font-weight: 700; font-size: 1rem; }
    nav ul { display: flex; list-style: none; gap: 15px; }
    nav a { color: white; text-decoration: none; font-size: 0.8rem; opacity: 0.9; }
    nav a:hover { opacity: 1; }
    .nav-register { background: var(--gold); padding: 5px 12px; border-radius: 3px; color: #333 !important; font-weight: 600; }

    /* Hero */
    .hero { background: linear-gradient(135deg, var(--blue) 0%, #1a3a6e 100%); color: white; padding: 40px 0; text-align: center; }
    .hero h1 { font-size: 1.8rem; margin-bottom: 5px; }
    .hero .subtitle { font-size: 1rem; opacity: 0.9; margin-bottom: 20px; }
    .hero-info { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
    .hero-info div { text-align: center; }
    .hero-info .label { font-size: 0.7rem; text-transform: uppercase; opacity: 0.7; }
    .hero-info .value { font-size: 0.95rem; font-weight: 600; }

    /* Sections */
    section { padding: 30px 0; }
    section:nth-child(even) { background: var(--light); }
    h2 { font-size: 1.3rem; color: var(--blue); margin-bottom: 15px; border-bottom: 2px solid var(--gold); display: inline-block; padding-bottom: 3px; }

    /* Dates */
    .dates { display: flex; gap: 15px; flex-wrap: wrap; margin-top: 10px; }
    .date-item { background: white; padding: 12px 20px; border-radius: 5px; border-top: 3px solid var(--gold); text-align: center; flex: 1; min-width: 140px; }
    .date-item .label { font-size: 0.75rem; color: #666; text-transform: uppercase; }
    .date-item .value { font-size: 0.95rem; font-weight: 700; color: var(--blue); margin-top: 3px; }

    /* Topics */
    .topics { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin-top: 10px; }
    .topic { background: white; padding: 12px; border-radius: 5px; border-left: 3px solid var(--blue); font-size: 0.85rem; }

    /* Program */
    .program-day { background: white; border-radius: 5px; margin-bottom: 15px; overflow: hidden; }
    .day-header { background: var(--blue); color: white; padding: 8px 15px; font-weight: 600; font-size: 0.9rem; }
    .day-header span { font-weight: 400; opacity: 0.8; margin-left: 10px; font-size: 0.8rem; }
    .session { display: flex; padding: 8px 15px; border-bottom: 1px solid #eee; font-size: 0.85rem; }
    .session:last-child { border: none; }
    .session-time { width: 50px; font-weight: 600; color: var(--blue); }

    /* Committee */
    .committee-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px; margin-top: 15px; }
    .member { text-align: center; padding: 10px 5px; }
    .member img { width: 55px; height: 55px; border-radius: 50%; object-fit: cover; border: 2px solid var(--blue); }
    .member .initials { width: 55px; height: 55px; border-radius: 50%; background: var(--blue); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto; }
    .member .name { font-size: 0.8rem; font-weight: 600; margin-top: 5px; }
    .member .affiliation { font-size: 0.65rem; color: #666; margin-top: 2px; }

    /* Venue */
    .venue-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px; }
    .venue-info h3 { color: var(--blue); font-size: 1rem; margin-bottom: 5px; }
    .venue-info p { font-size: 0.85rem; color: #666; margin-bottom: 10px; }
    .venue-info ul { list-style: none; font-size: 0.8rem; }
    .venue-info li { padding: 3px 0; padding-left: 15px; position: relative; }
    .venue-info li::before { content: "-"; position: absolute; left: 0; color: var(--gold); }
    .venue-map iframe { width: 100%; height: 200px; border: none; border-radius: 5px; }

    /* Network */
    .network-map { text-align: center; margin-top: 15px; }
    .network-map img { max-width: 100%; height: auto; border-radius: 5px; }

    /* Register */
    .register-section { background: linear-gradient(135deg, var(--blue) 0%, #1a3a6e 100%); color: white; text-align: center; padding: 30px 0; }
    .register-section h2 { color: white; border-color: var(--gold); }
    .register-section p { opacity: 0.9; margin-bottom: 15px; font-size: 0.9rem; }
    .register-btn { display: inline-block; background: var(--gold); color: #333; padding: 10px 30px; border-radius: 5px; text-decoration: none; font-weight: 700; }

    /* Footer */
    footer { background: #222; color: white; padding: 20px 0; text-align: center; font-size: 0.8rem; }
    footer a { color: var(--gold); }
    .footer-contacts { display: flex; justify-content: center; gap: 40px; margin-top: 10px; }

    /* Responsive */
    @media (max-width: 768px) {
        nav ul { gap: 8px; }
        nav a { font-size: 0.7rem; }
        .venue-grid { grid-template-columns: 1fr; }
        .hero h1 { font-size: 1.4rem; }
    }
    '''

    # Build HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI for Digital Finance Workshop 2026 | Swiss-MENA Research Network</title>
    <style>{css}</style>
</head>
<body>
    <nav>
        <div class="container">
            <div class="logo">AI for Digital Finance 2026</div>
            <ul>
                <li><a href="#dates">Dates</a></li>
                <li><a href="#topics">Topics</a></li>
                <li><a href="#program">Program</a></li>
                <li><a href="#committee">Committee</a></li>
                <li><a href="#venue">Venue</a></li>
                <li><a href="#register" class="nav-register">Register</a></li>
            </ul>
        </div>
    </nav>

    <section class="hero">
        <div class="container">
            <h1>AI for Digital Finance</h1>
            <p class="subtitle">Swiss-MENA Research Network Workshop</p>
            <div class="hero-info">
                <div><div class="label">Date</div><div class="value">April 21-23, 2026</div></div>
                <div><div class="label">Location</div><div class="value">American University of Sharjah, UAE</div></div>
                <div><div class="label">Participants</div><div class="value">80-100 Expected</div></div>
            </div>
        </div>
    </section>

    <section id="dates">
        <div class="container">
            <h2>Important Dates</h2>
            <div class="dates">'''

    for label, date in DATES:
        html += f'''
                <div class="date-item">
                    <div class="label">{label}</div>
                    <div class="value">{date}</div>
                </div>'''

    html += '''
            </div>
        </div>
    </section>

    <section id="topics">
        <div class="container">
            <h2>Topics</h2>
            <div class="topics">'''

    for topic in TOPICS:
        html += f'''
                <div class="topic">{topic}</div>'''

    html += '''
            </div>
        </div>
    </section>

    <section id="program">
        <div class="container">
            <h2>Program</h2>'''

    for day in PROGRAM:
        html += f'''
            <div class="program-day">
                <div class="day-header">{day["day"]}<span>{day["date"]}</span></div>'''
        for time, session in day["sessions"]:
            html += f'''
                <div class="session">
                    <div class="session-time">{time}</div>
                    <div>{session}</div>
                </div>'''
        html += '''
            </div>'''

    html += '''
        </div>
    </section>

    <section id="committee">
        <div class="container">
            <h2>Scientific Committee</h2>
            <p style="font-size: 0.85rem; color: #666; margin-bottom: 10px;">
                <strong>Chairs:</strong> Prof. Joerg Osterrieder (FHGR, Switzerland) & Prof. Stephen Chan (AUS, UAE)
            </p>
            <div class="committee-grid">'''

    for member in committee:
        photo_file = photo_map.get(member.lower())
        affiliation = affiliations.get(member, '')
        # Shorten affiliation
        aff_short = affiliation.replace("University of Applied Sciences", "UAS").replace("University", "U.").replace(", Romania", ", RO").replace(", Germany", ", DE").replace(", Switzerland", ", CH").replace(", Lithuania", ", LT").replace(", Italy", ", IT").replace(", Portugal", ", PT").replace(", Austria", ", AT").replace(", Kosovo", ", XK").replace(", UK", ", UK").replace(", China", ", CN").replace(", UAE", ", UAE")

        if photo_file:
            photo_b64 = load_image_base64(PEOPLE_ASSETS_DIR / photo_file)
            if photo_b64:
                html += f'''
                <div class="member">
                    <img src="{photo_b64}" alt="{member}">
                    <div class="name">{member}</div>
                    <div class="affiliation">{aff_short}</div>
                </div>'''
            else:
                initials = ''.join(n[0].upper() for n in member.split()[:2] if n)
                html += f'''
                <div class="member">
                    <div class="initials">{initials}</div>
                    <div class="name">{member}</div>
                    <div class="affiliation">{aff_short}</div>
                </div>'''
        else:
            initials = ''.join(n[0].upper() for n in member.split()[:2] if n)
            html += f'''
                <div class="member">
                    <div class="initials">{initials}</div>
                    <div class="name">{member}</div>
                    <div class="affiliation">{aff_short}</div>
                </div>'''

    html += '''
            </div>
        </div>
    </section>

    <section id="venue">
        <div class="container">
            <h2>Venue</h2>
            <div class="venue-grid">
                <div class="venue-info">
                    <h3>American University of Sharjah</h3>
                    <p>University City, Sharjah, UAE</p>
                    <ul>
                        <li>Modern conference center (200+ capacity)</li>
                        <li>Full AV equipment & high-speed WiFi</li>
                        <li>On-campus accommodation</li>
                        <li>25 min from Dubai Airport (DXB)</li>
                    </ul>
                </div>
                <div class="venue-map">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3607.0!2d55.505!3d25.286!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5f5f!2sAmerican%20University%20of%20Sharjah!5e0!3m2!1sen!2sae" loading="lazy"></iframe>
                </div>
            </div>
        </div>
    </section>

    <section id="network">
        <div class="container">
            <h2>Partner Network</h2>
            <p style="font-size: 0.85rem; color: #666;">FHGR (Switzerland) & AUS (UAE) as core partners, with Universities of Manchester, Renmin, Babes-Bolyai, and BFH.</p>'''

    if network_map:
        html += f'''
            <div class="network-map">
                <img src="{network_map}" alt="Partner Network Map">
            </div>'''

    html += '''
        </div>
    </section>

    <section id="register" class="register-section">
        <div class="container">
            <h2>Register</h2>
            <p>Join researchers and practitioners for 3 days of knowledge exchange and collaboration.</p>
            <a href="#" class="register-btn" onclick="alert('Registration opens January 2026'); return false;">Registration Opens Jan 2026</a>
        </div>
    </section>

    <footer>
        <div class="container">
            <strong>AI for Digital Finance: Swiss-MENA Research Network</strong><br>
            Connect & Collaborate Grant | Leading House MENA
            <div class="footer-contacts">
                <div>Prof. Joerg Osterrieder<br><a href="mailto:joerg.osterrieder@fhgr.ch">joerg.osterrieder@fhgr.ch</a></div>
                <div>Prof. Stephen Chan<br><a href="mailto:schan@aus.edu">schan@aus.edu</a></div>
            </div>
        </div>
    </footer>
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
