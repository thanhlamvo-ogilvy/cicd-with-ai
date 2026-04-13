"""Domain-specific exceptions for the application.

These exceptions represent business logic errors and should be caught
and converted to HTTP responses at the API layer, not in services.
"""


class AppException(Exception):
    """Base exception for all application errors."""


class ConversationNotFoundError(AppException):
    """Raised when a conversation cannot be found."""


class ProviderConfigurationError(AppException):
    """Raised when an AI provider is not properly configured."""


class ProviderNotFoundError(AppException):
    """Raised when requesting an unknown AI provider."""

