"""
Experiment 1c: Transformation Ambiguity

Test whether models can identify which transformation rule applies.

Training shows TWO rules:
- ★ marker → rotate left
- ◆ marker → reverse

Can models identify and apply correct rule to novel symbols?
"""

import json
from datetime import datetime
from typing import List
from pathlib import Path

from src.config import RANDOM_SEED, EXP1_SEQUENCE_LENGTH, EXPERIMENTS_DIR, RESULTS_DIR
from src.symbol_generator import SymbolGenerator
from src.experiments.experiment_1_sequential import (
    SequenceExample, SequentialTransformationExperiment, ExperimentResult
)
from src.models.base_model import BaseModel
from src.transformations import rotate_left_by_n, reverse


class AmbiguityExperiment(SequentialTransformationExperiment):
    """Test rule identification with ambiguous transformations."""
    
    def __init__(self, seed: int = RANDOM_SEED):
        super().__init__(seed)
        self.markers = {
            '★': ('rotate', rotate_left_by_n),
            '◆': ('reverse', reverse),
        }
    
    def generate_ambiguous_examples(
        self,
        symbols: List[str],
        n_per_rule: int = 3
    ) -> List[SequenceExample]:
        """Generate examples with rule markers."""
        examples = []
        symbol_idx = 0
        
        for marker, (rule_name, transform_fn) in self.markers.items():
            for _ in range(n_per_rule):
                input_seq = symbols[symbol_idx:symbol_idx + EXP1_SEQUENCE_LENGTH]
                symbol_idx += EXP1_SEQUENCE_LENGTH
                
                # Add marker
                input_with_marker = input_seq + [marker]
                
                # Apply transformation
                output_seq = transform_fn(input_seq)
                
                example = SequenceExample(
                    input_sequence=input_with_marker,
                    output_sequence=output_seq,
                    transformation=rule_name
                )
                examples.append(example)
        
        return examples
    
    def create_prompt(
        self,
        training_examples: List[SequenceExample],
        test_input: List[str]
    ) -> str:
        """Create prompt with marked examples."""
        training_str = "\n".join([ex.to_string() for ex in training_examples])
        test_str = " ".join(test_input)
        return f"{training_str}\n\n{test_str} →"
    
    def setup_experiment(self, n_per_rule: int = 3, n_test_per_rule: int = 10):
        """Generate ambiguous training and test sets."""
        print("\n" + "="*60)
        print("SETTING UP EXPERIMENT 1C: AMBIGUITY")
        print("="*60 + "\n")
        
        # Calculate symbols needed
        training_symbols_needed = n_per_rule * len(self.markers) * EXP1_SEQUENCE_LENGTH
        test_symbols_needed = n_test_per_rule * len(self.markers) * EXP1_SEQUENCE_LENGTH
        
        # Generate symbols
        training_symbol_set, test_symbol_set = self.generator.generate_experiment1_symbols(
            n_training=training_symbols_needed // EXP1_SEQUENCE_LENGTH,
            n_test=test_symbols_needed // EXP1_SEQUENCE_LENGTH,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Generate training
        print(f"Generating training ({n_per_rule} per rule)...")
        self.training_examples = self.generate_ambiguous_examples(
            training_symbol_set.symbols,
            n_per_rule=n_per_rule
        )
        
        # Generate test
        print(f"Generating test ({n_test_per_rule} per rule)...")
        self.test_examples = self.generate_ambiguous_examples(
            test_symbol_set.symbols,
            n_per_rule=n_test_per_rule
        )
        
        # Save
        examples_data = {
            'training': [ex.to_dict() for ex in self.training_examples],
            'test': [ex.to_dict() for ex in self.test_examples],
            'metadata': {
                'experiment': '1c_ambiguity',
                'rules': {marker: name for marker, (name, _) in self.markers.items()},
                'n_per_rule': n_per_rule,
                'generated_at': datetime.now().isoformat(),
            }
        }
        
        examples_file = EXPERIMENTS_DIR / "exp1c_ambiguity_examples.json"
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump(examples_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved to {examples_file}")
        print("\n" + "="*60)
        print(f"Training examples: {len(self.training_examples)}")
        print(f"Test examples: {len(self.test_examples)}")
        print("="*60 + "\n")


def run_experiment_1c(models: List[BaseModel]):
    """Run Experiment 1c."""
    exp = AmbiguityExperiment(seed=RANDOM_SEED)
    exp.setup_experiment(n_per_rule=3, n_test_per_rule=10)
    
    results = []
    for model in models:
        result = exp.run_model(
            model=model,
            training_examples=exp.training_examples,
            test_examples=exp.test_examples,
            experiment_type="1c_ambiguity"
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = RESULTS_DIR / "raw" / f"exp1c_ambiguity_{model.model_name}_{timestamp}.json"
        result.save(result_file)
        results.append(result)
    
    return results


if __name__ == "__main__":
    from src.models.gpt4_model import GPT4Model
    from src.models.claude_model import ClaudeModel
    
    print("="*70)
    print("EXPERIMENT 1C: TRANSFORMATION AMBIGUITY")
    print("="*70)
    print("\nCan models identify which rule (rotate vs reverse) applies?")
    print("Chance level: 50% (random rule selection)\n")
    
    models = [GPT4Model(), ClaudeModel()]
    results = run_experiment_1c(models)
    
    print("\n" + "="*70)
    print("EXPERIMENT 1C COMPLETE!")
    print("="*70)
