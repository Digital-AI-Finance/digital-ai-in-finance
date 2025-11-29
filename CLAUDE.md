# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CCG (Connect & Collaborate Grant) application package for the "AI for Digital Finance: Swiss-MENA Research Network" workshop (April 21-23, 2026, American University of Sharjah, UAE). Leading House MENA grant application materials.

**Key Details:**
- Co-organizers: Prof. Joerg Osterrieder (FHGR) & Prof. Stephen Chan (AUS)
- Participants: 80-100 (60% academic, 40% industry)
- Budget: CHF 24,500 total (CHF 5,000 CCG request)

## Repository Structure

```
Digital_AI_in_Finance/
├── *_final.md/.docx          # Final application sections (5 documents)
├── *_reduced.md/.docx        # Condensed versions of application sections
├── *.tex                     # LaTeX/Beamer presentations and article documents
├── *.py                      # Python scripts for charts/visualizations
├── convert*.js               # Node.js scripts for markdown-to-Word conversion
├── temp/                     # LaTeX auxiliary files (.aux, .log, .out, .snm, .nav)
├── previous/                 # Version control for previous file versions
├── FinalSubmission/          # Final submission-ready materials (PDFs, Excel)
└── node_modules/             # docx library for Word document generation
```

## Build Commands

```powershell
# Compile LaTeX to PDF
pdflatex filename.tex

# Move auxiliary files after compilation
Move-Item -Path *.aux,*.log,*.out,*.snm,*.nav,*.toc -Destination temp -Force -ErrorAction SilentlyContinue

# Generate Gantt chart (outputs PNG, PDF, and Excel)
python gantt_chart_generator.py

# Generate budget spreadsheet
python create_budget.py

# Convert all markdown to Word (uses docx library)
node convert_all_to_word.js

# Convert specific sections
node convert_aims_objectives.js
node convert_format.js
node convert_timeline.js
node convert_partnership.js
node convert_project_overview.js
node convert_reduced_to_word.js
```

## Key Python Dependencies
- matplotlib, pandas (Gantt charts, data visualization)
- openpyxl (Excel generation)
- numpy (data processing)

## Node.js Dependencies
- docx (Word document generation with formatting)

## File Naming Convention

All files use `YYYYMMDD_HHMM_` prefix (e.g., `20241030_1700_workshop_program.tex`). Before updating a file, move the previous version to `previous/` folder.

## CCG Program Requirements

- Events/Workshops: CHF 5,000 maximum
- Work costs: Maximum 20% for UAS/UTE staff (current: 12%)
- Application deadline: 4+ months before activity
- Co-funding required from MENA partner
- Reference PDF: `LHMENA-CCG-2025 (3).pdf`

## LaTeX Document Types

### Beamer Presentations (*.tex with \documentclass[8pt,aspectratio=169]{beamer})
- Theme: Madrid
- Colors: maincolor (#404040), accentblue (#4682B4), lightgray (#F0F0F0)
- Uses tikz for simple timelines, pgfplots for bar charts
- Example: `20241030_1700_ccg_workshop_proposal.tex`

### Article Documents (*.tex with \documentclass[11pt,a4paper]{article})
- Uses fancyhdr for headers/footers
- Color scheme: headerblue (#003366)
- Includes qrcode package for QR codes
- Example: `workshop_program_2026.tex`

### Common LaTeX Practices
- After compilation: Move .aux, .log, .out, .snm, .nav files to temp/
- Charts: Python-generated PDFs preferred over TikZ for complex visualizations
- Simple charts (bar graphs, timelines): TikZ/pgfplots acceptable

## Word Document Conversion

The `convert*.js` scripts use the `docx` library to create formatted Word documents:
- Font: Arial, 11pt default
- Heading styles: Title (16pt), Heading1 (14pt), Heading2 (12pt)
- Margins: 1 inch (1440 twips) all sides
- Bullet lists with proper indentation

## Quality Standards

- No clichés (avoid "cutting-edge", "groundbreaking")
- Character limits: 5,000 characters for text sections
- Professional academic tone
- Timestamp all new files with YYYYMMDD_HHMM_ prefix
- Include character counts at end of content sections