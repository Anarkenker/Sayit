class InputResolutionError(RuntimeError):
    """Raised when user-provided input cannot be loaded cleanly."""


class EmptyInputError(InputResolutionError):
    """Raised when an input source exists but contains no text."""


class ClipboardUnavailableError(InputResolutionError):
    """Raised when the current environment cannot access the clipboard."""
