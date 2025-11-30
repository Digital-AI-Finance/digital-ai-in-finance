"""
Generate network diagram for Swiss-MENA AI Finance Research Network
Simple circles with clean typography
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Network configuration
INSTITUTIONS = {
    # Core partners (center)
    "FHGR": {
        "name": "FHGR",
        "full_name": "Univ. Applied Sciences\nGrisons",
        "country": "CH",
        "type": "core",
        "position": (-1.5, 0),
        "color": "#2E5090"  # Swiss blue
    },
    "AUS": {
        "name": "AUS",
        "full_name": "American University\nof Sharjah",
        "country": "UAE",
        "type": "core",
        "position": (1.5, 0),
        "color": "#C41E3A"  # UAE red
    },
    # Satellite partners
    "Manchester": {
        "name": "Manchester",
        "full_name": "University of\nManchester",
        "country": "UK",
        "type": "satellite",
        "position": (-2.5, 2),
        "color": "#660099"
    },
    "Renmin": {
        "name": "Renmin",
        "full_name": "Renmin\nUniversity",
        "country": "CN",
        "type": "satellite",
        "position": (2.5, 2),
        "color": "#DE2910"
    },
    "Babes-Bolyai": {
        "name": "Babes-Bolyai",
        "full_name": "Babes-Bolyai\nUniversity",
        "country": "RO",
        "type": "satellite",
        "position": (-2.5, -2),
        "color": "#002B7F"
    },
    "Bern": {
        "name": "Bern",
        "full_name": "Bern Univ. of\nApplied Sciences",
        "country": "CH",
        "type": "satellite",
        "position": (0, -2.5),
        "color": "#2E5090"
    }
}

# Connections
CONNECTIONS = [
    # Core connection (thick)
    ("FHGR", "AUS", "core", 4),
    # FHGR connections
    ("FHGR", "Manchester", "research", 2),
    ("FHGR", "Renmin", "research", 2),
    ("FHGR", "Babes-Bolyai", "research", 2),
    ("FHGR", "Bern", "research", 2),
    # AUS connections
    ("AUS", "Manchester", "research", 1.5),
    ("AUS", "Renmin", "research", 1.5),
]

def create_network_diagram():
    """Create the network visualization"""

    fig, ax = plt.subplots(figsize=(12, 10), facecolor='white')
    ax.set_facecolor('white')

    # Draw connections first (behind nodes)
    for source, target, conn_type, width in CONNECTIONS:
        src_pos = INSTITUTIONS[source]["position"]
        tgt_pos = INSTITUTIONS[target]["position"]

        color = "#1a1a1a" if conn_type == "core" else "#888888"
        style = "-" if conn_type == "core" else "--"

        ax.plot([src_pos[0], tgt_pos[0]], [src_pos[1], tgt_pos[1]],
                color=color, linewidth=width, linestyle=style, alpha=0.6, zorder=1)

    # Draw nodes
    for key, inst in INSTITUTIONS.items():
        x, y = inst["position"]
        is_core = inst["type"] == "core"

        # Node size
        radius = 0.8 if is_core else 0.6

        # Draw circle
        circle = plt.Circle((x, y), radius,
                           facecolor=inst["color"],
                           edgecolor='white',
                           linewidth=3,
                           alpha=0.9,
                           zorder=2)
        ax.add_patch(circle)

        # Institution name (inside circle)
        ax.text(x, y + 0.1, inst["name"],
               fontsize=14 if is_core else 11,
               fontweight='bold',
               color='white',
               ha='center', va='center',
               zorder=3)

        # Country code (below name, inside circle)
        ax.text(x, y - 0.25, inst["country"],
               fontsize=10 if is_core else 8,
               color='white',
               alpha=0.8,
               ha='center', va='center',
               zorder=3)

        # Full name (outside circle, below)
        ax.text(x, y - radius - 0.3, inst["full_name"],
               fontsize=9,
               color='#333333',
               ha='center', va='top',
               zorder=3)

    # Title
    ax.text(0, 3.5, "Swiss-MENA AI Finance Research Network",
           fontsize=18, fontweight='bold', color='#1a1a1a',
           ha='center', va='center')

    ax.text(0, 3.0, "Core Partners and International Collaborators",
           fontsize=12, color='#666666',
           ha='center', va='center')

    # Legend
    legend_y = -4
    legend_items = [
        (mpatches.Patch(color='#2E5090', alpha=0.9), "Core Partner"),
        (mpatches.Patch(color='#888888', alpha=0.9), "Research Partner"),
        (plt.Line2D([0], [0], color='#1a1a1a', linewidth=4), "Primary Collaboration"),
        (plt.Line2D([0], [0], color='#888888', linewidth=2, linestyle='--'), "Research Connection"),
    ]

    legend = ax.legend([item[0] for item in legend_items],
                       [item[1] for item in legend_items],
                       loc='lower center',
                       ncol=4,
                       fontsize=10,
                       frameon=True,
                       fancybox=True,
                       shadow=False,
                       bbox_to_anchor=(0.5, -0.1))

    # Set axis limits
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4.5, 4)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()

    return fig

def main():
    # Output path
    script_dir = Path(__file__).parent
    images_dir = script_dir.parent / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    output_path = images_dir / "network_map.png"

    # Generate diagram
    print("Generating network diagram...")
    fig = create_network_diagram()

    # Save
    fig.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved: {output_path}")

    # Also save PDF version
    pdf_path = images_dir / "network_map.pdf"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved: {pdf_path}")

    plt.close()

if __name__ == "__main__":
    main()
