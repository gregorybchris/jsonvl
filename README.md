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

### Roadmap

- [x] Number, string, boolean, and null primitives
- [x] Array and object collections
- [x] Number constraints
- [ ] Path traversal for multi-level constraints
- [ ] Exists and forall quantifiers for array traversal
- [ ] Conditional validation
- [ ] Union types
- [ ] Type definitions and references
- [ ] Custom constraints
