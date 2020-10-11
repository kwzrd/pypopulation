import unittest

from pypopulation import implementation as imp

mock_a2_map = {"AA": 1}
mock_a3_map = {"BBB": 2}


class TestImplementationHelpers(unittest.TestCase):
    """
    Test private helpers in the implementation module.

    In short, this class tests private methods using the production resources file,
    not mocked data. This therefore also makes weak assertions about the resources.
    """

    def test_file_exists(self):
        """Resource path exists and leads to a file."""
        self.assertTrue(imp.DATAFILE.exists())
        self.assertTrue(imp.DATAFILE.is_file())

    def test_load_file(self):
        """Resource file loads into a Python list of dicts."""
        loaded = imp._load_file()
        self.assertIsInstance(loaded, list)
        for expected_dict in loaded:
            self.assertIsInstance(expected_dict, dict)

    def test_initialize(self):
        """Initialize produces two mappings as expected."""
        a2_map, a3_map = imp._initialize()

        def check(dct, key_length):
            """Perform a series of checks on `dct`."""
            for key, value in dct.items():
                self.assertIsInstance(key, str)  # keys must be strings
                self.assertIsInstance(value, int)  # Values must be integers
                self.assertEqual(len(key), key_length)  # Keys must be exactly `key_length` long
                self.assertTrue(key.isupper())  # Keys must be strictly upper-cased

        check(a2_map, 2)
        check(a3_map, 3)

    def test_normalize(self):
        """Normalization returns uppercase strings."""
        cases = [
            ("", ""),
            (" ", " "),
            ("a", "A"),
            ("1a", "1A"),
            ("aAa", "AAA"),
        ]
        for before, after in cases:
            self.assertEqual(imp._normalize(before), after)
