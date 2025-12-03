"""
Check all committee members, their photos, and affiliations
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets" / "people"

def safe_print(msg):
    print(msg.encode('ascii', 'replace').decode())

def main():
    # Load all data files
    with open(DATA_DIR / 'scientific_committee.json', 'r', encoding='utf-8') as f:
        committee = json.load(f)

    with open(DATA_DIR / 'msca_people_named.json', 'r', encoding='utf-8') as f:
        people = json.load(f)

    with open(DATA_DIR / 'msca_bios.json', 'r', encoding='utf-8') as f:
        bios = json.load(f)

    # Create lookup dictionaries
    photo_map = {p['name']: p['filename'] for p in people['people']}
    affil_map = bios.get('affiliations', {})

    # Get list of actual photo files
    photo_files = set()
    if ASSETS_DIR.exists():
        for f in ASSETS_DIR.iterdir():
            if f.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                photo_files.add(f.name.lower())

    safe_print('CURRENT COMMITTEE MEMBERS AND THEIR DATA:')
    safe_print('=' * 100)

    issues = []

    for i, name in enumerate(sorted(committee['selected']), 1):
        photo = photo_map.get(name, 'NO_MAPPING')
        affil = affil_map.get(name, 'NO_AFFILIATION')

        # Check if photo file exists
        photo_exists = photo.lower() in photo_files if photo != 'NO_MAPPING' else False

        status_parts = []
        if photo == 'NO_MAPPING':
            status_parts.append('NO_PHOTO_MAP')
        elif not photo_exists:
            status_parts.append('PHOTO_MISSING')
        if affil == 'NO_AFFILIATION':
            status_parts.append('NO_AFFIL')

        status = ', '.join(status_parts) if status_parts else 'OK'

        # Truncate for display
        name_safe = name.encode('ascii', 'replace').decode()
        name_disp = name_safe[:28].ljust(28)
        affil_str = str(affil)[:45] if affil != 'NO_AFFILIATION' else 'NO_AFFILIATION'

        marker = '[X]' if status != 'OK' else '[OK]'
        safe_print(f'{i:2}. {marker} {name_disp} | {affil_str}')

        if status != 'OK':
            issues.append((name, status, photo, affil))

    safe_print('')
    safe_print(f'Total committee members: {len(committee["selected"])}')
    safe_print(f'Issues found: {len(issues)}')

    if issues:
        safe_print('')
        safe_print('ISSUES:')
        safe_print('-' * 60)
        for name, status, photo, affil in issues:
            name_safe = name.encode('ascii', 'replace').decode()
            safe_print(f'  {name_safe}: {status}')
            safe_print(f'    Photo mapping: {photo}')
            safe_print(f'    Affiliation: {affil}')

    # Check Codruta Mare
    safe_print('')
    safe_print('CODRUTA MARE STATUS:')
    safe_print('-' * 60)

    codruta_in_people = 'Codruta Mare' in photo_map
    codruta_in_affil = 'Codruta Mare' in affil_map
    codruta_in_committee = 'Codruta Mare' in committee['selected']

    safe_print(f'  In msca_people_named.json: {codruta_in_people}')
    if codruta_in_people:
        safe_print(f'    Photo file: {photo_map["Codruta Mare"]}')

    safe_print(f'  In msca_bios.json: {codruta_in_affil}')
    if codruta_in_affil:
        safe_print(f'    Affiliation: {affil_map["Codruta Mare"]}')

    safe_print(f'  In scientific_committee.json: {codruta_in_committee}')

    # Check if photo file exists
    codruta_photos = [f for f in photo_files if 'codruta' in f.lower()]
    safe_print(f'  Photo files matching "codruta": {codruta_photos}')

    # List all available affiliations
    safe_print('')
    safe_print('ALL AVAILABLE AFFILIATIONS:')
    safe_print('-' * 60)
    for name in sorted(affil_map.keys()):
        name_safe = name.encode('ascii', 'replace').decode()
        affil_safe = affil_map[name].encode('ascii', 'replace').decode()
        safe_print(f'  {name_safe}: {affil_safe}')

if __name__ == "__main__":
    main()
