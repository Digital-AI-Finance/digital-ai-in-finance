import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Set up the figure with A4 landscape dimensions
fig, ax = plt.subplots(figsize=(16.5, 11.7), dpi=100)

# Define color scheme - professional blue gradients
colors = {
    'Administrative': '#E6F3FF',  # Light blue
    'Academic': '#99CCFF',        # Medium blue
    'Marketing/Outreach': '#4D94FF',  # Dark blue
    'Logistics': '#0056B3',       # Navy blue
    'Milestone': '#FFD700',       # Gold for milestones
    'Critical': '#FF6B6B'         # Red accent for critical path
}

# Define tasks with start dates, durations, categories, and responsibilities
tasks_data = [
    # Administrative tasks
    {'Task': 'CCG Application Submission', 'Start': '2024-12-01', 'Duration': 15, 'Category': 'Administrative',
     'Responsible': 'Osterrieder/Chan', 'Critical': False},
    {'Task': 'CCG Review Period', 'Start': '2024-12-15', 'Duration': 60, 'Category': 'Administrative',
     'Responsible': 'Leading House', 'Critical': True},
    {'Task': 'Committee Formation', 'Start': '2024-12-20', 'Duration': 30, 'Category': 'Administrative',
     'Responsible': 'Both', 'Critical': False},

    # Academic tasks
    {'Task': 'Call for Papers Draft', 'Start': '2025-01-15', 'Duration': 20, 'Category': 'Academic',
     'Responsible': 'Both', 'Critical': False},
    {'Task': 'Call for Papers Launch', 'Start': '2025-02-15', 'Duration': 10, 'Category': 'Academic',
     'Responsible': 'FHGR', 'Critical': True},
    {'Task': 'Paper Submission Period', 'Start': '2025-03-01', 'Duration': 180, 'Category': 'Academic',
     'Responsible': 'Authors', 'Critical': False},
    {'Task': 'Paper Review Process', 'Start': '2025-09-01', 'Duration': 30, 'Category': 'Academic',
     'Responsible': 'Committee', 'Critical': True},
    {'Task': 'Paper Notifications', 'Start': '2025-10-01', 'Duration': 10, 'Category': 'Academic',
     'Responsible': 'Chan', 'Critical': False},
    {'Task': 'Final Program Development', 'Start': '2025-10-15', 'Duration': 45, 'Category': 'Academic',
     'Responsible': 'Both', 'Critical': True},

    # Marketing/Outreach tasks
    {'Task': 'Website Development', 'Start': '2025-01-10', 'Duration': 40, 'Category': 'Marketing/Outreach',
     'Responsible': 'Both', 'Critical': False},
    {'Task': 'Website Launch', 'Start': '2025-02-20', 'Duration': 5, 'Category': 'Marketing/Outreach',
     'Responsible': 'FHGR', 'Critical': False},
    {'Task': 'Marketing Campaign', 'Start': '2025-03-01', 'Duration': 390, 'Category': 'Marketing/Outreach',
     'Responsible': 'Both', 'Critical': False},
    {'Task': 'Registration Opens', 'Start': '2025-03-15', 'Duration': 370, 'Category': 'Marketing/Outreach',
     'Responsible': 'AUS', 'Critical': False},
    {'Task': 'Speaker Invitations', 'Start': '2025-02-15', 'Duration': 365, 'Category': 'Marketing/Outreach',
     'Responsible': 'Osterrieder', 'Critical': True},
    {'Task': 'Registration Drive', 'Start': '2026-01-01', 'Duration': 105, 'Category': 'Marketing/Outreach',
     'Responsible': 'Both', 'Critical': True},

    # Logistics tasks
    {'Task': 'Venue Arrangements', 'Start': '2025-02-01', 'Duration': 60, 'Category': 'Logistics',
     'Responsible': 'Chan/AUS', 'Critical': False},
    {'Task': 'Catering Planning', 'Start': '2026-01-15', 'Duration': 90, 'Category': 'Logistics',
     'Responsible': 'AUS', 'Critical': False},
    {'Task': 'Materials Preparation', 'Start': '2026-02-01', 'Duration': 75, 'Category': 'Logistics',
     'Responsible': 'Both', 'Critical': False},
    {'Task': 'Technical Setup', 'Start': '2026-03-01', 'Duration': 45, 'Category': 'Logistics',
     'Responsible': 'Technical Team', 'Critical': True},
    {'Task': 'Final Preparations', 'Start': '2026-04-01', 'Duration': 20, 'Category': 'Logistics',
     'Responsible': 'All Teams', 'Critical': True},

    # Workshop execution
    {'Task': 'Workshop Execution', 'Start': '2026-04-21', 'Duration': 3, 'Category': 'Administrative',
     'Responsible': 'All', 'Critical': True},

    # Post-workshop
    {'Task': 'Proceedings Publication', 'Start': '2026-05-01', 'Duration': 60, 'Category': 'Academic',
     'Responsible': 'Both', 'Critical': False},
    {'Task': 'Final Reporting', 'Start': '2026-06-01', 'Duration': 30, 'Category': 'Administrative',
     'Responsible': 'Osterrieder', 'Critical': False},
    {'Task': 'Network Activation', 'Start': '2026-05-15', 'Duration': 60, 'Category': 'Administrative',
     'Responsible': 'Network Committee', 'Critical': False},
]

# Define milestones
milestones = [
    {'Name': 'CCG Approval', 'Date': '2025-02-15', 'Symbol': 'D'},
    {'Name': 'Speakers Confirmed', 'Date': '2026-03-15', 'Symbol': 'D'},
    {'Name': '80 Participants', 'Date': '2026-04-15', 'Symbol': 'D'},
    {'Name': 'MoU Signing', 'Date': '2026-04-23', 'Symbol': 'D'},
]

