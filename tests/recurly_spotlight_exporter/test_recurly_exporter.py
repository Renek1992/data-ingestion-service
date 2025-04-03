"""
test module for recurly exporter.
"""

import pytest
from datetime import date
from unittest.mock import Mock, patch, MagicMock
from src.recurly_spotlight_exporter.app import RecurlyFileExporter


@pytest.fixture
def mock_recurly_file_exporter():
    # Setup
    execution_date = date(2024, 4, 8)  # Example execution date
    exporter = RecurlyFileExporter(date=str(execution_date))
    yield exporter


@patch('shared.aws.aws_operations.s3__upload_file')
def test_main_success(mock_upload_file: MagicMock, mock_recurly_file_exporter: MagicMock):
    # Mock external dependencies
    mock_report_list = [
        {"name": "report_1.gz", "href": "http://example.com/report_1.gz"}
    ]
    mock_csv_file = b"mock csv content"

    mock_recurly_file_exporter.recurly_api.get_recurly_file_list = Mock(
        return_value=mock_report_list
    )
    mock_recurly_file_exporter.recurly_api.get_recurly_file = Mock(
        return_value=mock_csv_file
    )
    mock_upload_file.return_value = True  # Mock successful upload

    # Run main method
    mock_recurly_file_exporter.main()

    # Assertions
    assert mock_recurly_file_exporter.recurly_api.get_recurly_file_list.called
    assert mock_recurly_file_exporter.recurly_api.get_recurly_file.called


def test_main_with_exception(mock_recurly_file_exporter):
    # Mock external dependencies to simulate exception
    mock_recurly_file_exporter.recurly_api.get_recurly_file_list = Mock(
        side_effect=Exception("API Error")
    )

    # Run main method within a pytest raises context
    with pytest.raises(Exception) as e:
        mock_recurly_file_exporter.main()

    # Assertions
    assert mock_recurly_file_exporter.recurly_api.get_recurly_file_list.called
    assert "API Error" in str(e.value)