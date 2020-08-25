![Lint & Tests](https://github.com/kwzrd/pypopulation/workflows/Lint%20&%20Tests/badge.svg)

# pypopulation

Lightweight population lookup using [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166) alpha-1/2 country codes for **Python 3.5** and higher.

```python
>>> import pypopulation
>>> 
>>> pypopulation.get_population("DE")  # Germany
83132799
```

The aim is to provide a minimalist package with no dependencies that does one thing only, as best as possible. Population figures are read from a JSON file into Python dictionaries on the first lookup, _not_ at import time. The API then only exposes the dictionaries.

**The given figures are estimates at best.** Read below for more details on the data source.

## Interface

The API is formed by 3 functions:
* `get_population_a2`: population for a 2-letter country code
* `get_population_a3`: population for a 3-letter country code
* `get_population`: population for either either a 2-letter or a 3-letter country code

All functions return `None` if no country is found for the given country code. **Lookup is case insensitive**, i.e. `"DE"` and `"de"` give same results.

Lookups using country names are difficult & not currently supported, but the source JSON file does contain them. This is to make the source file more comprehensible. If all you have to work with is a country name, consider using [`pycountry`](https://pypi.org/project/pycountry/) to resolve your names to ISO 3166 codes first.

If you would like to build your own wrapper around the source JSON, you can do:
```python
countries: t.List[t.Dict] = pypopulation._load_file()
```

**Note**: This function is wrapped in `functools.lru_cache(max_size=1)`. 

## Installation

With `pip` from [PyPI](https://pypi.org/):

```
pip install pypopulation
```

## Development

I'm using [`Pipenv`](https://github.com/pypa/pipenv) to maintain development dependencies.

* `pipenv sync --dev`: create venv with dev deps
* `pipenv run lint`: run `Flake8` & friends
* `pipenv run test`: run `unittest` suite and produce a `.coverage` file

## Data source

The population figures were sourced from [The World Bank](https://data.worldbank.org/indicator/SP.POP.TOTL) (`2020-07-01`). This dataset provides the country name, alpha-3 code, and population figures found in the resource JSON file. The data was enriched with alpha-2 country codes for each row. Rows not corresponding to political countries were removed, e.g. "Middle East & North Africa (excluding high income)". Some country names were adjusted for readability, e.g. expanded abbreviations. **No adjustments were made to the population figures**. Please refer to the linked page for a more detailed description of the dataset.

This projects aims to expose the linked data to Python code. It does not guarantee correctness of the provided figures.
