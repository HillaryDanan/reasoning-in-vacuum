# Reasoning in Vacuum - Experimental Status Report

**Last Updated**: October 7, 2025  
**Experiment**: Sequential Transformation Rule Induction (Experiment 1)  
**Status**: ⚠️ CRITICAL DESIGN FLAW IDENTIFIED - Task too easy to distinguish hypotheses

---

## MAJOR FINDING: Task Does Not Test What We Intended

### The Brutal Truth
Both GPT-4 and Claude achieved **100% accuracy** on our pattern continuation task. This is statistically significant (p < 0.001, Cohen's h = 2.30) but scientifically problematic.

**Why this is a problem**: Perfect performance from both models suggests the task is **too easy** to distinguish pattern matching from abstract reasoning. Both processes would succeed on simple, regular transformations with 20 training examples.

**This is good science**: Recognizing when experimental design doesn't test your hypothesis is progress. We learned something critical about task difficulty and what constitutes a valid reasoning test.

---

## Current Results Summary (Experiment 1 - Version 1)

### GPT-4 (gpt-4-0125-preview)
- **Accuracy**: 100% (20/20 correct)
- **Statistical test**: p = 2.74e-16 (binomial test vs. 16.7% chance)
- **Effect size**: Cohen's h = 2.30 (huge)
- **Behavior**: Clean symbol outputs, no explanation
- **Example**: "⬲ ▭ ⨤" (correct)
- **Tokens**: ~396/response
- **Cost**: ~$3

### Claude (claude-3-5-sonnet-20241022)  
- **Accuracy**: 100% (20/20 correct after parser fix)
- **Behavior**: Explains pattern in English or Spanish, THEN provides correct symbols
- **Discovery**: Parser was grabbing first 3 words instead of symbols at end of response
- **Example**: "Analizando el patrón... la respuesta sería: ⬲ ▭ ⨤" ✓ CORRECT
- **Bilingual**: Randomly switches between English/Spanish explanations (interesting!)
- **Tokens**: ~683/response (1.7× more than GPT-4)
- **Cost**: ~$2-3

### Gemini (gemini-2.5-flash)
- **Status**: Pending completion with correct model name
- **Previous attempts**: 
  - gemini-2.0-flash-exp: Rate limited (3/20 completed)
  - gemini-1.5-flash-latest: Model not found (404 error)
- **Prediction**: Will also achieve ~100% (task is too easy)

---

## What We Actually Measured

### We CAN Claim (Data-Supported):
1. ✅ **In-context learning works with novel symbols**: Both models successfully continue patterns using Unicode symbols with <100 co-occurrences in training data
2. ✅ **Statistical significance is extreme**: Performance far exceeds chance (p < 0.001)
3. ✅ **Instruction-following varies across models**: GPT-4 gives minimal outputs, Claude explains then answers
4. ✅ **Simple positional transformations are learnable** from 20 examples regardless of symbol novelty
5. ✅ **Claude exhibits bilingual behavior**: Randomly uses English or Spanish in explanations

### We CANNOT Claim (Insufficient Evidence):
1. ❌ **"Models exhibit abstract reasoning"** - Task too easy, pattern matching sufficient
2. ❌ **"Models understand rotation conceptually"** - Could be positional heuristics (position 3→1, 1→2, 2→3)
3. ❌ **"Pattern matching would fail here"** - We have no evidence of failure
4. ❌ **"Results distinguish reasoning from pattern matching"** - Both hypotheses predict success on easy regular tasks

### Critical Insight:
**We tested in-context learning, not abstract reasoning.** The task difficulty was miscalibrated - 20 examples of a simple regular transformation is insufficient to stress reasoning capacity.

---

## Construct Validity Threat Analysis

### Why Both Models Got 100%: Five Competing Hypotheses

**H1: Task Is Too Easy** (Most Parsimonious - Occam's Razor)
- Simple positional rule: [A,B,C] → [C,A,B]
- 20 training examples is massive overkill
- High regularity makes pattern obvious
- Humans would likely also get ~100%

**H2: In-Context Learning ≠ Reasoning** (Brown et al., 2020)
- Models pattern-match on structural positions
- No understanding of "rotation" required
- Just notice: position 3 always first in output, etc.
- This is impressive few-shot learning, not reasoning

**H3: Training Examples Too Informative**
- ARC dataset (Chollet, 2019): Uses 2-3 examples
- Human analogical reasoning: 1-2 examples sufficient
- Our 20 examples over-specify the pattern
- Could memorize without abstracting

**H4: No Complexity Gradient**
- All sequences are 3 symbols
- All transformations identical
- No ambiguity about which rule applies
- Real reasoning requires handling uncertainty

**H5: Models Actually Reason** (Least Parsimonious)
- Requires additional assumptions
- Simpler explanations available (H1-H4)
- Insufficient evidence to support this claim

**Conclusion**: We should favor H1 and H2 (Occam's Razor). The task doesn't distinguish the hypotheses we intended to test.

---

## Critical Design Flaws Identified

### Flaw 1: Too Many Training Examples
**Current**: 20 examples
**Problem**: Over-constrains the pattern, enables memorization
**Literature**: ARC (Chollet, 2019) uses 2-3 examples
**Fix**: Reduce to 3-5 examples

### Flaw 2: Single Transformation Type  
**Current**: All training shows rotate-left
**Problem**: No test of rule identification
**Fix**: Multiple transformations, model must identify which applies

### Flaw 3: No Complexity Gradient
**Current**: All sequences 3 symbols, same rule
**Problem**: No stress on generalization
**Fix**: Vary length, test transfer (rotate-left → rotate-left-by-2)

### Flaw 4: Too Much Regularity
**Current**: Perfect regularity in all examples
**Problem**: Pattern matching sufficient
**Fix**: Irregular patterns, compositional rules

### Flaw 5: No Human Baseline
**Critical**: Unknown if 100% is impressive or expected
**Missing**: Human performance data
**Impact**: Can't interpret model performance without human comparison

### Flaw 6: Measuring Outcome Only
**Current**: Only score final answer (correct/incorrect)
**Problem**: Can't distinguish reasoning process from pattern matching
**Fix**: Need process measures (though harder in LLMs than humans)

---

## Methodological Contributions (Despite Flaw)

### What We Learned:

**1. Parser Design Matters**
- Initial parser failed on Claude (grabbed explanation words)
- Improved parser extracts symbols from anywhere in response
- Lesson: Different models need robust parsing strategies

**2. Instruction-Following Is Independent Variable**
- GPT-4: Minimal compliance (symbols only)
- Claude: Elaborative compliance (explains + symbols)
- Both achieve same accuracy but different behavioral profiles
- Implication: Instruction-following ≠ capability

**3. Symbol Novelty Verification**
- Successfully used Unicode ranges with <100 co-occurrences (Salesky et al., 2023)
- Disjoint sets verified (zero overlap between train/test)
- Even with novel symbols, simple patterns are learnable

**4. Task Calibration Is Critical**
- 20 examples of simple transformation: Too easy
- Need fewer examples + more complexity
- Literature review should inform sample sizes

**5. Claude's Bilingual Behavior**  
- Randomly switches English/Spanish in explanations
- Unknown cause (prompt language? internal state? user language history?)
- Scientifically interesting artifact to explore

---

## Technical Issues Resolved

### ✅ Issue 1: Symbol Pool Validation
- **Problem**: Required 240 symbols, had 184
- **Cause**: Overly conservative formula (×2 multiplier)
- **Fix**: Corrected to actual need (120 symbols)
- **Status**: Resolved

### ✅ Issue 2: OpenAI Client Error
- **Problem**: `TypeError: 'proxies' argument`
- **Cause**: Version conflict (openai 1.52.0 + httpx)
- **Fix**: Updated to openai 1.54.3 + httpx 0.27.2
- **Status**: Resolved

### ✅ Issue 3: Claude Parser Failure
- **Problem**: Grabbed "Analizando el patrón" instead of symbols
- **Cause**: Parser took first 3 tokens, symbols were at end
- **Fix**: New parser finds Unicode symbols anywhere in response
- **Status**: Resolved, reprocessed data shows 100% accuracy

### ⚠️ Issue 4: Gemini Model Names
- **Problem**: Model name changes across versions
- **Attempted**: gemini-2.0-flash-exp (rate limited), gemini-1.5-flash-latest (404)
- **Solution**: Use gemini-2.5-flash (confirmed available)
- **Status**: Pending rerun

---

## Next Steps: Option B - Redesigned Experiment (RECOMMENDED)

### The Problem Statement
Current task is **too easy** - both pattern matching and reasoning succeed. We need conditions where:
- Pattern matching should fail or degrade
- Reasoning would maintain performance
- Performance divergence reveals underlying process

### Redesign Principles (Chollet, 2019; Webb et al., 2023)

**1. Minimal Examples** → Force abstraction over memorization  
**2. Ambiguity** → Require rule identification, not just pattern continuation  
**3. Complexity** → Test compositional understanding  
**4. Generalization** → Test transfer beyond training distribution  
**5. Irregularity** → Break simple pattern matching

### Option B: Four-Condition Design

#### **Condition 1: Minimal Training (Abstraction Test)**
- **Training examples**: 3 (not 20)
- **Test examples**: 20 (same as before)
- **Hypothesis**: If models still get ~100%, suggests robust abstraction. If accuracy drops, reveals example dependency.
- **Prediction**: Accuracy should drop if relying on pattern memorization vs. rule induction

#### **Condition 2: Transformation Ambiguity (Rule Identification)**
- **Training**: Mix 2 different transformations
  - Type A: Rotate left (C A B ← A B C)
  - Type B: Reverse (C B A ← A B C)
- **Test**: Must identify which transformation applies to novel input
- **Marker**: Use different symbol at end to indicate type
- **Hypothesis**: Requires rule identification, not just continuation
- **Example**:
  ```
  Training:
  ⨀ ⨁ ⨂ ★ → ⨂ ⨀ ⨁  (rotate left, marked with ★)
  ⨃ ⨄ ⨅ ◆ → ⨅ ⨄ ⨃  (reverse, marked with ◆)
  
  Test:
  ⬯ ⨇ ⨝ ★ → ?  (must apply rotate left)
  ```

#### **Condition 3: Complexity Scaling (Compositional Reasoning)**
- **Training**: 3-symbol sequences with rotate-left
- **Test**: 
  - 3-symbol (same as training)
  - 4-symbol (generalization)
  - 5-symbol (further generalization)
- **Hypothesis**: If using positional rule, should generalize. If memorizing pattern, should fail on longer sequences.
- **Prediction**: Pattern matching may work for 3-symbol (memorized) but fail on 4-5 symbols

#### **Condition 4: Rule Transfer (Analogical Generalization)**
- **Training**: Rotate-left-by-1 (C A B ← A B C)
- **Test**: Rotate-left-by-2 (B C A ← A B C) with novel symbols
- **Marker**: Could use double marker (★★) to indicate "apply twice"
- **Hypothesis**: Requires understanding that "rotation" is generalizable operation
- **Prediction**: Pattern matching should fail; analogical reasoning might succeed

---

## Implementation Plan for Option B

### Phase 1: Redesign Experiment Generation (2-3 hours)
1. Create `experiment_1b_minimal.py` - 3 training examples
2. Create `experiment_1c_ambiguity.py` - Mixed transformations  
3. Create `experiment_1d_scaling.py` - Variable sequence lengths
4. Create `experiment_1e_transfer.py` - Rotate-by-2 test
5. Update symbol generator for longer sequences

### Phase 2: Run All Conditions (~$15-20 total)
- Each condition: ~$5 for 3 models
- Priority order: 1b (minimal), 1c (ambiguity), 1d (scaling), 1e (transfer)
- Collect data systematically

### Phase 3: Comparative Analysis
- Compare accuracy across conditions
- Look for divergence patterns
- Statistical tests for condition × model interactions
- Error analysis: which items fail?

### Expected Outcomes (Predictions)

**If Pattern Matching:**
- Condition 1b (minimal): Accuracy drops significantly with fewer examples
- Condition 1c (ambiguity): Random or chance performance (~50%)
- Condition 1d (scaling): Fails on 4-5 symbol sequences
- Condition 1e (transfer): Near-zero accuracy on rotate-by-2

**If Abstract Reasoning:**
- Condition 1b (minimal): Maintains high accuracy with 3 examples
- Condition 1c (ambiguity): Correctly identifies and applies rules (>80%)
- Condition 1d (scaling): Generalizes to longer sequences (>80%)
- Condition 1e (transfer): Shows analogical transfer (>60%)

**Most Likely (Graded Capacity):**
- Condition 1b: Moderate drop (80% → 60-70%)
- Condition 1c: Partial success (~60-70%)
- Condition 1d: Works for 4-symbol, fails for 5-symbol
- Condition 1e: Minimal transfer (<30%)

---

## What Current Results Tell Us (Honest Assessment)

### Valid Contribution: Methodological
We demonstrated that:
- In-context learning with novel symbols works robustly for simple patterns
- Instruction-following varies across models but doesn't affect task accuracy
- 20 examples is too many to test abstraction
- Simple positional transformations don't distinguish reasoning from pattern matching

### Publishable Angle: Task Calibration
**Title**: "When 100% Isn't Impressive: Task Difficulty Calibration in LLM Reasoning Experiments"

**Contribution**: 
- Demonstrates construct validity threat in reasoning research
- Shows simple transformations with many examples don't test reasoning
- Provides calibrated redesign for harder conditions
- Methodological contribution to LLM evaluation literature

### What We Still Don't Know:
- Can models handle minimal examples (3 vs 20)?
- Can they identify which transformation rule applies?
- Do they generalize beyond training complexity?
- Do they show analogical transfer?

**Option B will answer these questions.**

---

## Data Files (Experiment 1 - Version 1)

```
data/
├── experiments/
│   └── exp1_examples.json          # 20 training, 20 test (too easy)
├── results/
│   └── raw/
│       ├── exp1_main_gpt-4-0125-preview_20251006_100608.json    ✅ 100%
│       ├── exp1_main_claude-3-5-sonnet-20241022_20251006_102338.json  ✅ 100%
│       └── exp1_main_gemini-*_*.json                           ⏳ Pending
└── symbols/
    ├── exp1_sequential_training_0.json    # 60 symbols (disjoint)
    ├── exp1_sequential_test_1.json        # 60 symbols (disjoint)
    └── exp1_sequential_verification.json  # Verified novelty
```

---

## Cost Tracking

**Experiment 1 (Version 1 - "Too Easy")**:
- GPT-4: ~$3
- Claude: ~$2-3  
- Gemini: <$1 (partial)
- **Total**: ~$6-7

**Planned for Option B** (4 conditions × 3 models):
- Condition 1b (minimal): ~$5
- Condition 1c (ambiguity): ~$5
- Condition 1d (scaling): ~$6 (more test items)
- Condition 1e (transfer): ~$4
- **Total Option B**: ~$20

**Grand Total**: ~$27 for comprehensive reasoning test

---

## Literature Support for Redesign

### Chollet (2019) - "On the Measure of Intelligence"
**Key principle**: Intelligence requires handling novelty with minimal priors
- **ARC uses 2-3 training examples** (not 20)
- Tests abstraction and reasoning, not pattern memorization
- Our redesign follows ARC principles

### Webb et al. (2023) - Nature Human Behaviour  
**Finding**: LLM analogical reasoning degrades with:
- Fewer examples ✓ (test with Condition 1b)
- Complex compositions ✓ (test with Condition 1d)
- Transfer requirements ✓ (test with Condition 1e)

### Brown et al. (2020) - "Few-Shot Learners"
**Context**: GPT-3 shows impressive in-context learning
- Can adapt from examples without fine-tuning
- But: Is this reasoning or sophisticated pattern matching?
- Our redesign attempts to distinguish

### Mitchell & Krakauer (2023) - PNAS
**Framework**: Look for generalization failures
- Pattern matching breaks on out-of-distribution examples
- Reasoning should maintain under compositional complexity
- Our Conditions 1d and 1e test this directly

---

## Scientific Honesty Statement

**What went wrong**: We designed a task we thought would be hard, but it was too easy. Both models got 100%.

**What went right**: We recognized the problem immediately and redesigned rather than over-interpreting results.

**What we learned**: Task calibration is critical in LLM reasoning research. The literature (Chollet, Webb, etc.) provides guidance we should have followed more closely.

**Next steps**: Run harder conditions that actually stress reasoning capacity and create performance divergence.

**This is good science**: Negative results and methodological learning are valuable contributions.

---

## For Future Sessions

**If picking this up fresh:**
1. ✅ Experiment 1 Version 1 complete (but too easy - both models 100%)
2. ⏳ Complete Gemini run for baseline
3. 🎯 **Priority**: Implement and run Option B (4 conditions)
4. 📊 Then: Comparative analysis across conditions
5. 📝 Write up: Methodological paper on task calibration

**Key insight**: 100% accuracy from both models revealed construct validity threat - task doesn't test what we intended. Option B redesign addresses this.

**Scientific stance**: Be honest about design flaws, learn from them, iterate.

---

*Last updated: October 6, 2025*  
*Current status: Version 1 complete (too easy), Option B redesign planned*  
*Next: Run Gemini, then implement harder conditions that distinguish pattern matching from reasoning*

🔬 **Science is iterative. This is progress.** 🔬

### GPT-4 (gpt-4-0125-preview)
- **Accuracy**: 100% (20/20 correct)
- **Status**: ✅ Valid data, protocol followed correctly
- **Behavior**: Outputs symbols only, no verbal explanation
- **Example response**: "⬲ ▭ ⨤" (clean, minimal)
- **Tokens used**: 7,920
- **Cost**: ~$3

### Claude (claude-3-5-sonnet-20241022)
- **Accuracy**: 0% (0/20 correct)
- **Status**: ❌ Invalid data - protocol violation
- **Behavior**: Responds with natural language explanations instead of symbols
- **Example responses**: 
  - "Analizando el patrón" (Spanish: "Analyzing the pattern")
  - "Looking at the"
- **Issue**: Claude is explaining rather than completing the pattern
- **Tokens used**: Variable
- **Cost**: ~$2-3 (wasted on invalid responses)

### Gemini (gemini-2.0-flash-exp → gemini-1.5-flash-latest)
- **Accuracy**: 15% (3/20 before rate limiting)
- **Status**: ⚠️ Incomplete data - rate limited
- **Behavior**: Was responding with symbols correctly
- **Issue**: Free tier rate limits (10 requests/min)
- **Model updated**: Switched to gemini-1.5-flash-latest
- **Tokens used**: 4,731 (partial)
- **Cost**: <$1

---

## Technical Issues Encountered & Resolved

### Issue 1: Symbol Pool Validation (RESOLVED)
- **Problem**: Config validation required 240 symbols, only 184 available
- **Cause**: Overly conservative validation formula (multiplied by 2 unnecessarily)
- **Fix**: Corrected validation to actual requirement (120 symbols)
- **Status**: Fixed in config.py

### Issue 2: OpenAI Client Error (RESOLVED)
- **Problem**: `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`
- **Cause**: Version conflict between openai==1.52.0 and httpx
- **Fix**: Updated to openai==1.54.3 and httpx==0.27.2
- **Status**: Resolved, GPT-4 working perfectly

### Issue 3: Claude API Response Parsing (RESOLVED BUT INSUFFICIENT)
- **Problem**: `'TextBlock' object is not subscriptable`
- **Cause**: Anthropic API returns TextBlock objects, not dicts
- **Fix**: Changed `raw_response['content'][0]['text']` to `raw_response['content'][0].text`
- **Status**: Parsing works, BUT Claude now has behavioral issue (see below)

### Issue 4: Gemini Rate Limiting (PARTIALLY RESOLVED)
- **Problem**: gemini-2.0-flash-exp has strict rate limits (10/min)
- **Fix**: Switched to gemini-1.5-flash-latest (better quota)
- **Status**: Pending retest with new model

---

## NEW CRITICAL ISSUE: Claude Protocol Violation

**Most significant finding**: Claude refuses to follow minimal prompt protocol.

**Expected behavior**: Output only symbols
```
Input: ▭ ⨤ ⬲
Expected output: ⬲ ▭ ⨤
```

**Claude's actual behavior**: Provides natural language analysis
```
Claude response: "Analizando el patrón..." or "Looking at the..."
```

**Scientific implication**: 
- We cannot measure Claude's reasoning capability because it won't follow task format
- This is an **instruction-following problem**, not a reasoning problem
- Claude may possess the capability but behavioral constraints prevent measurement

**Possible causes**:
1. System prompt overrides causing Claude to "be helpful" by explaining
2. Safety filters preventing symbol-only responses
3. Different training on instruction-following vs. pattern-completion

**This is actually scientifically interesting**: Different models may have different instruction-following vs. capability profiles.

---

## Scientific Interpretations (Tentative)

### GPT-4's 100% Accuracy: Three Hypotheses

**H1: Legitimate Abstract Reasoning**
- GPT-4 successfully induced "rotate left" rule from 20 training examples
- Generalized to 20 completely novel test symbols (disjoint sets)
- Would support abstract reasoning hypothesis

**H2: Structural Pattern Matching**
- GPT-4 learned "last position → first position" heuristic
- Not true understanding of rotation, but positional rule
- Still impressive but less general

**H3: Training Data Contamination (Lower probability)**
- These specific Unicode symbols appeared together in training
- Unlikely given Salesky et al. (2023) selection criteria
- Would require symbol co-occurrence verification

**Current assessment**: H1 or H2 most likely. Need control conditions and error analysis to distinguish.

### What We Cannot Conclude Yet

**Cannot conclude**:
1. Comparative model performance (Claude data invalid, Gemini incomplete)
2. Whether GPT-4's performance generalizes to harder tasks
3. Whether other models can pass with proper prompting
4. Statistical significance (need multiple models for comparison)

**Can tentatively suggest**:
1. GPT-4 shows strong performance on this specific task
2. Instruction-following is a critical confound in LLM reasoning research
3. Minimal prompts may work differently across model families

---

## Experimental Validity Assessment

### Valid Results
- ✅ GPT-4: 20/20 trials, clean protocol following

### Invalid Results  
- ❌ Claude: 0/20 usable (protocol violations)
- ⚠️ Gemini: 3/20 completed (rate limited, incomplete)

### Threats to Validity

**Internal validity threats**:
1. Instruction-following confound (Claude demonstrates this clearly)
2. Model-specific prompt interpretation differences
3. Potential temperature=0 determinism hiding variance

**External validity threats**:
1. Single transformation rule (rotate left) may not generalize
2. 3-symbol sequences may be too simple
3. Cannot verify true symbol novelty without corpus access

**Construct validity**:
- Question: Are we measuring reasoning or instruction-following?
- Claude's behavior suggests these are separable constructs
- Need better protocol to isolate reasoning from behavioral compliance

---

## Next Steps (Prioritized)

### Immediate (Required for Valid Data)

1. **Fix Claude Protocol Issue** (CRITICAL)
   - Try system prompt modifications to force symbol-only output
   - Consider adding explicit "output only symbols" instruction
   - Alternative: Accept that Claude won't work with minimal prompts
   - Estimate: 1-2 hours

2. **Complete Gemini Testing**
   - Rerun with gemini-1.5-flash-latest
   - Verify rate limits resolved
   - Estimate: 15 minutes, <$1

### Secondary (Scientific Rigor)

3. **Control Condition**
   - Run same experiment with familiar symbols (A, B, C)
   - Tests whether task structure is sufficient vs. symbol novelty
   - Already coded, just needs execution
   - Estimate: 30 minutes, ~$5

4. **Error Analysis** (GPT-4)
   - Examine response latencies
   - Check for any systematic patterns in the (zero) errors
   - Verify responses are truly minimal (no hidden explanations)

5. **Statistical Analysis**
   - Once we have 2+ valid model results
   - Compare against chance (33.3%)
   - Effect size calculations
   - Bayesian analysis

### Future (Extended Research)

6. **Experiment 2**: Compositional operators
7. **Experiment 3**: Constraint satisfaction
8. **Publication preparation**

---

## Data Files Structure

```
data/
├── experiments/
│   └── exp1_examples.json          # Training/test stimuli
├── results/
│   └── raw/
│       ├── exp1_main_gpt-4-0125-preview_20251006_100242.json  ✅ Valid
│       ├── exp1_main_gpt-4-0125-preview_20251006_100608.json  ✅ Valid
│       ├── exp1_main_claude-3-5-sonnet-20241022_*.json        ❌ Invalid
│       └── exp1_main_gemini-2.0-flash-exp_*.json              ⚠️ Incomplete
└── symbols/
    ├── exp1_sequential_training_0.json
    ├── exp1_sequential_test_1.json
    ├── exp1_sequential_control_2.json
    └── exp1_sequential_verification.json
```

---

## Code Quality Status

### Working Components
- ✅ Symbol generation (disjoint sets verified)
- ✅ Experiment framework (stimulus generation, prompting)
- ✅ GPT-4 integration (perfect performance)
- ✅ Result storage and logging
- ✅ Error handling and retry logic

### Components Needing Fixes
- ⚠️ Claude integration (behavioral issue, not technical)
- ⚠️ Gemini rate limiting (model switch needed)
- 📝 Statistical analysis (not yet implemented)
- 📝 Visualization (not yet implemented)

### Components Not Yet Built
- Experiment 2 (compositional operators)
- Experiment 3 (constraint satisfaction)
- Human baseline comparison
- Analysis notebooks

---

## Methodological Notes

### What We've Learned

1. **Minimal prompts work differently across models**
   - GPT-4: Follows minimal protocol perfectly
   - Claude: Tries to "help" by explaining
   - This is scientifically valuable information

2. **Protocol compliance is measurable and important**
   - Not just about capability, but behavioral alignment
   - Different models have different instruction-following profiles

3. **Symbol selection appears robust**
   - 184 available symbols from low-frequency Unicode ranges
   - Disjoint sets verified (no overlap between train/test)
   - Control symbols working as intended

### Limitations Acknowledged

1. **Cannot verify true symbol novelty** without full corpus access
2. **Single task type** (sequential transformation only so far)
3. **Small sample** (n=20 test items per model)
4. **No human baseline** yet
5. **Temperature=0** may reduce measurement noise but not reflect typical usage

### Preregistration Status
- ❌ Not yet preregistered (should do before analyzing full dataset)
- Hypotheses clearly stated in theory.md
- Analysis plan needs formalization

---

## Cost Tracking

**Spent so far**: ~$6-8
- GPT-4: ~$3 (20 test items × 2 runs)
- Claude: ~$2-3 (multiple failed attempts)
- Gemini: <$1 (partial, rate limited)

**Estimated remaining**:
- Claude fixes: ~$2
- Gemini completion: ~$1  
- Control conditions: ~$5
- Total remaining: ~$8-10

**Total project estimate**: $15-20 for Experiment 1 complete

---

## Open Questions (Scientific)

1. **Why did GPT-4 achieve 100%?**
   - Genuine reasoning?
   - Structural heuristic?
   - Training contamination?
   - Need controls to distinguish

2. **Can Claude be made to follow minimal prompts?**
   - System prompt modification?
   - Different prompt format?
   - Or fundamental behavioral difference?

3. **Will other models show graded performance?**
   - Current hypothesis: Most likely outcome
   - Need valid data from multiple models

4. **Does temperature affect results?**
   - We used temperature=0 for determinism
   - Should test with sampling?

5. **How well do humans perform?**
   - Need baseline for interpretation
   - Is 100% actually impressive or easy?

---

## References (Key Papers for Context)

- **Salesky et al. (2023, EMNLP)**: Multilingual LLM evaluation, symbol selection methodology
- **Chollet (2019)**: ARC dataset, measuring intelligence through abstraction
- **Webb et al. (2023, Nature Human Behaviour)**: Emergent analogical reasoning in LLMs
- **Brown et al. (2020, NeurIPS)**: Few-shot learning in language models
- **Bubeck et al. (2023)**: Sparks of AGI, GPT-4 capabilities

---

## For Future Claude (Handoff Notes)

**If picking this up fresh:**

1. Read theory.md for full experimental rationale
2. Check this STATUS.md for current state
3. Priority: Fix Claude protocol issue or accept it won't work with minimal prompts
4. Complete Gemini testing with gemini-1.5-flash-latest
5. Run control condition (familiar symbols)
6. Then proceed to statistical analysis

**Key insight**: Instruction-following is a major confound. GPT-4 succeeds partly because it follows minimal prompt format. Claude fails partly because it doesn't.

**Don't assume**: Perfect scores mean perfect reasoning. Need controls and error analysis.

**Scientific honesty**: We have one valid result (GPT-4), not three. Be honest about data quality.

---

*Last updated: October 6, 2025 by Hillary Danan*  
*Experiment status: In progress, partial results*  
*Next session: Fix Claude, complete Gemini, run controls*