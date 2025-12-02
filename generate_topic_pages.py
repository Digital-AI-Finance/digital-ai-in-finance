"""
Generate 6 topic detail pages for the conference website
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR

TOPICS = {
    "llms": {
        "title": "LLMs in Finance",
        "subtitle": "Large Language Models for Financial Applications",
        "description": """
Large Language Models (LLMs) are transforming the financial industry by enabling sophisticated
natural language understanding and generation capabilities. From automated report generation
to sentiment analysis of market news, LLMs are becoming essential tools for financial
institutions seeking competitive advantages through AI-driven insights.

This research track explores the application of transformer-based models like GPT, BERT,
and their domain-specific variants (FinBERT, BloombergGPT) to financial tasks. We examine
both opportunities and challenges, including hallucination risks, regulatory compliance,
and the need for explainable outputs in high-stakes financial decisions.
        """,
        "questions": [
            "How can LLMs be fine-tuned for specific financial domains (credit risk, trading, compliance)?",
            "What are effective strategies for mitigating hallucination risks in financial LLM applications?",
            "How do regulatory requirements (MiFID II, GDPR) impact LLM deployment in finance?",
            "Can LLMs enhance financial inclusion through multilingual capabilities in MENA markets?",
            "What role do LLMs play in automated financial report generation and summarization?"
        ],
        "methodologies": [
            "Fine-tuning pre-trained models on financial corpora",
            "Retrieval-Augmented Generation (RAG) for factual grounding",
            "Prompt engineering for financial tasks",
            "Evaluation metrics: accuracy, hallucination rate, latency",
            "Human-in-the-loop validation frameworks"
        ],
        "applications": [
            "Automated earnings call analysis",
            "News sentiment extraction for trading signals",
            "Regulatory document processing and compliance checking",
            "Customer service chatbots for banking",
            "Financial report summarization"
        ]
    },
    "xai": {
        "title": "Explainable AI",
        "subtitle": "Transparency and Interpretability in Financial AI",
        "description": """
Explainable AI (XAI) addresses the critical need for transparency in AI-driven financial
decisions. As machine learning models become more complex, regulators and stakeholders
increasingly demand clear explanations for credit decisions, risk assessments, and
investment recommendations.

This track focuses on methods to make black-box models interpretable while maintaining
predictive performance. We explore both post-hoc explanation techniques and inherently
interpretable models suitable for regulated financial environments where accountability
and auditability are paramount.
        """,
        "questions": [
            "How can SHAP and LIME be adapted for complex financial time series models?",
            "What level of explainability satisfies regulatory requirements (ECB, BaFin, FINMA)?",
            "How do we balance model complexity with interpretability in credit scoring?",
            "Can attention mechanisms provide meaningful explanations for financial predictions?",
            "What are best practices for communicating AI explanations to non-technical stakeholders?"
        ],
        "methodologies": [
            "SHAP (SHapley Additive exPlanations) values",
            "LIME (Local Interpretable Model-agnostic Explanations)",
            "Attention visualization for transformer models",
            "Counterfactual explanations",
            "Inherently interpretable models (GAMs, rule-based systems)"
        ],
        "applications": [
            "Credit scoring model explanations for rejected applicants",
            "Risk model audit trails for regulatory compliance",
            "Investment recommendation justifications",
            "Fraud detection alert explanations",
            "Algorithmic trading decision logs"
        ]
    },
    "blockchain": {
        "title": "Blockchain Security",
        "subtitle": "Securing Digital Assets and Smart Contracts",
        "description": """
Blockchain technology underpins cryptocurrencies, DeFi protocols, and increasingly
traditional financial infrastructure. Security remains paramount as billions of dollars
in digital assets require protection from sophisticated attacks targeting smart contracts,
consensus mechanisms, and cryptographic primitives.

This research track examines security challenges across the blockchain ecosystem, from
formal verification of smart contracts to detection of market manipulation in
decentralized exchanges. We address both technical security measures and the regulatory
frameworks emerging to govern digital asset markets.
        """,
        "questions": [
            "How can formal verification methods reduce smart contract vulnerabilities?",
            "What machine learning approaches effectively detect DeFi exploits and rug pulls?",
            "How do cross-chain bridges create new attack surfaces, and how can they be secured?",
            "What regulatory frameworks are emerging for blockchain security in MENA and Europe?",
            "How can zero-knowledge proofs enhance privacy while maintaining compliance?"
        ],
        "methodologies": [
            "Static and dynamic smart contract analysis",
            "Formal verification (Solidity, Vyper)",
            "Anomaly detection for blockchain transactions",
            "Graph analysis for money laundering detection",
            "Penetration testing for DeFi protocols"
        ],
        "applications": [
            "Smart contract auditing and vulnerability assessment",
            "Real-time fraud detection in cryptocurrency exchanges",
            "AML/KYC compliance for digital asset platforms",
            "Secure custody solutions for institutional investors",
            "Cross-border payment security"
        ]
    },
    "risk": {
        "title": "Risk Management",
        "subtitle": "AI-Enhanced Risk Assessment and Mitigation",
        "description": """
