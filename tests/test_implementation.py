import unittest
from unittest.mock import MagicMock, patch

from pypopulation import implementation as imp

mock_a2_map = {"AA": 1}
mock_a3_map = {"BBB": 2}

mock_initialize = MagicMock(return_value=(mock_a2_map, mock_a3_map))


class TestImplementation(unittest.TestCase):
    """Test the implementation module."""

    def setUp(self) -> None:
        """
        Clear LRU caches.

        Ensure that nothing is cached before each test.
        """
        imp._load_file.cache_clear()
        imp._initialize.cache_clear()

    # region: resource file

    def test_file_exists(self):
        """Resource file exists and lives where expected."""
        self.assertTrue(imp.DATAFILE.exists())
        self.assertTrue(imp.DATAFILE.is_file())

    def test_file_loads(self):
        """Resource file is valid JSON and loads into a Python list."""
        obj = imp._load_file()
        self.assertIsInstance(obj, list)

    def test_file_is_cached(self):
        """Resource file is cached after first load."""
        obj_a = imp._load_file()
        obj_b = imp._load_file()
        self.assertIs(obj_a, obj_b)

    # endregion
    # region: map initialization

    def test_map_init(self):
        """Country maps initialize from the resource file."""
        a2_map, a3_map = imp._initialize()
        self.assertIsInstance(a2_map, dict)
        self.assertIsInstance(a3_map, dict)

    def test_map_is_cached(self):
        """Country maps are cached and do not re-build on re-query."""
        a2_map_a, a3_map_a = imp._initialize()
        a2_map_b, a3_map_b = imp._initialize()
        self.assertIs(a2_map_a, a2_map_b)
        self.assertIs(a3_map_a, a3_map_b)

    # endregion
