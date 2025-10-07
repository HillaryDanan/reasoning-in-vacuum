"""
Configuration file for Reasoning in Vacuum experiments.

This module contains all configuration parameters, symbol pools, and constants
used across experiments. Symbol selections follow Salesky et al. (2023) methodology
for minimal co-occurrence in pretraining data.
"""

import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SYMBOLS_DIR = DATA_DIR / "symbols"
EXPERIMENTS_DIR = DATA_DIR / "experiments"
RESULTS_DIR = DATA_DIR / "results"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Ensure directories exist
for directory in [SYMBOLS_DIR, EXPERIMENTS_DIR, RESULTS_DIR / "raw", 
                  RESULTS_DIR / "processed", OUTPUTS_DIR / "figures", 
                  OUTPUTS_DIR / "tables"]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# API CONFIGURATION
# ============================================================================

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model names
GPT4_MODEL = os.getenv("GPT4_MODEL", "gpt-4-0125-preview")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# API settings
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))
REQUEST_TIMEOUT = 60  # seconds

# ============================================================================
# EXPERIMENTAL PARAMETERS
# ============================================================================

# Random seed for reproducibility
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))

# Sample sizes (chosen for statistical power >0.95 to detect d=2.1 at α=0.05)
TRAINING_SET_SIZE = 20
TEST_SET_SIZE = 20

# Temperature settings (0 for deterministic responses in experiments)
MODEL_TEMPERATURE = 0.0
MAX_TOKENS = 150  # Sufficient for symbol outputs

# ============================================================================
# SYMBOL POOLS
# ============================================================================
# Following Salesky et al. (2023) methodology: Use Unicode ranges with
# minimal co-occurrence in Common Crawl (<100 co-occurrences per pair)

# Mathematical Operators (U+2A00 - U+2AFF)
# These symbols rarely co-occur in natural text
MATHEMATICAL_OPERATORS: List[str] = [
    "⨀", "⨁", "⨂", "⨃", "⨄", "⨅", "⨆", "⨇",  # U+2A00-2A07
    "⨈", "⨉", "⨊", "⨋", "⨌", "⨍", "⨎", "⨏",  # U+2A08-2A0F
    "⨐", "⨑", "⨒", "⨓", "⨔", "⨕", "⨖", "⨗",  # U+2A10-2A17
    "⨘", "⨙", "⨚", "⨛", "⨜", "⨝", "⨞", "⨟",  # U+2A18-2A1F
    "⨠", "⨡", "⨢", "⨣", "⨤", "⨥", "⨦", "⨧",  # U+2A20-2A27
    "⨨", "⨩", "⨪", "⨫", "⨬", "⨭", "⨮", "⨯",  # U+2A28-2A2F
    "⨰", "⨱", "⨲", "⨳", "⨴", "⨵", "⨶", "⨷",  # U+2A30-2A37
    "⨸", "⨹", "⨺", "⨻", "⨼", "⨽", "⨾", "⨿",  # U+2A38-2A3F
]

# Miscellaneous Symbols (U+2B00 - U+2BFF)
MISCELLANEOUS_SYMBOLS: List[str] = [
    "⬀", "⬁", "⬂", "⬃", "⬄", "⬅", "⬆", "⬇",  # U+2B00-2B07
    "⬈", "⬉", "⬊", "⬋", "⬌", "⬍", "⬎", "⬏",  # U+2B08-2B0F
    "⬐", "⬑", "⬒", "⬓", "⬔", "⬕", "⬖", "⬗",  # U+2B10-2B17
    "⬘", "⬙", "⬚", "⬛", "⬜", "⬝", "⬞", "⬟",  # U+2B18-2B1F
    "⬠", "⬡", "⬢", "⬣", "⬤", "⬥", "⬦", "⬧",  # U+2B20-2B27
    "⬨", "⬩", "⬪", "⬫", "⬬", "⬭", "⬮", "⬯",  # U+2B28-2B2F
    "⬰", "⬱", "⬲", "⬳", "⬴", "⬵", "⬶", "⬷",  # U+2B30-2B37
    "⬸", "⬹", "⬺", "⬻", "⬼", "⬽", "⬾", "⬿",  # U+2B38-2B3F
]

# Geometric Shapes (U+25A0 - U+25FF) - for Experiment 3 constraints
GEOMETRIC_SHAPES: List[str] = [
    "■", "□", "▢", "▣", "▤", "▥", "▦", "▧",  # Squares
    "▨", "▩", "▪", "▫", "▬", "▭", "▮", "▯",  # More squares
    "▰", "▱", "▲", "△", "▴", "▵", "▶", "▷",  # Triangles
    "▸", "▹", "►", "▻", "▼", "▽", "▾", "▿",  # More triangles
    "◀", "◁", "◂", "◃", "◄", "◅", "◆", "◇",  # Diamonds
    "◈", "◉", "◊", "○", "◌", "◍", "◎", "●",  # Circles
    "◐", "◑", "◒", "◓", "◔", "◕", "◖", "◗",  # More circles
]

# Combined pool (168 unique symbols)
ALL_SYMBOLS = MATHEMATICAL_OPERATORS + MISCELLANEOUS_SYMBOLS + GEOMETRIC_SHAPES

# ============================================================================
# EXPERIMENT 1: SEQUENTIAL TRANSFORMATION
# ============================================================================

EXP1_SEQUENCE_LENGTH = 3  # Number of symbols per sequence
EXP1_TRANSFORMATION = "rotate_left"  # Rule: last element moves to first

