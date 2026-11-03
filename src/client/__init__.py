"""Módulo de integração HTTP com a OpenF1 API."""

from src.client.base import BaseClient, RateLimiter
from src.client.endpoints import OpenF1Client
from src.client.exceptions import (
    APIConnectionError,
    OpenF1Error,
    RateLimitExceededError,
    ResourceNotFoundError,
    SessionNotFoundError,
)

__all__ = [
    "APIConnectionError",
    "BaseClient",
    "OpenF1Client",
    "OpenF1Error",
    "RateLimitExceededError",
    "RateLimiter",
    "ResourceNotFoundError",
    "SessionNotFoundError",
]
