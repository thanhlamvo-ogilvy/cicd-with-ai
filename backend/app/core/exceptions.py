"""Domain-specific exceptions for the application.

These exceptions represent business logic errors and should be caught
and converted to HTTP responses at the API layer, not in services.
"""


class AppError(Exception):
    """Base exception for all application errors."""


class ConversationNotFoundError(AppError):
    """Raised when a conversation cannot be found."""


class ProviderConfigurationError(AppError):
    """Raised when an AI provider is not properly configured."""


class ProviderNotFoundError(AppError):
    """Raised when requesting an unknown AI provider."""
