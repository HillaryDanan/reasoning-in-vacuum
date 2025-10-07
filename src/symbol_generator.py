"""
Symbol generator for Reasoning in Vacuum experiments.

This module handles generation of completely disjoint symbol sets for training
and test conditions, ensuring no symbol overlap between sets (critical for 
testing abstract reasoning vs. pattern matching).

Key principle: Training and test sets must use completely different symbols
to prevent any distributional pattern matching.
"""

import random
import json
from pathlib import Path
from typing import List, Set, Tuple, Dict
from dataclasses import dataclass, asdict

from src.config import (
    ALL_SYMBOLS,
    MATHEMATICAL_OPERATORS,
    MISCELLANEOUS_SYMBOLS,
    GEOMETRIC_SHAPES,
    RANDOM_SEED,
    SYMBOLS_DIR,
)


@dataclass
class SymbolSet:
    """
    Container for a set of symbols with metadata.
    
    Attributes:
        symbols: List of symbol strings
        set_type: Type identifier (e.g., 'training', 'test')
        experiment: Experiment identifier (e.g., 'exp1_sequential')
        metadata: Additional metadata dictionary
    """
    symbols: List[str]
    set_type: str
    experiment: str
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        # Add symbol count to metadata
        self.metadata['symbol_count'] = len(self.symbols)
        self.metadata['unique_count'] = len(set(self.symbols))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def save(self, filepath: Path):
        """Save symbol set to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: Path) -> 'SymbolSet':
        """Load symbol set from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)


