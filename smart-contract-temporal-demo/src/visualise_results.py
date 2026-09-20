import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load results
results = pd.read_csv('results/temporal_evaluation_static.csv')

print("Creating visualizations...")

# Create figure with 2 subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: F1-Score across periods
ax = axes[0]
periods = results['Period']
f1_scores = results['F1-Score']

colors = ['#2ecc71', '#f39c12', '#e74c3c']
ax.bar(range(len(periods)), f1_scores, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('F1-Score', fontsize=12, fontweight='bold')
ax.set_xlabel('Time Period', fontsize=12, fontweight='bold')
ax.set_title('Detector Performance Across Time Periods', fontsize=13, fontweight='bold')
ax.set_xticks(range(len(periods)))
ax.set_xticklabels(['Old\n(0.4.x)', 'Medium\n(0.5.x)', 'New\n(0.8.x)'], fontsize=11)
ax.set_ylim([0.8, 1.05])
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for i, v in enumerate(f1_scores):
    ax.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Plot 2: Precision and Recall comparison
ax = axes[1]
x = np.arange(len(periods))
width = 0.35

precision = results['Precision']
recall = results['Recall']

bars1 = ax.bar(x - width/2, precision, width, label='Precision', color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, recall, width, label='Recall', color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_ylabel('Score', fontsize=12, fontweight='bold')
ax.set_xlabel('Time Period', fontsize=12, fontweight='bold')
ax.set_title('Precision vs Recall Across Periods', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(['Old\n(0.4.x)', 'Medium\n(0.5.x)', 'New\n(0.8.x)'], fontsize=11)
ax.set_ylim([0.8, 1.05])
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/temporal_robustness_results.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/temporal_robustness_results.png")
plt.close()

print("\nResults Summary:")
print(results.to_string(index=False))