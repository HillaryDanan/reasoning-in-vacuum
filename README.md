# Reasoning in Vacuum

Testing whether large language models can induce abstract transformation rules from minimal examples using novel symbols.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

This project tests LLM performance on pattern completion tasks using Unicode symbols with documented low frequency in training corpora. The goal is to measure whether models can abstract transformation rules from varying numbers of training examples.

**Core question**: Does performance depend primarily on the number of training examples, or can models maintain accuracy with minimal examples?

---

## Experiment Design

### Task: Sequential Transformation Rule Induction

Models receive training examples demonstrating a rotate-left transformation on 3-symbol sequences, then complete test sequences using entirely different symbols.

**Example**:
```
Training:
⨀ ⨁ ⨂ → ⨂ ⨀ ⨁
⨃ ⨄ ⨅ → ⨅ ⨃ ⨄

Test (different symbols):
⬯ ⨇ ⨈ → ?
```

### Conditions Tested

1. **Version 1**: 20 training examples, 20 test items
2. **Version 1b**: 3 training examples, 20 test items  
3. **Condition 1c**: 6 training examples (2 different rules), 20 test items
4. **Condition 1d**: 3 training examples, 20 test items with varied sequence lengths (3-5 symbols)
5. **Condition 1e**: 3 training examples, 20 test items split between control (same rule) and transfer (analogous rule)

### Materials

- **Symbol pools**: Unicode ranges U+2A00-U+2AFF, U+2B00-U+2BFF (mathematical operators, miscellaneous symbols)
- **Symbol selection**: Based on Salesky et al. (2023) - documented <100 co-occurrences in Common Crawl
- **Design**: Completely disjoint training and test symbol sets (zero overlap)

---

## Results Summary

| Condition | Training | GPT-4 | Claude 3.5 | Chance | Significant? |
|-----------|----------|-------|------------|--------|--------------|
| V1 | 20 | 100% | 100% | 16.7% | Yes |
| V1b | 3 | 30% | 10% | 16.7% | No |
| 1c | 6 | 65% | 45% | 50.0% | No |
| 1d | 3 | 45% | 10% | varies | Poor |
| 1e | varies | varies | varies | 16.7% | Mixed |

**Key finding**: Performance collapsed from 100% (20 examples) to chance level (3 examples) for both models across multiple conditions.

---

## Repository Structure

```
reasoning-in-vacuum/
├── README.md                      # Project overview
├── status.md                      # Detailed results
├── PAPER_DRAFT.md                # Full analysis writeup
├── requirements.txt              # Dependencies
├── .env.example                  # API key template
│
├── src/
│   ├── config.py                 # Configuration
│   ├── symbol_generator.py       # Symbol pool generation
│   ├── experiments/
│   │   ├── experiment_1_sequential.py      # V1 (20 examples)
│   │   ├── experiment_1b_minimal.py        # V1b (3 examples)
│   │   ├── experiment_1c_ambiguity.py      # 1c (2 rules)
│   │   ├── experiment_1d_scaling.py        # 1d (varied length)
│   │   └── experiment_1e_transfer.py       # 1e (analogical transfer)
│   └── models/
│       ├── gpt4_model.py         # GPT-4 integration
│       └── claude_model.py       # Claude integration
│
├── data/
│   ├── experiments/              # Generated test sets
│   ├── results/raw/              # Model responses
│   └── symbols/                  # Symbol pools
│
└── scripts/
    ├── analyze_results.py        # Statistical analysis
    └── verify_symbols.py         # Symbol novelty verification
```

---

## Setup

### Prerequisites
- Python 3.12+
- API keys: OpenAI (GPT-4), Anthropic (Claude)

### Installation

```bash
git clone https://github.com/HillaryDanan/reasoning-in-vacuum.git
cd reasoning-in-vacuum

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Add API keys to .env
```

### Running Experiments

```bash
# Run specific condition
python3 -m src.experiments.experiment_1_sequential
python3 -m src.experiments.experiment_1b_minimal

# Analyze results
python3 scripts/analyze_results.py
```

---

## Methodology

### Statistical Analysis
- **Chance baseline**: 1/6 = 16.7% (random permutation of 3 symbols)
- **Test**: Binomial test comparing observed accuracy to chance
- **Alpha level**: 0.05 (two-tailed)

### Design Choices
- **No verbal instructions**: Models receive only input-output examples
- **Temperature**: 0.0 (deterministic sampling)
- **Disjoint symbol sets**: Training and test use completely different symbols
- **Symbol novelty**: Unicode ranges with <100 co-occurrences in training corpora

---

## Limitations

1. **Symbol novelty verification**: Cannot definitively verify absence from proprietary training corpora
2. **Sample size**: n=20 test items per condition
3. **Model coverage**: Tested GPT-4 and Claude 3.5 only
4. **Task specificity**: Results concern sequential transformation only
5. **No human baseline**: Human performance not measured

---

## Data Availability

All experimental data, code, and materials are in this repository:
- Raw model responses: `data/results/raw/`
- Generated test sets: `data/experiments/`
- Symbol pools: `data/symbols/`

---

## Citation

```bibtex
@misc{reasoning_in_vacuum_2025,
  title={Reasoning in Vacuum: Testing LLM Abstraction with Minimal Examples},
  author={Danan, Hillary},
  year={2025},
  url={https://github.com/HillaryDanan/reasoning-in-vacuum}
}
```

---

## References

- Salesky et al. (2023). Evaluating multilingual competence of large language models. EMNLP.
- Chollet (2019). On the measure of intelligence. arXiv:1911.01547
- Webb et al. (2023). Emergent analogical reasoning in large language models. Nature Human Behaviour.

---

## License

MIT License - See LICENSE file for details

---

*Last updated: October 2025*  
*Status: Experiments complete*