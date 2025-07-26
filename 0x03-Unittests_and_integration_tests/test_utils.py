#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""

import unittest
from typing import Any, Mapping, Tuple
from parameterized import parameterized

from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Tuple[str, ...],
        expected: Any
    ) -> None:
        """It should return the correct value from the nested map."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
        
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping[str, Any],
        path: Tuple[str, ...],
        missing_key: str
    ) -> None:
        """It should raise KeyError with the correct missing key."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{missing_key}'")

if __name__ == '__main__':
    unittest.main()