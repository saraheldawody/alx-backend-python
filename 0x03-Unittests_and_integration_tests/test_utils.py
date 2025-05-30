#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from unittest.mock import patch

from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class TestAccessNestedMap(unittest.TestCase):
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
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """
        Test access_nested_map with various inputs.
        This method uses parameterized tests to check that the function
        returns the expected result for different nested map structures
        """
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected
        )

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected_msg: str
    ) -> None:
        """
        Test access_nested_map with invalid paths.
        This method uses parameterized tests to check that the function
        raises a KeyError with the expected message when trying to access
        a key that does not exist in the nested map.
        """
        with self.assertRaises(KeyError) as ctx:
            access_nested_map(nested_map, path)

        self.assertEqual(
            str(ctx.exception),
            expected_msg
        )


class TestGetJson(unittest.TestCase):
    """
    Test cases for get_json function.
    This class inherits from unittest.TestCase and uses parameterized tests
    to check the behavior of the function when fetching JSON data from URLs.
    It mocks the requests.get method to simulate different responses
    and checks that the function returns the expected JSON data.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        url: str,
        payload: Any
    ) -> None:
        """
        Test get_json with mocked requests.
        This method uses parameterized tests to check that the function
        correctly fetches JSON data from a URL and returns it.
        It mocks the requests.get method to return a predefined JSON payload.
        """
        with patch('utils.requests.get') as mock_get:
            mock_get.return_value.json.return_value = payload
            result = get_json(url)

            mock_get.assert_called_once_with(url)
            self.assertEqual(result, payload)


class TestMemoize(unittest.TestCase):
    """
    Test cases for memoize decorator.
    This class inherits from unittest.TestCase and tests the memoize
    decorator to ensure it caches the results of method calls.
    It checks that the method is only called once and that subsequent calls
    return the cached result.
    """

    def test_memoize(self) -> None:
        """
        Test memoize decorator.
        This method tests the memoize decorator by defining a class with
        a method and a property that uses the decorator.
        It checks that the method is called only once and that the property
        returns the cached result on subsequent calls.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42

            obj = TestClass()
            first = obj.a_property
            second = obj.a_property

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
