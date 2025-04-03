"""
tests for telemetry objects.
"""

import pytest
import logging
import sys
from unittest.mock import MagicMock
from shared.telemetry.logging import PythonLogger


@pytest.fixture(name="mock_config") 
def mock_config():
    return MagicMock(log_level=logging.INFO)

def describe_logging():
    def test_get_logger(mock_config: MagicMock):
        logger = PythonLogger.get_logger(name="test_logger", config=mock_config)
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        assert logger.handlers[0].stream == sys.stdout