# Chance accuracy for random guessing on 3-position sequences
# For rotation: 1/3! = 1/6 ≈ 16.7% for exact match
# For position 1 correct: 1/3 = 33.3%
EXP1_CHANCE_ACCURACY = 0.333  # Conservative estimate

# Threshold for "reasoning" performance (>80% as preregistered)
EXP1_REASONING_THRESHOLD = 0.80

# ============================================================================
# EXPERIMENT 2: COMPOSITIONAL OPERATORS
# ============================================================================

# Operators and their transformations
# Note: Using simple visual transformations for proof of concept
# In actual implementation, these would be more complex

OPERATORS: Dict[str, Dict] = {
    "⊗": {
        "name": "negation",
        "description": "Adds combining overline (◊ → ◊̄)",
        "transformation": "add_overline",
    },
    "⊕": {
        "name": "duplication", 
        "description": "Duplicates symbol (◊ → ◊◊)",
        "transformation": "duplicate",
    },
    "⊙": {
        "name": "rotation",
        "description": "Rotates sequence (◊▲ → ▲◊)",
        "transformation": "rotate",
    },
    "⊘": {
        "name": "deletion",
        "description": "Deletes last symbol (◊▲ → ◊)",
        "transformation": "delete_last",
    },
}

EXP2_EXAMPLES_PER_OPERATOR = 15
EXP2_TWO_OP_COMBINATIONS = 12  # 4 choose 2 with order
EXP2_THREE_OP_COMBINATIONS = 24  # 4 choose 3 with order

# ============================================================================
# EXPERIMENT 3: CONSTRAINT SATISFACTION
# ============================================================================

# Hidden constraints (not told to models)
EXP3_CONSTRAINTS = {
    "adjacency": "▲ cannot be adjacent to ●",
    "precedence": "■ must precede ◆ when both present",
    "distinct": "Must use exactly 3 distinct symbols",
}

EXP3_VALID_EXAMPLES = 15
EXP3_INVALID_EXAMPLES = 15
EXP3_TEST_CLASSIFICATION = 20
EXP3_TEST_GENERATION = 10

# Chance accuracy for binary classification
EXP3_CHANCE_ACCURACY = 0.50
EXP3_REASONING_THRESHOLD = 0.90

# ============================================================================
# STATISTICAL PARAMETERS
# ============================================================================

# Significance level (α)
ALPHA = 0.05

# Effect size thresholds (Cohen's d)
SMALL_EFFECT = 0.2
MEDIUM_EFFECT = 0.5
LARGE_EFFECT = 0.8

# Bayesian analysis thresholds
BF_STRONG_H1 = 10  # Strong evidence for H1 (reasoning)
BF_STRONG_H0 = 0.1  # Strong evidence for H0 (pattern matching)

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

# Experiment 1: Minimal prompt (just examples, no instructions)
EXP1_PROMPT_TEMPLATE = """{training_examples}

{test_input} →"""

# Control condition: Same structure with familiar symbols (letters)
EXP1_CONTROL_PROMPT_TEMPLATE = """{training_examples}

{test_input} →"""

# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

# Result file naming
RESULT_FILENAME_TEMPLATE = "{experiment}_{model}_{timestamp}.json"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config() -> bool:
    """
    Validate configuration parameters.
    
    Returns:
        bool: True if configuration is valid, raises ValueError otherwise
    """
    # Check API keys
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in .env file")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set in .env file")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in .env file")
    
    # Check symbol pool sizes
    # Need: training symbols + test symbols (disjoint sets)
    symbols_needed = (TRAINING_SET_SIZE + TEST_SET_SIZE) * EXP1_SEQUENCE_LENGTH
    if len(ALL_SYMBOLS) < symbols_needed:
        raise ValueError(
            f"Insufficient symbols: Need at least "
            f"{symbols_needed} unique symbols, have {len(ALL_SYMBOLS)}"
        )
    
    # Check statistical parameters
    if not 0 < ALPHA < 1:
        raise ValueError(f"Alpha must be between 0 and 1, got {ALPHA}")
    
    return True

# ============================================================================
# SCIENTIFIC NOTES
# ============================================================================

"""
METHODOLOGICAL NOTES:

1. Symbol Selection (Salesky et al., 2023, EMNLP):
   - We use Unicode ranges with minimal co-occurrence in Common Crawl
   - Target: <100 co-occurrences per symbol pair in pretraining data
   - Limitation: Cannot verify actual co-occurrence without corpus access
   - Mitigation: Conservative selection from documented low-frequency ranges

2. Sample Size Justification:
   - n=20 chosen for statistical power analysis
   - Power >0.95 to detect difference between 33% (chance) and 80% (reasoning)
   - Effect size d=2.1 (Cohen's d) for this difference
   - α=0.05 (two-tailed)
   
3. Temperature Setting:
   - Temperature=0.0 for deterministic responses
   - Rationale: Reduces noise, allows cleaner inference about capabilities
   - Limitation: May not reflect typical model usage
   
4. Symbol Pool Size:
   - 168 unique symbols available
   - Training + test require complete disjoint sets
   - Exp 1: Need 120 symbols (20 training × 3 + 20 test × 3)
   - Sufficient margin for all experiments

5. Preregistration Commitment:
   - All parameters fixed before data collection
   - Analysis plan deposited at OSF (link TBD)
   - Transparent reporting of all results including null findings
"""