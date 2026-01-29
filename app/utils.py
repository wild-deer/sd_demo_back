import random
from typing import List, TypeVar

T = TypeVar('T')

def random_chunk_split(data: List[T], min_size: int, max_size: int) -> List[List[T]]:
    """
    Randomly splits an array into chunks with sizes between min_size and max_size.
    The last chunk may be smaller than min_size if the remaining elements are not enough.
    
    Args:
        data: The input list to split.
        min_size: Minimum chunk size.
        max_size: Maximum chunk size.
        
    Returns:
        A list of chunks.
    """
    if min_size > max_size:
        raise ValueError("min_size cannot be greater than max_size")
    if min_size <= 0:
        raise ValueError("min_size must be positive")
    
    chunks = []
    i = 0
    n = len(data)
    
    while i < n:
        chunk_size = random.randint(min_size, max_size)
        chunk = data[i : i + chunk_size]
        chunks.append(chunk)
        i += chunk_size
        
    return chunks
