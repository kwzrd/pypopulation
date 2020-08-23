![Lint & Tests](https://github.com/kwzrd/pypopulation/workflows/Lint%20&%20Tests/badge.svg)

# pypopulation

## Data source

The population figures were sourced from [The World Bank](https://data.worldbank.org/indicator/SP.POP.TOTL) (`2020-07-01`). This dataset provides the country name, alpha-3 code, and population figures found in the resource JSON file. The data was enriched with alpha-2 country codes for each row. Rows not corresponding to political countries were removed, e.g. "Middle East & North Africa (excluding high income)". Some country names were adjusted for readability, e.g. expanded abbreviations. **No adjustments were made to the population figures**. Please refer to the linked page for a more detailed description of the dataset.

This projects aims to expose the linked data to Python code. It does not guarantee correctness of the provided figures.