Modern risk management leverages artificial intelligence to process vast amounts of data,
identify emerging threats, and quantify exposures across market, credit, operational,
and cyber risk domains. AI enables real-time risk monitoring and more accurate stress
testing scenarios.

This track explores how machine learning transforms traditional risk frameworks, from
VaR calculations using neural networks to climate risk modeling with advanced scenario
analysis. We examine both the enhanced capabilities AI provides and the model risks it
introduces to financial institutions.
        """,
        "questions": [
            "How can deep learning improve Value-at-Risk (VaR) estimation accuracy?",
            "What role does AI play in climate risk modeling and stress testing?",
            "How should model risk management evolve to address AI/ML model risks?",
            "Can reinforcement learning optimize dynamic hedging strategies?",
            "How do we validate AI risk models for regulatory approval?"
        ],
        "methodologies": [
            "Deep learning for VaR and Expected Shortfall",
            "Recurrent neural networks for credit risk prediction",
            "Monte Carlo simulation with ML-generated scenarios",
            "Ensemble methods for operational risk",
            "Natural language processing for emerging risk identification"
        ],
        "applications": [
            "Real-time market risk monitoring dashboards",
            "Credit default prediction models",
            "Operational risk event classification",
            "Climate risk scenario generation",
            "Cyber risk quantification"
        ]
    },
    "banking": {
        "title": "Digital Banking",
        "subtitle": "Transformation of Financial Services in the Digital Era",
        "description": """
Digital banking represents a fundamental shift in how financial services are delivered,
combining mobile-first interfaces, API-driven architectures, and AI-powered
personalization. From neobanks to incumbent digital transformations, the industry is
reimagining customer experience and operational efficiency.

This track examines digital banking innovations in both developed and emerging markets,
with particular focus on MENA region opportunities. We explore how AI enhances customer
onboarding, personalized product recommendations, and fraud prevention while maintaining
regulatory compliance across jurisdictions.
        """,
        "questions": [
            "How can AI-powered onboarding reduce friction while ensuring KYC compliance?",
            "What personalization strategies drive customer engagement in digital banking?",
            "How do neobanks and traditional banks differ in their AI adoption strategies?",
            "What opportunities exist for digital banking innovation in MENA markets?",
            "How can open banking APIs enable new financial service ecosystems?"
        ],
        "methodologies": [
            "Customer journey analytics and optimization",
            "Recommendation systems for financial products",
            "Biometric authentication and identity verification",
            "Process mining for operational efficiency",
            "A/B testing for digital experience optimization"
        ],
        "applications": [
            "AI-powered customer service and chatbots",
            "Personalized savings and investment recommendations",
            "Automated loan decisioning",
            "Digital identity verification",
            "Open banking aggregation platforms"
        ]
    },
    "altdata": {
        "title": "Alternative Data",
        "subtitle": "Non-Traditional Data Sources for Financial Intelligence",
        "description": """
Alternative data encompasses non-traditional information sources that provide investment
insights beyond conventional financial statements and market data. Satellite imagery,
social media sentiment, web traffic, and IoT sensor data are transforming how investors
and financial institutions generate alpha and assess risks.

