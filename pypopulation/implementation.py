import functools
import json
import typing as t
from pathlib import Path

DATAFILE = Path(__file__).parent.joinpath("resources", "countries.json")

PopulationMap = t.Dict[str, int]  # From country code to its population


@functools.lru_cache(maxsize=1)
def _load_file() -> t.List[t.Dict]:
    """Load `DATAFILE` into a Python list object."""
    with DATAFILE.open(mode="r", encoding="UTF-8") as datafile:
        return json.load(datafile)


@functools.lru_cache(maxsize=1)
def _initialize() -> t.Tuple[PopulationMap, PopulationMap]:
    """Init Alpha-2 and Alpha-3 maps from `DATAFILE`."""
    country_list = _load_file()

    alpha_2: PopulationMap = {}
    alpha_3: PopulationMap = {}

    for country in country_list:
        a2, a3, pop = country["Alpha_2"], country["Alpha_3"], country["Population"]
        alpha_2[a2] = pop
        alpha_3[a3] = pop

    return alpha_2, alpha_3


def _normalize(country_code: str) -> str:
    """Normalize `country_code` casing."""
    return country_code.upper()


def get_population(country_code: str) -> t.Optional[int]:
    """
    Get population for either Alpha-2 or Alpha-3 `country_code` caseless.

    None if `country_code` does not exist in either map.
    """
    return get_population_a2(country_code) or get_population_a3(country_code)


def get_population_a2(country_code: str) -> t.Optional[int]:
    """
    Get population for Alpha-2 `country_code` caseless.

    None if `country_code` does not exist in the map.
    """
    a2_map, _ = _initialize()
    return a2_map.get(_normalize(country_code))


def get_population_a3(country_code: str) -> t.Optional[int]:
    """
    Get population for Alpha-3 `country_code` caseless.

    None if `country_code` does not exist in the map.
    """
    _, a3_map = _initialize()
    return a3_map.get(_normalize(country_code))
