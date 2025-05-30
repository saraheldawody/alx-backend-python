#!/usr/bin/env python3
from unittest import TestCase
from parameterized import parameterized
from utils import access_nested_map
from typing import Mapping, Sequence, Any
class TestAccessNestedMap(TestCase):
    """
    Test cases for access_nested_map function.
    This class inherits from unittest.TestCase and uses parameterized tests
    to check various scenarios of accessing nested maps.
    It tests the function with different nested map structures and paths
    to ensure it returns the expected values.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """
        Test access_nested_map with various inputs.
        This method uses parameterized tests to check that the function
        returns the expected result for different nested map structures
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
        
        
if __name__ == "__main__":
    import unittest
    unittest.main()
