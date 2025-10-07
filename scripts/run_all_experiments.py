#!/usr/bin/env python3
"""
Master script to run all experiments across all models.

This script:
1. Validates configuration
2. Initializes all models
3. Runs Experiment 1 (Sequential Transformation)
4. Saves results
5. Generates summary report

Usage:
    python3 scripts/run_all_experiments.py
"""

import sys
from pathlib import Path
import argparse
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import validate_config
from src.models.gpt4_model import GPT4Model
from src.models.claude_model import ClaudeModel
from src.models.gemini_model import GeminiModel
from src.experiments.experiment_1_sequential import run_experiment_1


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Run Reasoning in Vacuum experiments"
    )
    parser.add_argument(
        '--models',
        nargs='+',
        choices=['gpt4', 'claude', 'gemini', 'all'],
        default=['all'],
        help='Which models to test (default: all)'
    )
    parser.add_argument(
        '--control',
        action='store_true',
        help='Include control condition with familiar symbols'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate setup without making API calls'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print(" " * 15 + "REASONING IN VACUUM")
    print(" " * 10 + "Experimental Framework for LLM Reasoning")
    print("="*70 + "\n")
    
    # Validate configuration
    print("Validating configuration...")
    try:
        validate_config()
        print("✓ Configuration valid\n")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("\nPlease check your .env file and ensure all API keys are set.")
        sys.exit(1)
    
    if args.dry_run:
        print("✓ Dry run complete. Configuration is valid.")
        print("Remove --dry-run flag to execute experiments.\n")
        sys.exit(0)
    
    # Initialize models
    print("Initializing models...")
    models_to_test = []
    
    model_selection = args.models if 'all' not in args.models else ['gpt4', 'claude', 'gemini']
    
    if 'gpt4' in model_selection:
        try:
            models_to_test.append(GPT4Model())
            print("✓ GPT-4 initialized")
        except Exception as e:
            print(f"✗ Failed to initialize GPT-4: {e}")
    
    if 'claude' in model_selection:
        try:
            models_to_test.append(ClaudeModel())
            print("✓ Claude initialized")
        except Exception as e:
            print(f"✗ Failed to initialize Claude: {e}")
    
    if 'gemini' in model_selection:
        try:
            models_to_test.append(GeminiModel())
            print("✓ Gemini initialized")
        except Exception as e:
            print(f"✗ Failed to initialize Gemini: {e}")
    
    if not models_to_test:
        print("\n✗ No models successfully initialized. Exiting.")
        sys.exit(1)
    
    print(f"\nTesting {len(models_to_test)} model(s)\n")
    
    # Run Experiment 1
    print("="*70)
    print("EXPERIMENT 1: Sequential Transformation Rule Induction")
    print("="*70)
    print("\nTesting whether models can induce 'rotate left' transformation")
    print("from examples using completely novel symbol sets.\n")
    
    print("This experiment will:")
    print("- Generate 20 training examples with one set of symbols")
    print("- Test on 20 examples with COMPLETELY DIFFERENT symbols")
    print("- Score exact match accuracy\n")
    
    print("Expected outcomes:")
    print("- Pattern matching: ~33% accuracy (chance level)")
    print("- Abstract reasoning: >80% accuracy")
    print("\n" + "="*70 + "\n")
    
    input("Press Enter to begin experiments (or Ctrl+C to cancel)...")
    
    start_time = datetime.now()
    
    try:
        results = run_experiment_1(
            models=models_to_test,
            include_control=args.control
        )
    except KeyboardInterrupt:
        print("\n\n✗ Experiments cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n✗ Error during experiments: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Print summary
    print("\n" + "="*70)
    print(" " * 25 + "FINAL RESULTS")
    print("="*70 + "\n")
    
    print(f"Total execution time: {duration/60:.1f} minutes\n")
    
    print("Experiment 1 Results:")
    print("-" * 50)
    for result in results:
        status = "✓" if result.accuracy >= 0.80 else "✗"
        print(f"{status} {result.model_name:20s} {result.accuracy:6.1%} "
              f"({result.n_correct}/{result.n_total} correct)")
    
    print("\n" + "="*70)
    print("INTERPRETATION:")
    print("="*70)
    
    high_performers = [r for r in results if r.accuracy >= 0.80]
    low_performers = [r for r in results if r.accuracy < 0.40]
    medium_performers = [r for r in results if 0.40 <= r.accuracy < 0.80]
    
    if high_performers:
        print("\nHigh accuracy (>80% - suggests abstract reasoning):")
        for r in high_performers:
            print(f"  • {r.model_name}: {r.accuracy:.1%}")
    
    if medium_performers:
        print("\nMedium accuracy (40-80% - mixed/graded capacity):")
        for r in medium_performers:
            print(f"  • {r.model_name}: {r.accuracy:.1%}")
    
    if low_performers:
        print("\nLow accuracy (<40% - suggests pattern matching):")
        for r in low_performers:
            print(f"  • {r.model_name}: {r.accuracy:.1%}")
    
    print("\n" + "="*70)
    print("Next steps:")
    print("  1. Review detailed results in data/results/raw/")
    print("  2. Run statistical analysis: python3 src/analysis/statistical_tests.py")
    print("  3. Generate visualizations: python3 src/analysis/visualization.py")
    print("="*70 + "\n")
    
    # Print API usage summary
    print("API Usage Summary:")
    print("-" * 50)
    for model in models_to_test:
        stats = model.get_stats()
        print(f"{model.model_name}:")
        print(f"  Requests: {stats['total_requests']}")
        print(f"  Tokens: {stats['total_tokens']:,}")
        print(f"  Success rate: {stats['success_rate']:.1%}")
        print()
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()