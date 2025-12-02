"""
Verification script for Scientific Committee data
Cross-references all data sources against MSCA Digital Finance website
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets" / "people"

def load_json(filename):
    """Load JSON file from data directory"""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def list_photo_files():
    """List all photo files in assets/people"""
    if not ASSETS_DIR.exists():
        return []
    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    photos = []
    for f in ASSETS_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in extensions:
            photos.append(f.name)
    return sorted(photos)

def name_to_filename(name):
    """Convert name to expected filename format"""
    import re
    # Normalize special characters
    name = name.lower()
    # Remove accents manually for common cases
    replacements = {
        'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u',
        'n': 'n', 'c': 'c', "'": "_", "-": "_", ".": "", ",": ""
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    # Replace non-alphanumeric with underscore
    name = re.sub(r'[^a-z0-9]', '_', name)
    # Remove multiple underscores
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    return name + '.jpg'

def main():
    print("=" * 80)
    print("SCIENTIFIC COMMITTEE DATA VERIFICATION REPORT")
    print("=" * 80)
    print()

    # Load all data sources
    print("1. LOADING DATA SOURCES")
    print("-" * 40)

    scientific_committee = load_json("scientific_committee.json")
    msca_members_correct = load_json("msca_members_correct.json")
    msca_people_named = load_json("msca_people_named.json")
    msca_bios = load_json("msca_bios.json")

    print(f"   scientific_committee.json: {len(scientific_committee.get('selected', [])) if scientific_committee else 0} members")
    print(f"   msca_members_correct.json: {len(msca_members_correct.get('members', [])) if msca_members_correct else 0} members")
    print(f"   msca_people_named.json: {len(msca_people_named.get('people', [])) if msca_people_named else 0} members")
    print(f"   msca_bios.json affiliations: {len(msca_bios.get('affiliations', {})) if msca_bios else 0}")
    print()

    # Get photo files
    photo_files = list_photo_files()
    print(f"   Photo files in assets/people: {len(photo_files)}")
    print()

    # Build master data structure
    print("2. CROSS-REFERENCING DATA")
    print("-" * 40)

    # Get all unique names from all sources
    all_names = set()

    if scientific_committee:
        all_names.update(scientific_committee.get('selected', []))

    if msca_members_correct:
        for m in msca_members_correct.get('members', []):
            all_names.add(m['name'])

    if msca_people_named:
        for p in msca_people_named.get('people', []):
            all_names.add(p['name'])

    if msca_bios:
        all_names.update(msca_bios.get('affiliations', {}).keys())

    print(f"   Total unique names found: {len(all_names)}")
    print()

    # Build member data
    members_data = {}
    for name in all_names:
        members_data[name] = {
            'in_committee': False,
            'has_photo_mapping': False,
            'photo_file': None,
            'photo_exists': False,
            'affiliation': None,
            'bio': None
        }

    # Mark committee members
    if scientific_committee:
        for name in scientific_committee.get('selected', []):
            if name in members_data:
                members_data[name]['in_committee'] = True

    # Add photo mappings
    if msca_people_named:
        for p in msca_people_named.get('people', []):
            name = p['name']
            if name in members_data:
                members_data[name]['has_photo_mapping'] = True
                members_data[name]['photo_file'] = p['filename']

    # Add affiliations
    if msca_bios:
        for name, affil in msca_bios.get('affiliations', {}).items():
            if name in members_data:
                members_data[name]['affiliation'] = affil
        for name, bio in msca_bios.get('bios', {}).items():
            if name in members_data:
                members_data[name]['bio'] = bio

    # Check if photos exist
    photo_files_lower = {f.lower(): f for f in photo_files}
    for name, data in members_data.items():
        if data['photo_file']:
            photo_lower = data['photo_file'].lower()
            if photo_lower in photo_files_lower:
                data['photo_exists'] = True

    # Generate reports
    print("3. COMMITTEE MEMBER STATUS")
    print("-" * 40)

    committee_members = [(n, d) for n, d in members_data.items() if d['in_committee']]
    committee_members.sort(key=lambda x: x[0])

    issues_found = []

    for name, data in committee_members:
        status = []
        has_issue = False

        if not data['has_photo_mapping']:
            status.append("NO PHOTO MAPPING")
            has_issue = True
        elif not data['photo_exists']:
            status.append(f"PHOTO MISSING: {data['photo_file']}")
            has_issue = True
        else:
            status.append("Photo OK")

        if not data['affiliation']:
            status.append("NO AFFILIATION")
            has_issue = True
        else:
            status.append(f"Affil: {data['affiliation'][:40]}...")

        name_safe = name.encode('ascii', 'replace').decode()
        if has_issue:
            issues_found.append((name_safe, status))
            print(f"   [X] {name_safe}")
            for s in status:
                print(f"       - {s}")
        else:
            print(f"   [OK] {name_safe}: {data['affiliation'][:50] if data['affiliation'] else 'N/A'}...")

    print()

    # Summary
    print("4. VERIFICATION SUMMARY")
    print("-" * 40)

    total_committee = len(committee_members)
    with_photos = sum(1 for _, d in committee_members if d['photo_exists'])
    with_affiliations = sum(1 for _, d in committee_members if d['affiliation'])

    print(f"   Total committee members: {total_committee}")
    print(f"   With valid photos: {with_photos}/{total_committee}")
    print(f"   With affiliations: {with_affiliations}/{total_committee}")
    print(f"   Issues found: {len(issues_found)}")
    print()

    # List issues
    if issues_found:
        print("5. ISSUES REQUIRING ATTENTION")
        print("-" * 40)
        for name, status in issues_found:
            print(f"   {name}:")
            for s in status:
                print(f"      - {s}")
        print()

    # Photo file analysis
    print("6. PHOTO FILE ANALYSIS")
    print("-" * 40)

    # Named photos vs generic photos
    named_photos = [f for f in photo_files if not f.startswith('person_')]
    generic_photos = [f for f in photo_files if f.startswith('person_')]

    print(f"   Named photos (e.g., joerg_osterrieder.jpg): {len(named_photos)}")
    print(f"   Generic photos (e.g., person_01.jpg): {len(generic_photos)}")
    print()

    # List named photos
    print("   Named photos available:")
    for p in sorted(named_photos)[:20]:
        print(f"      - {p}")
    if len(named_photos) > 20:
        print(f"      ... and {len(named_photos) - 20} more")
    print()

    # Cross-check: photos without committee mapping
    mapped_photos = set()
    for _, data in members_data.items():
        if data['photo_file']:
            mapped_photos.add(data['photo_file'].lower())

    unmapped_named = [p for p in named_photos if p.lower() not in mapped_photos]
    if unmapped_named:
        print("   Named photos not mapped to any member:")
        for p in unmapped_named[:10]:
            print(f"      - {p}")
        if len(unmapped_named) > 10:
            print(f"      ... and {len(unmapped_named) - 10} more")

    print()
    print("=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)

    # Return status
    return len(issues_found) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
