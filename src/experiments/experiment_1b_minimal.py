"""
Experiment 1b: Minimal Training Examples

Test whether models can induce rotate-left transformation with only 3 training
examples (vs 20 in Version 1).

Hypothesis: If accuracy maintained (~80-100%), suggests robust abstraction.
           If drops significantly, reveals example-dependent pattern matching.
"""

import json
import random
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

from src.config import (
    RANDOM_SEED,
    EXP1_SEQUENCE_LENGTH,
    EXPERIMENTS_DIR,
    RESULTS_DIR,
)
from src.symbol_generator import SymbolGenerator
from src.experiments.experiment_1_sequential import (
    SequenceExample,
    SequentialTransformationExperiment,
    ExperimentResult
)
from src.models.base_model import BaseModel


class MinimalTrainingExperiment(SequentialTransformationExperiment):
    """
    Experiment 1b: Test with minimal training examples.
    
    Same as Experiment 1, but with only 3 training examples instead of 20.
    """
    
    def setup_experiment(self, n_training: int = 3, n_test: int = 20):
        """
        Generate minimal training set.
        
        Args:
            n_training: Number of training examples (default: 3)
            n_test: Number of test examples (default: 20)
        """
        print("\n" + "="*60)
        print("SETTING UP EXPERIMENT 1B: MINIMAL TRAINING")
        print("="*60 + "\n")
        
        # Generate symbol sets
        print(f"Generating symbol sets ({n_training} training, {n_test} test)...")
        training_symbol_set, test_symbol_set = self.generator.generate_experiment1_symbols(
            n_training=n_training,
            n_test=n_test,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Generate training examples
        print(f"Generating {n_training} training examples...")
        self.training_examples = self.generate_training_examples(
            symbols=training_symbol_set.symbols,
            n_examples=n_training,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Generate test examples
        print(f"Generating {n_test} test examples...")
        self.test_examples = self.generate_training_examples(
            symbols=test_symbol_set.symbols,
            n_examples=n_test,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Save examples
        examples_data = {
            'training': [ex.to_dict() for ex in self.training_examples],
            'test': [ex.to_dict() for ex in self.test_examples],
            'metadata': {
                'experiment': '1b_minimal_training',
                'n_training': n_training,
                'n_test': n_test,
                'sequence_length': EXP1_SEQUENCE_LENGTH,
                'transformation': 'rotate_left',
                'seed': self.seed,
                'generated_at': datetime.now().isoformat(),
            }
        }
        
        examples_file = EXPERIMENTS_DIR / "exp1b_minimal_examples.json"
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump(examples_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved examples to {examples_file}")
        
        print("\n" + "="*60)
        print("EXPERIMENT 1B SETUP COMPLETE")
        print("="*60)
        print(f"Training examples: {len(self.training_examples)} (minimal!)")
        print(f"Test examples: {len(self.test_examples)}")
        print("="*60 + "\n")


def run_experiment_1b(models: List[BaseModel], n_training: int = 3):
    """
    Run Experiment 1b on provided models.
    
    Args:
        models: List of model instances to test
        n_training: Number of training examples (default: 3)
    """
    # Initialize experiment
    exp = MinimalTrainingExperiment(seed=RANDOM_SEED)
    
    # Setup with minimal training
    exp.setup_experiment(n_training=n_training, n_test=20)
    
    # Run on each model
    results = []
    
    for model in models:
        result = exp.run_model(
            model=model,
            training_examples=exp.training_examples,
            test_examples=exp.test_examples,
            experiment_type="1b_minimal"
        )
        
        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = RESULTS_DIR / "raw" / f"exp1b_minimal_{model.model_name}_{timestamp}.json"
        result.save(result_file)
        results.append(result)
    
    # Print comparison to Version 1
    print("\n" + "="*70)
    print("COMPARISON: VERSION 1 (20 examples) vs 1B (3 examples)")
    print("="*70)
    print(f"{'Model':<30} {'V1 (20ex)':<12} {'1b (3ex)':<12} {'Drop'}")
    print("-"*70)
    
    v1_scores = {
        'gpt-4-0125-preview': 100.0,
        'claude-3-5-sonnet-20241022': 100.0,
    }
    
    for result in results:
        v1_acc = v1_scores.get(result.model_name, None)
        if v1_acc:
            drop = v1_acc - result.accuracy * 100
            drop_str = f"-{drop:.1f}%" if drop > 0 else f"+{abs(drop):.1f}%"
            print(f"{result.model_name:<30} {v1_acc:>6.1f}%    {result.accuracy*100:>6.1f}%    {drop_str}")
    
    print("="*70 + "\n")
    
    return results


if __name__ == "__main__":
    from src.models.gpt4_model import GPT4Model
    from src.models.claude_model import ClaudeModel
    
    print("="*70)
    print("EXPERIMENT 1B: MINIMAL TRAINING (3 EXAMPLES)")
    print("="*70)
    print("\nThis tests whether models can abstract from minimal examples.")
    print("Version 1 used 20 training examples → 100% accuracy")
    print("This version uses 3 training examples → ??% accuracy\n")
    
    # Initialize models
    models = [
        GPT4Model(),
        ClaudeModel(),
    ]
    
    # Run experiment
    results = run_experiment_1b(models, n_training=3)
    
    print("\n" + "="*70)
    print("EXPERIMENT 1B COMPLETE!")
    print("="*70)
