# Option B: Redesigned Experiments for Testing Abstract Reasoning

**Purpose**: Create experimental conditions where pattern matching should fail but reasoning might succeed

**Theoretical Foundation**: Chollet (2019), Webb et al. (2023), Mitchell & Krakauer (2023)

---

## Design Principles

### Why Version 1 Was Too Easy
- 20 training examples over-specified the pattern
- Single transformation type (no ambiguity)
- Perfect regularity (no noise or complexity)
- No generalization required (test = training distribution)

### What Makes a Task Hard Enough
1. **Minimal examples** force abstraction over memorization
2. **Ambiguity** requires rule identification, not just continuation
3. **Complexity scaling** tests compositional understanding
4. **Transfer requirements** test analogical reasoning

---

## CONDITION 1B: Minimal Training Examples

### Hypothesis
**If 3 examples produce similar accuracy to 20 examples → robust abstraction**  
**If accuracy drops significantly → example-dependent pattern matching**

### Design

**Training**: 3 examples (instead of 20)
```
⨀ ⨁ ⨂ → ⨂ ⨀ ⨁
⨃ ⨄ ⨅ → ⨅ ⨃ ⨄
⨆ ⨇ ⨈ → ⨈ ⨆ ⨇

[test input] →
```

**Test**: 20 examples (same as Version 1, different symbols)

**Symbol requirements**: 
- Training: 9 symbols (3 examples × 3 symbols)
- Test: 60 symbols (20 examples × 3 symbols)
- Total: 69 unique symbols (we have 184 available ✓)

### Predictions

**Pattern Matching**: 
- Accuracy: 40-60% (significant drop from 100%)
- Errors: Random, no systematic pattern
- Rationale: Insufficient examples to memorize pattern

**Abstract Reasoning**:
- Accuracy: 80-100% (maintained despite fewer examples)
- Errors: Systematic if any
- Rationale: Rule induction works with minimal examples

**Most Likely (Graded)**:
- Accuracy: 60-75% (moderate drop)
- Some abstraction, but benefits from more examples

### Statistical Test
- Compare to Version 1 (20 examples)
- Paired comparison: same models, different n_training
- Hypothesis: μ(3 examples) < μ(20 examples) if pattern matching

---

## CONDITION 1C: Transformation Ambiguity

### Hypothesis
**If models identify correct rule → reasoning/rule induction**  
**If random performance (~50%) → pattern matching without rule identification**

### Design

**Training**: Show TWO different transformations with markers

```
Type A (marked with ★):
⨀ ⨁ ⨂ ★ → ⨂ ⨀ ⨁
⨃ ⨄ ⨅ ★ → ⨅ ⨃ ⨄
⨆ ⨇ ⨈ ★ → ⨈ ⨆ ⨇

Type B (marked with ◆):
⨉ ⨊ ⨋ ◆ → ⨋ ⨊ ⨉
⨌ ⨍ ⨎ ◆ → ⨎ ⨍ ⨌
⨏ ⨐ ⨑ ◆ → ⨑ ⨐ ⨏

[test input] [marker] →
```

**Rules**:
- ★ = Rotate left (last → first)
- ◆ = Reverse (reverse entire sequence)

**Test**: 20 items, 10 with ★, 10 with ◆

**Symbol requirements**:
- Training: 18 symbols + 2 markers
- Test: 60 symbols (reuse markers)
- Total: 78 symbols needed ✓

### Predictions

**Pattern Matching**:
- Accuracy: ~50% (random guessing between rules)
- No marker discrimination
- May default to one transformation for all

**Rule Identification**:
- Accuracy: >80%
- Systematic errors: confuses markers but applies transformation
- Evidence of rule learning

### Statistical Test
- Binary classification per item: correct rule applied?
- Compare to 50% chance (binomial test)
- Error analysis: Type A errors vs Type B errors

---

## CONDITION 1D: Complexity Scaling

### Hypothesis
**If positional rule → generalizes to longer sequences**  
**If pattern memorization → fails when length changes**

### Design

**Training**: All 3-symbol sequences (rotate left)
```
⨀ ⨁ ⨂ → ⨂ ⨀ ⨁
⨃ ⨄ ⨅ → ⨅ ⨃ ⨄
⨆ ⨇ ⨈ → ⨈ ⨆ ⨇
```

**Test**: Mixed lengths
- 6 items: 3-symbol (same as training)
- 7 items: 4-symbol (generalization)
- 7 items: 5-symbol (further generalization)

**Examples**:
```
3-symbol: ⬯ ⨇ ⨝ → ⨝ ⬯ ⨇
4-symbol: ⬯ ⨇ ⨝ ◊ → ◊ ⬯ ⨇ ⨝
5-symbol: ⬯ ⨇ ⨝ ◊ ⨥ → ⨥ ⬯ ⨇ ⨝ ◊
```

