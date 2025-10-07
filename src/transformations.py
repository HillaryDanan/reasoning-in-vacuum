"""
Transformation functions for experimental conditions.

Each function takes a sequence and returns transformed sequence.
"""

from typing import List, Callable


def rotate_left_by_n(sequence: List[str], n: int = 1) -> List[str]:
    """
    Rotate sequence left by n positions.
    
    Example: rotate_left_by_n([A,B,C], 1) → [C,A,B]
             rotate_left_by_n([A,B,C], 2) → [B,C,A]
    
    Args:
        sequence: Input sequence
        n: Number of positions to rotate
        
    Returns:
        Rotated sequence
    """
    if len(sequence) == 0:
        return sequence
    n = n % len(sequence)  # Handle n > len
    return sequence[n:] + sequence[:n]


def rotate_right_by_n(sequence: List[str], n: int = 1) -> List[str]:
    """Rotate sequence right by n positions."""
    return rotate_left_by_n(sequence, -n)


def reverse(sequence: List[str]) -> List[str]:
    """Reverse entire sequence."""
    return sequence[::-1]


def swap_first_last(sequence: List[str]) -> List[str]:
    """Swap first and last elements."""
    if len(sequence) < 2:
        return sequence
    result = sequence.copy()
    result[0], result[-1] = result[-1], result[0]
    return result


def identity(sequence: List[str]) -> List[str]:
    """Return sequence unchanged (control)."""
    return sequence.copy()


# Dictionary of available transformations
TRANSFORMATIONS = {
    'rotate_left': lambda s: rotate_left_by_n(s, 1),
    'rotate_left_2': lambda s: rotate_left_by_n(s, 2),
    'rotate_right': lambda s: rotate_right_by_n(s, 1),
    'reverse': reverse,
    'swap': swap_first_last,
    'identity': identity,
}
