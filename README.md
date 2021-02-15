# jsonvl

jsonvl is a JSON validator for Python. This project is intended to be a replacement for the [jsonschema package](https://pypi.org/project/jsonschema/) which implements the [JSON Schema standard](https://json-schema.org/). jsonvl's goal is to curate a rich set of constraints for JSON data types while remaining extensible to arbitrary data constraints.

> Note: This package is a **work in progress** and contributions are welome.

## Installation

Install the current PyPI release:

```bash
pip install jsonvl
```

## Usage

### Validate JSON from the command line

```bash
jsonvl data.json schema.json
```

### Validate JSON in Python

```python
from jsonvl import validate_file

validate_file('data.json', 'schema.json')
```

## Roadmap

- [x] JSON data type checking
  - [x] Number, string, boolean, and null primitives
  - [x] Array and object collections
- [x] Number constraints
  - [x] lt
  - [x] gt
  - [x] eq
- [x] String constraints
  - [x] in
  - [x] eq
  - [x] format
    - [x] regex
    - [x] phone
    - [x] email
- [x] Array constraints
  - [x] max_size
  - [x] min_size
  - [x] unique
- [x] Path traversal for multi-level constraints
- [x] Quantifiers for array traversal
- [ ] Type definitions and references
- [ ] Conditional validation
- [ ] Union types (including nullable)
- [ ] Custom constraints

## Example

### Data

```json
{
  "play": "A Midsummer Night’s Dream",
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
  "attrs": {
    "play": "string",
    "characters": {
      "type": "array",
      "cons": {
        "unique": "@all.name"
      },
      "elem": {
        "type": "object",
        "attrs": {
          "name": {
            "type": "string",
            "cons": {
              "format": { "type": "regex", "pattern": "[A-Z][a-z]{0,10}" }
            }
          },
          "loves": {
            "type": "array",
            "elem": "string",
            "cons": { "max_size": 4 }
          }
        }
      }
    }
  }
}
```
