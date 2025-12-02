"""
Merge member data: correct photos with affiliations from existing data
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Load correct photo mappings
with open(DATA_DIR / 'msca_members_correct.json') as f:
    correct_data = json.load(f)

# Load existing affiliations
with open(DATA_DIR / 'msca_bios.json') as f:
    bios_data = json.load(f)

affiliations = bios_data.get('affiliations', {})

# Known affiliations for MSCA network (from project docs and website)
KNOWN_AFFILIATIONS = {
    "Stephen Chan": "American University of Sharjah, UAE",
    "Joerg Osterrieder": "FHGR, Switzerland",
    "Liana Stanca": "Babes-Bolyai University, Romania",
    "Audrius Kabasinskas": "Kaunas University of Technology, Lithuania",
    "Jeffrey Chu": "University of Manchester, UK",
    "Axel Gross-Klussmann": "Bern University of Applied Sciences, Switzerland",
    "Ruting Wang": "Renmin University of China, China",
    "Claudia Tarantola": "University of Pavia, Italy",
    "Sabrina Giordano": "University of Calabria, Italy",
    "Catarina Silva": "University of Coimbra, Portugal",
    "Ioana Coita": "University of Oradea, Romania",
    "Alessandra Tanda": "University of Pavia, Italy",
    "Anastas Dzurovski": "University of Pristina, Kosovo",
    "Albulena Shala": "University of Pristina, Kosovo",
    "Rezarta Perri": "University of Pristina, Kosovo",
    "Bettina Grun": "WU Vienna, Austria",
    "Bruno Spilak": "Humboldt University Berlin, Germany",
    "Barbara Będowska-Sójka": "Poznan University of Economics, Poland",
    "Giorgos Giannopoulos": "Athena Research Centre, Greece",
    "Adrian Costea": "Bucharest University of Economic Studies, Romania",
    "Mattia Bellotti": "University of Naples Federico II, Italy",
    "Marcella Corduas": "University of Naples Federico II, Italy",
    "Alfonso Iodice D'Enza": "University of Naples Federico II, Italy",
    "Fons Wijnhoven": "University of Twente, Netherlands",
    "Laura Spierdijk": "University of Twente, Netherlands",
    "Martijn Mes": "University of Twente, Netherlands",
    "Christina Kolb": "WU Vienna, Austria",
    "Franz Xaver Zobl": "WU Vienna, Austria",
    "Stefan Schlamp": "FHGR, Switzerland",
    "Sandro Schmid": "Bern University of Applied Sciences, Switzerland",
    "Daniela Schackis": "FHGR, Switzerland",
    "Gokce Nur Yilmaz": "Kaunas University of Technology, Lithuania",
    "Aidas Malakauskas": "Kaunas University of Technology, Lithuania",
    "Roman Timofeev": "Humboldt University Berlin, Germany",
    "Adam Kurpisz": "Athena Research Centre, Greece",
    "Alberto Ferrario": "Bern University of Applied Sciences, Switzerland",
    "Stefano Penazzi": "Cardo AI, Italy",
    "David Siang-Li Jheng": "Deutsche Bank, Germany",
    "Altin Kadareja": "Royalton Partners, UK",
    "Rebecca Di Francesco": "EIT Digital, EU",
    "Owen Chaffard": "LPA Group, Luxembourg",
    "Jorg Wenzel": "Royalton Partners, UK",
    "Valeri Andreev": "Swedbank, Sweden",
    "Adrian Bojan": "Raiffeisen Bank, Romania",
    "Hanna Kristín Skaftadóttir": "European Central Bank, Germany",
    "Abhista Abhista": "University of Twente, Netherlands",
}

# Merge data
merged_members = []
for member in correct_data['members']:
    name = member['name']
    # Get affiliation from known list or existing data
    affiliation = KNOWN_AFFILIATIONS.get(name, affiliations.get(name, ''))

    merged_members.append({
        'name': name,
        'affiliation': affiliation,
        'filename': member['filename']
    })

    print(f"{name}: {affiliation or 'Unknown'}")

# Save merged data
output = {
    'source': 'https://www.digital-finance-msca.com/our-people',
    'merged_date': '2025-12-02',
    'members': merged_members
}

with open(DATA_DIR / 'msca_members_merged.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(merged_members)} merged members")

# Also update msca_people_named.json format for the generator
people_named = {
    'people': [{'name': m['name'], 'filename': m['filename']} for m in merged_members]
}
with open(DATA_DIR / 'msca_people_named.json', 'w', encoding='utf-8') as f:
    json.dump(people_named, f, indent=2, ensure_ascii=False)

# Update bios with correct affiliations
bios_data['affiliations'] = {m['name']: m['affiliation'] for m in merged_members if m['affiliation']}
with open(DATA_DIR / 'msca_bios.json', 'w', encoding='utf-8') as f:
    json.dump(bios_data, f, indent=2, ensure_ascii=False)

print("Updated msca_people_named.json and msca_bios.json")
