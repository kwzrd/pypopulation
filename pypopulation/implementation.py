import json
import typing as t
from pathlib import Path

DATAFILE = Path(__file__).parent.joinpath("resources", "countries.json")

PopulationMap = t.Dict[str, int]  # From country code to its population


def _initialize() -> t.Tuple[PopulationMap, PopulationMap]:
    """Init Alpha-2 and Alpha-3 maps from `DATAFILE`."""
    with DATAFILE.open(mode="r", encoding="UTF-8") as datafile:
        country_list: t.List[t.Dict] = json.load(datafile)

    alpha_2: PopulationMap = {}
    alpha_3: PopulationMap = {}

    for country in country_list:
        a2, a3, pop = country["Alpha_2"], country["Alpha_3"], country["Population"]
        alpha_2[a2] = pop
        alpha_3[a3] = pop

    return alpha_2, alpha_3


a2_map, a3_map = _initialize()


def get_population(country_code: str) -> t.Optional[int]:
    """
    Get population for either Alpha-2 or Alpha-3 `country_code`.

    None if `country_code` does not exist in either map.
    """
    return a2_map.get(country_code) or a3_map.get(country_code)


def get_population_a2(country_code: str) -> t.Optional[int]:
    """
    Get population for Alpha-2 `country_code`.

    None if `country_code` does not exist in the map.
    """
    return a2_map.get(country_code)


def get_population_a3(country_code: str) -> t.Optional[int]:
    """
    Get population for Alpha-3 `country_code`.

    None if `country_code` does not exist in the map.
    """
    return a3_map.get(country_code)
