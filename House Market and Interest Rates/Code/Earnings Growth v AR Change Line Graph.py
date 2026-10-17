"""Line chart"""

import pandas as pd
import matplotlib.pyplot as plt

"""1.Loading Data"""

# Load data
df = pd.read_excel('AWE-AR Cleaned Data.xlsx')

# Filter to 2005-2024 (excluding 2004 which has no data)
df = df[df['Year'] >= 2005]

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))

"""2. The data added to the line chart"""

years = df['Year']

# Create line graph
ax.plot(years, df['Earnings Growth (%)'], marker='o', linewidth=2,
        label='Earnings Growth (%)', color='steelblue')
ax.plot(years, df['Ratio Change'], marker='s', linewidth=2,
        label='Affordability Ratio Change', color='coral')

# Zero reference line
ax.axhline(y=0, color='black', linewidth=0.8)

"""3. Labelling"""

# Labels
ax.set_xlabel('Year')
ax.set_ylabel('Change')
ax.set_title('Earnings Growth vs Affordability Ratio Change (2005-2024)')

# X-axis: show all years
ax.set_xticks(years)
ax.set_xticklabels(years.astype(int), rotation=45, ha='right')

# Legend with 2004 warning note
ax.legend(title='⚠ For 2004: No recorded data (N/A)', title_fontsize=9, loc='upper left')

# Grid
ax.grid(axis='y', linestyle='--', alpha=0.5)


plt.tight_layout()
plt.savefig('earnings_vs_affordability_clean.png', dpi=300)
plt.show()