#!/usr/bin/env python3
"""File:test_utils.py"""
# Author: Givens Emmah Abraham
"""Run utils module"""


from typing import Any, Dict
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """Run access nested map Object"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Run Access nested map with key path"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ('a', ), KeyError('a')),
        ({'a': 1}, ('a', 'b'), KeyError('b')),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Run Access nested map with exception"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        exception_message = str(context.exception)
        self.assertEqual(exception_message, str(expected))


class TestGetJson(unittest.TestCase):
    """Run GetJSON method"""

    @parameterized.expand([
        ('http://example.com', {'payload': True}),
        ('http://holberton.io', {'payload': False})
    ])
    def test_get_json(self, test_url: str, test_payload:
                      Dict[str, Any]) -> None:
        """Run that utils.get_json returns the expected result"""
        json_return = {'json.return_value': test_payload}
        with patch('requests.get', return_value=Mock(**json_return)) as\
                mock_get:
            self.assertEqual(get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Run utils.memoize method"""

    def test_memoize(self) -> None:
        """Run that utils.memoize memoizes a result"""
        class TestClass:
            """Run class doc"""

            def a_method(self) -> int:
                """a_method method"""
                return 42

            @memoize
            def a_property(self) -> int:
                """a_property method"""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=lambda: 42) as\
                mock_method:
            test = TestClass()

            instance1 = test.a_property()
            instance2 = test.a_property()

            self.assertEqual(instance1, 42)
            self.assertEqual(instance2, 42)

            mock_method.assert_called_once()
