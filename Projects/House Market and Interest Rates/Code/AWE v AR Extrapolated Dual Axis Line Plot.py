"""Dual axis line plot with projections to 2028"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

"""1. Load and filter data"""

df = pd.read_excel('AWE-AR Cleaned Data.xlsx')
df = df[(df['Year'] >= 2004) & (df['Year'] <= 2024)]

"""2. Projection calculations"""

recent_years = df[df['Year'] >= 2020]
awe_values = recent_years['AWE Annual Average (Index) from 2004'].values
awe_growth_rates = [(awe_values[i] - awe_values[i-1]) / awe_values[i-1] * 100 
                    for i in range(1, len(awe_values))]
avg_awe_growth = np.mean(awe_growth_rates)
slope_ar, intercept_ar, _, _, _ = stats.linregress(df['Year'], df['Affordability Ratio Annual Median'])
future_years = [2025, 2026, 2027, 2028]
last_awe = df['AWE Annual Average (Index) from 2004'].iloc[-1]
last_ar = df['Affordability Ratio Annual Median'].iloc[-1]

projected_awe = []
projected_ar = []

for i, year in enumerate(future_years):
    awe_proj = last_awe * ((1 + avg_awe_growth/100) ** (i + 1))
    projected_awe.append(awe_proj)
    ar_proj = slope_ar * year + intercept_ar
    projected_ar.append(ar_proj)


proj_years_full = [2024] + future_years
proj_awe_full = [last_awe] + projected_awe
proj_ar_full = [last_ar] + projected_ar

"""3. Create plot"""

fig, ax1 = plt.subplots(figsize=(16, 8))

color1 = 'steelblue'
color2 = 'darkred'

"""4. AWE Index"""

ax1.set_xlabel('Year', fontsize=13, fontweight='bold')
ax1.set_ylabel('AWE Index (2004 = 100)', color=color1, fontsize=13, fontweight='bold')
ax1.plot(df['Year'], df['AWE Annual Average (Index) from 2004'], 
         marker='o', color=color1, linewidth=3, label='AWE Index (Actual)', 
         markersize=8, markeredgecolor='white', markeredgewidth=2)
ax1.plot(proj_years_full, proj_awe_full, 
         marker='o', color=color1, linewidth=3, linestyle='--', 
         label='AWE Index (Projected)', markersize=8, 
         markeredgecolor='white', markeredgewidth=2, alpha=0.7)
ax1.fill_between(df['Year'], df['AWE Annual Average (Index) from 2004'], 
                 alpha=0.2, color=color1)
ax1.fill_between(proj_years_full, proj_awe_full, 
                 alpha=0.15, color=color1)

ax1.tick_params(axis='y', labelcolor=color1, labelsize=11)
ax1.grid(True, alpha=0.3, linestyle='--', linewidth=1)
ax1.set_axisbelow(True)
ax1.set_ylim(bottom=90)

"""5. Affordability Ratio"""

ax2 = ax1.twinx()
ax2.set_ylabel('Affordability Ratio (House Price/Earnings)', color=color2, fontsize=13, fontweight='bold')
ax2.plot(df['Year'], df['Affordability Ratio Annual Median'], 
         marker='s', color=color2, linewidth=3, label='Affordability Ratio (Actual)', 
         markersize=8, markeredgecolor='white', markeredgewidth=2)
ax2.plot(proj_years_full, proj_ar_full, 
         marker='s', color=color2, linewidth=3, linestyle='--',
         label='Affordability Ratio (Projected)', markersize=8, 
         markeredgecolor='white', markeredgewidth=2, alpha=0.7)
ax2.fill_between(df['Year'], df['Affordability Ratio Annual Median'], 
                 alpha=0.1, color=color2)
ax2.fill_between(proj_years_full, proj_ar_full, 
                 alpha=0.08, color=color2)

ax2.tick_params(axis='y', labelcolor=color2, labelsize=10)
ax2.set_ylim(bottom=5)

"""6. Graph """

ax1.axvline(x=2024, color='gray', linestyle=':', linewidth=2, alpha=0.7)
ax1.text(2024.2, ax1.get_ylim()[1] * 0.95, 'Projection →', fontsize=10, color='gray')
ax1.set_xlim(2004, 2028)
ax1.set_xticks(range(2004, 2029, 1))
ax1.tick_params(axis='x', rotation=45, labelsize=10)
plt.title('Average Weekly Earnings vs Housing Affordability (2004-2028)\nWith Projections Assuming No Economic Crisis', 
          fontsize=16, fontweight='bold', pad=20)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11, 
           framealpha=0.9, shadow=True, fancybox=True)
textstr = 'Projections based on:\n• AWE: 5-year average growth rate (5.87%)\n• Affordability: Linear trend'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax1.text(0.98, 0.03, textstr, transform=ax1.transAxes, fontsize=10,
         verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.show()