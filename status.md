# Reasoning in Vacuum - Experimental Results

**Last Updated**: October 7, 2025  
**Experiment**: Sequential Transformation Rule Induction  
**Status**: Complete (5 conditions tested)

---

## Experimental Conditions

### Version 1: Abundant Training Examples
- **Training**: 20 examples of rotate-left transformation
- **Test**: 20 novel sequences (disjoint symbol set)
- **GPT-4**: 100% (20/20 correct)
- **Claude 3.5**: 100% (20/20 correct)
- **Statistical test**: Both p < 0.001 vs. chance (16.7%)

### Version 1b: Minimal Training Examples
- **Training**: 3 examples of rotate-left transformation
- **Test**: 20 novel sequences (same test set as V1)
- **GPT-4**: 30% (6/20 correct), p = 0.102 vs. chance
- **Claude 3.5**: 10% (2/20 correct), p = 0.870 vs. chance
- **Result**: Neither significantly above chance level (16.7%)

### Condition 1c: Transformation Ambiguity
- **Training**: 6 examples (3 rotate-left marked with ★, 3 reverse marked with ◆)
- **Test**: 20 sequences requiring correct rule identification
- **GPT-4**: 65% (13/20 correct), p = 0.132 vs. chance (50%)
- **Claude 3.5**: 45% (9/20 correct), p = 0.824 vs. chance
- **Result**: Neither significantly above chance level

### Condition 1d: Complexity Scaling
- **Training**: 3 examples of 3-symbol sequences
- **Test**: Mixed lengths (7x 3-symbol, 7x 4-symbol, 6x 5-symbol)
- **GPT-4**: 45% (9/20 correct)
- **Claude 3.5**: 10% (2/20 correct)
- **Result**: Poor performance across all sequence lengths

### Condition 1e: Rule Transfer
- **Training**: 3 examples of rotate-by-1
- **Test**: 10 control (rotate-by-1), 10 transfer (rotate-by-2)
- **GPT-4 Control**: 10% (1/10 correct)
- **GPT-4 Transfer**: 90% (9/10 correct)
- **Claude 3.5**: 5% overall (1/20 correct)
- **Interpretation**: GPT-4 systematically applied wrong rotation amount (rotate-by-2 instead of rotate-by-1)

---

## Summary Across Conditions

| Condition | Training Examples | GPT-4 | Claude | Chance | Significant? |
|-----------|------------------|-------|--------|--------|--------------|
| V1 | 20 | 100% | 100% | 16.7% | Yes |
| V1b | 3 | 30% | 10% | 16.7% | No |
| 1c | 6 (2 rules) | 65% | 45% | 50.0% | No |
| 1d | 3 (varied length) | 45% | 10% | varies | Poor |
| 1e (control) | 3 | 10% | 0% | 16.7% | At/below chance |
| 1e (transfer) | 3 | 90% | 10% | 16.7% | Misapplication |

**Pattern**: Only Version 1 with 20 identical examples produced above-chance performance. All appropriately calibrated conditions (1b-1e) showed chance-level or poor performance.

---

## Key Findings

### 1. Example-Dependency
- Performance dropped from 100% (20 examples) to 30%/10% (3 examples)
- 70-90 percentage point decrease for both models

### 2. Chance-Level Performance
- Version 1b, 1c: Neither model significantly above chance baseline
- Statistical tests: all p > 0.10

### 3. Systematic Misapplication (Condition 1e)
- GPT-4 learned "rotation" as concept but wrong parameter (rotate-by-2 vs rotate-by-1)
- Applied incorrect transformation consistently (90% on transfer items)
- Failed on control items requiring correct transformation (10%)

### 4. No Robust Model Differences
- Both models showed similar collapse patterns
- No significant architectural advantages detected

---

## Technical Details

**Models tested**: 
- GPT-4 (gpt-4-0125-preview)
- Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)

**Materials**: Unicode symbols from U+2A00-U+2AFF, U+2B00-U+2BFF ranges (documented <100 co-occurrences in Common Crawl)

**Design**: Completely disjoint training/test symbol sets (zero overlap)

**Statistical tests**: Binomial tests vs. chance baseline, α = 0.05

---

## Data Files

```
data/
├── experiments/
│   ├── exp1_examples.json          # V1: 20 training + 20 test
│   ├── exp1b_examples.json         # V1b: 3 training + 20 test
│   ├── exp1c_examples.json         # 1c: 6 training (2 rules) + 20 test
│   ├── exp1d_examples.json         # 1d: 3 training + 20 test (varied length)
│   └── exp1e_examples.json         # 1e: 3 training + 20 test (control/transfer)
└── results/
    └── raw/
        ├── exp1_main_gpt-4_*.json
        ├── exp1_main_claude_*.json
        ├── exp1b_*.json
        ├── exp1c_*.json
        ├── exp1d_*.json
        └── exp1e_*.json
```

---

## Cost Summary

- Version 1: ~$6
- Version 1b: ~$3
- Condition 1c: ~$3
- Condition 1d: ~$2
- Condition 1e: ~$1
- **Total**: ~$15

---

*Last updated: October 7, 2025*  
*All experiments complete*