"""
tests for aws content
"""
import logging
import pytest
from unittest.mock import MagicMock, patch, Mock
from src.config import load_config
from shared.aws.aws_clients import (
    AwsSecretsManagerClient,
    AwsS3Client
)
from shared.aws.aws_operations import (
    sm__get_secret,
    s3__upload_file
)



@pytest.fixture(name="test_logger")
def logger():
    logger = logging.getLogger(name='pytest')
    return logger


@pytest.fixture(name="test_config")
def config():
    app_config = load_config()
    return app_config


@pytest.fixture(name="test_client")
def aws_client():
    with patch('shared.aws.aws_clients.Session.client') as mock_client:
        yield mock_client




def describe_aws_clients():
    def test_secrets_manager_client(
            test_config: MagicMock, 
            test_client: MagicMock
    ):
        sm_client = AwsSecretsManagerClient(config=test_config)
        test_client.assert_called_once_with(service_name="secretsmanager", region_name=test_config.aws_region)
        assert isinstance(sm_client.client, Mock)
        

    def test_s3_client(
            test_config: MagicMock, 
            test_client: MagicMock
    ):
        s3_client = AwsS3Client(config=test_config)
        test_client.assert_called_once_with(service_name="s3", region_name=test_config.aws_region)
        assert isinstance(s3_client.client, Mock)




def describe_aws_operations_sm__get_secret():
    @patch('shared.aws.aws_clients.Session.client')
    def test_sm__get_secret__success(
            mock_client_call: MagicMock, 
            test_logger: MagicMock, 
            test_config: MagicMock
    ):
        mock_client_call.return_value.get_secret_value.return_value = {'SecretString' : '{"key1" : "value1", "key2" : "value2"}'}
        sm_client = AwsSecretsManagerClient(config=test_config)
        resp = sm__get_secret(
            logger=test_logger, 
            client=sm_client.client,
            config=test_config
        )
        assert resp.secret_string == '{"key1" : "value1", "key2" : "value2"}'


    @patch('shared.aws.aws_clients.Session.client')
    def test_sm__get_secret__error(
            mock_client_call: MagicMock, 
            test_logger: MagicMock, 
            test_config: MagicMock
    ):
        mock_client_call.return_value.get_secret_value.side_effect = Exception("Simulated Error")
        sm_client = AwsSecretsManagerClient(config=test_config)
        with pytest.raises(Exception):
            sm__get_secret(
                logger=test_logger,
                client=sm_client,
                config=test_config
            )


def describe_aws_operations_s3__upload_file():
    @patch('shared.aws.aws_clients.Session.client')
    def test_s3__upload_file__success(
        mock_client_call: MagicMock,
        test_logger: MagicMock,
        test_config: MagicMock
    ):
        mock_client_call.return_value.put_object.return_value = True
        s3_client = AwsS3Client(config=test_config)
        resp = s3__upload_file(
            logger=test_logger,
            s3_client=s3_client,
            config=test_config,
            file_key='test.csv',
            body_content='test'
        )
        assert resp == True


    @patch('shared.aws.aws_clients.Session.client')

    def test_s3__upload_file__error(
        mock_client_call: MagicMock,
        test_logger: MagicMock,
        test_config: MagicMock
    ):
        mock_client_call.return_value.put_object.side_effect = Exception("Simulated Error")
        s3_client = AwsS3Client(config=test_config)
        with pytest.raises(Exception):
            s3__upload_file(
                logger=test_logger,
                s3_client=s3_client,
                file_key='test.csv',
                body_content='test'
            )