"""Root module for jsonvl."""
from jsonvl.core.validation import validate, validate_file
from jsonvl.core.validator import Validator


__all__ = ['Validator', 'validate', 'validate_file']