class SymbolGenerator:
    """
    Generator for creating disjoint symbol sets.
    
    This class ensures that training and test sets use completely different
    symbols, preventing any possibility of pattern matching on symbol identity.
    """
    
    def __init__(self, seed: int = RANDOM_SEED):
        """
        Initialize symbol generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.rng = random.Random(seed)
        
        # Track used symbols across all experiments
        self.used_symbols: Set[str] = set()
        
        # Available symbol pools
        self.available_symbols = ALL_SYMBOLS.copy()
        self.math_symbols = MATHEMATICAL_OPERATORS.copy()
        self.misc_symbols = MISCELLANEOUS_SYMBOLS.copy()
        self.geom_symbols = GEOMETRIC_SHAPES.copy()
        
        # Shuffle for randomization
        self.rng.shuffle(self.available_symbols)
        
    def get_disjoint_sets(
        self, 
        n_sets: int, 
        symbols_per_set: int,
        pool: List[str] = None
    ) -> List[List[str]]:
        """
        Generate n completely disjoint sets of symbols.
        
        Critical for experiments: ensures no symbol appears in multiple sets.
        
        Args:
            n_sets: Number of disjoint sets to create
            symbols_per_set: Number of symbols per set
            pool: Symbol pool to draw from (uses all available if None)
            
        Returns:
            List of n lists, each containing symbols_per_set unique symbols
            
        Raises:
            ValueError: If insufficient symbols available
        """
        if pool is None:
            pool = [s for s in self.available_symbols if s not in self.used_symbols]
        
        total_needed = n_sets * symbols_per_set
        
        if len(pool) < total_needed:
            raise ValueError(
                f"Insufficient symbols: need {total_needed}, "
                f"have {len(pool)} available"
            )
        
        # Sample without replacement
        sampled = self.rng.sample(pool, total_needed)
        
        # Split into n disjoint sets
        sets = []
        for i in range(n_sets):
            start_idx = i * symbols_per_set
            end_idx = start_idx + symbols_per_set
            symbol_set = sampled[start_idx:end_idx]
            sets.append(symbol_set)
            
            # Mark as used
            self.used_symbols.update(symbol_set)
        
        return sets
    
    def generate_experiment1_symbols(
        self,
        n_training: int = 20,
        n_test: int = 20,
        sequence_length: int = 3
    ) -> Tuple[SymbolSet, SymbolSet]:
        """
        Generate symbols for Experiment 1 (sequential transformation).
        
        Creates two completely disjoint sets:
        - Training set: n_training sequences
        - Test set: n_test sequences
        
        CRITICAL: Zero symbol overlap between sets.
        
        Args:
            n_training: Number of training sequences
            n_test: Number of test sequences  
            sequence_length: Symbols per sequence
            
        Returns:
            Tuple of (training_set, test_set) as SymbolSet objects
        """
        # Calculate total symbols needed
        training_symbols_needed = n_training * sequence_length
        test_symbols_needed = n_test * sequence_length
        
        # Generate disjoint sets
        sets = self.get_disjoint_sets(
            n_sets=2,
            symbols_per_set=max(training_symbols_needed, test_symbols_needed)
        )
        
        training_pool = sets[0][:training_symbols_needed]
        test_pool = sets[1][:test_symbols_needed]
        
        # Create SymbolSet objects with metadata
        training_set = SymbolSet(
            symbols=training_pool,
            set_type='training',
            experiment='exp1_sequential',
            metadata={
                'n_sequences': n_training,
                'sequence_length': sequence_length,
                'transformation_rule': 'rotate_left',
                'seed': self.seed,
            }
        )
        
        test_set = SymbolSet(
            symbols=test_pool,
            set_type='test',
            experiment='exp1_sequential',
            metadata={
                'n_sequences': n_test,
                'sequence_length': sequence_length,
                'transformation_rule': 'rotate_left',
                'seed': self.seed,
            }
        )
        
        # Verification: Ensure zero overlap
        overlap = set(training_pool) & set(test_pool)
        if overlap:
            raise RuntimeError(
                f"CRITICAL ERROR: Symbol overlap detected: {overlap}. "
                f"This violates experimental design!"
            )
        
        return training_set, test_set
    
    def generate_control_symbols(
        self,
        n_sequences: int = 20,
        sequence_length: int = 3
    ) -> SymbolSet:
        """
        Generate familiar symbols for control condition.
        
        Uses letters A-Z for structural familiarity control.
        Tests whether training structure is sufficient (vs. symbol novelty).
        
        Args:
            n_sequences: Number of sequences
            sequence_length: Symbols per sequence
            
        Returns:
            SymbolSet with familiar symbols (letters)
        """
        # Use letters for control
        letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        total_needed = n_sequences * sequence_length
        
        if len(letters) < total_needed:
            # Reuse letters if needed (controlled repetition)
            symbols = []
            while len(symbols) < total_needed:
                symbols.extend(letters)
            symbols = symbols[:total_needed]
        else:
            symbols = self.rng.sample(letters, total_needed)
        
        control_set = SymbolSet(
            symbols=symbols,
            set_type='control',
            experiment='exp1_sequential_control',
            metadata={
                'n_sequences': n_sequences,
                'sequence_length': sequence_length,
                'symbol_type': 'familiar_letters',
                'purpose': 'structural_control',
            }
        )
        
        return control_set
    
    def verify_symbol_novelty(self, symbols: List[str]) -> Dict:
        """
        Verify that symbols are from designated low-frequency ranges.
        
        Note: This checks Unicode ranges but cannot verify actual co-occurrence
        in Common Crawl without corpus access. We rely on Salesky et al. (2023)
        documentation that these ranges have minimal co-occurrence.
        
        Args:
            symbols: List of symbols to verify
            
        Returns:
            Dictionary with verification results
        """
        results = {
            'total_symbols': len(symbols),
            'unique_symbols': len(set(symbols)),
            'from_math_operators': 0,
            'from_misc_symbols': 0,
            'from_geometric_shapes': 0,
            'from_other_ranges': 0,
            'unicode_ranges': {},
        }
        
        for symbol in set(symbols):
            codepoint = ord(symbol)
            hex_code = f"U+{codepoint:04X}"
            
            # Track unicode range
            if codepoint not in results['unicode_ranges']:
                results['unicode_ranges'][hex_code] = symbol
            
            # Categorize by range
            if symbol in MATHEMATICAL_OPERATORS:
                results['from_math_operators'] += 1
            elif symbol in MISCELLANEOUS_SYMBOLS:
                results['from_misc_symbols'] += 1
            elif symbol in GEOMETRIC_SHAPES:
                results['from_geometric_shapes'] += 1
            else:
                results['from_other_ranges'] += 1
        
        # Check if all symbols are from designated ranges
        results['all_from_designated_ranges'] = (
            results['from_other_ranges'] == 0
        )
        
        return results
    
    def save_symbol_sets(
        self,
        symbol_sets: List[SymbolSet],
        base_filename: str = "symbols"
    ):
        """
        Save multiple symbol sets with verification report.
        
        Args:
            symbol_sets: List of SymbolSet objects to save
            base_filename: Base name for files
        """
        SYMBOLS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save each set
        for i, symbol_set in enumerate(symbol_sets):
            filename = f"{base_filename}_{symbol_set.set_type}_{i}.json"
            filepath = SYMBOLS_DIR / filename
            symbol_set.save(filepath)
            print(f"✓ Saved {symbol_set.set_type} set to {filepath}")
        
        # Generate verification report
        all_symbols = []
        for symbol_set in symbol_sets:
            all_symbols.extend(symbol_set.symbols)
        
        verification = self.verify_symbol_novelty(all_symbols)
        
        # Save verification report
        report_path = SYMBOLS_DIR / f"{base_filename}_verification.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(verification, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved verification report to {report_path}")
        
        # Print summary
        print("\n" + "="*60)
        print("SYMBOL SET VERIFICATION REPORT")
        print("="*60)
        print(f"Total symbols used: {verification['total_symbols']}")
        print(f"Unique symbols: {verification['unique_symbols']}")
        print(f"From Math Operators (U+2A00-U+2AFF): {verification['from_math_operators']}")
        print(f"From Misc Symbols (U+2B00-U+2BFF): {verification['from_misc_symbols']}")
        print(f"From Geometric Shapes (U+25A0-U+25FF): {verification['from_geometric_shapes']}")
        print(f"All from designated ranges: {verification['all_from_designated_ranges']}")
        print("="*60)
        
        # Check for symbol reuse across sets (should be zero!)
        all_symbols_flat = []
        set_names = []
        for symbol_set in symbol_sets:
            all_symbols_flat.extend(symbol_set.symbols)
            set_names.append(symbol_set.set_type)
        
        if len(all_symbols_flat) != len(set(all_symbols_flat)):
            duplicates = [s for s in set(all_symbols_flat) 
                         if all_symbols_flat.count(s) > 1]
            print(f"\n⚠️  WARNING: Symbol reuse detected: {duplicates}")
            print("This may violate experimental design if across train/test!")
        else:
            print("\n✓ No symbol reuse detected. All sets are disjoint.")
        print("="*60 + "\n")


def generate_all_experiment1_symbols():
    """
    Generate and save all symbol sets for Experiment 1.
    
    This is the main entry point for symbol generation before running experiments.
    """
    print("Generating symbols for Experiment 1: Sequential Transformation\n")
    
    generator = SymbolGenerator(seed=RANDOM_SEED)
    
    # Generate main experimental sets
    training_set, test_set = generator.generate_experiment1_symbols(
        n_training=20,
        n_test=20,
        sequence_length=3
    )
    
    # Generate control set
    control_set = generator.generate_control_symbols(
        n_sequences=20,
        sequence_length=3
    )
    
    # Save all sets
    generator.save_symbol_sets(
        [training_set, test_set, control_set],
        base_filename="exp1_sequential"
    )
    
    print("✓ Symbol generation complete!\n")
    
    return training_set, test_set, control_set


if __name__ == "__main__":
    # Generate symbols when run directly
    generate_all_experiment1_symbols()