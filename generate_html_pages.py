"""
Generate HTML marketing pages for AI for Digital Finance workshop
Creates two HTML files:
1. workshop_showcase.html - Main content page (no budget)
2. budget_showcase.html - Budget detail page
"""

import base64
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(r"D:\Joerg\Research\slides\Digital_AI_in_Finance")
DOCS_DIR = BASE_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "images"

def encode_image_base64(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_image_mime_type(filename):
    """Get MIME type from filename"""
    if filename.endswith(".png"):
        return "image/png"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        return "image/jpeg"
    elif filename.endswith(".pdf"):
        return "application/pdf"
    return "image/png"

# Encode images
network_map_b64 = ""
funding_sources_b64 = ""
budget_categories_b64 = ""
ccg_breakdown_b64 = ""

network_map_path = IMAGES_DIR / "network_map.png"
if network_map_path.exists():
    network_map_b64 = encode_image_base64(network_map_path)

funding_sources_path = IMAGES_DIR / "funding_sources.png"
if funding_sources_path.exists():
    funding_sources_b64 = encode_image_base64(funding_sources_path)

budget_categories_path = IMAGES_DIR / "budget_categories.png"
if budget_categories_path.exists():
    budget_categories_b64 = encode_image_base64(budget_categories_path)

ccg_breakdown_path = IMAGES_DIR / "ccg_breakdown.png"
if ccg_breakdown_path.exists():
    ccg_breakdown_b64 = encode_image_base64(ccg_breakdown_path)

# ============================================================================
# MAIN SHOWCASE HTML
# ============================================================================

main_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI for Digital Finance | Swiss-MENA Research Network</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --swiss-blue: #2E5090;
            --swiss-blue-light: #4A7BC8;
            --swiss-blue-dark: #1e3a5f;
            --uae-burgundy: #8B1538;
            --uae-burgundy-light: #a82d4d;
            --uae-gold: #D4AF37;
            --text-dark: #1a1a1a;
            --text-light: #f5f5f5;
            --bg-light: #f0f2f5;
            --bg-card: #ffffff;
            --border-color: #dde1e6;
        }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            font-size: 14px;
            line-height: 1.4;
            color: var(--text-dark);
            background: var(--bg-light);
        }}
        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--uae-burgundy) 100%);
            padding: 8px 20px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        nav ul {{
            display: flex;
            justify-content: center;
            gap: 8px;
            list-style: none;
            flex-wrap: wrap;
        }}
        nav a {{
            color: var(--text-light);
            text-decoration: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }}
        nav a:hover {{ background: rgba(255,255,255,0.2); }}
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--swiss-blue-dark) 50%, var(--uae-burgundy) 100%);
            color: white;
            padding: 70px 20px 40px;
            text-align: center;
        }}
        .hero h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}
        .hero .subtitle {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 32px;
            font-weight: 700;
            color: var(--uae-gold);
            display: block;
        }}
        .stat-label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
        }}
        /* Section styling */
        section {{
            padding: 30px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--swiss-blue);
            border-left: 4px solid var(--uae-burgundy);
            padding-left: 12px;
        }}
        /* Cards */
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
        }}
        .card {{
            background: var(--bg-card);
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid var(--border-color);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}
        .card h3 {{
            font-size: 15px;
            color: var(--swiss-blue);
            margin-bottom: 8px;
        }}
        .card p {{ font-size: 13px; color: #555; }}
        /* Day cards */
        .day-card {{
            border-top: 3px solid var(--swiss-blue);
        }}
        .day-card.day-2 {{ border-top-color: var(--uae-burgundy); }}
        .day-card.day-3 {{ border-top-color: var(--uae-gold); }}
        .day-number {{
            display: inline-block;
            background: var(--swiss-blue);
            color: white;
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 10px;
            margin-bottom: 8px;
        }}
        .day-card.day-2 .day-number {{ background: var(--uae-burgundy); }}
        .day-card.day-3 .day-number {{ background: #b8860b; }}
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            background: var(--bg-card);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--uae-burgundy) 100%);
            color: white;
            font-weight: 600;
            font-size: 12px;
        }}
        tr:hover {{ background: #f8f9fa; }}
        /* Network image */
        .network-img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        }}
        /* Organizer cards */
        .organizer {{
            display: flex;
            gap: 15px;
            align-items: flex-start;
        }}
        .organizer-avatar {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--uae-burgundy) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 20px;
            flex-shrink: 0;
        }}
        .organizer-info h3 {{ font-size: 15px; margin-bottom: 4px; }}
        .organizer-info .role {{
            font-size: 12px;
            color: var(--uae-burgundy);
            font-weight: 500;
        }}
        .organizer-info .email {{
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }}
        /* Footer */
        footer {{
            background: linear-gradient(135deg, var(--swiss-blue-dark) 0%, #3d0f1a 100%);
            color: var(--text-light);
            padding: 25px 20px;
            text-align: center;
        }}
        footer h4 {{
            color: var(--uae-gold);
            margin-bottom: 8px;
            font-size: 14px;
        }}
        footer p {{ font-size: 12px; opacity: 0.8; margin-bottom: 4px; }}
        footer a {{ color: var(--uae-gold); }}
        /* Themes lists */
        .themes {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }}
        .theme-tag {{
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--swiss-blue-light) 100%);
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        /* Two column layout */
        .two-col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        @media (max-width: 768px) {{
            .two-col {{ grid-template-columns: 1fr; }}
            .stats {{ gap: 15px; }}
            .stat-number {{ font-size: 24px; }}
        }}
        /* Animate on scroll */
        .fade-in {{
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s, transform 0.5s;
        }}
        .fade-in.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
        /* Bullet points */
        ul.bullet {{
            margin: 8px 0;
            padding-left: 18px;
        }}
        ul.bullet li {{
            margin-bottom: 4px;
            font-size: 13px;
        }}
        /* Partner grid */
        .partner-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}
        .partner {{
            background: var(--bg-card);
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid var(--swiss-blue);
            font-size: 13px;
        }}
        .partner.mena {{ border-left-color: var(--uae-burgundy); }}
        .partner strong {{ color: var(--swiss-blue); }}
        .partner.mena strong {{ color: var(--uae-burgundy); }}
        /* Link button */
        .btn {{
            display: inline-block;
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--uae-burgundy) 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 12px;
            font-weight: 500;
            margin-top: 10px;
            transition: opacity 0.2s;
        }}
        .btn:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <nav>
        <ul>
            <li><a href="#overview">Overview</a></li>
            <li><a href="#program">Program</a></li>
            <li><a href="#aims">Aims</a></li>
            <li><a href="#network">Network</a></li>
            <li><a href="#research">Research</a></li>
            <li><a href="#organizers">Organizers</a></li>
            <li><a href="budget_showcase.html">Budget</a></li>
        </ul>
    </nav>

    <header class="hero">
        <h1>AI for Digital Finance</h1>
        <p class="subtitle">Swiss-MENA Research Network | International Workshop</p>
        <p class="subtitle">April 21-23, 2026 | American University of Sharjah, UAE</p>
        <div class="stats">
            <div class="stat">
                <span class="stat-number" data-target="7">0</span>
                <span class="stat-label">Years Collaboration</span>
            </div>
            <div class="stat">
                <span class="stat-number" data-target="550">0</span>
                <span class="stat-label">Citations</span>
            </div>
            <div class="stat">
                <span class="stat-number" data-target="6">0</span>
                <span class="stat-label">Partner Institutions</span>
            </div>
            <div class="stat">
                <span class="stat-number" data-target="5">0</span>
                <span class="stat-label">Countries</span>
            </div>
        </div>
    </header>

    <section id="overview" class="fade-in">
        <h2 class="section-title">Project Overview</h2>
        <div class="two-col">
            <div class="card">
                <h3>The Vision</h3>
                <p>This three-day international workshop marks the formal launch of the first dedicated AI Finance Research Network bridging Switzerland and the Middle East. Building on a robust 7-year partnership between Prof. Joerg Osterrieder (FHGR) and Prof. Stephen Chan (AUS), this workshop transforms proven bilateral success into a sustainable multilateral research ecosystem.</p>
            </div>
            <div class="card">
                <h3>Strategic Significance</h3>
                <p>Switzerland's renowned precision in financial services and robust regulatory frameworks complement the UAE's dynamic growth and innovation-friendly environment. Both regions are actively developing AI strategies for their financial sectors, making this collaboration timely and strategically vital.</p>
            </div>
        </div>
        <div class="card" style="margin-top:15px;">
            <h3>Thematic Focus Areas</h3>
            <div class="themes">
                <span class="theme-tag">Large Language Models in Finance</span>
                <span class="theme-tag">Explainable AI for Compliance</span>
                <span class="theme-tag">ML for Fraud Detection</span>
                <span class="theme-tag">Risk Management</span>
                <span class="theme-tag">Blockchain Security</span>
            </div>
            <p style="margin-top:10px;">Workshop Format: Three-day intensive program combining academic presentations, industry case studies, doctoral training, and strategic network planning in hybrid format.</p>
        </div>
    </section>

    <section id="program" class="fade-in">
        <h2 class="section-title">Workshop Program</h2>
        <div class="card-grid">
            <div class="card day-card">
                <span class="day-number">DAY 1</span>
                <h3>Foundations & Frontiers</h3>
                <ul class="bullet">
                    <li>Keynote: LLMs in Financial Services</li>
                    <li>Paper sessions: AI Methods for Financial Markets</li>
                    <li>Session: Blockchain Security & Fraud Detection</li>
                    <li>Panel: Research Priorities in AI Finance</li>
                    <li>Welcome Reception</li>
                </ul>
            </div>
            <div class="card day-card day-2">
                <span class="day-number">DAY 2</span>
                <h3>Implementation & Innovation</h3>
                <ul class="bullet">
                    <li>Keynote: Digital Transformation in Gulf Banking</li>
                    <li>Paper sessions: Practical Applications</li>
                    <li>Case studies: DIFC, Emirates NBD, FAB</li>
                    <li>Industry Roundtable</li>
                    <li>Networking Dinner</li>
                </ul>
            </div>
            <div class="card day-card day-3">
                <span class="day-number">DAY 3</span>
                <h3>Network Launch</h3>
                <ul class="bullet">
                    <li>MSCA Doctoral Training Sessions</li>
                    <li>Early-career researcher presentations</li>
                    <li>Working Group Formation</li>
                    <li>5-Year Research Roadmap</li>
                    <li><strong>MoU Signing Ceremony</strong></li>
                </ul>
            </div>
        </div>
        <div class="card" style="margin-top:15px;">
            <h3>Target Audience</h3>
            <p><strong>80-100 participants</strong>: 60% academic (Switzerland, UAE, broader MENA) | 40% industry (banks, fintech, regulators)</p>
            <p style="margin-top:8px;">Stakeholders: DIFC, Emirates NBD, First Abu Dhabi Bank, Swiss fintech companies, regulatory officials, MSCA doctoral students.</p>
        </div>
    </section>

    <section id="aims" class="fade-in">
        <h2 class="section-title">Aims & Objectives</h2>
        <div class="card-grid">
            <div class="card">
                <h3>Core Objectives</h3>
                <ul class="bullet">
                    <li>Launch Swiss-MENA AI Finance Research Network via signed MoU</li>
                    <li>Bridge gap between academic AI research and industry implementation</li>
                    <li>Build research capacity through knowledge transfer</li>
                    <li>Create pathways for researcher mobility and joint supervision</li>
                </ul>
            </div>
            <div class="card">
                <h3>Expected Outcomes</h3>
                <ul class="bullet">
                    <li>MoU signatures from 10+ institutions</li>
                    <li>5-year strategic research roadmap</li>
                    <li>3-5 joint research proposals initiated</li>
                    <li>Open-access workshop proceedings</li>
                    <li>White paper for policymakers</li>
                </ul>
            </div>
            <div class="card">
                <h3>12-Month Targets</h3>
                <ul class="bullet">
                    <li>5+ joint publications in high-impact journals</li>
                    <li>2-3 formal industry-academia partnerships</li>
                    <li>Technology transfer opportunities identified</li>
                    <li>Follow-up bilateral funding applications</li>
                </ul>
            </div>
            <div class="card">
                <h3>Success Metrics</h3>
                <ul class="bullet">
                    <li>Participant satisfaction surveys</li>
                    <li>6 and 12-month impact tracking</li>
                    <li>Network membership growth</li>
                    <li>Publication and grant outputs</li>
                </ul>
            </div>
        </div>
    </section>

    <section id="network" class="fade-in">
        <h2 class="section-title">Partnership Network</h2>
        <div class="two-col">
            <div>
                <img src="data:image/png;base64,{network_map_b64}" alt="Network Map" class="network-img">
            </div>
            <div>
                <div class="card" style="margin-bottom:12px;">
                    <h3>7-Year Partnership Foundation</h3>
                    <p>The collaboration began in 2017 with groundbreaking cryptocurrency research, yielding publications with 500+ citations. Progressive deepening through blockchain security, fraud detection, and NFT research. Multiple grants secured, demonstrating international recognition of the partnership's value.</p>
                </div>
                <h3 style="font-size:14px;margin-bottom:10px;">Partner Institutions</h3>
                <div class="partner-grid">
                    <div class="partner"><strong>FHGR</strong><br>Switzerland - Network Coordinator</div>
                    <div class="partner mena"><strong>AUS</strong><br>UAE - MENA Coordinator</div>
                    <div class="partner"><strong>U. Manchester</strong><br>UK - ML/NLP Research</div>
                    <div class="partner"><strong>Renmin University</strong><br>China - Quant Finance</div>
                    <div class="partner"><strong>Babes-Bolyai</strong><br>Romania - Analytics</div>
                    <div class="partner"><strong>Bern UAS</strong><br>Switzerland - AI Banking</div>
                </div>
            </div>
        </div>
    </section>

    <section id="research" class="fade-in">
        <h2 class="section-title">Research Excellence</h2>
        <table>
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Publication</th>
                    <th>Journal</th>
                    <th>Citations</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>2017</td>
                    <td>GARCH Modelling of Cryptocurrencies</td>
                    <td>J. Risk Financial Management</td>
                    <td><strong>329</strong></td>
                </tr>
                <tr>
                    <td>2017</td>
                    <td>A Statistical Analysis of Cryptocurrencies</td>
                    <td>J. Risk Financial Management</td>
                    <td><strong>179</strong></td>
                </tr>
                <tr>
                    <td>2024</td>
                    <td>Stylized facts of metaverse NFTs</td>
                    <td>Physica A</td>
                    <td>6</td>
                </tr>
                <tr>
                    <td>2024</td>
                    <td>Blockchain Security: Anomalies & Fraud Detection</td>
                    <td>arXiv</td>
                    <td>4</td>
                </tr>
                <tr>
                    <td>2024</td>
                    <td>Metaverse Non Fungible Tokens</td>
                    <td>SSRN</td>
                    <td>3</td>
                </tr>
            </tbody>
        </table>
        <div class="card-grid" style="margin-top:15px;">
            <div class="card">
                <h3>Research Areas</h3>
                <div class="themes">
                    <span class="theme-tag">Cryptocurrency Markets</span>
                    <span class="theme-tag">Blockchain Security</span>
                    <span class="theme-tag">NFTs & Metaverse</span>
                    <span class="theme-tag">Fraud Detection</span>
                </div>
            </div>
            <div class="card">
                <h3>Impact Metrics</h3>
                <p><strong>7</strong> Joint Publications | <strong>550+</strong> Citations | <strong>86%</strong> Open Access</p>
            </div>
        </div>
    </section>

    <section id="organizers" class="fade-in">
        <h2 class="section-title">Organizers</h2>
        <div class="card-grid">
            <div class="card">
                <div class="organizer">
                    <div class="organizer-avatar">JO</div>
                    <div class="organizer-info">
                        <h3>Prof. Dr. Joerg Osterrieder</h3>
                        <p class="role">Network Coordinator | FHGR, Switzerland</p>
                        <p>Financial ML, Risk Management, Blockchain</p>
                        <p class="email">joerg.osterrieder@fhgr.ch</p>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="organizer">
                    <div class="organizer-avatar">SC</div>
                    <div class="organizer-info">
                        <h3>Prof. Dr. Stephen Chan</h3>
                        <p class="role">MENA Coordinator | AUS, UAE</p>
                        <p>Statistical Finance, Cryptocurrency Markets</p>
                        <p class="email">schan@aus.edu</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <h4>Leading House for the Middle East and North Africa</h4>
        <p>Connect & Collaborate Grant Program | HES-SO, Switzerland</p>
        <p style="margin-top:12px;">Workshop Registration: April 2026 | <a href="budget_showcase.html">View Budget Details</a></p>
        <p style="margin-top:8px;opacity:0.6;">Documentation generated November 2024</p>
    </footer>

    <script>
        // Animate stats on scroll
        const animateStats = () => {{
            document.querySelectorAll('.stat-number').forEach(stat => {{
                const target = parseInt(stat.dataset.target);
                const duration = 1500;
                const start = performance.now();
                const animate = (now) => {{
                    const elapsed = now - start;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    stat.textContent = Math.floor(target * eased) + (target > 100 ? '+' : '');
                    if (progress < 1) requestAnimationFrame(animate);
                }};
                requestAnimationFrame(animate);
            }});
        }};

        // Intersection Observer for fade-in
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

        // Trigger stat animation when hero is visible
        const heroObserver = new IntersectionObserver((entries) => {{
            if (entries[0].isIntersecting) {{
                animateStats();
                heroObserver.disconnect();
            }}
        }});
        heroObserver.observe(document.querySelector('.hero'));
    </script>
