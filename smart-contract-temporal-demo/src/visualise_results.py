# 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load results
results = pd.read_csv('results/temporal_evaluation_static.csv')

print("Creating improved visualization...")

# Create figure with better styling
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Smart Contract Vulnerability Detector - Temporal Robustness', 
             fontsize=16, fontweight='bold', y=1.02)

# ===== CHART 1: F1-Score Degradation =====
ax = axes[0]

periods = results['Period']
f1_scores = results['F1-Score']

# Better colors that show degradation
colors = ['#27ae60', '#f39c12', '#e74c3c']  # Green → Orange → Red
x_pos = np.arange(len(periods))
width = 0.6

bars = ax.bar(x_pos, f1_scores, width=width, color=colors, alpha=0.85, 
              edgecolor='black', linewidth=2)

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, f1_scores)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
            f'{val:.3f}',
            ha='center', va='bottom', fontweight='bold', fontsize=13)

# Add degradation line
if len(f1_scores) > 1:
    ax.plot(x_pos, f1_scores, 'k--', linewidth=2.5, alpha=0.6, marker='o', markersize=10)

ax.set_ylabel('F1-Score', fontsize=12, fontweight='bold')
ax.set_xlabel('Time Period (Solidity Version)', fontsize=12, fontweight='bold')
ax.set_title('F1-Score Degradation Over Time', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x_pos)
ax.set_xticklabels(['Period Old\n(0.4.x)\n2015-2017', 
                    'Period Medium\n(0.5.x)\n2017-2019',
                    'Period New\n(0.8.x)\n2020-2024'], fontsize=11)
ax.set_ylim([0.4, 1.05])
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add degradation annotation
degradation_pct = (f1_scores.iloc[0] - f1_scores.iloc[-1]) / f1_scores.iloc[0] * 100
ax.text(1, 0.5, f'Degradation: {degradation_pct:.1f}%', 
        fontsize=11, ha='center',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.4, pad=0.8))

# ===== CHART 2: Precision vs Recall =====
ax = axes[1]

x = np.arange(len(periods))
width = 0.35

precision = results['Precision']
recall = results['Recall']

bars1 = ax.bar(x - width/2, precision, width, label='Precision', 
               color='#3498db', alpha=0.85, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, recall, width, label='Recall', 
               color='#e74c3c', alpha=0.85, edgecolor='black', linewidth=1.5)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Score', fontsize=12, fontweight='bold')
ax.set_xlabel('Time Period (Solidity Version)', fontsize=12, fontweight='bold')
ax.set_title('Precision vs Recall Across Periods', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(['Period Old\n(0.4.x)\n2015-2017', 
                    'Period Medium\n(0.5.x)\n2017-2019',
                    'Period New\n(0.8.x)\n2020-2024'], fontsize=11)
ax.set_ylim([0.4, 1.05])
ax.legend(fontsize=11, loc='upper right')
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('results/temporal_robustness_results_improved.png', dpi=300, bbox_inches='tight')
print("✓ Saved improved visualization: results/temporal_robustness_results_improved.png")
plt.show()

# Print summary
print("\n" + "="*60)
print("PERFORMANCE SUMMARY")
print("="*60)
print(results.to_string(index=False))
print("\n" + "="*60)