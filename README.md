# Reasoning in Vacuum

**Testing whether Large Language Models perform abstract reasoning or sophisticated pattern matching through language-free symbol manipulation.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🧠 Core Idea

Can LLMs induce abstract transformation rules from examples using symbols they've never seen before? Or do they just pattern-match over training data?

We test this by presenting input-output mappings using **arbitrary Unicode symbols** with structure defined only through examples. No language. No instructions. No familiar patterns. Just pure structure.

If models can solve these tasks, they're doing something that looks like abstract reasoning. If they fail at chance levels, they're pattern matching.

## 🎯 Three Experiments

### Experiment 1: Sequential Transformation Rule Induction
**Question**: Can models learn "rotate left by 1" from examples with novel symbols?

```
Training (20 examples):
⧈ ⧉ ⨀ → ⨀ ⧈ ⧉
⨁ ⨂ ⨃ → ⨃ ⨁ ⨂
...

Test (20 examples with DIFFERENT symbols):
⊛ ⊜ ⊝ → ?
```

**Predictions**:
- Pattern matching: ~33% accuracy (chance)
- Abstract reasoning: >80% accuracy

### Experiment 2: Compositional Operator Application
**Question**: Can models compose learned operations?

```
Learn operators:
⊗ ◊ → ◊̄  (negation)
⊕ ◊ → ◊◊  (duplication)

Test composition:
⊗ ⊕ ◊ → ?  (should be: ◊̄◊̄)
```

**Predictions**:
- Pattern matching: Degrades exponentially with composition depth
- Compositional reasoning: Maintains performance

### Experiment 3: Relational Constraint Satisfaction
**Question**: Can models induce implicit constraints?

```
Valid examples:
▲ ■ ◆
□ ◇ ●
■ ◆ ▲

Invalid (marked ✗):
● ▲ ■  ✗
◆ ■ □  ✗

Test: Classify new sequences + generate valid ones
```

**Predictions**:
- Pattern matching: ~50% classification (chance)
- Abstract reasoning: >90% classification, constraint-satisfying generation

## 🔬 Why This Matters

### Theoretical Contribution
- **Distinguishes mechanism from behavior**: Success/failure reveals underlying process
- **No semantic scaffolding**: Tests reasoning "in vacuum" without linguistic crutches
- **Distributional independence**: Symbols chosen to have <100 co-occurrences in Common Crawl

### Practical Implications
- **Identifies capacity limits**: Where does abstraction break down?
- **Guides architecture development**: What reasoning operations are substrate-independent?
- **Benchmark for AGI**: Tests core reasoning without task-specific training

## 📁 Repository Structure

```
reasoning-in-vacuum/
├── README.md                          # You are here
├── theory.md                          # Full theoretical framework & predictions
├── requirements.txt                   # Python dependencies
├── .env.example                       # API key template
├── .gitignore                         # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── config.py                      # Configuration & symbol pools
│   ├── symbol_generator.py            # Generate novel symbol sets
│   ├── experiments/
│   │   ├── __init__.py
│   │   ├── experiment_1_sequential.py # Sequential transformation
│   │   ├── experiment_2_composition.py # Operator composition
│   │   └── experiment_3_constraints.py # Constraint satisfaction
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py              # Base model interface
│   │   ├── gpt4_model.py              # GPT-4 wrapper
│   │   ├── claude_model.py            # Claude wrapper
│   │   └── gemini_model.py            # Gemini wrapper
│   └── analysis/
│       ├── __init__.py
│       ├── statistical_tests.py       # Hypothesis testing
│       ├── visualization.py           # Plot results
│       └── error_analysis.py          # Error pattern analysis
│
├── data/
│   ├── symbols/
│   │   ├── mathematical_operators.json # U+2A00-U+2AFF
│   │   └── misc_symbols.json          # U+2B00-U+2BFF
│   ├── experiments/
│   │   ├── exp1_training.json         # Generated training sets
│   │   ├── exp1_test.json             # Generated test sets
│   │   └── ...
│   └── results/
│       ├── raw/                       # Raw model responses
│       ├── processed/                 # Scored & analyzed
│       └── human_baseline/            # Human performance data
│
├── notebooks/
│   ├── 01_symbol_verification.ipynb   # Verify symbol novelty
│   ├── 02_run_experiments.ipynb       # Execute all tests
│   └── 03_analysis.ipynb              # Statistical analysis & viz
│
├── scripts/
│   ├── verify_symbols.py              # Check co-occurrence stats
│   ├── run_all_experiments.py         # Master experiment runner
│   └── generate_report.py             # Create results report
│
└── outputs/
    ├── figures/                       # Generated plots
    ├── tables/                        # Results tables  
    └── report.pdf                     # Final analysis report
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- API keys for: OpenAI (GPT-4), Anthropic (Claude), Google (Gemini)
- ~$20-40 in API credits total

### Installation

```bash
# Clone repo
git clone https://github.com/HillaryDanan/reasoning-in-vacuum.git
cd reasoning-in-vacuum

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Verify setup
python3 scripts/verify_symbols.py
```

### Running Experiments

```bash
# Run all three experiments on all models
python3 scripts/run_all_experiments.py

# Run specific experiment
python3 -m src.experiments.experiment_1_sequential --model gpt4

# Analyze results
python3 scripts/generate_report.py
```

### Jupyter Notebooks

```bash
jupyter notebook notebooks/02_run_experiments.ipynb
```

## 📊 Expected Results Timeline

- **Symbol generation & verification**: 1 hour
- **Experiment execution**: 2-3 hours (API rate limits)
- **Statistical analysis**: 1 hour
- **Total**: ~5 hours hands-on time

## 🤝 Contributing

This is a scientific research project. Contributions welcome:

1. **Improve experimental design**: Suggest controls, additional conditions
2. **Add models**: Extend to other LLMs (Llama, Mistral, etc.)
3. **Statistical analysis**: Additional tests, visualizations
4. **Replication**: Run experiments and share results

## 📄 License

MIT License - See LICENSE file for details

## 📚 Citation

If you use this framework in your research, please cite:

```bibtex
@misc{reasoning_in_vacuum_2025,
  title={Reasoning in Vacuum: Probing LLM Abstraction Through Symbol Manipulation},
  author={Danan, Hillary},
  year={2025},
  url={https://github.com/HillaryDanan/reasoning-in-vacuum}
}
```

## 🙏 Acknowledgments

Inspired by:
- François Chollet's ARC dataset (measuring intelligence through abstraction)
- Melanie Mitchell's work on AI reasoning capabilities
- The mechanistic interpretability community

## 📧 Contact

Questions? Open an issue or reach out!

---

**Status**: 🔬 Active research project | Last updated: October 2025