"""
Interactive selection of Scientific Committee members from MSCA people

Run this script to go through each person one-by-one and decide
whether to include them in the Scientific Committee.
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets" / "people"

# Institution names to skip (not people)
INSTITUTIONS = {
    'Babes-Bolyai University', 'Bifroest University', 'Cardo AI',
    'Deloitte Consulting', 'Deutsche Bank', 'Deutsche Boerse',
    'European Central Bank', 'Fraunhofer Institute', 'LPA Group',
    'Raiffeisen Bank International AG', 'Sun Yat-sen University',
    'Swedbank AB', 'TED University'
}


def load_data():
    """Load scraped people data"""
    with open(DATA_DIR / 'msca_people.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def save_selection(selected):
    """Save selected committee members"""
    with open(DATA_DIR / 'scientific_committee.json', 'w', encoding='utf-8') as f:
        json.dump(selected, f, indent=2, ensure_ascii=False)
    print(f"\nSelection saved to {DATA_DIR / 'scientific_committee.json'}")


def display_person_info(name, index, total):
    """Display person information"""
    print("\n" + "=" * 60)
    print(f"[{index}/{total}] {name}")
    print("=" * 60)

    # Try to find if there's an image
    # (Note: We have images but no direct name-to-image mapping yet)

    print("\nInclude in Scientific Committee?")
    print("  [y] Yes - include")
    print("  [n] No - skip")
    print("  [q] Quit and save progress")
    print("  [a] Add all remaining (auto-yes)")
    print("  [s] Skip all remaining (auto-no)")


def main():
    print("Scientific Committee Selection")
    print("=" * 60)
    print("Go through each person from the MSCA Digital Finance network")
    print("and decide who to include in the Scientific Committee.")
    print("=" * 60)

    # Load data
    data = load_data()
    names = data.get('potential_names', [])

    # Filter out institution names
    people = [n for n in names if n not in INSTITUTIONS]

    print(f"\nTotal people to review: {len(people)}")
    print("(Filtered out institution names)")

    # Check for existing progress
    selection_file = DATA_DIR / 'scientific_committee.json'
    selected = []
    skipped = []
    start_index = 0

    if selection_file.exists():
        try:
            with open(selection_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            if existing.get('selected') or existing.get('skipped'):
                print(f"\nFound existing selection:")
                print(f"  - Selected: {len(existing.get('selected', []))}")
                print(f"  - Skipped: {len(existing.get('skipped', []))}")

                resume = input("\nResume from where you left off? [y/n]: ").strip().lower()
                if resume == 'y':
                    selected = existing.get('selected', [])
                    skipped = existing.get('skipped', [])
                    # Find where to resume
                    reviewed = set(selected + skipped)
                    for i, name in enumerate(people):
                        if name not in reviewed:
                            start_index = i
                            break
                    else:
                        print("\nAll people have been reviewed!")
                        return
        except:
            pass

    input("\nPress Enter to start reviewing...")

    auto_mode = None  # 'yes' or 'no' for auto-selection

    for i, name in enumerate(people[start_index:], start=start_index + 1):
        if name in set(selected + skipped):
            continue

        if auto_mode == 'yes':
            selected.append(name)
            print(f"[{i}/{len(people)}] {name} -> AUTO-SELECTED")
            continue
        elif auto_mode == 'no':
            skipped.append(name)
            print(f"[{i}/{len(people)}] {name} -> AUTO-SKIPPED")
            continue

        display_person_info(name, i, len(people))

        while True:
            choice = input("\nYour choice: ").strip().lower()

            if choice == 'y':
                selected.append(name)
                print(f"  -> Added to committee")
                break
            elif choice == 'n':
                skipped.append(name)
                print(f"  -> Skipped")
                break
            elif choice == 'q':
                print("\nSaving progress...")
                save_selection({
                    'selected': selected,
                    'skipped': skipped,
                    'total_reviewed': len(selected) + len(skipped),
                    'total_people': len(people)
                })
                return
            elif choice == 'a':
                print("\nAuto-selecting all remaining...")
                auto_mode = 'yes'
                selected.append(name)
                break
            elif choice == 's':
                print("\nAuto-skipping all remaining...")
                auto_mode = 'no'
                skipped.append(name)
                break
            else:
                print("Invalid choice. Please enter y, n, q, a, or s")

    # Save final selection
    save_selection({
        'selected': selected,
        'skipped': skipped,
        'total_reviewed': len(selected) + len(skipped),
        'total_people': len(people),
        'completed': True
    })

    print("\n" + "=" * 60)
    print("Selection Complete!")
    print("=" * 60)
    print(f"Selected for Scientific Committee: {len(selected)}")
    print(f"Skipped: {len(skipped)}")

    if selected:
        print("\nSelected members:")
        for name in selected:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
