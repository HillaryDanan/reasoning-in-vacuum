"""
Experiment 1d: Complexity Scaling

Train on 3-symbol sequences, test on 3, 4, 5-symbol sequences.
Can models generalize the rotation rule to longer sequences?
"""

import json
from datetime import datetime
from typing import List
from pathlib import Path

from src.config import RANDOM_SEED, EXPERIMENTS_DIR, RESULTS_DIR
from src.symbol_generator import SymbolGenerator
from src.experiments.experiment_1_sequential import (
    SequenceExample, SequentialTransformationExperiment, ExperimentResult
)
from src.models.base_model import BaseModel
from src.transformations import rotate_left_by_n


class ScalingExperiment(SequentialTransformationExperiment):
    """Test generalization across sequence lengths."""
    
    def generate_variable_length_examples(
        self,
        symbols: List[str],
        lengths: List[int],
        n_per_length: int
    ) -> List[SequenceExample]:
        """Generate examples of different lengths."""
        examples = []
        symbol_idx = 0
        
        for length in lengths:
            for _ in range(n_per_length):
                input_seq = symbols[symbol_idx:symbol_idx + length]
                symbol_idx += length
                
                output_seq = rotate_left_by_n(input_seq, 1)
                
                example = SequenceExample(
                    input_sequence=input_seq,
                    output_sequence=output_seq,
                    transformation="rotate_left"
                )
                examples.append(example)
        
        return examples
    
    def setup_experiment(self):
        """Generate training (3-symbol) and test (3,4,5-symbol)."""
        print("\n" + "="*60)
        print("SETTING UP EXPERIMENT 1D: SCALING")
        print("="*60 + "\n")
        
        # Training: 3 examples of length 3
        training_symbols_needed = 3 * 3  # 9 symbols
        
        # Test: 6 length-3, 7 length-4, 7 length-5
        test_symbols_needed = (6*3) + (7*4) + (7*5)  # 18+28+35 = 81
        
        # Generate symbols
        training_symbol_set, test_symbol_set = self.generator.generate_experiment1_symbols(
            n_training=3,
            n_test=27,  # Total items, variable length
            sequence_length=3  # Base length
        )
        
        # Get enough test symbols (need 81 total)
        # We'll need to generate more
        additional_symbols = [s for s in self.generator.available_symbols 
                            if s not in training_symbol_set.symbols 
                            and s not in test_symbol_set.symbols][:21]
        test_symbols = test_symbol_set.symbols + additional_symbols
        
        # Generate training (length 3 only)
        print("Generating training (3-symbol sequences)...")
        self.training_examples = self.generate_variable_length_examples(
            training_symbol_set.symbols,
            lengths=[3],
            n_per_length=3
        )
        
        # Generate test (mixed lengths)
        print("Generating test (3,4,5-symbol sequences)...")
        self.test_examples = self.generate_variable_length_examples(
            test_symbols,
            lengths=[3, 4, 5],
            n_per_length=7  # Will give 21 total, we'll take first 20
        )[:20]
        
        # Save
        examples_data = {
            'training': [ex.to_dict() for ex in self.training_examples],
            'test': [ex.to_dict() for ex in self.test_examples],
            'metadata': {
                'experiment': '1d_scaling',
                'training_length': 3,
                'test_lengths': [3, 4, 5],
                'generated_at': datetime.now().isoformat(),
            }
        }
        
        examples_file = EXPERIMENTS_DIR / "exp1d_scaling_examples.json"
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump(examples_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved to {examples_file}")
        print("\n" + "="*60)
        print(f"Training: {len(self.training_examples)} (all length 3)")
        print(f"Test: {len(self.test_examples)} (mixed 3,4,5)")
        print("="*60 + "\n")


def run_experiment_1d(models: List[BaseModel]):
    """Run Experiment 1d."""
    exp = ScalingExperiment(seed=RANDOM_SEED)
    exp.setup_experiment()
    
    results = []
    for model in models:
        result = exp.run_model(
            model=model,
            training_examples=exp.training_examples,
            test_examples=exp.test_examples,
            experiment_type="1d_scaling"
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = RESULTS_DIR / "raw" / f"exp1d_scaling_{model.model_name}_{timestamp}.json"
        result.save(result_file)
        results.append(result)
    
    return results


if __name__ == "__main__":
    from src.models.gpt4_model import GPT4Model
    from src.models.claude_model import ClaudeModel
    
    print("="*70)
    print("EXPERIMENT 1D: COMPLEXITY SCALING")
    print("="*70)
    print("\nTrain on 3-symbol, test on 3,4,5-symbol sequences.")
    print("Can the rule generalize to longer sequences?\n")
    
    models = [GPT4Model(), ClaudeModel()]
    results = run_experiment_1d(models)
    
    print("\n" + "="*70)
    print("EXPERIMENT 1D COMPLETE!")
    print("="*70)
