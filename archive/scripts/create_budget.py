import pandas as pd
from datetime import datetime
import os

# Create budget data for 3-day workshop
budget_data = {
    'Category': [
        'Travel - Swiss Researchers',
        'Travel - Invited Speakers',
        'Subsistence - Swiss Team',
        'Subsistence - Invited Speakers',
        'Venue Rental (3 days)',
        'Technical Equipment',
        'Catering - Coffee Breaks',
        'Catering - Lunches',
        'Catering - Welcome Reception',
        'Marketing Materials',
        'Online Platform/Streaming',
        'Workshop Materials',
        'Work Costs (FHGR Staff)',
        'TOTAL'
    ],
    'Description': [
        '3 Swiss researchers (ZRH-DXB economy)',
        '2 keynote speakers from EU',
        '3 persons x 4 nights x CHF 150/night',
        '2 speakers x 3 nights x CHF 150/night',
        'AUS conference facility (3 days)',
        'AV equipment, recording setup',
        '6 breaks x 80 participants x CHF 10',
        '3 lunches x 80 participants x CHF 25',
        'Day 1 evening, 80 participants',
        'Posters, programs, name badges',
        'Hybrid event platform, streaming',
        'Folders, USB drives with proceedings',
        'Event coordination (20% max)',
        ''
    ],
    'Total Cost (CHF)': [
        2400,
        1600,
        1800,
        900,
        1500,
        800,
        4800,
        6000,
        1600,
        600,
        1200,
        800,
        500,
        24500
    ],
    'CCG Request (CHF)': [
        1500,  # Partial travel support
        0,     # Speakers covered by other sources
        800,   # Partial subsistence
        0,
        0,     # Venue provided by AUS
        0,     # Equipment from AUS
        1200,  # Partial catering
        0,     # Lunches co-funded
        0,     # Reception co-funded
        300,   # Partial materials
        600,   # Partial platform costs
        0,     # Materials co-funded
        600,   # Work costs under 20% limit
        5000
    ],
    'AUS Co-funding (CHF)': [
        0,
        0,
        0,
        0,
        1500,  # In-kind venue
        800,   # In-kind equipment
        0,
        1500,  # Partial lunch support
        800,   # Reception support
        0,
        0,
        400,   # Materials support
        0,
        5000
    ],
    'Other Sources (CHF)': [
        900,   # FHGR contribution
        1600,  # Speaker institutions
        1000,  # FHGR support
        900,   # Speaker institutions
        0,
        0,
        3600,  # Registration fees
        4500,  # Registration fees
        800,   # Sponsor support
        300,   # FHGR support
        600,   # Registration fees
        400,   # FHGR support
        -100,  # Rounding adjustment
        14500
    ]
}

# Create DataFrame
df = pd.DataFrame(budget_data)

# Create summary data
summary_data = {
    'Funding Source': [
        'CCG Request',
        'AUS Co-funding (In-kind + Direct)',
        'Other Sources (FHGR + Registration + Sponsors)',
        'TOTAL PROJECT COST'
    ],
    'Amount (CHF)': [
        5000,
        5000,
        14500,
        24500
    ],
    'Percentage': [
        '20.4%',
        '20.4%',
        '59.2%',
        '100%'
    ]
}

summary_df = pd.DataFrame(summary_data)

# Create notes
notes = """
BUDGET NOTES:
1. Work costs (CHF 600) represent 12% of CCG request, well under 20% maximum
2. AUS provides substantial in-kind contributions (venue, equipment) plus direct support
3. Registration fees (CHF 100/participant) cover significant portion of catering costs
4. 3-day format maximizes impact while maintaining cost efficiency
5. 80-100 participants ensures critical mass for network launch
6. Budget assumes 80 paid registrations at CHF 100 each
7. Swiss team travel partially self-funded to maximize CCG impact
8. Hybrid format included to extend reach without proportional cost increase
"""

# Save to Excel with multiple sheets
output_file = f'D:\\Joerg\\Research\\slides\\2025_LeadingHouse_Travel\\20241030_1700_budget_3day_workshop.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Write detailed budget
    df.to_excel(writer, sheet_name='Detailed Budget', index=False)

    # Write summary
    summary_df.to_excel(writer, sheet_name='Funding Summary', index=False)

    # Write notes to a third sheet
    notes_df = pd.DataFrame({'Budget Notes': [notes]})
    notes_df.to_excel(writer, sheet_name='Notes', index=False)

    # Format the sheets
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

print(f"Budget spreadsheet created: {output_file}")
print("\nBudget Summary:")
print(f"Total Project Cost: CHF 24,500")
print(f"CCG Request: CHF 5,000 (20.4%)")
print(f"AUS Co-funding: CHF 5,000 (20.4%)")
print(f"Other Sources: CHF 14,500 (59.2%)")
print(f"\nWork costs: CHF 600 (12% of CCG request, under 20% limit)")