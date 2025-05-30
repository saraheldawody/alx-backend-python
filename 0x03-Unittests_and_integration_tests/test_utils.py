"""
0. Parameterize a unit test
mandatory
Familiarize yourself with the utils.access_nested_map function and understand its purpose. Play with it in the Python console to make sure you understand.

In this task you will write the first unit test for utils.access_nested_map.

Create a TestAccessNestedMap class that inherits from unittest.TestCase.

Implement the TestAccessNestedMap.test_access_nested_map method to test that the method returns what it is supposed to.

Decorate the method with @parameterized.expand to test the function for following inputs:

nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")
For each of these inputs, test with assertEqual that the function returns the expected result.

The body of the test method should not be longer than 2 lines.

Repo:

GitHub repository: alx-backend-python
Directory: 0x03-Unittests_and_integration_tests
File: test_utils.py
"""

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
