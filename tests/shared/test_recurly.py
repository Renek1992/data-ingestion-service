"""
tests for recurly.
"""
import logging
import pytest
from unittest.mock import MagicMock, patch
from shared.recurly.api import RecurlyAPI
from shared.common.errors import InvalidFileListLengthError


@pytest.fixture(name="mock_config")
def mock_config():
    return MagicMock(api_endpoint='https://example.com/api/', api_key='test_api_key')


@pytest.fixture(name="mock_logger")
def mock_logger():
    return MagicMock(spec=logging.Logger)


@pytest.fixture(name="mock_response")
def mock_response():
    response = MagicMock()
    response.json.return_value = {"files": [{"name": "test.csv.gz", "md5sum": "abcd1234", "href": "https://example.com/download"}]}
    return response


@pytest.fixture(name="mock_requests_session")
def mock_requests_session(mock_response):
    session = MagicMock()
    session.get.return_value = mock_response
    return session


def describe_recurly_api():
    def test_get_recurly_file_list(mock_config, mock_logger, mock_requests_session):
        api = RecurlyAPI(config=mock_config, logger=mock_logger)
        api.session = mock_requests_session
        file_list = api.get_recurly_file_list(date='2022-01-01')
        assert len(file_list) == 1
        assert file_list[0]['name'] == 'test.csv.gz'


    def test_get_recurly_file_list_empty(mock_config, mock_logger, mock_requests_session):
        mock_response = MagicMock()
        mock_response.json.return_value = {"files": []}
        mock_requests_session.get.return_value = mock_response
        api = RecurlyAPI(config=mock_config, logger=mock_logger)
        api.session = mock_requests_session
        with pytest.raises(InvalidFileListLengthError):
            api.get_recurly_file_list(date='2022-01-01')


    def test_get_recurly_file(mock_config, mock_logger, mock_requests_session):
        api = RecurlyAPI(config=mock_config, logger=mock_logger)
        api._download_file = MagicMock(return_value=MagicMock(content=b'Test content'))
        api._decrompress_file_content = MagicMock(return_value='Decompressed content')
        file_content = api.get_recurly_file(download_url='https://example.com/download')
        assert file_content == 'Decompressed content'