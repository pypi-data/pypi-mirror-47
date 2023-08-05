"""Validation rules."""
import re
from schema import SchemaError

class Mandatory:  # noqa: pylint - too-few-public-methods
    """Validation rule to check if the given mandatory value exists."""

    @staticmethod
    def validate(value=None):
        """
        Check if the given mandatory value exists.

        Args:
            value (any): Value to be validated.
        """
        return value is not None


class RegexValidator:  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a value matches a regular expression."""

    def __init__(self, regex=''):
        """
        Compile a regular expression to a regular expression pattern.

        Args:
            regex (str): Regular expression for parameter validation.
        """
        self._regexp = re.compile(regex)

    def validate(self, value=None):
        """
        Check if a value adheres to the defined regular expression.

        Args:
            value (str): Value to be validated.
        """
        return self._regexp.search(value) is not None


class SchemaValidator:  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a value matches a regular expression."""

    def __init__(self, schema):
        """
        Set the schema field.

        Args:
            schema (Schema): The expected schema.
        """
        self._schema = schema

    def validate(self, value=None):
        """
        Check if the object adheres to the defined schema.

        Args:
            value (object): Value to be validated.
        """
        try:
            return self._schema.validate(value) == value
        except SchemaError:
            return False
