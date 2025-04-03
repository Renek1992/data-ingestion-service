"""
Provides clients for AWS secrets manager.
"""

from boto3.session import Session

from shared.common.types import AppConfig
from mypy_boto3_secretsmanager.client import SecretsManagerClient
from mypy_boto3_s3.client import S3Client


class AwsSecretsManagerClient:
    def __init__(self, config: AppConfig):
        session = Session()
        self.client: SecretsManagerClient = session.client(
            service_name="secretsmanager", region_name=config.aws_region
        )


class AwsS3Client:
    def __init__(self, config: AppConfig) -> None:
        session = Session()
        self.client: S3Client = session.client(
            service_name="s3", region_name=config.aws_region
        )
