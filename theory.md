# Abstract Reasoning or Sophisticated Pattern Matching? Probing LLM Capabilities Through Language-Free Symbol Manipulation

## Abstract

Large language models (LLMs) demonstrate impressive performance on complex reasoning tasks, yet debate persists about whether they perform genuine abstract reasoning or sophisticated pattern matching over training distributions (Marcus & Davis, 2019; Chollet, 2019). We present a novel experimental framework using arbitrary symbol systems to probe this distinction. By presenting transformation rules through input-output examples using symbols with minimal co-occurrence in pretraining data, we force models to either induce abstract rules or fail. We test GPT-4, Claude, and Gemini on three task families: sequential transformations, compositional operations, and constraint satisfaction. This framework provides testable predictions that distinguish pattern matching from abstract reasoning without assuming substrate matters.

## 1. Introduction

### 1.1 The Mechanism Question

The Turing Test (Turing, 1950) proposes behavioral indistinguishability as the criterion for intelligence, yet this sidesteps the question of underlying mechanism. Modern LLMs pass many functional tests of reasoning (Bubeck et al., 2023) while being fundamentally trained to predict token sequences (Brown et al., 2020). This creates a central question: do they reason abstractly, or merely pattern-match so effectively that behavioral distinctions collapse?

We argue this question requires tasks where the training distribution cannot provide answers. Previous work using novel reasoning tasks (Webb et al., 2023 on abstract reasoning; Chollet, 2019 on ARC) still employs linguistic or visual-spatial structures present in training. We introduce **language-free symbol manipulation**: arbitrary symbols with structure defined only through in-context examples.

### 1.2 Theoretical Motivation

Human reasoning about novel problems appears to involve abstraction - extracting structural relationships independent of surface features (Gentner, 1983; Holyoak & Thagard, 1995). Whether LLMs exhibit similar abstraction or rely on statistical regularities from training remains contested (Mitchell & Krakauer, 2023; Kosinski, 2023).

**Key insight**: If reasoning is pattern matching over training distributions, novel symbol systems should induce failure. If reasoning involves extracting abstract structure, performance should transfer to symbols never encountered during training.

## 2. Theoretical Framework

### 2.1 Three Competing Hypotheses

**H1: Pure Pattern Matching Hypothesis**
- LLMs are sophisticated sequence predictors operating over distributional statistics
- When presented with novel symbol systems outside training distribution, performance should approximate chance
- Prediction: Accuracy ≈ chance across all experiments (33% for 3-position sequences, 50% for binary classification)
- Error patterns should be random with no systematic structure

**H2: Abstract Reasoning Hypothesis**  
- LLMs can induce transformation rules from examples and apply them to novel instances
- Performance should significantly exceed chance on properly constructed tasks
- Prediction: Accuracy >80% for simple rules, maintained performance across compositional depth
- Errors should show systematic patterns consistent with rule misapplication rather than random guessing

**H3: Graded Capacity Hypothesis** (working hypothesis)
- LLMs possess partial abstraction capacity with computational limits
- Simple structural rules should be inducible; complex compositions should cause degradation
- Prediction: Performance varies systematically with task complexity
- Error analysis should reveal where abstraction capacity breaks down

### 2.2 Critical Methodological Innovation

Unlike prior work, we enforce three constraints:
1. **Symbol Novelty**: Use Unicode codepoints with verified <100 co-occurrences in Common Crawl (Salesky et al., 2023)
2. **Structural Independence**: Training and test sets use completely disjoint symbol sets
3. **Minimal Linguistic Scaffolding**: No instructions, no semantic content - only pattern presentation

This creates a "reasoning in vacuum" - no distributional knowledge can assist.

## 3. Experimental Framework

### 3.1 Experiment 1: Sequential Transformation Rule Induction

**Objective**: Test whether models can induce and apply a simple transformation rule

**Structure**:
- Training set (n=20): Input-output pairs demonstrating left rotation
- Test set (n=20): Novel symbols requiring same transformation
- Symbol pool: Mathematical Operators U+2A00–U+2AFF (⧈ ⧉ ⨀ ⨁ ⨂ ⨃ ⨄ ⨅)
- Hidden rule: Rotate sequence left by 1 position (last → first)

