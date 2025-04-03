"""
main function for recurly spotlight exporter.
"""
from datetime import datetime
from src.config import load_config
from shared.telemetry.logging import PythonLogger
from shared.recurly.api import RecurlyAPI
from shared.aws.aws_operations import s3__upload_file
from shared.aws.aws_clients import AwsS3Client
from shared.telemetry.helpers.alerting import send_slack_message

class RecurlyFileExporter:
    def __init__(self, date: str) -> None:
        # load middleware services
        self.app_config = load_config()
        self.logger = PythonLogger.get_logger(
            name="RecurlyFileExporter", config=self.app_config
        )
        self.date = date
        self.recurly_api = RecurlyAPI(config=self.app_config, logger=self.logger)
        self.s3_client = AwsS3Client(config=self.app_config)

    def main(self):
        self.logger.info(f"Getting Recurly Spotlight data for date: {self.date}")
        file_list = self.recurly_api.get_recurly_file_list(self.date)
        for report in file_list:
            try:
                # set param names
                file_prefix = (
                    "spotlight/" + report["name"].split("_")[0] + "/" + self.date + "/"
                )
                file_name = report["name"].split(".gz")[0]
                file_url = report["href"]

                # get file
                csv_file = self.recurly_api.get_recurly_file(file_url)
                if csv_file:
                    # upload file
                    resp = s3__upload_file(
                        logger=self.logger,
                        s3_client=self.s3_client,
                        config=self.app_config,
                        file_key=file_prefix + file_name,
                        body_content=csv_file,
                    )
                    if resp:
                        self.logger.info(f"Uploaded file: {file_prefix + file_name}")
                    else:
                        err_msg = f"Upload for file: {file_name} failed"
                        send_slack_message(
                            app_config=self.app_config,
                            error_msg=err_msg,
                            severity="error"
                        )
                        
            except Exception as e:
                send_slack_message(
                            app_config=self.app_config,
                            error_msg=str(e),
                            severity="error"
                        )
                raise e





def lambda_handler(message, context):
    """
    AWS Lambda entrypoint / handler
    """
    execution_date = datetime.strptime(message["time"], "%Y-%m-%dT%H:%M:%SZ").date()
    recurly_file_exporter = RecurlyFileExporter(date=str(execution_date))
    recurly_file_exporter.main()
