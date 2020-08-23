import unittest

from pypopulation.implementation import DATAFILE


class TestCountries(unittest.TestCase):
    """Test the `resources.json` data file."""

    def test_exists(self):
        """The resource file lives where expected."""
        self.assertTrue(DATAFILE.exists())
