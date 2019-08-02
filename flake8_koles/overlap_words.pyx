"""Cython get_overlapped_words module."""
import re
from typing import List, Tuple

def get_overlapped_words(string: str, pattern: str) -> List[Tuple[int, str]]:
    """Return a list containing matching pattern words and their positions."""
    if pattern == '':
        return []

    regex = re.compile(f'(?=({pattern}))', flags=re.IGNORECASE)
    return [
        (match.start(), match.group(1)) for match in regex.finditer(string)
    ]
