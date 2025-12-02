"""
Encode and Decode Strings

Design an algorithm to encode a list of strings to a single string.
The encoded string is then decoded back to the original list of strings.

Challenge: Handle strings that may contain ANY characters including delimiters.

Example:
    Input: ["hello", "world"]
    Encode: "5#hello5#world"
    Decode: ["hello", "world"]
"""

from typing import List


class Codec1:
    """
    Approach 1: Length Prefix Encoding (Most Robust!)

    Format: length + delimiter + string
    Example: "5#hello5#world"

    Time Complexity: O(n) for both encode and decode
    Space Complexity: O(n)

    Pros: Handles ANY characters (including special chars, delimiters, etc.)
    """

    def encode(self, strs: List[str]) -> str:
        """
        Encodes a list of strings to a single string.

        Format: len(s)#s for each string
        Example: ["abc", "de"] → "3#abc2#de"
        """
        encoded = ""
        for s in strs:
            encoded += str(len(s)) + "#" + s
        return encoded

    def decode(self, s: str) -> List[str]:
        """
        Decodes a single string back to a list of strings.

        Algorithm:
        1. Read length until we hit '#'
        2. Read exactly that many characters
        3. Repeat until end of string
        """
        decoded = []
        i = 0

        while i < len(s):
            # Find the delimiter '#'
            j = i
            while s[j] != '#':
                j += 1

            # Extract length
            length = int(s[i:j])

            # Extract string of that length
            string = s[j + 1 : j + 1 + length]
            decoded.append(string)

            # Move to next encoded string
            i = j + 1 + length

        return decoded


class Codec2:
    """
    Approach 2: Escape Character Encoding

    Format: Use delimiter and escape special occurrences
    Example: ["a,b", "c"] → "a\\,b,c"

    Time Complexity: O(n)
    Space Complexity: O(n)

    Cons: More complex, harder to handle edge cases
    """

    def encode(self, strs: List[str]) -> str:
        """
        Encodes using comma as delimiter and backslash as escape.
        """
        if not strs:
            return ""

        encoded = []
        for s in strs:
            # Escape backslashes and commas
            escaped = s.replace("\\", "\\\\").replace(",", "\\,")
            encoded.append(escaped)

        return ",".join(encoded)

    def decode(self, s: str) -> List[str]:
        """
        Decodes by handling escaped characters.
        """
        if not s:
            return []

        decoded = []
        current = ""
        i = 0

        while i < len(s):
            if s[i] == "\\":
                # Escaped character - add next char literally
                if i + 1 < len(s):
                    current += s[i + 1]
                    i += 2
            elif s[i] == ",":
                # Delimiter - finish current string
                decoded.append(current)
                current = ""
                i += 1
            else:
                current += s[i]
                i += 1

        # Don't forget last string
        decoded.append(current)
        return decoded


class Codec3:
    """
    Approach 3: Non-ASCII Delimiter (Simple but Limited)

    Format: Use a character unlikely to appear in strings
    Example: ["hello", "world"] → "hello†world"

    Time Complexity: O(n)
    Space Complexity: O(n)

    Cons: Fails if strings contain the delimiter character
    """

    DELIMITER = chr(257)  # Non-ASCII character

    def encode(self, strs: List[str]) -> str:
        """
        Encodes using a special delimiter character.
        """
        return self.DELIMITER.join(strs)

    def decode(self, s: str) -> List[str]:
        """
        Decodes by splitting on delimiter.
        """
        if not s:
            return []
        return s.split(self.DELIMITER)


class Codec4:
    """
    Approach 4: Chunked Encoding (Python-specific)

    Uses Python's str.encode() and bytes representation.
    Most Pythonic but not language-agnostic.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    def encode(self, strs: List[str]) -> str:
        """
        Encodes using length prefix with format: len:string
        """
        parts = []
        for s in strs:
            parts.append(f"{len(s)}:{s}")
        return "".join(parts)

    def decode(self, s: str) -> List[str]:
        """
        Decodes by reading length prefix.
        """
        decoded = []
        i = 0

        while i < len(s):
            # Find the colon
            colon_pos = s.find(":", i)
            length = int(s[i:colon_pos])

            # Extract string
            start = colon_pos + 1
            decoded.append(s[start:start + length])

            # Move to next
            i = start + length

        return decoded


def test_codec(codec_class, test_cases):
    """Helper function to test a codec."""
    codec = codec_class()

    for i, test in enumerate(test_cases, 1):
        encoded = codec.encode(test)
        decoded = codec.decode(encoded)

        status = "✓" if decoded == test else "✗"
        print(f"  Test {i} {status}")
        print(f"    Input:   {test}")
        print(f"    Encoded: {repr(encoded)}")
        print(f"    Decoded: {decoded}")
        print()


if __name__ == "__main__":
    # Comprehensive test cases
    test_cases = [
        # Basic cases
        ["hello", "world"],
        [""],
        ["", ""],
        ["a"],

        # Edge cases with special characters
        ["a,b", "c,d"],  # Contains delimiter
        ["a#b", "c#d"],  # Contains # (length delimiter)
        ["\\", "/"],     # Contains backslash

        # Complex strings
        ["Hello, World!", "Python#123", "Test:Case"],
        ["multi\nline\nstring", "with\ttabs"],

        # Empty strings mixed
        ["", "abc", "", "def", ""],

        # Very long string
        ["a" * 1000, "b"],
    ]

    codecs = [
        ("Length Prefix Encoding (RECOMMENDED)", Codec1),
        ("Escape Character Encoding", Codec2),
        ("Non-ASCII Delimiter", Codec3),
        ("Chunked Encoding (Pythonic)", Codec4),
    ]

    for codec_name, codec_class in codecs:
        print("=" * 70)
        print(f"{codec_name}")
        print("=" * 70)
        test_codec(codec_class, test_cases)

    # Demonstrate the robustness of Length Prefix
    print("\n" + "=" * 70)
    print("WHY LENGTH PREFIX IS BEST")
    print("=" * 70)
    print("""
The Length Prefix approach (Codec1) is the most robust because:

1. Handles ANY characters:
   - Works with ",", "#", "\\", newlines, tabs, unicode, etc.
   - No escaping needed!

2. Simple and efficient:
   - O(n) encode and decode
   - No complex escape logic

3. Language-agnostic:
   - Can be implemented in any programming language
   - Clear specification

4. Example with tricky input:
""")

    tricky = ["#,\\", "a:b", "x\ny\tz"]
    codec = Codec1()
    encoded = codec.encode(tricky)
    decoded = codec.decode(encoded)

    print(f"   Input:   {tricky}")
    print(f"   Encoded: {repr(encoded)}")
    print(f"   Decoded: {decoded}")
    print(f"   Match:   {decoded == tricky} ✓")