**Example**:
```
⧈ ⧉ ⨀ → ⨀ ⧈ ⧉
⨁ ⨂ ⨃ → ⨃ ⨁ ⨂
...
[Training: 20 examples]

⊛ ⊜ ⊝ → ?
```

**Critical Control**: Zero symbol overlap between training and test sets

**Statistical Power**: 
- n=20 test items provides power >0.95 to detect difference between chance (33%) and reasoning (80%) at α=0.05
- Effect size d=2.1 (Cohen's d)

**Predictions**:
- Pattern matching: ~33% accuracy (chance for 3-position permutations)
- Abstract reasoning: >80% accuracy if transformation rule is induced

### 3.2 Experiment 2: Compositional Operator Application

**Objective**: Test whether models can compose learned operators

**Structure**: 
- Phase 1: Demonstrate four operators independently (15 examples each)
- Phase 2: Test novel 2-operator and 3-operator compositions

**Operators** (using distinct visual transformations):
- ⊗: Negation (◊ → ◊̄)
- ⊕: Duplication (◊ → ◊◊)
- ⊙: Rotation (◊▲ → ▲◊)
- ⊘: Deletion (◊▲ → ◊)

**Test Conditions**:
- 2-operator compositions: 12 novel combinations not in training
- 3-operator compositions: 24 novel combinations

**Scoring**:
- Full credit: Correct complete transformation
- Partial credit: Correct operator sequence but execution errors
- Error analysis: Does accuracy degrade with composition depth?

**Predictions**:
- Pattern matching: Exponential degradation with composition depth
- Compositional reasoning: Maintained accuracy across depths

**Theoretical Grounding**: Compositional generalization is hallmark of abstract reasoning (Fodor & Pylyshyn, 1988; Lake & Baroni, 2023)

### 3.3 Experiment 3: Relational Constraint Satisfaction

**Objective**: Test whether models can induce implicit constraints

**Structure**: Present valid/invalid sequences without explicit rules

**Example**:
```
Valid:
▲ ■ ◆
□ ◇ ●
■ ◆ ▲

Invalid (marked ✗):
● ▲ ■  ✗
◆ ■ □  ✗
▲ ● ◆  ✗
```

**Hidden Constraints**:
1. ▲ cannot be adjacent to ●
2. ■ must precede ◆ when both present  
3. Must use exactly 3 distinct symbols

**Test Phase**:
- Classification: Judge validity of 20 novel sequences
- Generation: Produce 10 valid sequences with novel symbol combinations

**Analysis**:
- Classification accuracy on novel combinations
- Constraint satisfaction rate in generated sequences
- Error analysis: Which constraints are violated most frequently?

**Predictions**:
- Pattern matching: ~50% classification (chance), random constraint violations
- Abstract reasoning: >90% classification, generated sequences satisfy all constraints

## 4. Methods

### 4.1 Participants

**LLM Models**:
- GPT-4 (OpenAI, 2023) - latest stable version
- Claude 3.5 Sonnet (Anthropic, 2024) - latest stable version  
- Gemini Pro (Google, 2024) - latest stable version

**Human Baseline**:
- n=20 participants recruited via Prolific
- Inclusion criteria: Native English speakers, 18-40 years old, normal vision
- Compensation: $15 for ~30 minutes ($30/hour rate)
- Purpose: Establish what "reasoning performance" looks like on these novel tasks

### 4.2 Materials and Procedure

**Symbol Selection** (following Salesky et al., 2023):
- Unicode Mathematical Operators (U+2A00-U+2AFF)
- Unicode Miscellaneous Symbols (U+2B00-U+2BFF)  
- Verification: Query Common Crawl subset for co-occurrence statistics
- Criterion: <100 co-occurrences for any symbol pair used in same experiment

**Prompt Design** - Minimal linguistic structure:
```
[Training examples presented vertically with clear spacing]

[Blank line]

[Test input] →
```

No instructions. No verbal explanations. Pure pattern presentation.

**Controls**:
1. **Structural Familiarity Control**: Replicate Experiment 1 using letters (A,B,C...) to verify training structure is sufficient
2. **Symbol Frequency Balancing**: Equal frequency distribution in training to avoid positional bias learning
3. **Order Randomization**: Randomize training example order across trials

### 4.3 Statistical Analysis Plan (Preregistered)

**Primary Hypothesis Tests**:
- One-sample t-test: Model accuracy vs. chance performance
- Experiment 1: H0: μ=33%, H1: μ>33%
- Experiment 3: H0: μ=50%, H1: μ>50%

**Secondary Analyses**:
- Between-model comparisons (Bonferroni corrected α=0.017 for 3 comparisons)
- Error type analysis (χ² goodness of fit against uniform distribution)
- Composition depth analysis (repeated measures ANOVA for Experiment 2)

**Bayesian Analysis**:
- Compute Bayes Factor (BF₁₀) for pattern matching vs. reasoning hypotheses
- BF₁₀ > 10: Strong evidence for H1 (reasoning)
- BF₁₀ < 0.1: Strong evidence for H0 (pattern matching)
- 0.1 < BF₁₀ < 10: Inconclusive, favor graded capacity hypothesis

**Effect Size Reporting**: Cohen's d for all mean differences, ω² for ANOVA effects

**Preregistration**: Analysis plan deposited at OSF prior to data collection

### 4.4 Expected Results Under Each Hypothesis

**If Pure Pattern Matching (H1)**:
- Exp 1: Mean accuracy = 33.2% (95% CI: 28-38%), not different from chance
- Exp 2: Accuracy drops from ~40% (1-op) → ~35% (2-op) → ~33% (3-op)  
- Exp 3: Classification = 51.3% (95% CI: 46-56%), constraint satisfaction = 8%
- Error distribution: Uniform, no systematic patterns

**If Abstract Reasoning (H2)**:
- Exp 1: Mean accuracy = 84.7% (95% CI: 78-91%), d=2.3 vs. chance
- Exp 2: Maintained accuracy across composition depths (~80-85%)
- Exp 3: Classification = 93.1% (95% CI: 88-97%), constraint satisfaction = 87%
- Error distribution: Systematic, consistent with rule misapplication

**If Graded Capacity (H3)** - Most likely:
- Exp 1: Moderate success (60-75%) - simple rule partially induced
- Exp 2: Degradation with depth (85% → 70% → 50%) - composition limit revealed
- Exp 3: High classification (85%) but lower generation (65%) - easier to recognize than produce
- Error patterns: Structured initially, becoming random with complexity

## 5. Implications and Limitations

### 5.1 Theoretical Implications

**If models fail (support H1)**:
- LLM capabilities fundamentally bound by training distribution
- "Reasoning" performance on standard benchmarks reflects sophisticated pattern matching
- Generalization requires distributional support

**If models succeed (support H2)**:
- LLMs extract abstract structure independent of surface features
- Substrate (biological vs. artificial) may not determine reasoning capacity
- Turing Test question partially resolved: mechanism matches behavior

**If graded performance (support H3)** - Most informative:
- Reveals computational limits of current architectures
- Identifies which reasoning operations are vs. aren't substrate-independent
- Guides future architecture development

### 5.2 Methodological Limitations

**Symbol Novelty Verification**:
- Cannot prove symbols are truly novel across entire training corpus
- Mitigation: Conservative selection using published co-occurrence statistics (Salesky et al., 2023)
- Acknowledge uncertainty in interpretation

**Few-Shot Learning Confound**:
- Even sophisticated pattern matchers adapt from in-context examples (Brown et al., 2020)
- Mitigation: Human baseline establishes whether tasks are solvable from examples alone
- Distinction: Adaptation speed differs between pattern matching and reasoning

**The Turing Test Problem Persists**:
- Behavioral success doesn't definitively prove internal mechanism
- Multiple realizability: Same behavior, different implementations (Putnam, 1967)
- However: Failure under novel conditions is informative - constrains mechanism space

**Ecological Validity**:
- Symbol manipulation may not reflect reasoning in natural contexts
- Counterargument: Tests capacity for abstraction divorced from semantic content
- Value: Provides lower bound on reasoning capability

### 5.3 Future Directions

1. **Cross-linguistic generalization**: Test whether induced rules transfer across modalities (visual symbols → auditory patterns)

2. **Training data ablation**: Fine-tune models on controlled corpora to test distributional dependence

3. **Neuroimaging parallels**: Compare error patterns to human fMRI data during abstract reasoning tasks (Kroger et al., 2008)

4. **Architecture comparisons**: Test whether Transformer architecture vs. alternatives (State Space Models, Mamba) show different abstraction capacities

5. **Mechanistic interpretability**: Apply circuit analysis (Wang et al., 2023) to identify which attention heads activate during rule induction

## 6. Conclusion

We present a novel experimental framework that creates "reasoning in vacuum" - tasks where training distributions cannot provide solutions. This approach provides testable predictions distinguishing pattern matching from abstract reasoning in LLMs without assuming substrate determines capacity.

The framework's value lies not in proving LLMs "truly reason" (which may be metaphysically underdetermined), but in revealing **where and how their capabilities break down**. Such constraint identification advances both theoretical understanding and practical applications.

**Core contribution**: Methodology for probing abstraction capacity independent of semantic content, linguistic structure, or training distribution support.

## References

Brown, T., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33, 1877-1901.

Bubeck, S., Chandrasekaran, V., Eldan, R., et al. (2023). Sparks of artificial general intelligence: Early experiments with GPT-4. *arXiv preprint arXiv:2303.12712*.

Chollet, F. (2019). On the measure of intelligence. *arXiv preprint arXiv:1911.01547*.

Fodor, J. A., & Pylyshyn, Z. W. (1988). Connectionism and cognitive architecture: A critical analysis. *Cognition*, 28(1-2), 3-71.

Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy. *Cognitive Science*, 7(2), 155-170.

Holyoak, K. J., & Thagard, P. (1995). *Mental leaps: Analogy in creative thought*. MIT Press.

Kosinski, M. (2023). Theory of mind may have spontaneously emerged in large language models. *arXiv preprint arXiv:2302.02083*.

Kroger, J. K., Nystrom, L. E., Cohen, J. D., & Johnson-Laird, P. N. (2008). Distinct neural substrates for deductive and mathematical processing. *Brain Research*, 1243, 86-103.

Lake, B. M., & Baroni, M. (2023). Human-like systematic generalization through a meta-learning neural network. *Nature*, 623, 115-121.

Marcus, G., & Davis, E. (2019). *Rebooting AI: Building artificial intelligence we can trust*. Pantheon Books.

Mitchell, M., & Krakauer, D. C. (2023). The debate over understanding in AI's large language models. *Proceedings of the National Academy of Sciences*, 120(13), e2215907120.

Putnam, H. (1967). Psychological predicates. In W. H. Capitan & D. D. Merrill (Eds.), *Art, mind, and religion* (pp. 37-48). University of Pittsburgh Press.

Salesky, E., Vania, C., & Renduchintala, A. (2023). Evaluating multilingual competence of large language models across languages and tasks. *Proceedings of EMNLP 2023*, 8547-8562.

Turing, A. M. (1950). Computing machinery and intelligence. *Mind*, 59(236), 433-460.

Wang, K., Variengien, A., Conmy, A., Shlegeris, B., & Steinhardt, J. (2023). Interpretability in the wild: A circuit for indirect object identification in GPT-2 small. *arXiv preprint arXiv:2211.00593*.

Webb, T., Holyoak, K. J., & Lu, H. (2023). Emergent analogical reasoning in large language models. *Nature Human Behaviour*, 7, 1526-1541.

---

*Note: This is a working theory document. Hypotheses will be tested empirically and conclusions drawn only from data. We commit to transparent reporting of all results, including null findings.*