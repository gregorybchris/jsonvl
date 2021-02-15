# jsonvl

JSON validation for Python.

## Installation

Install the current PyPI release:

```bash
pip install jsonvl
```

Or install from source:

```bash
pip install git+https://github.com/gregorybchris/jsonvl
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
