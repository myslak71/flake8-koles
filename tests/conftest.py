"""Pytest configuration module."""
from unittest.mock import patch

import pytest

from flake8_koles.checker import KolesChecker


@pytest.fixture
def koles_checker():
    """Return clean KolesChecker instance."""
    with patch('flake8_koles.checker.KolesChecker.__init__') as mock_init:
        mock_init.return_value = None
        koles_checker = KolesChecker('test_tree', 'test_filename')
        yield koles_checker
