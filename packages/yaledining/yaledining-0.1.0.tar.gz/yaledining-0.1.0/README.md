# tbapy [![PyPI version](https://badge.fury.io/py/yaledining.svg)](https://badge.fury.io/py/yaledining)

> Python library for interfacing with the Yale Dining API.

[API documentation](https://developers.yale.edu/yale-dining)

## Setup
First, install the module:

```sh
pip3 install yaledining
```

Then, to use these functions, you must import the `tbapy` module:

```py
import yaledining
```

Before using the library, you must instantiate its class, for example:

```py
dining = yaledining.YaleDining()
```

This API does not require authentication.

The Blue Alliance's API requires that all applications identify themselves with an auth key when retrieving data. To obtain an auth key, visit TBA's [Account page](https://www.thebluealliance.com/account).


## Retrieval Functions
- `get_locations()`
- `get_menus(location_id)`
- `get_nutrition(item_id)`
- `get_traits(item_id)`
- `get_ingredients(item_id)`

See `example.py` for several usage examples.

## Author
[Erik Boesen](https://github.com/ErikBoesen)

## License
[GPL](LICENSE)
