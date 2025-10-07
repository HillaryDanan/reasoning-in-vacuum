# Reasoning in Vacuum - Experimental Status Report

**Last Updated**: October 6, 2025  
**Experiment**: Sequential Transformation Rule Induction (Experiment 1)  
**Status**: Partial results collected, significant protocol issues identified

---

## Current Results Summary

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