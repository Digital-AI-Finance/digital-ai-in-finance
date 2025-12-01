"""
Generate AI Digital Finance HTML pages
Based on official CCG submission materials

Outputs:
- ai_digital_finance.html (public page - no budget)
- budget_internal.html (internal only - budget details)
"""

import base64
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "images"
DATA_DIR = DOCS_DIR / "data"
PEOPLE_DATA_DIR = BASE_DIR / "data"
PEOPLE_ASSETS_DIR = BASE_DIR / "assets" / "people"
OUTPUT_PUBLIC = BASE_DIR / "ai_digital_finance.html"
OUTPUT_BUDGET = BASE_DIR / "budget_internal.html"

# Official Budget Data (from Excel - CHF 18,000 total)
BUDGET_DATA = {
    "total": 18000,
    "ccg_request": 5000,
    "swiss_partners": {
        "total": 5140,
        "travel_ccg": 2640,
        "work_inkind": 2500
    },
    "mena_partners": {
        "total": 12860,
        "event_ccg": 2360,
        "event_inkind": 4900,
        "work_inkind": 5000,
        "publication_inkind": 600
    }
}

# Publications data
def load_publications():
    pub_file = DATA_DIR / "publications.json"
    if pub_file.exists():
        with open(pub_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Load Scientific Committee
def load_scientific_committee():
    committee_file = PEOPLE_DATA_DIR / "scientific_committee.json"
    if committee_file.exists():
        with open(committee_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('selected', [])
    return []

# Load photo mappings
def load_photo_mappings():
    """Load name-to-photo mappings from named scrape"""
    photo_file = PEOPLE_DATA_DIR / "msca_people_named.json"
    if photo_file.exists():
        with open(photo_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Create name -> filename mapping (lowercase for matching)
            mapping = {}
            for person in data.get('people', []):
                name_lower = person['name'].lower()
                mapping[name_lower] = person['filename']
            return mapping
    return {}

# Load photo as base64
def load_photo_base64(filename):
    """Load a photo file and return base64 encoded string"""
    photo_path = PEOPLE_ASSETS_DIR / filename
    if photo_path.exists():
        with open(photo_path, 'rb') as f:
            ext = photo_path.suffix.lower()
            mime = 'image/jpeg'
            if ext == '.png':
                mime = 'image/png'
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return None

# Load affiliations
def load_affiliations():
    """Load affiliations from MSCA bios file"""
    bios_file = PEOPLE_DATA_DIR / "msca_bios.json"
    if bios_file.exists():
        with open(bios_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('affiliations', {})
    return {}

# Important dates for the conference
IMPORTANT_DATES = [
    {"label": "Submission Deadline", "date": "February 15, 2026"},
    {"label": "Notification", "date": "March 1, 2026"},
    {"label": "Early Registration", "date": "March 15, 2026"},
    {"label": "Workshop", "date": "April 21-23, 2026"}
]

# Load and encode network map
def load_network_map_base64():
    img_path = IMAGES_DIR / "network_map.png"
    if img_path.exists():
        with open(img_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return ""

# Workshop topics
WORKSHOP_TOPICS = [
    {
        "title": "Large Language Models in Finance",
        "desc": "Applications of GPT, BERT, and domain-specific LLMs for financial text analysis, sentiment extraction, and automated reporting."
    },
    {
        "title": "Explainable AI for Compliance",
        "desc": "Interpretable ML models for regulatory compliance, audit trails, and transparent decision-making in financial services."
    },
    {
        "title": "Blockchain Security & Fraud Detection",
        "desc": "Machine learning approaches for cryptocurrency fraud detection, smart contract analysis, and blockchain forensics."
    },
    {
        "title": "Machine Learning for Risk Management",
        "desc": "Advanced ML techniques for credit risk, market risk, operational risk assessment and portfolio optimization."
    },
    {
        "title": "Digital Banking Innovation",
        "desc": "AI-powered digital banking services, robo-advisors, personalized financial products, and customer analytics."
    },
    {
        "title": "Alternative Data in Finance",
        "desc": "Non-traditional data sources including satellite imagery, social media, web scraping for financial predictions."
    }
]

# Venue information
VENUE_INFO = {
    "name": "American University of Sharjah",
    "location": "Sharjah, United Arab Emirates",
    "building": "Conference Center",
    "address": "University City, Sharjah, UAE",
    "description": "AUS is a leading comprehensive coeducational university in the Gulf region, offering undergraduate and graduate programs. The campus features modern conference facilities with full AV support, breakout rooms, and catering services.",
    "features": [
        "Modern conference center with 200+ capacity",
        "State-of-the-art audiovisual equipment",
        "High-speed WiFi throughout campus",
        "On-campus accommodation available",
        "Located 25 minutes from Dubai International Airport"
    ]
}

# Common CSS styles
def get_common_styles():
    return '''
        :root {
            --swiss-blue: #2E5090;
            --uae-burgundy: #8B1538;
            --gold: #D4AF37;
            --dark-gray: #333333;
            --light-gray: #f8f9fa;
            --border-gray: #e0e0e0;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--dark-gray);
            background: #ffffff;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Navigation */
        nav {
            background: var(--swiss-blue);
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        nav .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        nav .logo {
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
        }

        nav ul {
            display: flex;
            list-style: none;
            gap: 25px;
        }

        nav a {
            color: white;
            text-decoration: none;
            font-size: 0.9rem;
            opacity: 0.9;
            transition: opacity 0.2s;
        }

        nav a:hover {
            opacity: 1;
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, var(--swiss-blue) 0%, #1a3a6e 100%);
            color: white;
            padding: 80px 0;
            text-align: center;
        }

        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .hero .subtitle {
            font-size: 1.3rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }

        .hero-details {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 30px;
        }

        .hero-detail {
            text-align: center;
        }

        .hero-detail .label {
            font-size: 0.85rem;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .hero-detail .value {
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 5px;
        }

        /* Sections */
        section {
            padding: 60px 0;
        }

        section:nth-child(even) {
            background: var(--light-gray);
        }

        h2 {
            font-size: 1.8rem;
            color: var(--swiss-blue);
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 3px solid var(--gold);
            display: inline-block;
        }

        h3 {
            font-size: 1.3rem;
            color: var(--dark-gray);
            margin: 25px 0 15px;
        }

        p {
            margin-bottom: 15px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-left: 4px solid var(--swiss-blue);
        }

        .stat-card .number {
            font-size: 2rem;
            font-weight: 700;
            color: var(--swiss-blue);
        }

        .stat-card .label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
        }

        /* Aims List */
        .aims-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .aim-item {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .aim-item h4 {
            color: var(--swiss-blue);
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .aim-item p {
            font-size: 0.95rem;
            color: #555;
            margin: 0;
        }

        /* Schedule */
        .schedule-day {
            background: white;
            border-radius: 8px;
            margin-bottom: 30px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .day-header {
            background: var(--swiss-blue);
            color: white;
            padding: 15px 20px;
        }

        .day-header h3 {
            color: white;
            margin: 0;
            font-size: 1.2rem;
        }

        .day-header .date {
            opacity: 0.9;
            font-size: 0.9rem;
        }

        .session {
            padding: 15px 20px;
            border-bottom: 1px solid var(--border-gray);
            display: flex;
            gap: 20px;
        }

        .session:last-child {
            border-bottom: none;
        }

        .session-time {
            min-width: 100px;
            font-weight: 600;
            color: var(--swiss-blue);
            font-size: 0.9rem;
        }

        .session-content {
            flex: 1;
        }

        .session-title {
            font-weight: 600;
            margin-bottom: 5px;
        }

        .session-speaker {
            font-size: 0.9rem;
            color: #666;
        }

        .session-type {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-left: 10px;
        }

        .session-type.keynote {
            background: var(--gold);
            color: white;
        }

        .session-type.panel {
            background: var(--uae-burgundy);
            color: white;
        }

        .session-type.workshop {
            background: var(--swiss-blue);
            color: white;
        }

        .session-type.break {
            background: #e0e0e0;
            color: #666;
        }

        /* Organizers */
        .organizers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
        }

        .organizer-card {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .organizer-card h3 {
            color: var(--swiss-blue);
            margin-top: 0;
        }

        .organizer-card .affiliation {
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 15px;
        }

        .organizer-card .bio {
            font-size: 0.95rem;
            margin-bottom: 15px;
        }

        .organizer-card .highlights {
            list-style: none;
            padding: 0;
        }

        .organizer-card .highlights li {
            padding: 5px 0;
            font-size: 0.9rem;
            padding-left: 20px;
            position: relative;
        }

        .organizer-card .highlights li::before {
            content: "-";
            position: absolute;
            left: 0;
            color: var(--swiss-blue);
            font-weight: bold;
        }

        /* Network Map */
        .network-map {
            text-align: center;
            margin: 30px 0;
        }

        .network-map img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        /* Publications Table */
        .publications-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 0.9rem;
        }

        .publications-table th {
            background: var(--swiss-blue);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        .publications-table td {
            padding: 12px;
            border-bottom: 1px solid var(--border-gray);
        }

        .publications-table tr:hover {
            background: var(--light-gray);
        }

        .publications-table a {
            color: var(--swiss-blue);
            text-decoration: none;
        }

        .publications-table a:hover {
            text-decoration: underline;
        }

        /* Budget Section */
        .budget-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }

        .chart-container {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .chart-container h4 {
            text-align: center;
            margin-bottom: 20px;
            color: var(--dark-gray);
        }

        .budget-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
            font-size: 0.9rem;
        }

        .budget-table th {
            background: var(--swiss-blue);
            color: white;
            padding: 12px;
            text-align: left;
        }

        .budget-table td {
            padding: 12px;
            border-bottom: 1px solid var(--border-gray);
        }

        .budget-table tr.subtotal {
            background: var(--light-gray);
            font-weight: 600;
        }

        .budget-table tr.total {
            background: var(--swiss-blue);
            color: white;
            font-weight: 700;
        }

        .budget-table .amount {
            text-align: right;
            font-family: 'Courier New', monospace;
        }

        /* Timeline/Gantt */
        .timeline {
            position: relative;
            margin: 40px 0;
        }

        .timeline-phase {
            margin-bottom: 40px;
        }

        .phase-header {
            background: var(--swiss-blue);
            color: white;
            padding: 12px 20px;
            border-radius: 8px 8px 0 0;
            font-weight: 600;
        }

        .phase-content {
            background: white;
            border: 1px solid var(--border-gray);
            border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 20px;
        }

        .milestone {
            display: flex;
            align-items: flex-start;
            padding: 10px 0;
            border-bottom: 1px dashed var(--border-gray);
        }

        .milestone:last-child {
            border-bottom: none;
        }

        .milestone-date {
            min-width: 120px;
            font-weight: 600;
            color: var(--swiss-blue);
            font-size: 0.9rem;
        }

        .milestone-content {
            flex: 1;
        }

        .milestone-title {
            font-weight: 600;
        }

        .milestone-desc {
            font-size: 0.9rem;
            color: #666;
            margin-top: 3px;
        }

        /* Footer */
        footer {
            background: var(--dark-gray);
            color: white;
            padding: 40px 0;
            text-align: center;
        }

        footer a {
            color: var(--gold);
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }

        .footer-contacts {
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 20px;
        }

        .footer-contact {
            text-align: center;
        }

        .footer-contact .name {
            font-weight: 600;
            margin-bottom: 5px;
        }

        /* Internal warning banner */
        .internal-banner {
            background: #dc3545;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: 600;
        }

        /* Topics Grid */
        .topics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }

        .topic-card {
            background: white;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-top: 4px solid var(--gold);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .topic-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        .topic-card h4 {
            color: var(--swiss-blue);
            margin-bottom: 12px;
            font-size: 1.1rem;
        }

        .topic-card p {
            font-size: 0.95rem;
            color: #555;
            margin: 0;
            line-height: 1.5;
        }

        /* Scientific Committee Grid */
        .committee-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .committee-member {
            text-align: center;
            padding: 15px;
        }

        .committee-member .name {
            font-weight: 600;
            color: var(--dark-gray);
            font-size: 0.95rem;
        }

        .committee-member .affiliation {
            font-size: 0.8rem;
            color: #666;
            margin-top: 5px;
        }

        /* Venue Section */
        .venue-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-top: 30px;
        }

        .venue-info {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .venue-info h3 {
            color: var(--swiss-blue);
            margin-top: 0;
            margin-bottom: 5px;
        }

        .venue-info .location {
            color: #666;
            font-size: 0.95rem;
            margin-bottom: 20px;
        }

        .venue-features {
            list-style: none;
            padding: 0;
            margin-top: 20px;
        }

        .venue-features li {
            padding: 8px 0;
            font-size: 0.95rem;
            padding-left: 25px;
            position: relative;
        }

        .venue-features li::before {
            content: "*";
            position: absolute;
            left: 0;
            color: var(--gold);
            font-weight: bold;
        }

        .venue-map {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .venue-map iframe {
            width: 100%;
            height: 100%;
            min-height: 350px;
            border: none;
        }

        /* Keynote Speakers */
        .keynotes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }

        .keynote-card {
            background: white;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: center;
            border-bottom: 4px solid var(--swiss-blue);
        }

        .keynote-card .placeholder-img {
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, var(--swiss-blue) 0%, #1a3a6e 100%);
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: 700;
        }

        .keynote-card h4 {
            color: var(--dark-gray);
            margin-bottom: 5px;
        }

        .keynote-card .role {
            color: var(--swiss-blue);
            font-size: 0.9rem;
            margin-bottom: 10px;
        }

        .keynote-card .talk-title {
            font-style: italic;
            color: #666;
            font-size: 0.9rem;
        }

        /* Important Dates */
        .dates-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .date-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-top: 4px solid var(--gold);
        }

        .date-card .date-label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .date-card .date-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--swiss-blue);
            margin-top: 10px;
        }

        /* Registration Section */
        .registration-cta {
            background: linear-gradient(135deg, var(--swiss-blue) 0%, #1a3a6e 100%);
            padding: 60px 0;
            text-align: center;
            color: white;
        }

        .registration-cta h2 {
            color: white;
            border-bottom-color: var(--gold);
        }

        .registration-cta p {
            max-width: 600px;
            margin: 0 auto 30px;
            opacity: 0.9;
        }

        .register-button {
            display: inline-block;
            background: var(--gold);
            color: var(--dark-gray);
            padding: 15px 40px;
            font-size: 1.1rem;
            font-weight: 700;
            text-decoration: none;
            border-radius: 5px;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .register-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        /* Committee with photos */
        .committee-member img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 10px;
            border: 3px solid var(--swiss-blue);
        }

        .committee-member .initials {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--swiss-blue) 0%, #1a3a6e 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 auto 10px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 1.8rem;
            }

            .budget-grid {
                grid-template-columns: 1fr;
            }

            .organizers-grid {
                grid-template-columns: 1fr;
            }

            .venue-container {
                grid-template-columns: 1fr;
            }

            nav ul {
                display: none;
            }

            .session {
                flex-direction: column;
                gap: 5px;
            }

            .committee-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    '''

def generate_public_html(publications, network_map_b64, scientific_committee, photo_mappings, affiliations):
    """Generate the public HTML page (without budget)"""

    total_citations = sum(p.get('citations', 0) for p in publications)
    styles = get_common_styles()

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI for Digital Finance: Swiss-MENA Research Network Workshop</title>
    <style>{styles}</style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="container">
            <div class="logo">AI for Digital Finance</div>
            <ul>
                <li><a href="#overview">Overview</a></li>
                <li><a href="#dates">Dates</a></li>
                <li><a href="#topics">Topics</a></li>
                <li><a href="#program">Program</a></li>
                <li><a href="#keynotes">Keynotes</a></li>
                <li><a href="#committee">Committee</a></li>
                <li><a href="#venue">Venue</a></li>
                <li><a href="#network">Network</a></li>
                <li><a href="#register" style="background: var(--gold); padding: 8px 15px; border-radius: 4px; color: #333;">Register</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>AI for Digital Finance</h1>
            <p class="subtitle">Swiss-MENA Research Network Workshop</p>
            <div class="hero-details">
                <div class="hero-detail">
                    <div class="label">Dates</div>
                    <div class="value">April 21-23, 2026</div>
                </div>
                <div class="hero-detail">
                    <div class="label">Location</div>
                    <div class="value">American University of Sharjah, UAE</div>
                </div>
                <div class="hero-detail">
                    <div class="label">Participants</div>
                    <div class="value">80-100 Expected</div>
                </div>
                <div class="hero-detail">
                    <div class="label">Format</div>
                    <div class="value">60% Academic / 40% Industry</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Overview Section -->
    <section id="overview">
        <div class="container">
            <h2>Project Overview</h2>
            <p>This three-day workshop brings together researchers from Switzerland and the MENA region to explore the transformative potential of artificial intelligence in financial services. The event establishes a long-term collaborative platform between Swiss and UAE institutions, with FHGR and AUS as core partners.</p>

            <p>The workshop addresses critical challenges and opportunities at the intersection of AI, machine learning, and financial technology, including large language models, explainable AI for compliance, blockchain security, and digital banking innovation.</p>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="number">3</div>
                    <div class="label">Days of Programming</div>
                </div>
                <div class="stat-card">
                    <div class="number">80-100</div>
                    <div class="label">Expected Participants</div>
                </div>
                <div class="stat-card">
                    <div class="number">6</div>
                    <div class="label">Partner Institutions</div>
                </div>
                <div class="stat-card">
                    <div class="number">5</div>
                    <div class="label">Countries</div>
                </div>
            </div>

            <h3>Project Aims</h3>
            <div class="aims-list">
                <div class="aim-item">
                    <h4>Build Collaborative Infrastructure</h4>
                    <p>Establish formal bilateral research agreements between Swiss and MENA institutions for sustained collaboration beyond the workshop.</p>
                </div>
                <div class="aim-item">
                    <h4>Knowledge Exchange</h4>
                    <p>Facilitate deep exchange between academic researchers and industry practitioners on AI applications in finance.</p>
                </div>
                <div class="aim-item">
                    <h4>Joint Research Initiation</h4>
                    <p>Identify and launch concrete joint research projects in AI for finance, with plans for follow-up funding applications.</p>
                </div>
                <div class="aim-item">
                    <h4>Capacity Building</h4>
                    <p>Train early-career researchers in emerging AI technologies and methodologies relevant to financial applications.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Important Dates Section -->
    <section id="dates">
        <div class="container">
            <h2>Important Dates</h2>
            <p>Mark your calendar for these key deadlines and the workshop dates.</p>

            <div class="dates-grid">'''

    # Add important dates
    for date_item in IMPORTANT_DATES:
        html += f'''
                <div class="date-card">
                    <div class="date-label">{date_item["label"]}</div>
                    <div class="date-value">{date_item["date"]}</div>
                </div>'''

    html += '''
            </div>
        </div>
    </section>

    <!-- Topics Section -->
    <section id="topics">
        <div class="container">
            <h2>Workshop Topics</h2>
            <p>The workshop welcomes contributions across six key thematic areas at the intersection of artificial intelligence and financial services.</p>

            <div class="topics-grid">'''

    # Add topics
    for topic in WORKSHOP_TOPICS:
        html += f'''
                <div class="topic-card">
                    <h4>{topic["title"]}</h4>
                    <p>{topic["desc"]}</p>
                </div>'''

    html += '''
            </div>

            <h3 style="margin-top: 40px;">Call for Contributions</h3>
            <p>We invite submissions from researchers, practitioners, and students working on AI applications in finance. Accepted contributions will be presented as oral presentations or posters during the workshop sessions.</p>
            <p><strong>Submission deadline:</strong> February 15, 2026 | <strong>Notification:</strong> March 1, 2026</p>
        </div>
    </section>

    <!-- Program Section -->
    <section id="program">
        <div class="container">
            <h2>Workshop Program</h2>
            <p>A comprehensive three-day program combining keynote presentations, panel discussions, hands-on workshops, and networking opportunities.</p>

            <!-- Day 1 -->
            <div class="schedule-day">
                <div class="day-header">
                    <h3>Day 1: Research Frontiers</h3>
                    <div class="date">Tuesday, April 21, 2026</div>
                </div>
                <div class="session">
                    <div class="session-time">08:30 - 09:00</div>
                    <div class="session-content">
                        <div class="session-title">Registration & Welcome Coffee</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">09:00 - 09:30</div>
                    <div class="session-content">
                        <div class="session-title">Opening Ceremony <span class="session-type keynote">Keynote</span></div>
                        <div class="session-speaker">Welcome addresses by AUS and FHGR leadership</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">09:30 - 10:30</div>
                    <div class="session-content">
                        <div class="session-title">Keynote: AI Transformation in Financial Services <span class="session-type keynote">Keynote</span></div>
                        <div class="session-speaker">Industry Leader (TBC)</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">10:30 - 11:00</div>
                    <div class="session-content">
                        <div class="session-title">Coffee Break <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">11:00 - 12:30</div>
                    <div class="session-content">
                        <div class="session-title">Panel: Large Language Models in Finance <span class="session-type panel">Panel</span></div>
                        <div class="session-speaker">Panelists from academia and industry</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">12:30 - 14:00</div>
                    <div class="session-content">
                        <div class="session-title">Networking Lunch <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">14:00 - 15:30</div>
                    <div class="session-content">
                        <div class="session-title">Research Presentations: AI/ML Applications</div>
                        <div class="session-speaker">Selected paper presentations from participants</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">15:30 - 16:00</div>
                    <div class="session-content">
                        <div class="session-title">Coffee Break <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">16:00 - 17:30</div>
                    <div class="session-content">
                        <div class="session-title">Workshop: Hands-on LLM Applications <span class="session-type workshop">Workshop</span></div>
                        <div class="session-speaker">Interactive session with code examples</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">18:00 - 20:00</div>
                    <div class="session-content">
                        <div class="session-title">Welcome Reception</div>
                        <div class="session-speaker">Networking dinner at AUS campus</div>
                    </div>
                </div>
            </div>

            <!-- Day 2 -->
            <div class="schedule-day">
                <div class="day-header">
                    <h3>Day 2: Industry Applications</h3>
                    <div class="date">Wednesday, April 22, 2026</div>
                </div>
                <div class="session">
                    <div class="session-time">08:30 - 09:00</div>
                    <div class="session-content">
                        <div class="session-title">Morning Coffee</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">09:00 - 10:00</div>
                    <div class="session-content">
                        <div class="session-title">Keynote: Explainable AI for Financial Compliance <span class="session-type keynote">Keynote</span></div>
                        <div class="session-speaker">Regulatory Technology Expert (TBC)</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">10:00 - 10:30</div>
                    <div class="session-content">
                        <div class="session-title">Coffee Break <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">10:30 - 12:00</div>
                    <div class="session-content">
                        <div class="session-title">Panel: Blockchain Security & Fraud Detection <span class="session-type panel">Panel</span></div>
                        <div class="session-speaker">Industry and academic experts</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">12:00 - 13:30</div>
                    <div class="session-content">
                        <div class="session-title">Networking Lunch <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">13:30 - 15:00</div>
                    <div class="session-content">
                        <div class="session-title">Research Presentations: Risk & Compliance</div>
                        <div class="session-speaker">Selected paper presentations from participants</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">15:00 - 15:30</div>
                    <div class="session-content">
                        <div class="session-title">Coffee Break <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">15:30 - 17:30</div>
                    <div class="session-content">
                        <div class="session-title">Workshop: Anomaly Detection in Financial Networks <span class="session-type workshop">Workshop</span></div>
                        <div class="session-speaker">Hands-on technical workshop</div>
                    </div>
                </div>
            </div>

            <!-- Day 3 -->
            <div class="schedule-day">
                <div class="day-header">
                    <h3>Day 3: Network Launch</h3>
                    <div class="date">Thursday, April 23, 2026</div>
                </div>
                <div class="session">
                    <div class="session-time">08:30 - 09:00</div>
                    <div class="session-content">
                        <div class="session-title">Morning Coffee</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">09:00 - 10:00</div>
                    <div class="session-content">
                        <div class="session-title">Keynote: Digital Banking Innovation in MENA <span class="session-type keynote">Keynote</span></div>
                        <div class="session-speaker">Regional Banking Leader (TBC)</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">10:00 - 10:30</div>
                    <div class="session-content">
                        <div class="session-title">Coffee Break <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">10:30 - 12:00</div>
                    <div class="session-content">
                        <div class="session-title">Research Collaboration Planning <span class="session-type workshop">Workshop</span></div>
                        <div class="session-speaker">Breakout groups for joint project planning</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">12:00 - 13:30</div>
                    <div class="session-content">
                        <div class="session-title">Networking Lunch <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">13:30 - 15:00</div>
                    <div class="session-content">
                        <div class="session-title">Panel: Future of Swiss-MENA Collaboration <span class="session-type panel">Panel</span></div>
                        <div class="session-speaker">Representatives from all partner institutions</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">15:00 - 15:30</div>
                    <div class="session-content">
                        <div class="session-title">Coffee Break <span class="session-type break">Break</span></div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">15:30 - 16:30</div>
                    <div class="session-content">
                        <div class="session-title">Bilateral Agreement Signing Ceremony <span class="session-type keynote">Ceremony</span></div>
                        <div class="session-speaker">FHGR-AUS research partnership formalization</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">16:30 - 17:00</div>
                    <div class="session-content">
                        <div class="session-title">Closing Remarks</div>
                        <div class="session-speaker">Workshop summary and next steps</div>
                    </div>
                </div>
                <div class="session">
                    <div class="session-time">19:00 - 21:00</div>
                    <div class="session-content">
                        <div class="session-title">Gala Dinner</div>
                        <div class="session-speaker">Celebratory closing dinner</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Keynote Speakers Section -->
    <section id="keynotes">
        <div class="container">
            <h2>Keynote Speakers</h2>
            <p>Distinguished speakers from academia and industry will deliver keynote presentations on the latest developments in AI and digital finance.</p>

            <div class="keynotes-grid">
                <div class="keynote-card">
                    <div class="placeholder-img">?</div>
                    <h4>Industry Leader (TBC)</h4>
                    <div class="role">AI & Finance Industry</div>
                    <div class="talk-title">"AI Transformation in Financial Services"</div>
                </div>
                <div class="keynote-card">
                    <div class="placeholder-img">?</div>
                    <h4>Regulatory Expert (TBC)</h4>
                    <div class="role">Regulatory Technology</div>
                    <div class="talk-title">"Explainable AI for Financial Compliance"</div>
                </div>
                <div class="keynote-card">
                    <div class="placeholder-img">?</div>
                    <h4>Banking Leader (TBC)</h4>
                    <div class="role">MENA Banking Sector</div>
                    <div class="talk-title">"Digital Banking Innovation in MENA"</div>
                </div>
            </div>

            <p style="margin-top: 30px; text-align: center; color: #666; font-style: italic;">Keynote speakers will be confirmed by February 2026</p>
        </div>
    </section>

    <!-- Scientific Committee Section -->
    <section id="committee">
        <div class="container">
            <h2>Scientific Committee</h2>
            <p>The Scientific Committee comprises leading researchers from the MSCA Digital Finance network and partner institutions, providing expertise across AI, machine learning, statistics, and finance.</p>

            <h3>Organizing Committee</h3>
            <div class="organizers-grid" style="margin-bottom: 40px;">
                <div class="organizer-card">
                    <h3>Prof. Dr. Joerg Osterrieder</h3>
                    <div class="affiliation">FHGR, Switzerland - Workshop Chair</div>
                </div>
                <div class="organizer-card">
                    <h3>Prof. Stephen Chan</h3>
                    <div class="affiliation">AUS, UAE - Workshop Co-Chair</div>
                </div>
            </div>

            <h3>Scientific Committee Members</h3>
            <p style="color: #666; font-size: 0.9rem;">Members from the MSCA Digital Finance Research Network</p>

            <div class="committee-grid">'''

    # Add scientific committee members with photos and affiliations
    for member in scientific_committee:
        # Try to find photo for this member
        member_lower = member.lower()
        photo_filename = photo_mappings.get(member_lower)
        affiliation = affiliations.get(member, '')

        if photo_filename:
            photo_b64 = load_photo_base64(photo_filename)
            if photo_b64:
                html += f'''
                <div class="committee-member">
                    <img src="{photo_b64}" alt="{member}">
                    <div class="name">{member}</div>
                    <div class="affiliation">{affiliation}</div>
                </div>'''
            else:
                # Photo file not found, show initials
                initials = ''.join(n[0].upper() for n in member.split()[:2] if n)
                html += f'''
                <div class="committee-member">
                    <div class="initials">{initials}</div>
                    <div class="name">{member}</div>
                    <div class="affiliation">{affiliation}</div>
                </div>'''
        else:
            # No photo mapping, show initials
            initials = ''.join(n[0].upper() for n in member.split()[:2] if n)
            html += f'''
                <div class="committee-member">
                    <div class="initials">{initials}</div>
                    <div class="name">{member}</div>
                    <div class="affiliation">{affiliation}</div>
                </div>'''

    html += f'''
            </div>
        </div>
    </section>

    <!-- Venue Section -->
    <section id="venue">
        <div class="container">
            <h2>Venue & Location</h2>
            <p>The workshop will be held at the American University of Sharjah, one of the leading universities in the Gulf region.</p>

            <div class="venue-container">
                <div class="venue-info">
                    <h3>{VENUE_INFO["name"]}</h3>
                    <div class="location">{VENUE_INFO["location"]}</div>
                    <p>{VENUE_INFO["description"]}</p>
                    <ul class="venue-features">'''

    for feature in VENUE_INFO["features"]:
        html += f'''
                        <li>{feature}</li>'''

    html += '''
                    </ul>
                </div>
                <div class="venue-map">
                    <iframe
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3607.0244723!2d55.5052!3d25.2862!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5f5f0b3b1b1b1b%3A0x1b1b1b1b1b1b1b1b!2sAmerican%20University%20of%20Sharjah!5e0!3m2!1sen!2sae!4v1700000000000!5m2!1sen!2sae"
                        allowfullscreen=""
                        loading="lazy"
                        referrerpolicy="no-referrer-when-downgrade">
                    </iframe>
                </div>
            </div>

            <h3 style="margin-top: 40px;">Travel Information</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="number">DXB</div>
                    <div class="label">Dubai International Airport (25 min)</div>
                </div>
                <div class="stat-card">
                    <div class="number">SHJ</div>
                    <div class="label">Sharjah International Airport (15 min)</div>
                </div>
                <div class="stat-card">
                    <div class="number">Apr 21-23</div>
                    <div class="label">Workshop Dates, 2026</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Organizers Section (now simplified) -->
    <section id="organizers" style="display: none;">
        <div class="container">
            <h2>Workshop Organizers</h2>
            <div class="organizers-grid">
                <div class="organizer-card">
                    <h3>Prof. Dr. Joerg Osterrieder</h3>
                    <div class="affiliation">University of Applied Sciences Grisons (FHGR), Switzerland</div>
                    <p class="bio">Professor of Finance and Data Science, specializing in machine learning applications in quantitative finance, cryptocurrency analysis, and explainable AI for financial services.</p>
                    <ul class="highlights">
                        <li>PhD from ETH Zurich in Mathematics</li>
                        <li>MSCA Research Coordinator (4.5M EUR budget)</li>
                        <li>COST Action Chair (860K EUR)</li>
                        <li>6 Swiss National Science Foundation projects</li>
                        <li>136+ peer-reviewed publications</li>
                        <li>Former positions at Deutsche Bank, Credit Suisse, Royal Bank of Scotland</li>
                    </ul>
                </div>
                <div class="organizer-card">
                    <h3>Prof. Stephen Chan</h3>
                    <div class="affiliation">American University of Sharjah (AUS), UAE</div>
                    <p class="bio">Associate Professor of Statistics, expertise in statistical modeling, financial econometrics, cryptocurrency research, and risk analysis.</p>
                    <ul class="highlights">
                        <li>PhD in Statistics from University of Manchester</li>
                        <li>1,800+ citations, h-index 16</li>
                        <li>Principal Investigator on 7 AUS Faculty Research Grants (750K AED)</li>
                        <li>Long-standing collaboration with Prof. Osterrieder (since 2017)</li>
                        <li>30+ joint publications in cryptocurrency and blockchain</li>
                        <li>Expert in GARCH modeling and statistical distributions</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Network Section -->
    <section id="network">
        <div class="container">
            <h2>Partner Network</h2>
            <p>The Swiss-MENA AI Finance Research Network connects leading institutions across Europe, Middle East, and Asia. FHGR (Switzerland) and AUS (UAE) serve as core partners, with satellite connections to Universities of Manchester (UK), Renmin (China), Babes-Bolyai (Romania), and Bern University of Applied Sciences (Switzerland).</p>

            <div class="network-map">
                <img src="data:image/png;base64,{network_map_b64}" alt="Swiss-MENA AI Finance Research Network">
            </div>

            <h3>Core Partners</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="number">FHGR</div>
                    <div class="label">University of Applied Sciences Grisons, Switzerland</div>
                </div>
                <div class="stat-card">
                    <div class="number">AUS</div>
                    <div class="label">American University of Sharjah, UAE</div>
                </div>
            </div>

            <h3>Research Partners</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="number">Manchester</div>
                    <div class="label">University of Manchester, UK</div>
                </div>
                <div class="stat-card">
                    <div class="number">Renmin</div>
                    <div class="label">Renmin University, China</div>
                </div>
                <div class="stat-card">
                    <div class="number">Babes-Bolyai</div>
                    <div class="label">Babes-Bolyai University, Romania</div>
                </div>
                <div class="stat-card">
                    <div class="number">BFH</div>
                    <div class="label">Bern University of Applied Sciences, Switzerland</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Publications Section -->
    <section id="publications">
        <div class="container">
            <h2>Joint Publications</h2>
            <p>Prof. Osterrieder and Prof. Chan have collaborated since 2017, producing {len(publications)} joint publications with {total_citations} total citations spanning cryptocurrency analysis, blockchain security, and statistical finance.</p>

            <table class="publications-table">
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Title</th>
                        <th>Journal</th>
                        <th>Citations</th>
                        <th>DOI</th>
                    </tr>
                </thead>
                <tbody>'''

    # Add publications
    for pub in sorted(publications, key=lambda x: x.get('year', 0) or 0, reverse=True):
        title = pub.get('title', 'Unknown')[:80]
        if len(pub.get('title', '')) > 80:
            title += '...'
        doi_link = f'<a href="{pub["doi_url"]}" target="_blank">Link</a>' if pub.get('doi_url') else '-'

        html += f'''
                    <tr>
                        <td>{pub.get('year', 'N/A')}</td>
                        <td>{title}</td>
                        <td>{pub.get('journal', 'Unknown')}</td>
                        <td>{pub.get('citations', 0)}</td>
                        <td>{doi_link}</td>
                    </tr>'''

    html += '''
                </tbody>
            </table>
        </div>
    </section>

    <!-- Timeline Section -->
    <section id="timeline">
        <div class="container">
            <h2>Project Timeline</h2>
            <p>The project spans from December 2025 through July 2026, organized in three main phases with key milestones.</p>

            <div class="timeline">
                <!-- Phase 1 -->
                <div class="timeline-phase">
                    <div class="phase-header">Phase 1: Pre-Workshop Preparation (December 2025 - March 2026)</div>
                    <div class="phase-content">
                        <div class="milestone">
                            <div class="milestone-date">Dec 2025</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Project Kickoff</div>
                                <div class="milestone-desc">Initial planning meeting, confirm program structure</div>
                            </div>
                        </div>
                        <div class="milestone">
                            <div class="milestone-date">Jan 2026</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Call for Participation</div>
                                <div class="milestone-desc">Open registration, distribute call for papers/presentations</div>
                            </div>
                        </div>
                        <div class="milestone">
                            <div class="milestone-date">Feb 2026</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Speaker Confirmation</div>
                                <div class="milestone-desc">Finalize keynote speakers and panelists</div>
                            </div>
                        </div>
                        <div class="milestone">
                            <div class="milestone-date">Mar 2026</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Program Finalization</div>
                                <div class="milestone-desc">Complete participant selection, finalize detailed agenda</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Phase 2 -->
                <div class="timeline-phase">
                    <div class="phase-header">Phase 2: Workshop Implementation (April 2026)</div>
                    <div class="phase-content">
                        <div class="milestone">
                            <div class="milestone-date">Apr 21-23</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Three-Day Workshop</div>
                                <div class="milestone-desc">Main event at American University of Sharjah</div>
                            </div>
                        </div>
                        <div class="milestone">
                            <div class="milestone-date">Apr 23</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Bilateral Agreement Signing</div>
                                <div class="milestone-desc">Formalization of FHGR-AUS research partnership</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Phase 3 -->
                <div class="timeline-phase">
                    <div class="phase-header">Phase 3: Post-Workshop Follow-up (May - July 2026)</div>
                    <div class="phase-content">
                        <div class="milestone">
                            <div class="milestone-date">May 2026</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Documentation & Dissemination</div>
                                <div class="milestone-desc">Workshop proceedings, publication of outcomes</div>
                            </div>
                        </div>
                        <div class="milestone">
                            <div class="milestone-date">Jun 2026</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Joint Project Planning</div>
                                <div class="milestone-desc">Development of concrete research proposals</div>
                            </div>
                        </div>
                        <div class="milestone">
                            <div class="milestone-date">Jul 2026</div>
                            <div class="milestone-content">
                                <div class="milestone-title">Final Reporting</div>
                                <div class="milestone-desc">CCG final report submission, outcome documentation</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Registration Section -->
    <section id="register" class="registration-cta">
        <div class="container">
            <h2>Register Now</h2>
            <p>Join leading researchers and industry practitioners from Switzerland and the MENA region for three days of knowledge exchange, collaboration, and networking.</p>
            <a href="#" class="register-button" onclick="alert('Registration will open in January 2026'); return false;">Registration Opens January 2026</a>
            <p style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">Early bird registration deadline: March 15, 2026</p>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <h3>AI for Digital Finance: Swiss-MENA Research Network</h3>
            <p>A Connect & Collaborate Grant (CCG) Project | Leading House MENA</p>
            <div class="footer-contacts">
                <div class="footer-contact">
                    <div class="name">Prof. Dr. Joerg Osterrieder</div>
                    <div><a href="mailto:joerg.osterrieder@fhgr.ch">joerg.osterrieder@fhgr.ch</a></div>
                    <div>FHGR, Switzerland</div>
                </div>
                <div class="footer-contact">
                    <div class="name">Prof. Stephen Chan</div>
                    <div><a href="mailto:schan@aus.edu">schan@aus.edu</a></div>
                    <div>AUS, UAE</div>
                </div>
            </div>
            <p style="margin-top: 30px; font-size: 0.85rem; opacity: 0.8;">
                GitHub: <a href="https://github.com/Digital-AI-Finance/digital-ai-in-finance">Digital-AI-Finance/digital-ai-in-finance</a>
            </p>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation
        document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>'''

    return html


def generate_budget_html():
    """Generate the internal budget HTML page"""

    styles = get_common_styles()

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Budget Details (Internal) | AI for Digital Finance</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>{styles}</style>
</head>
<body>
    <!-- Internal Warning Banner -->
    <div class="internal-banner">
        INTERNAL DOCUMENT - NOT FOR PUBLIC DISTRIBUTION
    </div>

    <!-- Navigation -->
    <nav>
        <div class="container">
            <div class="logo">AI for Digital Finance - Budget</div>
            <ul>
                <li><a href="ai_digital_finance.html">Back to Public Page</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero" style="padding: 50px 0;">
        <div class="container">
            <h1>Budget Overview</h1>
            <p class="subtitle">Internal Document - CCG Grant Application</p>
            <div class="hero-details">
                <div class="hero-detail">
                    <div class="label">Total Budget</div>
                    <div class="value">CHF 18,000</div>
                </div>
                <div class="hero-detail">
                    <div class="label">CCG Request</div>
                    <div class="value">CHF 5,000</div>
                </div>
                <div class="hero-detail">
                    <div class="label">Co-funding Rate</div>
                    <div class="value">72%</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Budget Charts -->
    <section id="charts">
        <div class="container">
            <h2>Funding Overview</h2>
            <p>The CCG request of CHF 5,000 (28%) is complemented by substantial co-funding from Swiss and MENA partners (72%).</p>

            <div class="budget-grid">
                <div class="chart-container">
                    <h4>Funding Sources</h4>
                    <canvas id="fundingChart"></canvas>
                </div>
                <div class="chart-container">
                    <h4>Budget by Partner</h4>
                    <canvas id="partnerChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- Detailed Budget -->
    <section id="details">
        <div class="container">
            <h2>Detailed Budget Breakdown</h2>

            <table class="budget-table">
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Description</th>
                        <th>Type</th>
                        <th class="amount">Amount (CHF)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td colspan="4" style="background: var(--swiss-blue); color: white; font-weight: 600;">Swiss Partners</td>
                    </tr>
                    <tr>
                        <td>Travel</td>
                        <td>Travel costs for Swiss participants to UAE</td>
                        <td>CCG Request</td>
                        <td class="amount">2,640</td>
                    </tr>
                    <tr>
                        <td>Work Costs</td>
                        <td>Workshop preparation and coordination</td>
                        <td>In-kind</td>
                        <td class="amount">2,500</td>
                    </tr>
                    <tr class="subtotal">
                        <td colspan="3">Swiss Partners Subtotal</td>
                        <td class="amount">5,140</td>
                    </tr>
                    <tr>
                        <td colspan="4" style="background: var(--uae-burgundy); color: white; font-weight: 600;">MENA Partners</td>
                    </tr>
                    <tr>
                        <td>Event Costs</td>
                        <td>Venue, equipment, catering</td>
                        <td>CCG Request</td>
                        <td class="amount">2,360</td>
                    </tr>
                    <tr>
                        <td>Event Costs</td>
                        <td>Additional venue and logistics support</td>
                        <td>In-kind</td>
                        <td class="amount">4,900</td>
                    </tr>
                    <tr>
                        <td>Work Costs</td>
                        <td>Local coordination and administration</td>
                        <td>In-kind</td>
                        <td class="amount">5,000</td>
                    </tr>
                    <tr>
                        <td>Publication</td>
                        <td>Post-workshop publication costs</td>
                        <td>In-kind</td>
                        <td class="amount">600</td>
                    </tr>
                    <tr class="subtotal">
                        <td colspan="3">MENA Partners Subtotal</td>
                        <td class="amount">12,860</td>
                    </tr>
                    <tr class="total">
                        <td colspan="3">TOTAL PROJECT BUDGET</td>
                        <td class="amount">18,000</td>
                    </tr>
                </tbody>
            </table>

            <h3>Funding Summary</h3>
            <table class="budget-table">
                <thead>
                    <tr>
                        <th>Funding Source</th>
                        <th class="amount">Amount (CHF)</th>
                        <th class="amount">Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>CCG Request</td>
                        <td class="amount">5,000</td>
                        <td class="amount">27.8%</td>
                    </tr>
                    <tr>
                        <td>Co-funding (In-kind)</td>
                        <td class="amount">13,000</td>
                        <td class="amount">72.2%</td>
                    </tr>
                    <tr class="total">
                        <td>Total</td>
                        <td class="amount">18,000</td>
                        <td class="amount">100%</td>
                    </tr>
                </tbody>
            </table>

            <h3>CCG Compliance Check</h3>
            <table class="budget-table">
                <thead>
                    <tr>
                        <th>Requirement</th>
                        <th>Limit</th>
                        <th>Actual</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Maximum CCG for workshops</td>
                        <td>CHF 5,000</td>
                        <td>CHF 5,000</td>
                        <td style="color: green; font-weight: bold;">OK</td>
                    </tr>
                    <tr>
                        <td>Maximum work costs</td>
                        <td>20%</td>
                        <td>~14%</td>
                        <td style="color: green; font-weight: bold;">OK</td>
                    </tr>
                    <tr>
                        <td>Co-funding required</td>
                        <td>Yes</td>
                        <td>72%</td>
                        <td style="color: green; font-weight: bold;">OK</td>
                    </tr>
                    <tr>
                        <td>MENA partner contribution</td>
                        <td>Required</td>
                        <td>CHF 12,860</td>
                        <td style="color: green; font-weight: bold;">OK</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p style="color: #ff6b6b; font-weight: bold;">INTERNAL DOCUMENT - NOT FOR PUBLIC DISTRIBUTION</p>
            <p style="margin-top: 15px;">AI for Digital Finance: Swiss-MENA Research Network</p>
            <p><a href="ai_digital_finance.html">Return to Public Page</a></p>
        </div>
    </footer>

    <!-- Chart.js Scripts -->
    <script>
        // Funding Sources Pie Chart
        const fundingCtx = document.getElementById('fundingChart').getContext('2d');
        new Chart(fundingCtx, {{
            type: 'pie',
            data: {{
                labels: ['CCG Request', 'Co-funding (In-kind)'],
                datasets: [{{
                    data: [5000, 13000],
                    backgroundColor: ['#2E5090', '#D4AF37'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `CHF ${{value.toLocaleString()}} (${{percentage}}%)`;
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Partner Budget Bar Chart
        const partnerCtx = document.getElementById('partnerChart').getContext('2d');
        new Chart(partnerCtx, {{
            type: 'bar',
            data: {{
                labels: ['Swiss Partners', 'MENA Partners'],
                datasets: [
                    {{
                        label: 'CCG Request',
                        data: [2640, 2360],
                        backgroundColor: '#2E5090'
                    }},
                    {{
                        label: 'In-kind',
                        data: [2500, 10500],
                        backgroundColor: '#D4AF37'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{
                    x: {{
                        stacked: true
                    }},
                    y: {{
                        stacked: true,
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return 'CHF ' + value.toLocaleString();
                            }}
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return `${{context.dataset.label}}: CHF ${{context.raw.toLocaleString()}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

    return html


def main():
    print("Generating AI Digital Finance HTML pages...")

    publications = load_publications()
    network_map_b64 = load_network_map_base64()
    scientific_committee = load_scientific_committee()
    photo_mappings = load_photo_mappings()
    affiliations = load_affiliations()

    print(f"  Loaded {len(publications)} publications")
    print(f"  Loaded {len(scientific_committee)} Scientific Committee members")
    print(f"  Loaded {len(photo_mappings)} photo mappings")
    print(f"  Loaded {len(affiliations)} affiliations")

    # Generate public page (no budget)
    print("  Generating public page (ai_digital_finance.html)...")
    public_html = generate_public_html(publications, network_map_b64, scientific_committee, photo_mappings, affiliations)
    with open(OUTPUT_PUBLIC, 'w', encoding='utf-8') as f:
        f.write(public_html)
    print(f"  -> {OUTPUT_PUBLIC} ({OUTPUT_PUBLIC.stat().st_size / 1024:.1f} KB)")

    # Generate internal budget page
    print("  Generating internal budget page (budget_internal.html)...")
    budget_html = generate_budget_html()
    with open(OUTPUT_BUDGET, 'w', encoding='utf-8') as f:
        f.write(budget_html)
    print(f"  -> {OUTPUT_BUDGET} ({OUTPUT_BUDGET.stat().st_size / 1024:.1f} KB)")

    print("\nDone! Two pages generated:")
    print("  - ai_digital_finance.html (PUBLIC - no budget)")
    print("  - budget_internal.html (INTERNAL - budget details)")


if __name__ == "__main__":
    main()
