"""Transformation functions for experiments."""
from typing import List

def rotate_left_by_n(sequence: List[str], n: int = 1) -> List[str]:
    """Rotate sequence left by n positions."""
    if len(sequence) == 0:
        return sequence
    n = n % len(sequence)
    return sequence[n:] + sequence[:n]

def reverse(sequence: List[str]) -> List[str]:
    """Reverse entire sequence."""
    return sequence[::-1]