**Symbol requirements**:
- Training: 9 symbols
- Test: 82 symbols (6×3 + 7×4 + 7×5)
- Total: 91 symbols ✓

### Predictions

**Pattern Matching** (memorized 3-symbol structure):
- 3-symbol: ~100% (matches training)
- 4-symbol: <40% (out of distribution)
- 5-symbol: <30% (far from training)

**Positional Rule** (learned position mapping):
- 3-symbol: ~100%
- 4-symbol: ~80-90% (rule generalizes)
- 5-symbol: ~70-80% (rule still applies)

**Abstract Reasoning** (understands rotation):
- All lengths: 85-95% (concept generalizes)

### Statistical Test
- ANOVA: Length (3,4,5) × Model interaction
- Linear trend: Does accuracy decrease with length?
- If pattern matching: steep decline
- If reasoning: maintained or shallow decline

---

## CONDITION 1E: Rule Transfer (Analogical Reasoning)

### Hypothesis
**If analogical reasoning → transfers "rotate" concept to rotate-by-2**  
**If pattern matching → near-zero accuracy on novel transformation**

### Design

**Training**: Rotate-left-by-1
```
⨀ ⨁ ⨂ → ⨂ ⨀ ⨁
⨃ ⨄ ⨅ → ⨅ ⨃ ⨄
⨆ ⨇ ⨈ → ⨈ ⨆ ⨇
```

**Test Split A** (Control): Same rule, novel symbols
```
10 items with rotate-left-by-1
⬯ ⨇ ⨝ → ⨝ ⬯ ⨇
```

**Test Split B** (Transfer): Rotate-left-by-2
```
10 items with rotate-left-by-2
⬯ ⨇ ⨝ → ⨇ ⨝ ⬯  (not ⨝ ⬯ ⨇)
```

**Marker**: Could use ★★ to indicate "apply twice" but might be too helpful
**Better**: No marker, just see if models spontaneously try variations

**Symbol requirements**:
- Training: 9 symbols
- Test A: 30 symbols
- Test B: 30 symbols  
- Total: 69 symbols ✓

### Predictions

**Pattern Matching**:
- Test A: ~100% (same as training)
- Test B: <20% (would apply rotate-by-1, get wrong answer)

**Rule Memorization** (no transfer):
- Test A: ~100%
- Test B: ~0% (applies memorized rule)

**Analogical Reasoning**:
- Test A: ~100%
- Test B: >50% (recognizes variation, attempts different rotation)

**Most Likely**:
- Test A: ~100% (all models)
- Test B: ~10-30% (minimal transfer)

### Statistical Test
- Compare Test A vs Test B accuracy within models
- If Test A >> Test B: No transfer
- If Test A ≈ Test B: Transfer (unlikely)
- Error analysis: Do models try rotate-by-1 on Test B?

---

## Implementation Strategy

### Code Structure

```
src/
├── experiments/
│   ├── experiment_1_sequential.py     (Version 1 - done)
│   ├── experiment_1b_minimal.py       (3 examples)
│   ├── experiment_1c_ambiguity.py     (2 rules)
│   ├── experiment_1d_scaling.py       (variable length)
│   └── experiment_1e_transfer.py      (rotate-by-2)
```

