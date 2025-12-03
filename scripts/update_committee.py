"""
Update committee: remove and add members as specified
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Members to REMOVE
REMOVE = [
    "Alfonso Iodice D'Enza",
    "Axel Gross-Klussmann",
    "Barbara Bedowska-Sojka",
    "Bettina Grun",
    "Bruno Spilak",
    "Christina Kolb",
    "Fons Wijnhoven",
    "Franz Xaver Zobl",
    "Laura Spierdijk",
    "Marcella Corduas",
    "Mattia Bellotti"
]

# Members to ADD (with their data)
ADD = [
    {
        "name": "Codruta Mare",
        "affiliation": "Babes-Bolyai University, Romania",
        "photo": "codruta_mare.jpg"
    },
    {
        "name": "Daniel Traian Pele",
        "affiliation": "Bucharest University of Economic Studies, Romania",
        "photo": "daniel_traian_pele.jpg"
    },
    {
        "name": "Wolfgang Haerdle",
        "affiliation": "Humboldt University Berlin, Germany",
        "photo": "wolfgang_haerdle.jpg"
    },
    {
        "name": "Maria Iannario",
        "affiliation": "University of Naples Federico II, Italy",
        "photo": "maria_iannario.jpg"
    }
]

def main():
    print("=" * 60)
    print("UPDATING COMMITTEE")
    print("=" * 60)

    # Load data
    sc_path = DATA_DIR / "scientific_committee.json"
    with open(sc_path, 'r', encoding='utf-8') as f:
        sc_data = json.load(f)

    pn_path = DATA_DIR / "msca_people_named.json"
    with open(pn_path, 'r', encoding='utf-8') as f:
        pn_data = json.load(f)

    bios_path = DATA_DIR / "msca_bios.json"
    with open(bios_path, 'r', encoding='utf-8') as f:
        bios_data = json.load(f)

    # Remove members
    print("\nREMOVING:")
    for name in REMOVE:
        if name in sc_data['selected']:
            sc_data['selected'].remove(name)
            print(f"  - {name}")
        else:
            print(f"  - {name} (not found)")

    # Add members
    print("\nADDING:")
    for member in ADD:
        name = member['name']
        affil = member['affiliation']
        photo = member['photo']

        # Add to committee
        if name not in sc_data['selected']:
            sc_data['selected'].append(name)
            print(f"  + {name}")
        else:
            print(f"  + {name} (already in committee)")

        # Add photo mapping
        existing_names = [p['name'] for p in pn_data['people']]
        if name not in existing_names:
            pn_data['people'].append({'name': name, 'filename': photo})
            print(f"    Photo: {photo}")

        # Add affiliation
        if name not in bios_data.get('affiliations', {}):
            bios_data['affiliations'][name] = affil
            print(f"    Affiliation: {affil}")

    # Sort and update count
    sc_data['selected'].sort()
    sc_data['total_selected'] = len(sc_data['selected'])

    # Save all files
    with open(sc_path, 'w', encoding='utf-8') as f:
        json.dump(sc_data, f, indent=2, ensure_ascii=False)

    with open(pn_path, 'w', encoding='utf-8') as f:
        json.dump(pn_data, f, indent=2, ensure_ascii=False)

    with open(bios_path, 'w', encoding='utf-8') as f:
        json.dump(bios_data, f, indent=2, ensure_ascii=False)

    print(f"\nTotal committee members: {sc_data['total_selected']}")
    print("\nUpdated files saved.")

if __name__ == "__main__":
    main()
