class AlreadyPlacedExcpetion(Exception):
    """Will raise when the piece is already palced"""

    def __init__(self):
        super().__init__("The position has already been taken")

class ValidationError(Exception):
    """The exception will be raised when a validation failed in models"""

    def __init__(self, message):
        super().__init__(message)