"""
Provides a repository of aws operations utilizing AWS clients.
"""

from logging import Logger
from shared.common.types import Secret, AppConfig
from shared.aws.aws_clients import AwsSecretsManagerClient, AwsS3Client
from botocore.exceptions import ClientError


def sm__get_secret(
    logger: Logger, client: AwsSecretsManagerClient, config: AppConfig
) -> Secret:
    try:
        resp = client.get_secret_value(SecretId=config.secret_id)
        logger.info("Secret extraction successfull")
    except ClientError as e:
        logger.debug(f"app configuration: {config}")
        logger.error(f"Secret extraction failed: {e}")
        raise e

    return Secret(secret_name=config.secret_id, secret_string=resp["SecretString"])


def s3__upload_file(
    logger: Logger,
    s3_client: AwsS3Client,
    config: AppConfig,
    file_key: str,
    body_content: str,
) -> bool:
    result = False
    try:
        resp = s3_client.client.put_object(
            Bucket=config.bucket_name, Key=file_key, Body=body_content
        )
        if resp:
            result = True
    except ClientError as e:
        logger.debug(f"bucket: {config.bucket_name} // file_key: {file_key}")
        logger.error(f"File upload failed: {e}")
        raise e
    return result