</body>
</html>
'''

# ============================================================================
# BUDGET SHOWCASE HTML
# ============================================================================

budget_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Budget Overview | AI for Digital Finance</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --swiss-blue: #2E5090;
            --swiss-blue-light: #4A7BC8;
            --swiss-blue-dark: #1e3a5f;
            --uae-burgundy: #8B1538;
            --uae-gold: #D4AF37;
            --text-dark: #1a1a1a;
            --text-light: #f5f5f5;
            --bg-light: #f0f2f5;
            --bg-card: #ffffff;
            --border-color: #dde1e6;
            --success: #2e7d32;
        }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            line-height: 1.4;
            color: var(--text-dark);
            background: var(--bg-light);
        }}
        /* Header */
        header {{
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--uae-burgundy) 100%);
            color: white;
            padding: 40px 20px 30px;
            text-align: center;
        }}
        header h1 {{
            font-size: 24px;
            margin-bottom: 8px;
        }}
        header .total {{
            font-size: 36px;
            font-weight: 700;
            color: var(--uae-gold);
        }}
        header a {{
            color: var(--uae-gold);
            font-size: 12px;
            display: inline-block;
            margin-top: 15px;
        }}
        /* Section */
        section {{
            padding: 25px 20px;
            max-width: 1100px;
            margin: 0 auto;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--swiss-blue);
            border-left: 4px solid var(--uae-burgundy);
            padding-left: 12px;
        }}
        /* Cards */
        .card {{
            background: var(--bg-card);
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid var(--border-color);
            margin-bottom: 15px;
        }}
        .card h3 {{
            font-size: 14px;
            color: var(--swiss-blue);
            margin-bottom: 10px;
        }}
        /* Chart images */
        .chart-img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            display: block;
            margin: 0 auto;
        }}
        /* Grid layouts */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .grid-3 {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
        }}
        @media (max-width: 768px) {{
            .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
        }}
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            background: var(--bg-card);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            background: linear-gradient(135deg, var(--swiss-blue) 0%, var(--uae-burgundy) 100%);
            color: white;
            font-weight: 600;
            font-size: 12px;
        }}
        tr:hover {{ background: #f8f9fa; }}
        td:last-child {{ text-align: right; }}
        th:last-child {{ text-align: right; }}
        .total-row {{
            background: #f0f4f8;
            font-weight: 700;
        }}
        /* Status badges */
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        }}
        .badge-ok {{
            background: #e8f5e9;
            color: var(--success);
        }}
        /* Summary boxes */
        .summary-box {{
            text-align: center;
            padding: 15px;
            background: var(--bg-card);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        .summary-box .amount {{
            font-size: 24px;
            font-weight: 700;
            color: var(--swiss-blue);
        }}
        .summary-box .label {{
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }}
        .summary-box .pct {{
            font-size: 14px;
            color: var(--uae-burgundy);
            font-weight: 600;
        }}
        /* Footer */
        footer {{
            background: var(--swiss-blue-dark);
            color: var(--text-light);
            padding: 20px;
            text-align: center;
            font-size: 12px;
        }}
        footer a {{ color: var(--uae-gold); }}
    </style>
</head>
<body>
    <header>
        <a href="workshop_showcase.html">&larr; Back to Workshop Overview</a>
        <h1>Budget Overview</h1>
        <div class="total">CHF 24,500</div>
        <p>Total Project Cost</p>
    </header>

    <section>
        <h2 class="section-title">Funding Sources</h2>
        <div class="grid-2">
            <div>
                <img src="data:image/png;base64,{funding_sources_b64}" alt="Funding Sources" class="chart-img">
            </div>
            <div>
                <div class="grid-3">
                    <div class="summary-box">
                        <div class="amount">CHF 5,000</div>
                        <div class="label">CCG Request</div>
                        <div class="pct">20.4%</div>
                    </div>
                    <div class="summary-box">
                        <div class="amount">CHF 5,000</div>
                        <div class="label">AUS Co-funding</div>
                        <div class="pct">20.4%</div>
                    </div>
                    <div class="summary-box">
                        <div class="amount">CHF 14,500</div>
                        <div class="label">Other Sources</div>
                        <div class="pct">59.2%</div>
                    </div>
                </div>
                <div class="card" style="margin-top:15px;">
                    <h3>Other Sources Breakdown</h3>
                    <table>
                        <tr><td>Registration Fees (80 x CHF 100)</td><td>CHF 8,000</td></tr>
                        <tr><td>FHGR Contribution</td><td>CHF 2,500</td></tr>
                        <tr><td>Speaker Institutions</td><td>CHF 2,500</td></tr>
                        <tr><td>Industry Sponsors</td><td>CHF 1,500</td></tr>
                        <tr class="total-row"><td>Total</td><td>CHF 14,500</td></tr>
                    </table>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="section-title">Budget by Category</h2>
        <div class="grid-2">
            <div>
                <img src="data:image/png;base64,{budget_categories_b64}" alt="Budget Categories" class="chart-img">
            </div>
            <div>
                <table>
                    <thead>
                        <tr><th>Category</th><th>Amount (CHF)</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Catering (coffee breaks, lunches, reception)</td><td>12,400</td></tr>
                        <tr><td>Travel (Swiss researchers, speakers)</td><td>4,000</td></tr>
                        <tr><td>Accommodation</td><td>2,700</td></tr>
                        <tr><td>Materials & Platform</td><td>2,600</td></tr>
                        <tr><td>Venue & Equipment</td><td>2,300</td></tr>
                        <tr><td>Work Costs (coordination)</td><td>500</td></tr>
                        <tr class="total-row"><td><strong>Total</strong></td><td><strong>24,500</strong></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <section>
        <h2 class="section-title">CCG Request Breakdown: CHF 5,000</h2>
        <div class="grid-2">
            <div>
                <img src="data:image/png;base64,{ccg_breakdown_b64}" alt="CCG Breakdown" class="chart-img">
            </div>
            <div>
                <table>
                    <thead>
                        <tr><th>Category</th><th>Amount (CHF)</th><th>%</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Travel</td><td>1,500</td><td>30%</td></tr>
                        <tr><td>Catering</td><td>1,200</td><td>24%</td></tr>
                        <tr><td>Subsistence</td><td>800</td><td>16%</td></tr>
                        <tr><td>Work Costs</td><td>600</td><td>12%</td></tr>
                        <tr><td>Online Platform</td><td>600</td><td>12%</td></tr>
                        <tr><td>Materials</td><td>300</td><td>6%</td></tr>
                        <tr class="total-row"><td><strong>Total</strong></td><td><strong>5,000</strong></td><td><strong>100%</strong></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <section>
        <h2 class="section-title">AUS Co-funding: CHF 5,000</h2>
        <table>
            <thead>
                <tr><th>Item</th><th>Type</th><th>Amount (CHF)</th></tr>
            </thead>
            <tbody>
                <tr><td>Venue Rental (3 days)</td><td>In-kind</td><td>1,500</td></tr>
                <tr><td>Technical Equipment (AV, streaming)</td><td>In-kind</td><td>800</td></tr>
                <tr><td>Lunch Support</td><td>Direct</td><td>1,500</td></tr>
                <tr><td>Welcome Reception Support</td><td>Direct</td><td>800</td></tr>
                <tr><td>Workshop Materials</td><td>Direct</td><td>400</td></tr>
                <tr class="total-row"><td><strong>Total</strong></td><td></td><td><strong>5,000</strong></td></tr>
            </tbody>
        </table>
    </section>

    <section>
        <h2 class="section-title">CCG Compliance Check</h2>
        <table>
            <thead>
                <tr><th>Requirement</th><th>Limit</th><th>Actual</th><th>Status</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>Maximum CCG for workshops</td>
                    <td>CHF 5,000</td>
                    <td>CHF 5,000</td>
                    <td><span class="badge badge-ok">OK</span></td>
                </tr>
                <tr>
                    <td>Maximum work costs</td>
                    <td>20%</td>
                    <td>12%</td>
                    <td><span class="badge badge-ok">OK</span></td>
                </tr>
                <tr>
                    <td>Co-funding required</td>
                    <td>Yes</td>
                    <td>80%</td>
                    <td><span class="badge badge-ok">OK</span></td>
                </tr>
                <tr>
                    <td>MENA partner contribution</td>
                    <td>Required</td>
                    <td>CHF 5,000</td>
                    <td><span class="badge badge-ok">OK</span></td>
                </tr>
            </tbody>
        </table>
    </section>

    <footer>
        <p><a href="workshop_showcase.html">&larr; Back to Workshop Overview</a></p>
        <p style="margin-top:10px;opacity:0.7;">AI for Digital Finance: Swiss-MENA Research Network | April 21-23, 2026</p>
    </footer>
</body>
</html>
'''

# Write files
main_path = BASE_DIR / "workshop_showcase.html"
budget_path = BASE_DIR / "budget_showcase.html"

with open(main_path, "w", encoding="utf-8") as f:
    f.write(main_html)
print(f"Created: {main_path}")

with open(budget_path, "w", encoding="utf-8") as f:
    f.write(budget_html)
print(f"Created: {budget_path}")

print("\nBoth HTML files generated successfully!")
print(f"- Main showcase: {main_path}")
print(f"- Budget page: {budget_path}")
