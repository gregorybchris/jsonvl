# JsonVL

[![GitHub CI](https://github.com/gregorybchris/jsonvl/workflows/JsonVL-CI/badge.svg?branch=main)](https://github.com/gregorybchris/jsonvl/actions?query=workflow%3AJsonVL-CI)
[![codecov](https://codecov.io/gh/gregorybchris/jsonvl/branch/main/graph/badge.svg?token=S8VQAMZ2OP)](https://codecov.io/gh/gregorybchris/jsonvl)

JsonVL is a JSON validator for Python. This project is intended to be a replacement for the [jsonschema package](https://pypi.org/project/jsonschema/) which implements the [JSON Schema standard](https://json-schema.org/). JsonVL's goal is to curate a rich set of validation methods for JSON data types while remaining extensible to new constraints.

## Installation

Install the latest [PyPI release](https://pypi.org/project/jsonv/):

```bash
pip install jsonvl
```

## Usage

### Validate JSON files from the command line

```bash
jsonvl data.json schema.json
```

### Validate JSON files in Python

```python
from jsonvl import validate_file

validate_file('data.json', 'schema.json')
```

### Validate in-memory JSON data in Python

```python
from jsonvl import validate

validate(data, schema)
```

## Documentation

The JsonVL documentation is hosted by [Read the Docs](https://jsonvl.readthedocs.io) and is a work in progress.

## Example

Below is an example pair of JSON data and JSON schema. More examples can be found in the [examples](./examples) folder.

### Data

```json
{
  "play": "A Midsummer Night's Dream",
  "characters": [
    { "name": "Helena", "loves": ["Demitrius"] },
    { "name": "Demitrius", "loves": ["Hermia", "Helena"] },
    { "name": "Hermia", "loves": ["Lysander"] },
    { "name": "Lysander", "loves": ["Hermia", "Helena", "Hermia"] },
    { "name": "Titania", "loves": ["Oberon", "Bottom", "Oberon"] },
    { "name": "Oberon", "loves": ["Titania"] },
    { "name": "Bottom", "loves": [] },
    { "name": "Puck", "loves": [] }
  ]
}
```

### Schema

```json
{
  "type": "object",
  "attr": {
    "play": "string",
    "characters": {
      "type": "array",
      "cons": {
        "unique": "@all.name"
      },
      "elem": {
        "type": "object",
        "attr": {
          "name": "#name",
          "loves": {
            "type": "array",
            "elem": "#name",
            "cons": { "max_size": 4 }
          }
        }
      }
    }
  },
  "defs": {
    "#name": {
      "type": "string",
      "cons": {
        "format": { "type": "regex", "pattern": "[A-Z][a-z]{0,10}" }
      }
    }
  }
}
```
