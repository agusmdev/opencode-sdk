"""Base model configuration for all SDK models."""

from pydantic import BaseModel, ConfigDict


class OpenCodeModel(BaseModel):
    """
    Base model for all SDK models.

    Provides consistent configuration across all models:
    - Allows population by field name or alias (for camelCase API responses)
    - Validates on assignment for data integrity
    - Uses enum values instead of enum objects for serialization
    - Ignores extra fields from API responses (forward-compatible)
    """

    model_config = ConfigDict(
        # Allow population by field name or alias
        populate_by_name=True,
        # Validate on assignment
        validate_assignment=True,
        # Use enum values
        use_enum_values=True,
        # Ignore extra fields from API (forward-compatible)
        extra="ignore",
        # Use attribute docstrings for field descriptions
        use_attribute_docstrings=True,
    )


class InputModel(BaseModel):
    """
    Base model for request input models.

    Stricter configuration for user inputs:
    - Forbids extra fields to catch typos
    - Same alias handling as OpenCodeModel
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        use_enum_values=True,
        # Forbid extra fields to catch user errors
        extra="forbid",
        use_attribute_docstrings=True,
    )
