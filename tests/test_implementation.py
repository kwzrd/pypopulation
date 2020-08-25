import typing as t
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
    # region: lookup methodology (on mock data)

    def check_pairs(self, pairs: t.Iterable[t.Tuple], func: t.Callable):
        """Run `pairs` of input, expected output and compare them against `func` result."""
        for code, expected_population in pairs:
            with self.subTest(code=code, expected_population=expected_population):
                self.assertEqual(expected_population, func(code))

    def test_normalize(self):
        """The `_normalize_` functions makes all strings uppercase."""
        pairs = [("", ""), (" ", " "), ("a", "A"), ("A", "A"), ("aBc", "ABC")]
        self.check_pairs(pairs, imp._normalize)

    def test_general_lookup_not_a_country(self):
        """Check both maps and return None when queried code does not exist."""
        patch_a2 = patch("pypopulation.implementation.get_population_a2", MagicMock(return_value=None))
        patch_a3 = patch("pypopulation.implementation.get_population_a3", MagicMock(return_value=None))

        with patch_a2 as mock_a2, patch_a3 as mock_a3:
            out_value = imp.get_population("not_a_country")

        self.assertIsNone(out_value)
        mock_a2.assert_called_once_with("not_a_country")
        mock_a3.assert_called_once_with("not_a_country")

    def test_general_lookup_ask_a2_a3(self):
        """Check both maps and return population when queried code exists in a3 map."""
        patch_a2 = patch("pypopulation.implementation.get_population_a2", MagicMock(return_value=None))
        patch_a3 = patch("pypopulation.implementation.get_population_a3", MagicMock(return_value=1234))

        with patch_a2 as mock_a2, patch_a3 as mock_a3:
            out_value = imp.get_population("alpha_3")

        self.assertEqual(out_value, 1234)
        mock_a2.assert_called_once_with("alpha_3")
        mock_a3.assert_called_once_with("alpha_3")

    def test_general_lookup_ask_a2_only(self):
        """Check first map only and return population when queried code exists in a2 map."""
        patch_a2 = patch("pypopulation.implementation.get_population_a2", MagicMock(return_value=1234))
        patch_a3 = patch("pypopulation.implementation.get_population_a3", MagicMock(return_value=5678))

        with patch_a2 as mock_a2, patch_a3 as mock_a3:
            out_value = imp.get_population("alpha_2")

        self.assertEqual(out_value, 1234)
        mock_a2.assert_called_once_with("alpha_2")
        mock_a3.assert_not_called()  # In this case, the A3 map is never called

    @patch("pypopulation.implementation._initialize", mock_initialize)
    def test_alpha_2_lookup(self):
        """Find populations for 'AA' but not 'BBB' using `get_population_a2`."""
        none_pairs = [(code, None) for code in ("", "a", "A", "b", "B")]
        good_pairs = [(code, 1) for code in ("aa", "aA", "AA")]
        self.check_pairs(none_pairs + good_pairs, imp.get_population_a2)

    @patch("pypopulation.implementation._initialize", mock_initialize)
    def test_alpha_3_lookup(self):
        """Find populations for 'BBB' but not 'AA' using `get_population_a3`."""
        none_pairs = [(code, None) for code in ("", "a", "A", "b", "B")]
        good_pairs = [(code, 2) for code in ("bbb", "bbB", "BBB")]
        self.check_pairs(none_pairs + good_pairs, imp.get_population_a3)

    # endregion
    # region: lookups on the actual data

    def check_type(self, codes: t.Iterable[str], type_: t.Any, func: t.Callable):
        """Check that all `codes` produce an instance of `type_` when passed to `func`."""
        for country_code in codes:
            with self.subTest(country_code=country_code, expected_type=type_):
                self.assertIsInstance(func(country_code), type_)

    def check_values(self, codes: t.Iterable[str], func: t.Callable):
        """Check that all `codes` produce the same result when passed to `func`."""
        values = set(func(code) for code in codes)
        self.assertEqual(len(values), 1)

    def test_germany(self):
        """The same integer is returned for alternatives of Germany's country code."""
        a2_codes = ["de", "DE", "dE"]
        self.check_type(a2_codes, int, imp.get_population_a2)
        self.check_values(a2_codes, imp.get_population_a2)

        a3_codes = ["deu", "DEU", "dEu"]
        self.check_type(a3_codes, int, imp.get_population_a3)
        self.check_values(a3_codes, imp.get_population_a3)

        all_codes = a2_codes + a3_codes
        self.check_type(all_codes, int, imp.get_population)
        self.check_values(all_codes, imp.get_population)

    def test_non_country(self):
        """None is returned for non-existing countries."""
        non_country_codes = "abcde", "", "e"
        self.check_type(non_country_codes, type(None), imp.get_population)
