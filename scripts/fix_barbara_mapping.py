"""Fix Barbara Bedowska-Sojka name mapping across all data files"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def safe_print(msg):
    """Print with ASCII encoding to avoid console errors"""
    print(msg.encode('ascii', 'replace').decode())

def main():
    # The correct ASCII-safe name to use consistently
    correct_name = "Barbara Bedowska-Sojka"
    photo_file = "barbara_b_dowska_s_jka.jpg"
    affiliation = "Poznan University of Economics and Business, Poland"

    # Check photo exists
    photo_path = BASE_DIR / "assets" / "people" / photo_file
    if photo_path.exists():
        safe_print(f"Photo exists: {photo_file}")
    else:
        # Check for alternative
        for f in (BASE_DIR / "assets" / "people").iterdir():
            if 'barbara' in f.name.lower():
                safe_print(f"Found alternative: {f.name}")
                photo_file = f.name
                break

    # Update scientific_committee.json
    sc_path = DATA_DIR / "scientific_committee.json"
    with open(sc_path, 'r', encoding='utf-8') as f:
        sc_data = json.load(f)

    # Replace any Barbara variant with correct name
    new_selected = []
    barbara_found = False
    for name in sc_data['selected']:
        if 'barbara' in name.lower() or 'bedowska' in name.lower():
            new_selected.append(correct_name)
            barbara_found = True
            safe_print(f"Updated scientific_committee: '{name}' -> '{correct_name}'")
        else:
            new_selected.append(name)

    sc_data['selected'] = new_selected
    with open(sc_path, 'w', encoding='utf-8') as f:
        json.dump(sc_data, f, indent=2, ensure_ascii=False)

    # Update msca_people_named.json
    pn_path = DATA_DIR / "msca_people_named.json"
    with open(pn_path, 'r', encoding='utf-8') as f:
        pn_data = json.load(f)

    for person in pn_data['people']:
        if 'barbara' in person['name'].lower() or 'bedowska' in person['name'].lower():
            old_name = person['name']
            person['name'] = correct_name
            safe_print(f"Updated msca_people_named: '{old_name}' -> '{correct_name}'")

    with open(pn_path, 'w', encoding='utf-8') as f:
        json.dump(pn_data, f, indent=2, ensure_ascii=False)

    # Update msca_members_correct.json
    mc_path = DATA_DIR / "msca_members_correct.json"
    with open(mc_path, 'r', encoding='utf-8') as f:
        mc_data = json.load(f)

    for member in mc_data['members']:
        if 'barbara' in member['name'].lower() or 'bedowska' in member['name'].lower():
            old_name = member['name']
            member['name'] = correct_name
            safe_print(f"Updated msca_members_correct: '{old_name}' -> '{correct_name}'")

    with open(mc_path, 'w', encoding='utf-8') as f:
        json.dump(mc_data, f, indent=2, ensure_ascii=False)

    # Update msca_bios.json - add affiliation
    bios_path = DATA_DIR / "msca_bios.json"
    with open(bios_path, 'r', encoding='utf-8') as f:
        bios_data = json.load(f)

    # Remove any old Barbara key and add new one
    old_keys = [k for k in bios_data.get('affiliations', {}) if 'barbara' in k.lower() or 'bedowska' in k.lower()]
    for k in old_keys:
        del bios_data['affiliations'][k]
        safe_print(f"Removed old affiliation key: {k}")

    bios_data['affiliations'][correct_name] = affiliation
    safe_print(f"Added affiliation: {correct_name} -> {affiliation}")

    with open(bios_path, 'w', encoding='utf-8') as f:
        json.dump(bios_data, f, indent=2, ensure_ascii=False)

    safe_print("\nAll files updated successfully!")
    safe_print(f"Name: {correct_name}")
    safe_print(f"Photo: {photo_file}")
    safe_print(f"Affiliation: {affiliation}")

if __name__ == "__main__":
    main()
