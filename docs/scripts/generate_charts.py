"""
Generate budget visualizations for documentation
- Pie chart: Funding sources
- Bar chart: Budget categories
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Budget data
FUNDING_SOURCES = {
    "CCG Request": 5000,
    "AUS Co-funding": 5000,
    "Other Sources": 14500
}

BUDGET_CATEGORIES = {
    "Travel": 4000,
    "Accommodation": 2700,
    "Venue & Equipment": 2300,
    "Catering": 12400,
    "Materials & Platform": 2600,
    "Work Costs": 500
}

CCG_BREAKDOWN = {
    "Travel": 1500,
    "Accommodation": 800,
    "Catering": 1200,
    "Materials": 300,
    "Platform": 600,
    "Work Costs": 600
}

# Color scheme - professional blues and grays
COLORS_PIE = ['#2E5090', '#C41E3A', '#4A4A4A']
COLORS_BAR = '#2E5090'

def create_funding_pie():
    """Create pie chart of funding sources"""

    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')

    labels = list(FUNDING_SOURCES.keys())
    sizes = list(FUNDING_SOURCES.values())
    total = sum(sizes)

    # Calculate percentages
    percentages = [f"{s/total*100:.1f}%" for s in sizes]

    # Create pie
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct='',
        colors=COLORS_PIE,
        startangle=90,
        explode=(0.02, 0.02, 0.02),
        shadow=False,
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'}
    )

    # Add custom labels
    for i, (wedge, label, pct, size) in enumerate(zip(wedges, labels, percentages, sizes)):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = np.cos(np.radians(angle))
        y = np.sin(np.radians(angle))

        # Position for label
        ax.annotate(
            f"{label}\nCHF {size:,}\n({pct})",
            xy=(x * 0.6, y * 0.6),
            ha='center', va='center',
            fontsize=11,
            fontweight='bold',
            color='white'
        )

    ax.set_title("Funding Sources\nTotal: CHF 24,500",
                fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig

def create_budget_bar():
    """Create bar chart of budget categories"""

    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    ax.set_facecolor('white')

    categories = list(BUDGET_CATEGORIES.keys())
    values = list(BUDGET_CATEGORIES.values())

    # Create bars
    bars = ax.barh(categories, values, color=COLORS_BAR, height=0.6, alpha=0.9)

    # Add value labels
    for bar, value in zip(bars, values):
        ax.text(value + 200, bar.get_y() + bar.get_height()/2,
               f"CHF {value:,}",
               va='center', ha='left',
               fontsize=10, fontweight='bold')

    ax.set_xlabel("Amount (CHF)", fontsize=11)
    ax.set_title("Budget by Category", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, max(values) * 1.2)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    return fig

def create_ccg_breakdown():
    """Create pie chart of CCG request breakdown"""

    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')

    labels = list(CCG_BREAKDOWN.keys())
    sizes = list(CCG_BREAKDOWN.values())
    total = sum(sizes)

    # Colors - gradient of blues
    colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(labels)))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=lambda pct: f'{pct:.0f}%' if pct > 5 else '',
        colors=colors,
        startangle=90,
        wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'}
    )

    # Style the labels
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')

    ax.set_title("CCG Request Breakdown\nTotal: CHF 5,000",
                fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig

def main():
    # Output path
    script_dir = Path(__file__).parent
    images_dir = script_dir.parent / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Generate funding pie chart
    print("Generating funding sources pie chart...")
    fig1 = create_funding_pie()
    fig1.savefig(images_dir / "funding_sources.png", dpi=150, bbox_inches='tight',
                 facecolor='white', edgecolor='none')
    print(f"  Saved: {images_dir / 'funding_sources.png'}")

    # Generate budget bar chart
    print("Generating budget categories bar chart...")
    fig2 = create_budget_bar()
    fig2.savefig(images_dir / "budget_categories.png", dpi=150, bbox_inches='tight',
                 facecolor='white', edgecolor='none')
    print(f"  Saved: {images_dir / 'budget_categories.png'}")

    # Generate CCG breakdown
    print("Generating CCG breakdown pie chart...")
    fig3 = create_ccg_breakdown()
    fig3.savefig(images_dir / "ccg_breakdown.png", dpi=150, bbox_inches='tight',
                 facecolor='white', edgecolor='none')
    print(f"  Saved: {images_dir / 'ccg_breakdown.png'}")

    plt.close('all')
    print("\nAll charts generated successfully!")

if __name__ == "__main__":
    main()