# Convert to DataFrame
df = pd.DataFrame(tasks_data)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = df['Start'] + pd.to_timedelta(df['Duration'], unit='D')

# Sort by start date and category
df = df.sort_values(['Category', 'Start'])
df = df.reset_index(drop=True)

# Create the plot
fig.patch.set_facecolor('white')
ax.set_facecolor('#FAFAFA')

# Plot tasks
for idx, task in df.iterrows():
    start = task['Start']
    end = task['End']

    # Select color based on category
    color = colors[task['Category']]

    # Create rectangle for task
    if task['Critical']:
        # Critical path with bold border
        rect = FancyBboxPatch((mdates.date2num(start), idx - 0.4),
                              mdates.date2num(end) - mdates.date2num(start), 0.8,
                              boxstyle="round,pad=0.02",
                              facecolor=color, edgecolor='#333333', linewidth=2.5,
                              alpha=0.9)
    else:
        rect = FancyBboxPatch((mdates.date2num(start), idx - 0.4),
                              mdates.date2num(end) - mdates.date2num(start), 0.8,
                              boxstyle="round,pad=0.02",
                              facecolor=color, edgecolor='#666666', linewidth=1,
                              alpha=0.8)
    ax.add_patch(rect)

    # Add task name on the left
    ax.text(mdates.date2num(start) - 5, idx, task['Task'],
            va='center', ha='right', fontsize=9, fontweight='normal')

    # Add responsible party in the bar if space permits
    bar_width = mdates.date2num(end) - mdates.date2num(start)
    if bar_width > 30:  # Only add text if bar is wide enough
        ax.text(mdates.date2num(start) + bar_width/2, idx,
                f"({task['Responsible']})",
                va='center', ha='center', fontsize=7, color='white', fontweight='bold')

# Add dependencies for paper workflow
paper_tasks = df[df['Task'].isin(['Call for Papers Launch', 'Paper Review Process', 'Final Program Development'])]
for i in range(len(paper_tasks) - 1):
    task1 = paper_tasks.iloc[i]
    task2 = paper_tasks.iloc[i + 1]

    # Draw arrow from end of task1 to start of task2
    ax.annotate('', xy=(mdates.date2num(task2['Start']), task2.name),
                xytext=(mdates.date2num(task1['End']), task1.name),
                arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=1.5, alpha=0.6))

# Add milestones
for milestone in milestones:
    date = pd.to_datetime(milestone['Date'])
    y_pos = len(df) + 0.5

    # Add vertical line
    ax.axvline(x=mdates.date2num(date), color='#FFD700', linestyle='--', alpha=0.5, linewidth=1)

    # Add diamond marker
    ax.scatter(mdates.date2num(date), y_pos, s=150, marker='D',
              color=colors['Milestone'], edgecolor='#333333', linewidth=1.5, zorder=5)

    # Add milestone label
    ax.text(mdates.date2num(date), y_pos + 0.8, milestone['Name'],
           rotation=45, ha='left', va='bottom', fontsize=9, fontweight='bold')

# Format x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator())

# Set axis limits
ax.set_xlim(mdates.date2num(datetime(2024, 11, 15)), mdates.date2num(datetime(2026, 8, 1)))
ax.set_ylim(-1, len(df) + 2)

# Remove y-axis ticks
ax.set_yticks([])

# Grid
ax.grid(True, axis='x', alpha=0.3, linestyle=':', color='gray')

# Labels and title
ax.set_xlabel('Timeline', fontsize=12, fontweight='bold')
ax.set_title('AI for Digital Finance Workshop - Implementation Timeline\nSwiss-MENA Research Network Launch',
            fontsize=16, fontweight='bold', pad=20)

# Rotate x-axis labels
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Create legend
legend_elements = [
    mpatches.Rectangle((0, 0), 1, 1, fc=colors['Administrative'], ec='black', label='Administrative'),
    mpatches.Rectangle((0, 0), 1, 1, fc=colors['Academic'], ec='black', label='Academic'),
    mpatches.Rectangle((0, 0), 1, 1, fc=colors['Marketing/Outreach'], ec='black', label='Marketing/Outreach'),
    mpatches.Rectangle((0, 0), 1, 1, fc=colors['Logistics'], ec='black', label='Logistics'),
    mpatches.Rectangle((0, 0), 1, 1, fc='white', ec='black', linewidth=2.5, label='Critical Path'),
    plt.scatter([], [], marker='D', s=100, c=colors['Milestone'], edgecolor='black', label='Milestone')
]

ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98),
         ncol=3, frameon=True, fancybox=True, shadow=True, fontsize=9)

# Add subtitle with key dates
subtitle = "Key Dates: Application Dec 2024 | Approval Feb 2025 | Workshop Apr 21-23, 2026 | Network Launch Apr 23, 2026"
fig.text(0.5, 0.02, subtitle, ha='center', fontsize=10, style='italic', color='#555555')

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(left=0.25, right=0.98, top=0.93, bottom=0.08)

# Save outputs
print("Generating Gantt chart outputs...")
plt.savefig('workshop_timeline_gantt.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('workshop_timeline_gantt.pdf', format='pdf', bbox_inches='tight', facecolor='white')
print("PNG saved: workshop_timeline_gantt.png")
print("PDF saved: workshop_timeline_gantt.pdf")

# Also save the data to Excel
df_export = df[['Task', 'Start', 'End', 'Duration', 'Category', 'Responsible', 'Critical']]
df_export.to_excel('gantt_data.xlsx', index=False)
print("Data saved: gantt_data.xlsx")

# Don't show the plot interactively (just save files)
# plt.show()

print("\nGantt chart generation complete!")