#!/usr/bin/env python3
from scipy import stats

# Chance level for rule identification
chance = 0.50  # 50% (random between two rules)

# GPT-4: 13/20 correct
gpt4_result = stats.binomtest(13, 20, chance, alternative='greater')
print("="*60)
print("EXPERIMENT 1C: AMBIGUITY (Rule Identification)")
print("="*60)
print(f"\nGPT-4: 65% (13/20 correct)")
print(f"vs chance (50%): p = {gpt4_result.pvalue:.4f}")
print(f"Significant at α=0.05? {'YES' if gpt4_result.pvalue < 0.05 else 'NO'}")

# Claude: 9/20 correct  
claude_result = stats.binomtest(9, 20, chance, alternative='two-sided')
print(f"\nClaude: 45% (9/20 correct)")
print(f"vs chance (50%): p = {claude_result.pvalue:.4f}")
print(f"Different from chance? {'YES' if claude_result.pvalue < 0.05 else 'NO'}")

# Test difference between models
from scipy.stats import fisher_exact
contingency = [[13, 7], [9, 11]]  # [correct, incorrect] for each model
_, p_diff = fisher_exact(contingency)
print(f"\nGPT-4 vs Claude difference: p = {p_diff:.4f}")
print(f"Significant? {'YES' if p_diff < 0.05 else 'NO'}")
print("="*60)
