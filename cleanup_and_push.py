"""
Cleanup script for Digital_AI_in_Finance repository
- Archives non-essential files
- Keeps FinalSubmission and key source files
- Creates new private GitHub repo and pushes
"""

import os
import shutil
from pathlib import Path

# Configuration
BASE_DIR = Path(r"D:\Joerg\Research\slides\Digital_AI_in_Finance")
ARCHIVE_DIR = BASE_DIR / "archive"
REPO_NAME = "digital-ai-in-finance"
ORG_NAME = "Digital-AI-Finance"

# Files/folders to KEEP in main repo (not archive)
KEEP_ITEMS = {
    "FinalSubmission",           # Submitted files - most important
    "CLAUDE.md",                 # Project instructions
    ".claude",                   # Claude settings
    "cleanup_and_push.py",       # This script
    ".git",                      # Git folder if exists
    ".gitignore",                # Git ignore
    "README.md",                 # If exists
}

# Files to completely DELETE (not archive)
DELETE_ITEMS = {
    "node_modules",              # npm packages - can be reinstalled
    "temp",                      # LaTeX temp files
    ".snm",                      # Beamer temp files
}

def create_archive_structure():
    """Create archive folder structure"""
    subfolders = [
        "drafts",                # Draft markdown and docx files
        "presentations",         # Beamer/LaTeX presentations
        "scripts",               # Python and JS conversion scripts
        "charts",                # Gantt charts and visualizations
        "budget",                # Budget spreadsheets
        "templates",             # Letter templates
    ]

    for folder in subfolders:
        (ARCHIVE_DIR / folder).mkdir(parents=True, exist_ok=True)

    print(f"Created archive structure in {ARCHIVE_DIR}")

def categorize_file(filename):
    """Determine which archive subfolder a file belongs to"""
    name = filename.lower()

    if name.endswith('.js') or name.endswith('.py'):
        return "scripts"
    elif name.endswith('.tex'):
        return "presentations"
    elif 'gantt' in name or 'chart' in name:
        return "charts"
    elif 'budget' in name:
        return "budget"
    elif 'template' in name or 'letter' in name:
        return "templates"
    elif name.endswith(('.md', '.docx')):
        return "drafts"
    elif name.endswith(('.pdf', '.xlsx', '.png')):
        # Check content type
        if 'gantt' in name or 'chart' in name:
            return "charts"
        elif 'budget' in name:
            return "budget"
        else:
            return "drafts"
    else:
        return "drafts"

def cleanup_files():
    """Move files to archive or delete as appropriate"""

    # First, delete items we don't want
    for item_name in DELETE_ITEMS:
        for item in BASE_DIR.glob(f"**/{item_name}"):
            if item.exists():
                if item.is_dir():
                    print(f"Deleting directory: {item}")
                    shutil.rmtree(item)
                else:
                    print(f"Deleting file: {item}")
                    item.unlink()

    # Also delete .snm files
    for snm_file in BASE_DIR.glob("*.snm"):
        print(f"Deleting: {snm_file}")
        snm_file.unlink()

    # Create archive structure
    create_archive_structure()

    # Move files to archive
    for item in BASE_DIR.iterdir():
        if item.name in KEEP_ITEMS:
            print(f"Keeping: {item.name}")
            continue

        if item.name == "archive":
            continue

        if item.is_file():
            category = categorize_file(item.name)
            dest = ARCHIVE_DIR / category / item.name
            print(f"Archiving: {item.name} -> archive/{category}/")
            shutil.move(str(item), str(dest))
        elif item.is_dir():
            # Move entire directory to archive/drafts
            dest = ARCHIVE_DIR / "drafts" / item.name
            print(f"Archiving directory: {item.name} -> archive/drafts/")
            shutil.move(str(item), str(dest))

def create_readme():
    """Create a README.md for the repository"""
    readme_content = """# AI for Digital Finance: Swiss-MENA Research Network

## Overview

CCG (Connect & Collaborate Grant) application materials for the "AI for Digital Finance: Swiss-MENA Research Network" workshop.

- **Event**: April 21-23, 2026
- **Location**: American University of Sharjah, UAE
- **Co-organizers**: Prof. Joerg Osterrieder (FHGR) & Prof. Stephen Chan (AUS)

## Submitted Materials

The `FinalSubmission/` folder contains the official submitted documents:

| File | Description |
|------|-------------|
| `proposal_ai-in-digital-finance.pdf` | Main CCG application proposal |
| `workshop_program_2026.pdf` | Detailed 3-day workshop program |
| `lhmena-ccg-2025-budget_table-ai-for-digital-finance.xlsx` | Budget breakdown |
| `gannt_chart.pdf` | Project timeline visualization |
| `osterrieder_cv.pdf` | CV - Prof. Joerg Osterrieder |
| `cv_chan_stephen.pdf` | CV - Prof. Stephen Chan |

## Budget Summary

- **Total Project Cost**: CHF 24,500
- **CCG Request**: CHF 5,000 (20.4%)
- **AUS Co-funding**: CHF 5,000 (20.4%)
- **Other Sources**: CHF 14,500 (59.2%)

## Workshop Focus

- AI/ML Technologies in Finance
- Large Language Models (LLMs)
- Explainable AI for Compliance
- Blockchain Security and Fraud Detection
- Digital Banking Innovation

## Archive

The `archive/` folder contains working drafts, scripts, and intermediate files used during application preparation.

## Contact

- Prof. Joerg Osterrieder: joerg.osterrieder@fhgr.ch
- Prof. Stephen Chan: schan@aus.edu
"""

    readme_path = BASE_DIR / "README.md"
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"Created: {readme_path}")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Node modules
node_modules/

# LaTeX temp files
*.aux
*.log
*.out
*.snm
*.nav
*.toc
*.synctex.gz
temp/

# Python
__pycache__/
*.pyc
.venv/

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
"""

    gitignore_path = BASE_DIR / ".gitignore"
    gitignore_path.write_text(gitignore_content, encoding='utf-8')
    print(f"Created: {gitignore_path}")

def show_final_structure():
    """Display the final repository structure"""
    print("\n" + "="*50)
    print("FINAL REPOSITORY STRUCTURE:")
    print("="*50)

    for item in sorted(BASE_DIR.iterdir()):
        if item.name.startswith('.'):
            continue
        if item.is_dir():
            print(f"  {item.name}/")
            for subitem in sorted(item.iterdir()):
                if subitem.is_dir():
                    count = len(list(subitem.iterdir()))
                    print(f"    {subitem.name}/ ({count} files)")
                else:
                    print(f"    {subitem.name}")
        else:
            print(f"  {item.name}")

def main():
    print("="*50)
    print("Digital_AI_in_Finance Cleanup Script")
    print("="*50)

    # Step 1: Cleanup and archive
    print("\n[1/3] Cleaning up and archiving files...")
    cleanup_files()

    # Step 2: Create README and .gitignore
    print("\n[2/3] Creating README.md and .gitignore...")
    create_readme()
    create_gitignore()

    # Step 3: Show final structure
    print("\n[3/3] Final structure:")
    show_final_structure()

    print("\n" + "="*50)
    print("Cleanup complete!")
    print("="*50)
    print("\nNext steps (run manually):")
    print(f"  cd {BASE_DIR}")
    print("  git init")
    print(f"  gh repo create {ORG_NAME}/{REPO_NAME} --private")
    print(f"  git remote add origin https://github.com/{ORG_NAME}/{REPO_NAME}.git")
    print("  git add .")
    print('  git commit -m "Initial commit: CCG application materials"')
    print("  git push -u origin main")

if __name__ == "__main__":
    main()
