"""
Experiment 1e: Rule Transfer

Train on rotate-by-1, test on rotate-by-1 (control) vs rotate-by-2 (transfer).
Tests analogical transfer capability.
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
from src.transformations import rotate_left_by_n


class TransferExperiment(SequentialTransformationExperiment):
    """Test analogical transfer to novel transformation."""
    
    def generate_transfer_examples(
        self,
        symbols: List[str],
        rotation_amount: int,
        n_examples: int
    ) -> List[SequenceExample]:
        """Generate examples with specified rotation."""
        examples = []
        symbol_idx = 0
        
        for _ in range(n_examples):
            input_seq = symbols[symbol_idx:symbol_idx + EXP1_SEQUENCE_LENGTH]
            symbol_idx += EXP1_SEQUENCE_LENGTH
            
            output_seq = rotate_left_by_n(input_seq, rotation_amount)
            
            example = SequenceExample(
                input_sequence=input_seq,
                output_sequence=output_seq,
                transformation=f"rotate_left_{rotation_amount}"
            )
            examples.append(example)
        
        return examples
    
    def setup_experiment(self):
        """Generate training (rotate-1) and test (10 rotate-1, 10 rotate-2)."""
        print("\n" + "="*60)
        print("SETTING UP EXPERIMENT 1E: TRANSFER")
        print("="*60 + "\n")
        
        # Need symbols for: 3 training + 10 control + 10 transfer
        training_symbols_needed = 3 * EXP1_SEQUENCE_LENGTH
        test_symbols_needed = 20 * EXP1_SEQUENCE_LENGTH
        
        training_symbol_set, test_symbol_set = self.generator.generate_experiment1_symbols(
            n_training=3,
            n_test=20,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Generate training (rotate-by-1)
        print("Generating training (rotate-by-1)...")
        self.training_examples = self.generate_transfer_examples(
            training_symbol_set.symbols,
            rotation_amount=1,
            n_examples=3
        )
        
        # Split test symbols
        control_symbols = test_symbol_set.symbols[:30]  # First 10 sequences
        transfer_symbols = test_symbol_set.symbols[30:]  # Last 10 sequences
        
        # Generate test - control (rotate-by-1)
        print("Generating test control (rotate-by-1)...")
        control_examples = self.generate_transfer_examples(
            control_symbols,
            rotation_amount=1,
            n_examples=10
        )
        
        # Generate test - transfer (rotate-by-2)
        print("Generating test transfer (rotate-by-2)...")
        transfer_examples = self.generate_transfer_examples(
            transfer_symbols,
            rotation_amount=2,
            n_examples=10
        )
        
        # Combine and shuffle
        import random
        self.test_examples = control_examples + transfer_examples
        random.Random(RANDOM_SEED).shuffle(self.test_examples)
        
        # Tag which are control vs transfer
        for i, ex in enumerate(self.test_examples):
            if ex.transformation == "rotate_left_1":
                ex.metadata = {'test_type': 'control'}
            else:
                ex.metadata = {'test_type': 'transfer'}
        
        # Save
        examples_data = {
            'training': [ex.to_dict() for ex in self.training_examples],
            'test': [ex.to_dict() for ex in self.test_examples],
            'metadata': {
                'experiment': '1e_transfer',
                'training_rule': 'rotate_by_1',
                'control_rule': 'rotate_by_1',
                'transfer_rule': 'rotate_by_2',
                'generated_at': datetime.now().isoformat(),
            }
        }
        
        examples_file = EXPERIMENTS_DIR / "exp1e_transfer_examples.json"
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump(examples_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved to {examples_file}")
        print("\n" + "="*60)
        print(f"Training: {len(self.training_examples)} (rotate-by-1)")
        print(f"Test: {len(self.test_examples)} (10 control + 10 transfer)")
        print("="*60 + "\n")


def run_experiment_1e(models: List[BaseModel]):
    """Run Experiment 1e."""
    exp = TransferExperiment(seed=RANDOM_SEED)
    exp.setup_experiment()
    
    results = []
    for model in models:
        result = exp.run_model(
            model=model,
            training_examples=exp.training_examples,
            test_examples=exp.test_examples,
            experiment_type="1e_transfer"
        )
        
        # Analyze control vs transfer separately
        control_correct = sum(1 for r in result.responses 
                            if r.get('correct') and 
                            result.responses[result.responses.index(r)].get('metadata', {}).get('test_type') == 'control')
        transfer_correct = sum(1 for r in result.responses 
                             if r.get('correct') and 
                             result.responses[result.responses.index(r)].get('metadata', {}).get('test_type') == 'transfer')
        
        print(f"\n{result.model_name} breakdown:")
        print(f"  Control (rotate-by-1): {control_correct}/10")
        print(f"  Transfer (rotate-by-2): {transfer_correct}/10")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = RESULTS_DIR / "raw" / f"exp1e_transfer_{model.model_name}_{timestamp}.json"
        result.save(result_file)
        results.append(result)
    
    return results


if __name__ == "__main__":
    from src.models.gpt4_model import GPT4Model
    from src.models.claude_model import ClaudeModel
    
    print("="*70)
    print("EXPERIMENT 1E: RULE TRANSFER")
    print("="*70)
    print("\nTrain on rotate-by-1, test on rotate-by-1 vs rotate-by-2.")
    print("Tests analogical transfer capability.\n")
    
    models = [GPT4Model(), ClaudeModel()]
    results = run_experiment_1e(models)
    
    print("\n" + "="*70)
    print("EXPERIMENT 1E COMPLETE!")
    print("="*70)
