"""
Provides an interface for the Recurly API
"""

import io
import gzip
import csv
import logging
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

from retry import retry
from shared.telemetry.helpers.alerting import send_slack_message
from shared.common.errors import InvalidFileListLengthError
from shared.common.types import AppConfig
from typing import List


retry_settings = {
    "tries": 3,
    "delay": 1.0,
    "max_delay": 10.0,
    "backoff": 2.0,
    "jitter": 0.5,
}


class RecurlyAPI:
    def __init__(self, config: AppConfig, logger: logging.Logger):
        super(RecurlyAPI, self).__init__()
        self.app_config = config
        self.request_url = self.app_config.api_endpoint
        self.api_key = self.app_config.api_key
        self.session = requests.Session()
        self.logger = logger


    @retry(requests.exceptions.HTTPError, **retry_settings)
    def __get(self, url: str) -> requests.Response:
        headers = {
            "Accept": "application/vnd.recurly.v2021-02-25",
            "X-Api-Version": "2.29",
            "Content-Type": "application/xml; charset=utf-8",
        }
        self.logger.debug(f"url: {url}")
        resp = self.session.get(
            url=url, auth=HTTPBasicAuth(self.api_key, ""), headers=headers
        )
        resp.raise_for_status()
        return resp


    def __post(self, url):
        raise NotImplementedError()


    def get_recurly_file_list(self, date: str) -> List:
        """
        Returns:
            List[Dict]: [
                {
                    'name': 'report_name.csv.gz',
                    'md5sum': 'str',
                    'href': 'https://storage.googleapis.com/freightliner...'
                }
            ]
        """
        url = self.request_url + date + "/export_files"
        try:
            results = self.__get(url=url)
            self.logger.debug(f"{results.json()}")
            file_list = results.json()["files"]
            self.logger.info(f"Got file list with {len(file_list)} urls.")
            if len(file_list) == 0:
                err_msg = f"File list length invalid: {len(file_list)}"
                send_slack_message(
                    app_config=self.app_config,
                    error_msg=err_msg,
                    severity="error"
                )
                raise InvalidFileListLengthError(err_msg)
            return file_list
        except HTTPError as e:
            err_msg = f"HTTPError occurred: {e}"
            send_slack_message(
                app_config=self.app_config,
                error_msg=err_msg,
                severity="warn"
            )
            raise e


    def _download_file(self, download_url: str) -> requests.Response:
        resp = self.__get(url=download_url)
        return resp


    def _decrompress_file_content(self, compressed_content: bytes) -> io.StringIO:
        with gzip.open(
            io.BytesIO(compressed_content), mode="rt", encoding="utf-8"
        ) as uncompressed:
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_reader = csv.reader(uncompressed)
            for row in csv_reader:
                csv_writer.writerow(row)
            csv_content = csv_buffer.getvalue()
        return csv_content


    def get_recurly_file(self, download_url: str) -> str:
        resp = self._download_file(download_url=download_url)
        csv_file = self._decrompress_file_content(compressed_content=resp.content)
        return csv_file
