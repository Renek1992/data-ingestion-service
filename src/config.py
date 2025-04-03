"""
Provides the app configuration across different environments.

Note:
-------
Config needs to be expanded if more services are being added and secrets need to be specific.
"""

import os
import ast

import boto3
from abc import ABC, abstractmethod
from shared.common.types import AppConfig, Secret


class ConfigFactory(ABC):
    @abstractmethod
    def create_config(self):
        pass


class LocalConfig(ConfigFactory):
    def create_config(self) -> AppConfig:
        print("Loading LocalConfig...")
        return AppConfig(
            secret_id=os.environ.get("SECRET_ID"),
            environment=os.environ.get("ENVIRONMENT"),
            aws_region=os.environ.get("AWS_REGION"),
            slack_token=os.environ.get("SLACK_TOKEN"),
            log_level=os.environ.get("LOG_LEVEL"),
            app_name=os.environ.get("APP_NAME"),
            api_endpoint=os.environ.get("API_ENDPOINT"),
            api_key=os.environ.get("API_KEY"),
            bucket_name=os.environ.get("BUCKET_NAME"),
        )


class LiveConfig(ConfigFactory):
    def create_config(self) -> AppConfig:
        secret_obj = _load_secret()
        secret_dict = ast.literal_eval(secret_obj.secret_string)
        print("Loading LiveConfig...")
        return AppConfig(
            secret_id=os.environ.get("SECRET_ID"),
            environment=os.environ.get("ENVIRONMENT"),
            aws_region=os.environ.get("AWS_REGION"),
            slack_token=secret_dict["SLACK_TOKEN"],
            log_level=secret_dict["LOG_LEVEL"],
            app_name=secret_dict["APP_NAME"],
            api_endpoint=secret_dict["API_ENDPOINT"],
            api_key=secret_dict["API_KEY"],
            bucket_name=os.environ.get("BUCKET_NAME"),
        )


def _load_secret() -> Secret:
    client = boto3.client("secretsmanager")
    resp = client.get_secret_value(SecretId=str(os.environ.get("SECRET_ID")))
    return Secret(
        secret_name=str(os.environ.get("SECRET_ID")), secret_string=resp["SecretString"]
    )


def load_config() -> AppConfig:
    env = os.environ.get("ENVIRONMENT")
    if env == "local":
        return LocalConfig().create_config()
    else:
        return LiveConfig().create_config()
