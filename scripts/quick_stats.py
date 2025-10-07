#!/usr/bin/env python3
import json
from scipy import stats
import numpy as np

# Load GPT-4 results
with open('data/results/raw/exp1_main_gpt-4-0125-preview_20251006_100608.json', 'r') as f:
    data = json.load(f)

n_correct = data['n_correct']
n_total = data['n_total']
accuracy = data['accuracy']

# Chance level for exact match: 1/6 for 3-position rotation
chance = 1/6

# Binomial test: Is observed accuracy different from chance?
# Use binomtest (new API) instead of deprecated binom_test
result = stats.binomtest(n_correct, n_total, chance, alternative='greater')
p_value = result.pvalue

print("="*60)
print("STATISTICAL TEST: GPT-4 vs Chance Performance")
print("="*60)
print(f"Observed: {n_correct}/{n_total} correct ({accuracy:.1%})")
print(f"Chance level: {chance:.1%}")
print(f"Binomial test p-value: {p_value:.2e}")
print(f"Significant at α=0.05? {'YES' if p_value < 0.05 else 'NO'}")
print("="*60)

# Effect size (Cohen's h for proportions)
observed_prop = accuracy
chance_prop = chance
h = 2 * (np.arcsin(np.sqrt(observed_prop)) - np.arcsin(np.sqrt(chance_prop)))
print(f"\nEffect size (Cohen's h): {h:.2f}")
if abs(h) > 1.2:
    interp = "Huge (h > 1.2)"
elif abs(h) > 0.8:
    interp = "Large (h > 0.8)"
elif abs(h) > 0.5:
    interp = "Medium (h > 0.5)"
else:
    interp = "Small (h < 0.5)"
print(f"Interpretation: {interp}")
print("="*60)
