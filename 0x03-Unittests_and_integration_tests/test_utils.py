#!/usr/bin/env python3
from unittest import TestCase
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from unittest.mock import patch

from utils import access_nested_map, get_json, memoize


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

    @parameterized.expand([
        ({},       ("a",),       "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected_message: str
    ) -> None:
        """
        Test that access_nested_map raises a KeyError for invalid paths.
        Uses assertRaises context manager to check the exception and its message.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(TestCase):
    """
    Test cases for get_json function.
    Mocks HTTP calls to avoid external requests.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Any) -> None:
        """
        Test that get_json returns the expected payload and that requests.get
        is called exactly once with the correct URL.
        """
        with patch('utils.requests.get') as mock_get:
            mock_get.return_value.json.return_value = test_payload
            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(TestCase):
    """
    Test cases for memoize decorator.
    Ensures that the decorated method caches its result.
    """

    def test_memoize(self) -> None:
        """
        Define a TestClass with a memoized property and ensure
        the underlying method is called only once across multiple accesses.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42
            test_instance = TestClass()

            first = test_instance.a_property
            second = test_instance.a_property

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_a_method.assert_called_once()


if __name__ == "__main__":
    import unittest
    unittest.main()