This track explores the acquisition, processing, and modeling of alternative data for
financial applications. We address data quality challenges, privacy considerations, and
the evolving regulatory landscape around alternative data usage in investment decisions.
        """,
        "questions": [
            "How can satellite imagery predict retail performance and supply chain disruptions?",
            "What NLP techniques best extract trading signals from social media and news?",
            "How do we assess the decay rate and alpha potential of alternative data sources?",
            "What privacy and ethical considerations apply to alternative data in finance?",
            "How can alternative data improve credit assessment for underbanked populations?"
        ],
        "methodologies": [
            "Satellite image analysis using CNNs",
            "Social media sentiment analysis",
            "Web scraping and data aggregation",
            "Time series analysis for signal extraction",
            "Data fusion techniques"
        ],
        "applications": [
            "Hedge fund alpha generation",
            "ESG scoring from satellite and sensor data",
            "Consumer credit scoring with alternative data",
            "Supply chain monitoring",
            "Real estate valuation with location intelligence"
        ]
    }
}

def generate_topic_page(topic_id, topic_data):
    css = '''
    :root { --blue: #2E5090; --gold: #D4AF37; --dark: #1a1a2e; --light: #f5f5f5; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, -apple-system, sans-serif; font-size: 14px; line-height: 1.6; color: #333; background: var(--light); }

    .header { background: linear-gradient(135deg, var(--blue), #1a3a6e); color: white; padding: 40px 20px; text-align: center; }
    .header h1 { font-size: 2rem; margin-bottom: 5px; }
    .header p { opacity: 0.9; font-size: 1.1rem; }
    .back-link { position: absolute; top: 20px; left: 20px; color: white; text-decoration: none; font-size: 0.9rem; opacity: 0.8; }
    .back-link:hover { opacity: 1; }

    .container { max-width: 900px; margin: 0 auto; padding: 30px 20px; }

    .section { background: white; border-radius: 8px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .section h2 { color: var(--blue); font-size: 1.2rem; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
    .section h2::before { content: ''; width: 4px; height: 20px; background: var(--gold); }

    .description { font-size: 0.95rem; color: #444; text-align: justify; }

    ul { list-style: none; }
    ul li { padding: 8px 0 8px 25px; position: relative; border-bottom: 1px solid #eee; }
    ul li:last-child { border-bottom: none; }
    ul li::before { content: ''; position: absolute; left: 0; top: 14px; width: 8px; height: 8px; background: var(--gold); border-radius: 50%; }

    .cta { text-align: center; margin-top: 30px; }
    .cta a { display: inline-block; background: var(--blue); color: white; padding: 12px 30px; border-radius: 5px; text-decoration: none; font-weight: 600; transition: background 0.3s; }
    .cta a:hover { background: #1a3a6e; }

    .topics-nav { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; margin-bottom: 30px; }
    .topics-nav a { background: white; color: var(--blue); padding: 8px 15px; border-radius: 20px; text-decoration: none; font-size: 0.85rem; border: 1px solid #ddd; transition: all 0.3s; }
    .topics-nav a:hover, .topics-nav a.active { background: var(--blue); color: white; border-color: var(--blue); }

    footer { text-align: center; padding: 30px; color: #666; font-size: 0.85rem; }
    footer a { color: var(--blue); }
    '''

    # Build navigation for other topics
    nav_html = ''
    for tid, tdata in TOPICS.items():
        active = 'active' if tid == topic_id else ''
        nav_html += f'<a href="topic_{tid}.html" class="{active}">{tdata["title"]}</a>'

    # Build questions list
    questions_html = ''.join(f'<li>{q}</li>' for q in topic_data['questions'])

    # Build methodologies list
    methods_html = ''.join(f'<li>{m}</li>' for m in topic_data['methodologies'])

    # Build applications list
    apps_html = ''.join(f'<li>{a}</li>' for a in topic_data['applications'])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic_data['title']} - AI for Digital Finance 2026</title>
    <style>{css}</style>
</head>
<body>
    <header class="header">
        <a href="index.html" class="back-link">&larr; Back to Conference</a>
        <h1>{topic_data['title']}</h1>
        <p>{topic_data['subtitle']}</p>
    </header>

    <div class="container">
        <div class="topics-nav">
            {nav_html}
        </div>

        <div class="section">
            <h2>Overview</h2>
            <div class="description">
                {topic_data['description'].strip()}
            </div>
        </div>

        <div class="section">
            <h2>Key Research Questions</h2>
            <ul>
                {questions_html}
            </ul>
        </div>

        <div class="section">
            <h2>Methodologies</h2>
            <ul>
                {methods_html}
            </ul>
        </div>

        <div class="section">
            <h2>Industry Applications</h2>
            <ul>
                {apps_html}
            </ul>
        </div>

        <div class="cta">
            <a href="index.html#topics">Submit Your Research</a>
        </div>
    </div>

    <footer>
        <p>AI for Digital Finance Workshop | April 21-23, 2026 | American University of Sharjah, UAE</p>
        <p><a href="index.html">Back to Main Conference Page</a></p>
    </footer>
</body>
</html>'''

    return html

def main():
    print("Generating topic pages...")

    for topic_id, topic_data in TOPICS.items():
        html = generate_topic_page(topic_id, topic_data)
        output_file = OUTPUT_DIR / f"topic_{topic_id}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Created: {output_file.name}")

    print(f"\nGenerated {len(TOPICS)} topic pages")

if __name__ == "__main__":
    main()
