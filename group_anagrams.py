"""
Group Anagrams

Given an array of strings strs, group the anagrams together.
An anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
typically using all the original letters exactly once.

Time Complexity: O(n * k log k) where n is the number of strings and k is the max length of a string
Space Complexity: O(n * k) for storing the grouped anagrams
"""

from collections import defaultdict
from typing import List


def groupAnagrams(strs: List[str]) -> List[List[str]]:
    """
    Groups anagrams together using sorted string as key.

    Args:
        strs: List of strings to group

    Returns:
        List of grouped anagrams

    Example:
        >>> groupAnagrams(["eat","tea","tan","ate","nat","bat"])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    """
    anagram_map = defaultdict(list)

    for s in strs:
        # Sort the string to create a key
        # All anagrams will have the same sorted key
        key = ''.join(sorted(s))
        anagram_map[key].append(s)

    return list(anagram_map.values())


def groupAnagramsOptimized(strs: List[str]) -> List[List[str]]:
    """
    Groups anagrams using character count as key (avoids sorting).

    Time Complexity: O(n * k) where n is the number of strings and k is the max length
    Space Complexity: O(n * k)

    Args:
        strs: List of strings to group

    Returns:
        List of grouped anagrams

    Example:
        >>> groupAnagramsOptimized(["eat","tea","tan","ate","nat","bat"])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    """
    anagram_map = defaultdict(list)

    for s in strs:
        # Create a count array for 26 lowercase letters
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1

        # Use tuple of counts as key (lists can't be dict keys)
        key = tuple(count)
        anagram_map[key].append(s)

    return list(anagram_map.values())


if __name__ == "__main__":
    # Test cases
    test_cases = [
        ["eat", "tea", "tan", "ate", "nat", "bat"],
        [""],
        ["a"],
        ["ab", "ba", "abc", "cba", "bac", "cab"],
    ]

    print("Method 1: Using Sorted String as Key")
    print("=" * 50)
    for i, test in enumerate(test_cases, 1):
        result = groupAnagrams(test)
        print(f"Test {i}: {test}")
        print(f"Result: {result}")
        print()

    print("\nMethod 2: Using Character Count as Key (Optimized)")
    print("=" * 50)
    for i, test in enumerate(test_cases, 1):
        result = groupAnagramsOptimized(test)
        print(f"Test {i}: {test}")
        print(f"Result: {result}")
        print()
