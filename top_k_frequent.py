"""
Top K Frequent Elements

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Follow up: Your algorithm's time complexity must be better than O(n log n).
"""

from collections import Counter, defaultdict
from typing import List
import heapq


def topKFrequentSorting(nums: List[int], k: int) -> List[int]:
    """
    Approach 1: Using sorting

    Time Complexity: O(n log n) - dominated by sorting
    Space Complexity: O(n) - for the frequency map

    Args:
        nums: List of integers
        k: Number of top frequent elements to return

    Returns:
        List of k most frequent elements

    Example:
        >>> topKFrequentSorting([1,1,1,2,2,3], 2)
        [1, 2]
    """
    # Count frequencies
    freq_map = Counter(nums)

    # Sort by frequency (descending) and take top k
    sorted_items = sorted(freq_map.items(), key=lambda x: x[1], reverse=True)

    return [num for num, freq in sorted_items[:k]]


def topKFrequentHeap(nums: List[int], k: int) -> List[int]:
    """
    Approach 2: Using Min Heap

    Time Complexity: O(n log k) - heap operations are O(log k), done n times
    Space Complexity: O(n + k) - frequency map + heap

    This is more efficient when k is much smaller than n.

    Args:
        nums: List of integers
        k: Number of top frequent elements to return

    Returns:
        List of k most frequent elements

    Example:
        >>> topKFrequentHeap([1,1,1,2,2,3], 2)
        [1, 2]
    """
    # Count frequencies
    freq_map = Counter(nums)

    # Use min heap of size k
    # Heap stores (frequency, number) tuples
    min_heap = []

    for num, freq in freq_map.items():
        heapq.heappush(min_heap, (freq, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # Remove smallest frequency

    # Extract numbers from heap
    return [num for freq, num in min_heap]


def topKFrequentBucketSort(nums: List[int], k: int) -> List[int]:
    """
    Approach 3: Using Bucket Sort (Optimal!)

    Time Complexity: O(n) - linear time!
    Space Complexity: O(n) - for buckets

    This achieves O(n) by using bucket sort where index = frequency.

    Args:
        nums: List of integers
        k: Number of top frequent elements to return

    Returns:
        List of k most frequent elements

    Example:
        >>> topKFrequentBucketSort([1,1,1,2,2,3], 2)
        [1, 2]
    """
    # Count frequencies
    freq_map = Counter(nums)

    # Create buckets: bucket[i] contains all numbers with frequency i
    # Maximum frequency is len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]

    for num, freq in freq_map.items():
        buckets[freq].append(num)

    # Collect top k elements from highest frequency buckets
    result = []
    for freq in range(len(buckets) - 1, 0, -1):  # Start from highest frequency
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

    return result


def topKFrequentPythonic(nums: List[int], k: int) -> List[int]:
    """
    Approach 4: Pythonic one-liner using Counter.most_common()

    Time Complexity: O(n log k) - uses heap internally
    Space Complexity: O(n)

    Most readable and concise solution.

    Args:
        nums: List of integers
        k: Number of top frequent elements to return

    Returns:
        List of k most frequent elements

    Example:
        >>> topKFrequentPythonic([1,1,1,2,2,3], 2)
        [1, 2]
    """
    return [num for num, freq in Counter(nums).most_common(k)]


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([1, 1, 1, 2, 2, 3], 2),
        ([1], 1),
        ([1, 2], 2),
        ([4, 1, -1, 2, -1, 2, 3], 2),
        ([1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4], 3),
    ]

    methods = [
        ("Sorting (O(n log n))", topKFrequentSorting),
        ("Min Heap (O(n log k))", topKFrequentHeap),
        ("Bucket Sort (O(n)) - OPTIMAL", topKFrequentBucketSort),
        ("Pythonic Counter.most_common()", topKFrequentPythonic),
    ]

    for method_name, method in methods:
        print(f"\n{method_name}")
        print("=" * 60)
        for i, (nums, k) in enumerate(test_cases, 1):
            result = method(nums, k)
            print(f"Test {i}: nums={nums}, k={k}")
            print(f"Result: {result}")
            print()

    # Performance comparison explanation
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    print("""
When to use each approach:

1. Sorting O(n log n):
   - Simple to understand and implement
   - Good for small datasets
   - NOT optimal for large datasets

2. Min Heap O(n log k):
   - Best when k << n (k much smaller than n)
   - Example: k=10, n=1,000,000
   - Saves space and time compared to sorting

3. Bucket Sort O(n):
   - OPTIMAL time complexity
   - Best for competitive programming
   - Requires extra O(n) space

4. Pythonic Counter.most_common():
   - Most readable and maintainable
   - Good for production code
   - Uses heap internally (O(n log k))
   - Recommended for most real-world cases
    """)