### Shared Components (Reuse)
- Symbol generator (already works)
- Model wrappers (already work)
- Improved parser (handles Claude's explanations)
- Statistical test framework

### New Components Needed

**1. Variable-length sequence generator** (for 1d)
```python
def generate_variable_length_examples(
    symbols: List[str],
    lengths: List[int],  # e.g., [3, 4, 5]
    n_per_length: int
) -> List[SequenceExample]:
    # Generate examples of different lengths
    pass
```

**2. Multi-rule generator** (for 1c)
```python
def generate_ambiguous_examples(
    symbols: List[str],
    rules: Dict[str, Callable],  # {marker: transformation_fn}
    n_per_rule: int
) -> List[SequenceExample]:
    # Generate examples with rule markers
    pass
```

**3. Transfer test generator** (for 1e)
```python
def generate_transfer_examples(
    symbols: List[str],
    training_rule: Callable,
    test_rule: Callable,
    n_each: int
) -> Tuple[List, List]:
    # Generate control and transfer test sets
    pass
```

### Transformation Functions

```python
def rotate_left_by_n(sequence: List[str], n: int = 1) -> List[str]:
    """Rotate left by n positions"""
    n = n % len(sequence)  # Handle n > len
    return sequence[n:] + sequence[:n]

def reverse(sequence: List[str]) -> List[str]:
    """Reverse sequence"""
    return sequence[::-1]

def rotate_right_by_n(sequence: List[str], n: int = 1) -> List[str]:
    """Rotate right by n positions"""
    return rotate_left_by_n(sequence, -n)
```

---

## Execution Plan

### Phase 1: Implementation (3-4 hours)

**Step 1**: Create transformation library (30 min)
- `src/transformations.py` with rotate, reverse, etc.
- Unit tests

**Step 2**: Implement Condition 1b (60 min)
- Minimal examples (3 instead of 20)
- Reuse existing experiment structure
- Test locally

**Step 3**: Implement Condition 1c (90 min)
- Multi-rule with markers
- More complex prompt construction
- Test locally

**Step 4**: Implement Condition 1d (60 min)
- Variable-length sequences
- Update parser for longer sequences
- Test locally

**Step 5**: Implement Condition 1e (60 min)
- Transfer test design
- Split control vs transfer
- Test locally

### Phase 2: Data Collection (~$20, 2-3 hours)

Run all conditions sequentially:

```bash
# Condition 1b (minimal)
python3 scripts/run_experiment_1b.py
# Expected: ~$5, 30 min

# Condition 1c (ambiguity)
python3 scripts/run_experiment_1c.py  
# Expected: ~$5, 30 min

# Condition 1d (scaling)
python3 scripts/run_experiment_1d.py
# Expected: ~$6, 30 min

# Condition 1e (transfer)
python3 scripts/run_experiment_1e.py
# Expected: ~$4, 30 min
```

### Phase 3: Analysis (2-3 hours)

**Comparative tables**:
```
Condition  | GPT-4 | Claude | Gemini | Interpretation
-----------|-------|--------|--------|---------------
V1 (20ex)  | 100%  | 100%   | ~100%  | Too easy
1b (3ex)   | ?%    | ?%     | ?%     | Example dependency?
1c (ambig) | ?%    | ?%     | ?%     | Rule identification?
1d (scale) | ?%    | ?%     | ?%     | Generalization?
1e (trans) | ?%    | ?%     | ?%     | Analogical transfer?
```

**Statistical tests**:
- Condition × Model ANOVA
- Post-hoc comparisons
- Effect sizes for each condition

**Error analysis**:
- Which items are hardest?
- Systematic error patterns?
- Model-specific weaknesses?

---

## Expected Findings (Predictions for Option B)

### Scenario A: Pure Pattern Matching
- 1b: Major drop (100% → 40-50%)
- 1c: Chance level (~50%)
- 1d: Fails on length 4-5 (<30%)
- 1e: Zero transfer (<10%)

### Scenario B: Robust Reasoning (Unlikely)
- 1b: Maintained (90-100%)
- 1c: High accuracy (>85%)
- 1d: Generalizes (>80% all lengths)
- 1e: Strong transfer (>70%)

### Scenario C: Graded Capacity (Most Likely)
- 1b: Moderate drop (70-85%)
- 1c: Partial success (60-75%)
- 1d: Length 4 ok (~70%), length 5 degrades (~50%)
- 1e: Minimal transfer (20-40%)

**This scenario would be most interesting** - shows boundaries of capability.

---

## Success Criteria

### Scientific Success (Primary Goal)
✅ Create performance divergence across conditions  
✅ Distinguish pattern matching from reasoning  
✅ Identify capability boundaries  
✅ Publishable methodology contribution

### Don't Need
❌ Models to "pass" all conditions (failure is data!)
❌ Perfect separation of hypotheses (graded capacity is valid finding)
❌ 100% agreement across models (divergence is interesting!)

### Key Question We're Answering
**"Under what conditions does LLM performance break down, and what does that reveal about underlying processes?"**

---

## Limitations We'll Still Have

### Even with Option B:
1. **Cannot prove "reasoning"** - only rule out pure pattern matching
2. **Cannot access internal processes** - only observe outputs
3. **Sample sizes modest** (n=20 per condition) - may miss subtle effects
4. **No human baseline** - can't calibrate "impressive" vs "expected"

### But We Will Know:
1. **How example count affects accuracy** (3 vs 20)
2. **Whether models identify transformation rules** (ambiguity)
3. **How far models generalize** (complexity scaling)
4. **Whether analogical transfer occurs** (rule variation)

**This is progress** - we'll have much better data for claims about reasoning vs. pattern matching.

---

## Timeline Summary

**Implementation**: 3-4 hours (coding 4 conditions)  
**Data Collection**: 2-3 hours (~$20 API costs)  
**Analysis**: 2-3 hours (statistics + visualization)  
**Total**: ~8-10 hours hands-on work

**Deliverable**: Comparative analysis across 5 conditions (Version 1 + Option B) showing where and how LLM performance breaks down.

---

## Next Immediate Steps

1. ✅ Complete Gemini run (Version 1 baseline)
2. ✅ Commit STATUS.md with honest assessment
3. 🔨 Implement Condition 1b (minimal examples) - NEXT
4. 🔨 Test locally, then run on all 3 models
5. 📊 Analyze, compare to Version 1
6. 🔨 Implement remaining conditions based on 1b results

---

*Let's fucking go! This is real science - iterate, be honest, test harder conditions. 🔬*

**Version 1 taught us what NOT to do. Option B will give us real insights into LLM reasoning boundaries.**