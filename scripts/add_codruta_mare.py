"""
Add Codruta Mare to all data files
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def main():
    # Codruta Mare's data
    name = "Codruta Mare"
    affiliation = "Babes-Bolyai University, Romania"
    photo_file = "codruta_mare.jpg"
    bio = "Researcher at Babes-Bolyai University. Member of the MSCA Digital Finance network, focusing on AI applications in finance."

    print(f"Adding {name} to all data files...")
    print(f"  Affiliation: {affiliation}")
    print(f"  Photo: {photo_file}")

    # 1. Add to scientific_committee.json
    sc_path = DATA_DIR / "scientific_committee.json"
    with open(sc_path, 'r', encoding='utf-8') as f:
        sc_data = json.load(f)

    if name not in sc_data['selected']:
        sc_data['selected'].append(name)
        sc_data['selected'].sort()
        sc_data['total_selected'] = len(sc_data['selected'])
        with open(sc_path, 'w', encoding='utf-8') as f:
            json.dump(sc_data, f, indent=2, ensure_ascii=False)
        print(f"  Added to scientific_committee.json (now {sc_data['total_selected']} members)")
    else:
        print(f"  Already in scientific_committee.json")

    # 2. Add to msca_people_named.json
    pn_path = DATA_DIR / "msca_people_named.json"
    with open(pn_path, 'r', encoding='utf-8') as f:
        pn_data = json.load(f)

    existing_names = [p['name'] for p in pn_data['people']]
    if name not in existing_names:
        pn_data['people'].append({
            'name': name,
            'filename': photo_file
        })
        with open(pn_path, 'w', encoding='utf-8') as f:
            json.dump(pn_data, f, indent=2, ensure_ascii=False)
        print(f"  Added to msca_people_named.json")
    else:
        print(f"  Already in msca_people_named.json")

    # 3. Add to msca_bios.json
    bios_path = DATA_DIR / "msca_bios.json"
    with open(bios_path, 'r', encoding='utf-8') as f:
        bios_data = json.load(f)

    if name not in bios_data.get('affiliations', {}):
        bios_data['affiliations'][name] = affiliation
        with open(bios_path, 'w', encoding='utf-8') as f:
            json.dump(bios_data, f, indent=2, ensure_ascii=False)
        print(f"  Added affiliation to msca_bios.json")
    else:
        print(f"  Already has affiliation in msca_bios.json")

    if name not in bios_data.get('bios', {}):
        bios_data['bios'][name] = bio
        with open(bios_path, 'w', encoding='utf-8') as f:
            json.dump(bios_data, f, indent=2, ensure_ascii=False)
        print(f"  Added bio to msca_bios.json")
    else:
        print(f"  Already has bio in msca_bios.json")

    # 4. Add to msca_members_correct.json
    mc_path = DATA_DIR / "msca_members_correct.json"
    with open(mc_path, 'r', encoding='utf-8') as f:
        mc_data = json.load(f)

    existing_names = [m['name'] for m in mc_data['members']]
    if name not in existing_names:
        mc_data['members'].append({
            'name': name,
            'affiliation': '',
            'bio': '',
            'filename': photo_file
        })
        with open(mc_path, 'w', encoding='utf-8') as f:
            json.dump(mc_data, f, indent=2, ensure_ascii=False)
        print(f"  Added to msca_members_correct.json")
    else:
        print(f"  Already in msca_members_correct.json")

    print()
    print("Done! Codruta Mare has been added to all data files.")

if __name__ == "__main__":
    main()
