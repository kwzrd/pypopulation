import unittest

from pypopulation import implementation as imp


class TestImplementation(unittest.TestCase):
    """Test the implementation module."""

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
