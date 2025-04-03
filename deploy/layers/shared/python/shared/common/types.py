"""
common colleciton of types.
"""

from typing import Literal
from pydantic.dataclasses import dataclass


LogLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


@dataclass
class Secret:
    """
    provides data types for a SecretsManager secret.
    """

    secret_name: str
    secret_string: str


@dataclass
class AppConfig:
    """
    provides data types for the app config.
    """

    secret_id: str
    environment: str
    log_level: str
    app_name: str
    api_endpoint: str
    api_key: str
    aws_region: str
    bucket_name: str


@dataclass
class RecurlyResponse:
    status_code: int
