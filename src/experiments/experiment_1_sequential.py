"""
Experiment 1: Sequential Transformation Rule Induction

Tests whether LLMs can induce and apply a simple transformation rule
(rotate left by 1 position) using completely novel symbols.

This is the core test distinguishing pattern matching from abstract reasoning.

CRITICAL DESIGN PRINCIPLE:
- Training and test sets use completely disjoint symbol sets
- No verbal instructions, only pattern presentation
- Chance accuracy: 33.3% (1/3 for position 1 correct)
- Reasoning threshold: 80% accuracy
"""

import json
import random
from pathlib import Path
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from src.config import (
    TRAINING_SET_SIZE,
    TEST_SET_SIZE,
    EXP1_SEQUENCE_LENGTH,
    EXP1_PROMPT_TEMPLATE,
    RANDOM_SEED,
    EXPERIMENTS_DIR,
    RESULTS_DIR,
)
from src.symbol_generator import SymbolGenerator
from src.models.base_model import BaseModel, ModelResponse


@dataclass
class SequenceExample:
    """
    A single input-output sequence example.
    
    Attributes:
        input_sequence: List of input symbols
        output_sequence: List of output symbols
        transformation: Name of transformation applied
    """
    input_sequence: List[str]
    output_sequence: List[str]
    transformation: str = "rotate_left"
    
    def to_string(self) -> str:
        """Format as prompt string: 'A B C → C A B'"""
        input_str = " ".join(self.input_sequence)
        output_str = " ".join(self.output_sequence)
        return f"{input_str} → {output_str}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class ExperimentResult:
    """
    Result from testing a single model on experiment.
    
    Attributes:
        model_name: Name of model tested
        experiment_type: Type of experiment (normal vs control)
        accuracy: Overall accuracy (0.0 to 1.0)
        n_correct: Number of correct responses
        n_total: Total number of test items
        responses: List of individual test responses
        metadata: Additional information
        timestamp: When experiment was run
    """
    model_name: str
    experiment_type: str
    accuracy: float
    n_correct: int
    n_total: int
    responses: List[Dict]
    metadata: Dict
    timestamp: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def save(self, filepath: Path):
        """Save result to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"✓ Saved result to {filepath}")


class SequentialTransformationExperiment:
    """
    Experiment 1: Sequential Transformation Rule Induction
    
    This class handles:
    - Generating training and test examples
    - Creating prompts
    - Running models
    - Scoring responses
    - Analyzing results
    """
    
    def __init__(self, seed: int = RANDOM_SEED):
        """
        Initialize experiment.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.rng = random.Random(seed)
        self.generator = SymbolGenerator(seed=seed)
        
        # Will be populated during setup
        self.training_examples: List[SequenceExample] = []
        self.test_examples: List[SequenceExample] = []
        self.control_examples: List[SequenceExample] = []
        
    def rotate_left(self, sequence: List[str]) -> List[str]:
        """
        Apply rotate-left transformation: last element moves to first.
        
        Example: [A, B, C] → [C, A, B]
        
        Args:
            sequence: Input sequence
            
        Returns:
            Rotated sequence
        """
        if len(sequence) == 0:
            return sequence
        return [sequence[-1]] + sequence[:-1]
    
    def generate_training_examples(
        self,
        symbols: List[str],
        n_examples: int = TRAINING_SET_SIZE,
        sequence_length: int = EXP1_SEQUENCE_LENGTH
    ) -> List[SequenceExample]:
        """
        Generate training examples demonstrating the transformation rule.
        
        Args:
            symbols: Pool of symbols to use
            n_examples: Number of examples to generate
            sequence_length: Length of each sequence
            
        Returns:
            List of SequenceExample objects
        """
        if len(symbols) < n_examples * sequence_length:
            raise ValueError(
                f"Insufficient symbols: need {n_examples * sequence_length}, "
                f"have {len(symbols)}"
            )
        
        examples = []
        symbol_idx = 0
        
        for _ in range(n_examples):
            # Get next sequence of symbols
            input_seq = symbols[symbol_idx:symbol_idx + sequence_length]
            symbol_idx += sequence_length
            
            # Apply transformation
            output_seq = self.rotate_left(input_seq)
            
            example = SequenceExample(
                input_sequence=input_seq,
                output_sequence=output_seq,
                transformation="rotate_left"
            )
            examples.append(example)
        
        return examples
    
    def create_prompt(
        self,
        training_examples: List[SequenceExample],
        test_input: List[str]
    ) -> str:
        """
        Create minimal prompt with training examples and test input.
        
        NO INSTRUCTIONS. NO EXPLANATIONS. Just pattern presentation.
        
        Args:
            training_examples: List of training examples
            test_input: Test input sequence
            
        Returns:
            Formatted prompt string
        """
        # Format training examples
        training_str = "\n".join([ex.to_string() for ex in training_examples])
        
        # Format test input
        test_str = " ".join(test_input)
        
        # Use template
        prompt = EXP1_PROMPT_TEMPLATE.format(
            training_examples=training_str,
            test_input=test_str
        )
        
        return prompt
    
    def parse_response(self, response_text: str, expected_length: int = 3) -> List[str]:
        """
        Parse model response into sequence of symbols.
        
        Handles various response formats:
        - "A B C" (minimal)
        - "The answer is: A B C" (with explanation)
        - "A, B, C" (with commas)
        - Multi-line with symbols at end
        
        Strategy: Extract all tokens, find sequences of special symbols
        
        Args:
            response_text: Raw text from model
            expected_length: Expected number of symbols
            
        Returns:
            List of parsed symbols (may be empty if parsing fails)
        """
        import unicodedata
        
        # Remove common formatting
        text = response_text.strip()
        text = text.replace("→", " ").replace("->", " ")
        text = text.replace(",", " ")
        
        # Split on whitespace
        tokens = text.split()
        
        # Try to find a sequence of expected_length special symbols
        # Special symbols are in our Unicode ranges (not ASCII letters)
        def is_special_symbol(token):
            """Check if token is a Unicode symbol (not regular letter/word)"""
            if len(token) != 1:
                return False
            char = token[0]
            # Check if it's in our designated ranges or geometric shapes
            codepoint = ord(char)
            return (
                (0x2A00 <= codepoint <= 0x2AFF) or  # Math operators
                (0x2B00 <= codepoint <= 0x2BFF) or  # Misc symbols  
                (0x25A0 <= codepoint <= 0x25FF) or  # Geometric shapes
                unicodedata.category(char).startswith('S')  # Any symbol
            )
        
        # Find all special symbols
        special_symbols = [t for t in tokens if is_special_symbol(t)]
        
        # If we found the expected number, take the last sequence
        # (handles cases where symbols appear after explanation)
        if len(special_symbols) >= expected_length:
            # Take LAST expected_length symbols (handles explanations before answer)
            return special_symbols[-expected_length:]
        elif len(special_symbols) > 0:
            # Return whatever symbols we found
            return special_symbols[:expected_length]
        else:
            # Fallback: just take first N tokens (original behavior)
            return [t for t in tokens if t][:expected_length]
    
    def score_response(
        self,
        predicted: List[str],
        expected: List[str],
        strict: bool = True
    ) -> Dict[str, Any]:
        """
        Score a model's response.
        
        Args:
            predicted: Model's predicted sequence
            expected: Correct sequence
            strict: If True, require exact match. If False, partial credit.
            
        Returns:
            Dictionary with scoring information
        """
        if strict:
            # Exact match required
            correct = (predicted == expected)
            score = 1.0 if correct else 0.0
        else:
            # Partial credit: position-wise accuracy
            if len(predicted) != len(expected):
                score = 0.0
                correct = False
            else:
                matches = sum(p == e for p, e in zip(predicted, expected))
                score = matches / len(expected)
                correct = (score == 1.0)
        
        return {
            'correct': correct,
            'score': score,
            'predicted': predicted,
            'expected': expected,
            'exact_match': predicted == expected,
        }
    
    def run_model(
        self,
        model: BaseModel,
        training_examples: List[SequenceExample],
        test_examples: List[SequenceExample],
        experiment_type: str = "main"
    ) -> ExperimentResult:
        """
        Run experiment on a single model.
        
        Args:
            model: Model instance to test
            training_examples: Training examples
            test_examples: Test examples
            experiment_type: 'main' or 'control'
            
        Returns:
            ExperimentResult object
        """
        print(f"\n{'='*60}")
        print(f"Running Experiment 1 on {model.model_name}")
        print(f"Type: {experiment_type}")
        print(f"{'='*60}\n")
        
        responses = []
        n_correct = 0
        
        for i, test_example in enumerate(test_examples):
            print(f"Test item {i+1}/{len(test_examples)}...")
            
            # Create prompt
            prompt = self.create_prompt(training_examples, test_example.input_sequence)
            
            # Get model response
            model_response = model.generate(prompt)
            
            # Parse response
            predicted = self.parse_response(
                model_response.text,
                expected_length=len(test_example.output_sequence)
            )
            
            # Score response
            score_info = self.score_response(
                predicted,
                test_example.output_sequence,
                strict=True  # Exact match required
            )
            
            if score_info['correct']:
                n_correct += 1
            
            # Store detailed response
            response_data = {
                'item_number': i + 1,
                'input': test_example.input_sequence,
                'expected_output': test_example.output_sequence,
                'model_output_raw': model_response.text,
                'model_output_parsed': predicted,
                'correct': score_info['correct'],
                'score': score_info['score'],
                'model_metadata': model_response.metadata,
            }
            responses.append(response_data)
            
            # Progress indicator
            status = "✓" if score_info['correct'] else "✗"
            print(f"  {status} Expected: {test_example.output_sequence}")
            print(f"    Predicted: {predicted}\n")
        
        # Calculate overall accuracy
        accuracy = n_correct / len(test_examples)
        
        print(f"\n{'='*60}")
        print(f"RESULTS: {model.model_name}")
        print(f"{'='*60}")
        print(f"Correct: {n_correct}/{len(test_examples)}")
        print(f"Accuracy: {accuracy:.1%}")
        print(f"{'='*60}\n")
        
        # Create result object
        result = ExperimentResult(
            model_name=model.model_name,
            experiment_type=experiment_type,
            accuracy=accuracy,
            n_correct=n_correct,
            n_total=len(test_examples),
            responses=responses,
            metadata={
                'n_training_examples': len(training_examples),
                'sequence_length': EXP1_SEQUENCE_LENGTH,
                'transformation': 'rotate_left',
                'seed': self.seed,
                'model_stats': model.get_stats(),
            },
            timestamp=datetime.now().isoformat()
        )
        
        return result
    
    def setup_experiment(self):
        """
        Generate all necessary symbols and examples.
        
        This creates:
        - Training set with one pool of symbols
        - Test set with completely different symbols
        - Control set with familiar symbols (letters)
        """
        print("\n" + "="*60)
        print("SETTING UP EXPERIMENT 1")
        print("="*60 + "\n")
        
        # Generate symbol sets
        print("Generating symbol sets...")
        training_symbol_set, test_symbol_set = self.generator.generate_experiment1_symbols(
            n_training=TRAINING_SET_SIZE,
            n_test=TEST_SET_SIZE,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Generate training examples
        print("Generating training examples...")
        self.training_examples = self.generate_training_examples(
            symbols=training_symbol_set.symbols,
            n_examples=TRAINING_SET_SIZE,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Generate test examples
        print("Generating test examples...")
        self.test_examples = self.generate_training_examples(  # Same logic, different symbols
            symbols=test_symbol_set.symbols,
            n_examples=TEST_SET_SIZE,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Generate control examples (using letters)
        print("Generating control examples...")
        control_symbol_set = self.generator.generate_control_symbols(
            n_sequences=TRAINING_SET_SIZE + TEST_SET_SIZE,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Split control into training and test
        control_train_symbols = control_symbol_set.symbols[:TRAINING_SET_SIZE * EXP1_SEQUENCE_LENGTH]
        control_test_symbols = control_symbol_set.symbols[TRAINING_SET_SIZE * EXP1_SEQUENCE_LENGTH:]
        
        control_training = self.generate_training_examples(
            symbols=control_train_symbols,
            n_examples=TRAINING_SET_SIZE,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        self.control_examples = self.generate_training_examples(
            symbols=control_test_symbols,
            n_examples=TEST_SET_SIZE,
            sequence_length=EXP1_SEQUENCE_LENGTH
        )
        
        # Save examples to file
        examples_data = {
            'training': [ex.to_dict() for ex in self.training_examples],
            'test': [ex.to_dict() for ex in self.test_examples],
            'control_training': [ex.to_dict() for ex in control_training],
            'control_test': [ex.to_dict() for ex in self.control_examples],
            'metadata': {
                'seed': self.seed,
                'n_training': TRAINING_SET_SIZE,
                'n_test': TEST_SET_SIZE,
                'sequence_length': EXP1_SEQUENCE_LENGTH,
                'generated_at': datetime.now().isoformat(),
            }
        }
        
        examples_file = EXPERIMENTS_DIR / "exp1_examples.json"
        with open(examples_file, 'w', encoding='utf-8') as f:
            json.dump(examples_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved examples to {examples_file}")
        
        print("\n" + "="*60)
        print("EXPERIMENT SETUP COMPLETE")
        print("="*60)
        print(f"Training examples: {len(self.training_examples)}")
        print(f"Test examples: {len(self.test_examples)}")
        print(f"Control examples: {len(self.control_examples)}")
        print("="*60 + "\n")


def run_experiment_1(models: List[BaseModel], include_control: bool = True):
    """
    Run Experiment 1 on all provided models.
    
    Args:
        models: List of model instances to test
        include_control: Whether to run control condition
    """
    # Initialize experiment
    exp = SequentialTransformationExperiment(seed=RANDOM_SEED)
    
    # Setup
    exp.setup_experiment()
    
    # Run on each model
    results = []
    
    for model in models:
        # Main experimental condition
        result = exp.run_model(
            model=model,
            training_examples=exp.training_examples,
            test_examples=exp.test_examples,
            experiment_type="main"
        )
        
        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = RESULTS_DIR / "raw" / f"exp1_main_{model.model_name}_{timestamp}.json"
        result.save(result_file)
        results.append(result)
        
        # Control condition (if requested)
        if include_control:
            # TODO: Implement control with same training examples but familiar symbols
            pass
    
    return results


if __name__ == "__main__":
    # Example usage
    from src.models.gpt4_model import GPT4Model
    from src.models.claude_model import ClaudeModel
    from src.models.gemini_model import GeminiModel
    
    print("="*60)
    print("EXPERIMENT 1: SEQUENTIAL TRANSFORMATION")
    print("="*60)
    print("\nThis will test whether models can induce the 'rotate left'")
    print("transformation rule from examples using novel symbols.\n")
    
    # Initialize models
    models = [
        GPT4Model(),
        ClaudeModel(),
        GeminiModel(),
    ]
    
    # Run experiment
    results = run_experiment_1(models, include_control=False)
    
    print("\n" + "="*60)
    print("EXPERIMENT COMPLETE!")
    print("="*60)
    
    for result in results:
        print(f"\n{result.model_name}: {result.accuracy:.1%} accuracy")