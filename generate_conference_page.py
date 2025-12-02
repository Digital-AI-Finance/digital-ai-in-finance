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
    ("LLMs in Finance", "topic_llms.html"),
    ("Explainable AI", "topic_xai.html"),
    ("Blockchain Security", "topic_blockchain.html"),
    ("Risk Management", "topic_risk.html"),
    ("Digital Banking", "topic_banking.html"),
    ("Alternative Data", "topic_altdata.html")
]

KEYNOTES = [
    ("TBC", "Keynote Speaker 1", "Institution TBC", "Talk title to be announced"),
    ("TBC", "Keynote Speaker 2", "Institution TBC", "Talk title to be announced"),
    ("TBC", "Keynote Speaker 3", "Institution TBC", "Talk title to be announced")
]

SESSIONS = {
    "Opening & Keynote": "Welcome address by conference chairs followed by the opening keynote on AI transformation in MENA financial markets.",
    "Panel: LLMs": "Industry-academia panel discussing practical applications of Large Language Models in banking and investment management.",
    "Research": "Contributed paper sessions featuring peer-reviewed research from workshop participants.",
    "Workshop": "Hands-on tutorial sessions covering tools and techniques for AI in finance research.",
    "Reception": "Networking reception at the AUS campus with refreshments.",
    "Keynote: XAI": "Featured talk on explainable AI requirements for regulatory compliance in financial services.",
    "Panel: Blockchain": "Discussion on security challenges and opportunities in DeFi and digital asset markets.",
    "Keynote: MENA Banking": "Special keynote on digital banking transformation across the MENA region.",
    "Collaboration": "Structured networking session to identify research collaboration opportunities.",
    "Panel": "Closing panel on the future of AI research collaboration between Swiss and MENA institutions.",
    "Signing": "Formal signing ceremony for research partnership agreements.",
    "Gala": "Conference gala dinner at a premier Sharjah venue."
}

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
    :root {
        --blue: #2E5090; --gold: #D4AF37; --dark: #1a1a2e; --light: #f0f0f0;
        --bg: white; --text: #333; --text-muted: #666;
    }
    [data-theme="dark"] {
        --bg: #1a1a2e; --light: #2a2a4e; --text: #e0e0e0; --text-muted: #aaa;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, -apple-system, sans-serif; font-size: 13px; line-height: 1.4; color: var(--text); display: flex; min-height: 100vh; background: var(--bg); transition: background 0.3s, color 0.3s; }

    /* Sidebar */
    .sidebar { width: 200px; background: var(--dark); color: white; position: fixed; height: 100vh; padding: 15px; overflow-y: auto; z-index: 100; }
    .sidebar h1 { font-size: 0.95rem; color: var(--gold); margin-bottom: 5px; }
    .sidebar .subtitle { font-size: 0.7rem; opacity: 0.7; margin-bottom: 15px; border-bottom: 1px solid #444; padding-bottom: 10px; }
    .sidebar nav a { display: block; color: white; text-decoration: none; padding: 6px 10px; font-size: 0.8rem; border-radius: 4px; margin-bottom: 2px; opacity: 0.8; }
    .sidebar nav a:hover { background: rgba(255,255,255,0.1); opacity: 1; }
    .sidebar .register-btn { display: block; background: var(--gold); color: var(--dark); text-align: center; padding: 8px; border-radius: 4px; font-weight: 700; font-size: 0.8rem; margin-top: 15px; text-decoration: none; }
    .sidebar .info { margin-top: 20px; padding-top: 15px; border-top: 1px solid #444; font-size: 0.7rem; opacity: 0.6; }
    .theme-toggle { background: none; border: 1px solid #555; color: white; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 0.7rem; margin-top: 10px; width: 100%; }
    .theme-toggle:hover { background: rgba(255,255,255,0.1); }

    /* Main */
    main { margin-left: 200px; flex: 1; background: var(--bg); }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, rgba(46,80,144,0.9), rgba(26,58,110,0.95)),
                    url('https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1200&q=80') center/cover;
        color: white; padding: 40px 20px; text-align: center; position: relative;
    }
    .hero h1 { font-size: 1.8rem; color: white; margin-bottom: 5px; }
    .hero .tagline { opacity: 0.9; font-size: 1rem; margin-bottom: 15px; }
    .countdown { display: flex; gap: 15px; justify-content: center; margin: 20px 0; }
    .countdown-item { background: rgba(255,255,255,0.15); padding: 10px 15px; border-radius: 8px; min-width: 70px; }
    .countdown-item .num { font-size: 1.8rem; font-weight: 700; display: block; }
    .countdown-item .label { font-size: 0.7rem; text-transform: uppercase; opacity: 0.8; }
    .hero-info { display: flex; gap: 25px; justify-content: center; flex-wrap: wrap; }
    .hero-info div span:first-child { font-size: 0.65rem; text-transform: uppercase; opacity: 0.7; }
    .hero-info div span:last-child { display: block; font-weight: 600; font-size: 0.9rem; }

    /* Stats Bar */
    .stats-bar { display: flex; justify-content: center; gap: 40px; padding: 20px; background: var(--dark); color: white; }
    .stat { text-align: center; }
    .stat .num { font-size: 1.5rem; font-weight: 700; color: var(--gold); }
    .stat .label { font-size: 0.7rem; text-transform: uppercase; opacity: 0.7; }

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
    .topic { background: var(--blue); color: white; padding: 5px 10px; border-radius: 3px; font-size: 0.75rem; text-decoration: none; transition: all 0.3s; cursor: pointer; }
    .topic:hover { background: #1a3a6e; transform: translateY(-2px); }

    /* Call for Papers */
    .cfp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
    .cfp-box { background: var(--light); padding: 12px; border-radius: 5px; }
    .cfp-box h4 { font-size: 0.8rem; color: var(--blue); margin-bottom: 5px; }
    .cfp-box p, .cfp-box li { font-size: 0.75rem; color: #555; }
    .cfp-box ul { list-style: none; margin-top: 5px; }
    .cfp-box li { padding: 2px 0; }
    .cfp-btn { display: inline-block; background: var(--gold); color: var(--dark); padding: 8px 20px; border-radius: 4px; text-decoration: none; font-weight: 600; font-size: 0.8rem; margin-top: 10px; }

    /* Keynotes */
    .keynotes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .keynote { background: var(--light); border-radius: 5px; padding: 15px; text-align: center; }
    .keynote-photo { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, var(--blue), #1a3a6e); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 700; margin: 0 auto 10px; }
    .keynote .name { font-weight: 600; font-size: 0.85rem; color: var(--blue); }
    .keynote .inst { font-size: 0.7rem; color: #888; }
    .keynote .talk { font-size: 0.75rem; color: #555; margin-top: 5px; font-style: italic; }

    /* Program */
    .program { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
    .day { background: var(--light); border-radius: 5px; overflow: hidden; }
    .day-header { background: var(--blue); color: white; padding: 6px 10px; font-size: 0.8rem; font-weight: 600; }
    .day-header span { opacity: 0.8; font-weight: 400; }
    .session { padding: 4px 10px; font-size: 0.75rem; border-bottom: 1px solid #ddd; display: flex; cursor: pointer; transition: background 0.2s; }
    .session:hover { background: rgba(46, 80, 144, 0.1); }
    .session:last-child { border: none; }
    .session-time { width: 40px; font-weight: 600; color: var(--blue); }
    .session-title { flex: 1; }

    /* Modal */
    .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center; }
    .modal.active { display: flex; }
    .modal-content { background: white; padding: 25px; border-radius: 8px; max-width: 500px; width: 90%; position: relative; }
    .modal-close { position: absolute; top: 10px; right: 15px; font-size: 1.5rem; cursor: pointer; color: #888; }
    .modal-close:hover { color: #333; }
    .modal h3 { color: var(--blue); margin-bottom: 10px; }
    .modal p { font-size: 0.9rem; color: #555; line-height: 1.5; }

    /* Share */
    .share-bar { display: flex; gap: 8px; justify-content: center; padding: 15px; background: var(--dark); }
    .share-btn { display: flex; align-items: center; gap: 5px; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 0.75rem; color: white; transition: opacity 0.2s; }
    .share-btn:hover { opacity: 0.8; }
    .share-linkedin { background: #0077B5; }
    .share-twitter { background: #1DA1F2; }
    .share-copy { background: #555; cursor: pointer; border: none; }
    .hashtag { color: var(--gold); font-size: 0.8rem; margin-left: 10px; }

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
    .chairs { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 8px; }

    /* Newsletter */
    .newsletter { background: linear-gradient(135deg, var(--blue), #1a3a6e); color: white; text-align: center; }
    .newsletter h2 { color: white; justify-content: center; }
    .newsletter h2::before { background: var(--gold); }
    .newsletter p { opacity: 0.9; margin-bottom: 15px; }
    .newsletter-form { display: flex; gap: 10px; max-width: 400px; margin: 0 auto; }
    .newsletter-form input { flex: 1; padding: 10px; border: none; border-radius: 4px; font-size: 0.85rem; }
    .newsletter-form button { background: var(--gold); color: var(--dark); border: none; padding: 10px 20px; border-radius: 4px; font-weight: 600; cursor: pointer; }
    .newsletter-form button:hover { opacity: 0.9; }

    /* Placeholder Sections */
    .placeholder-section { background: var(--light); text-align: center; }
    .placeholder-section .coming-soon { color: var(--text-muted); font-style: italic; padding: 30px; }
    .placeholder-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; opacity: 0.5; }
    .placeholder-card { background: var(--bg); border: 2px dashed #ccc; border-radius: 8px; padding: 20px; }

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
            <a href="#keynotes">Keynotes</a>
            <a href="#program">Program</a>
            <a href="#committee">Committee</a>
            <a href="#venue">Venue</a>
            <a href="#network">Network</a>
            <a href="#papers">Accepted Papers</a>
            <a href="#gallery">Gallery</a>
            <a href="#cfp">Call for Papers</a>
        </nav>
        <a href="#" class="register-btn" onclick="alert('Opens Jan 2026'); return false;">Register</a>
        <button class="theme-toggle" onclick="toggleTheme()">Toggle Dark Mode</button>
        <div class="info">
            Apr 21-23, 2026<br>
            AUS, Sharjah, UAE<br><br>
            80-100 participants
        </div>
    </aside>

    <main>
        <section class="hero">
            <h1>AI for Digital Finance Workshop</h1>
            <p class="tagline">Swiss-MENA Research Network | April 21-23, 2026</p>
            <div class="countdown" id="countdown">
                <div class="countdown-item"><span class="num" id="days">---</span><span class="label">Days</span></div>
                <div class="countdown-item"><span class="num" id="hours">--</span><span class="label">Hours</span></div>
                <div class="countdown-item"><span class="num" id="mins">--</span><span class="label">Minutes</span></div>
                <div class="countdown-item"><span class="num" id="secs">--</span><span class="label">Seconds</span></div>
            </div>
            <div class="hero-info">
                <div><span>Venue</span><span>American University of Sharjah</span></div>
                <div><span>Location</span><span>Sharjah, UAE</span></div>
            </div>
        </section>

        <div class="stats-bar">
            <div class="stat"><span class="num" data-target="80">0</span><span class="label">Participants</span></div>
            <div class="stat"><span class="num" data-target="6">0</span><span class="label">Topics</span></div>
            <div class="stat"><span class="num" data-target="3">0</span><span class="label">Days</span></div>
            <div class="stat"><span class="num" data-target="27">0</span><span class="label">Speakers</span></div>
        </div>

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

    for topic_name, topic_url in TOPICS:
        html += f'<a href="{topic_url}" class="topic">{topic_name}</a>'

    html += '''
            </div>
        </section>

        <section id="keynotes">
            <h2>Keynote Speakers</h2>
            <div class="keynotes">'''

    for initials, name, inst, talk in KEYNOTES:
        html += f'''<div class="keynote">
                <div class="keynote-photo">{initials}</div>
                <div class="name">{name}</div>
                <div class="inst">{inst}</div>
                <div class="talk">{talk}</div>
            </div>'''

    html += '''
            </div>
        </section>

        <section id="program">
            <h2>Program</h2>
            <div class="program">'''

    for day, date, sessions in PROGRAM:
        html += f'<div class="day"><div class="day-header">{day} <span>({date})</span></div>'
        for time, title in sessions:
            desc = SESSIONS.get(title, "Session details to be announced.")
            html += f'<div class="session" onclick="showModal(\'{title}\', \'{desc}\')"><span class="session-time">{time}</span><span class="session-title">{title}</span></div>'
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

        <section id="papers" class="placeholder-section">
            <h2>Accepted Papers</h2>
            <p class="coming-soon">Paper submissions open February 2026. Accepted papers will be listed here after the review process.</p>
            <div class="placeholder-grid">
                <div class="placeholder-card">Paper 1</div>
                <div class="placeholder-card">Paper 2</div>
                <div class="placeholder-card">Paper 3</div>
                <div class="placeholder-card">Paper 4</div>
            </div>
        </section>

        <section id="gallery" class="placeholder-section">
            <h2>Photo Gallery</h2>
            <p class="coming-soon">Photos from the workshop will be shared here after the event in April 2026.</p>
            <div class="placeholder-grid">
                <div class="placeholder-card">Photo</div>
                <div class="placeholder-card">Photo</div>
                <div class="placeholder-card">Photo</div>
                <div class="placeholder-card">Photo</div>
            </div>
        </section>

        <section id="newsletter" class="newsletter">
            <h2>Stay Updated</h2>
            <p>Subscribe to receive updates on speakers, accepted papers, and registration.</p>
            <form class="newsletter-form" onsubmit="subscribeNewsletter(event)">
                <input type="email" placeholder="Your email address" required>
                <button type="submit">Subscribe</button>
            </form>
        </section>

        <section id="cfp">
            <h2>Call for Papers</h2>
            <div class="cfp-grid">
                <div class="cfp-box">
                    <h4>Submission Guidelines</h4>
                    <ul>
                        <li>Extended abstract: 2-4 pages</li>
                        <li>Full paper: 8-12 pages</li>
                        <li>Format: PDF, double-column</li>
                        <li>Blind review process</li>
                    </ul>
                </div>
                <div class="cfp-box">
                    <h4>Key Deadlines</h4>
                    <ul>
                        <li>Submission: February 15, 2026</li>
                        <li>Notification: March 1, 2026</li>
                        <li>Camera-ready: March 15, 2026</li>
                    </ul>
                </div>
            </div>
            <div style="text-align:center;margin-top:15px;">
                <a href="mailto:submissions@ai-digital-finance.org" class="cfp-btn">Submit Paper</a>
            </div>
        </section>

        <div class="share-bar">
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://digital-ai-finance.github.io/digital-ai-in-finance/" target="_blank" class="share-btn share-linkedin">
                <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                LinkedIn
            </a>
            <a href="https://twitter.com/intent/tweet?url=https://digital-ai-finance.github.io/digital-ai-in-finance/&text=AI%20for%20Digital%20Finance%20Workshop%202026%20-%20Swiss-MENA%20Research%20Network" target="_blank" class="share-btn share-twitter">
                <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                Share
            </a>
            <button onclick="copyLink()" class="share-btn share-copy">
                <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg>
                Copy Link
            </button>
            <span class="hashtag">#AIDigitalFinance2026</span>
        </div>
    </main>

    <div class="modal" id="sessionModal" onclick="closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <h3 id="modalTitle"></h3>
            <p id="modalDesc"></p>
        </div>
    </div>

    <script>
        // Modal functions
        function showModal(title, desc) {
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalDesc').textContent = desc;
            document.getElementById('sessionModal').classList.add('active');
        }
        function closeModal(e) {
            if (!e || e.target.classList.contains('modal')) {
                document.getElementById('sessionModal').classList.remove('active');
            }
        }
        function copyLink() {
            navigator.clipboard.writeText('https://digital-ai-finance.github.io/digital-ai-in-finance/');
            alert('Link copied to clipboard!');
        }
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

        // Countdown Timer
        function updateCountdown() {
            const target = new Date('2026-04-21T09:00:00+04:00').getTime();
            const now = new Date().getTime();
            const diff = target - now;
            if (diff > 0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const secs = Math.floor((diff % (1000 * 60)) / 1000);
                document.getElementById('days').textContent = days;
                document.getElementById('hours').textContent = hours.toString().padStart(2, '0');
                document.getElementById('mins').textContent = mins.toString().padStart(2, '0');
                document.getElementById('secs').textContent = secs.toString().padStart(2, '0');
            } else {
                document.getElementById('countdown').innerHTML = '<div class="countdown-item"><span class="num">LIVE</span><span class="label">Now</span></div>';
            }
        }
        updateCountdown();
        setInterval(updateCountdown, 1000);

        // Animated Stats
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    document.querySelectorAll('.stat .num').forEach(num => {
                        const target = parseInt(num.dataset.target);
                        let current = 0;
                        const increment = target / 50;
                        const timer = setInterval(() => {
                            current += increment;
                            if (current >= target) {
                                num.textContent = target + '+';
                                clearInterval(timer);
                            } else {
                                num.textContent = Math.floor(current);
                            }
                        }, 30);
                    });
                    statsObserver.disconnect();
                }
            });
        }, { threshold: 0.5 });
        statsObserver.observe(document.querySelector('.stats-bar'));

        // Dark Mode Toggle
        function toggleTheme() {
            const body = document.body;
            const isDark = body.getAttribute('data-theme') === 'dark';
            body.setAttribute('data-theme', isDark ? '' : 'dark');
            localStorage.setItem('theme', isDark ? 'light' : 'dark');
        }
        // Load saved theme
        if (localStorage.getItem('theme') === 'dark') {
            document.body.setAttribute('data-theme', 'dark');
        }

        // Newsletter
        function subscribeNewsletter(e) {
            e.preventDefault();
            const email = e.target.querySelector('input').value;
            alert('Thank you for subscribing! You will receive updates at ' + email);
            e.target.reset();
        }
    </script>
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
