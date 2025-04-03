"""
conftest tests.
"""

import os
import pytest
from unittest.mock import MagicMock, patch

from src.config import (
    AppConfig,
    ConfigFactory,
    LocalConfig,
    LiveConfig,
    _load_secret,
    load_config,
)


@pytest.fixture
def mock_secret():
    return MagicMock(
        secret_string='{"LOG_LEVEL": "INFO", "APP_NAME": "TestApp", "API_ENDPOINT": "https://example.com/api/", "API_KEY": "test_api_key", "SLACK_TOKEN": "test_key"}'
    )

@pytest.fixture
def mock_boto3_client(mock_secret):
    client = MagicMock()
    client.get_secret_value.return_value = {'SecretString': mock_secret.secret_string}
    return client

@pytest.fixture
def mock_os_environ(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "local")
    monkeypatch.setenv("SECRET_ID", "test_secret_id")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("APP_NAME", "TestApp")
    monkeypatch.setenv("API_ENDPOINT", "https://example.com/api/")
    monkeypatch.setenv("API_KEY", "test_api_key")
    monkeypatch.setenv("BUCKET_NAME", "test_bucket")
    monkeypatch.setenv("SLACK_TOKEN", "test_key")



def describe_config_tests():
    def test_local_config_create_config(mock_os_environ):
        config = LocalConfig().create_config()
        assert isinstance(config, AppConfig)
        assert config.log_level == "DEBUG"
        assert config.app_name == "TestApp"
        assert config.api_endpoint == "https://example.com/api/"
        assert config.api_key == "test_api_key"
        assert config.bucket_name == "test_bucket"
        assert config.slack_token == "test_key"


    @patch('src.config.boto3.client', autospec=True)
    def test_live_config_create_config(mock_boto3_client, mock_secret, mock_os_environ):
        mock_boto3_client.return_value.get_secret_value.return_value = {'SecretString': mock_secret.secret_string}
        config = LiveConfig().create_config()

        assert isinstance(config, AppConfig)
        assert config.log_level == "INFO"
        assert config.app_name == "TestApp"
        assert config.api_endpoint == "https://example.com/api/"
        assert config.api_key == "test_api_key"
        assert config.bucket_name == "test_bucket"
        assert config.slack_token == "test_key"


    def test_load_config_local(mock_os_environ):
        config = load_config()
        assert isinstance(config, AppConfig)
        assert config.log_level == "DEBUG"
        assert config.app_name == "TestApp"
        assert config.api_endpoint == "https://example.com/api/"
        assert config.api_key == "test_api_key"
        assert config.bucket_name == "test_bucket"
        assert config.slack_token == "test_key"

    @patch('src.config.boto3.client', autospec=True)
    def test_load_config_live(mock_boto3_client, mock_secret, mock_os_environ):
        mock_boto3_client.return_value.get_secret_value.return_value = {'SecretString': mock_secret.secret_string}
        os.environ["ENVIRONMENT"] = "live"

        config = load_config()

        assert isinstance(config, AppConfig)
        assert config.log_level == "INFO"
        assert config.app_name == "TestApp"
        assert config.api_endpoint == "https://example.com/api/"
        assert config.api_key == "test_api_key"
        assert config.bucket_name == "test_bucket"
        assert config.slack_token == "test_key"