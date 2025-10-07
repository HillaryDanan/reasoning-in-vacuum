#!/usr/bin/env python3
from scipy import stats

# Chance level
chance = 1/6  # 16.7%

# GPT-4: 6/20 correct
gpt4_result = stats.binomtest(6, 20, chance, alternative='greater')
print("="*60)
print("GPT-4: 30% (6/20 correct)")
print(f"vs chance (16.7%): p = {gpt4_result.pvalue:.4f}")
print(f"Significant? {'YES' if gpt4_result.pvalue < 0.05 else 'NO'}")
print()

# Claude: 2/20 correct
claude_result = stats.binomtest(2, 20, chance, alternative='greater')
print("Claude: 10% (2/20 correct)")
print(f"vs chance (16.7%): p = {claude_result.pvalue:.4f}")
print(f"Significant? {'YES (BELOW chance!)' if 2/20 < chance else 'NO'}")
print()

# Test if BELOW chance
claude_below = stats.binomtest(2, 20, chance, alternative='less')
print(f"Testing if BELOW chance: p = {claude_below.pvalue:.4f}")
print("="*60)
