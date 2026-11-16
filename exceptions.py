class WhatShouldIEatError(Exception):
    """Base class for all custom errors in this project."""


class RecipeDataError(WhatShouldIEatError):
    """Raised when the recipe file is missing, unreadable or malformed."""


class InvalidInputError(WhatShouldIEatError):
    """Raised when the user provides invalid input."""
