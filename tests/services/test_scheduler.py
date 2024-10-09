import unittest

import pytest
from unittest.mock import patch, MagicMock
import starkbank
from services.scheduler import Scheduler


@pytest.fixture
def mock_project():
    return MagicMock()


@pytest.fixture
def scheduler(mock_project):
    return Scheduler(project=mock_project)


@patch('starkbank.invoice.create')
def test_create_invoices(mock_create, scheduler):
    mock_invoice = MagicMock()
    mock_invoice.id = 'inv_123'
    mock_invoice.amount = 200
    mock_invoice.due = '2024-11-01T00:00:00Z'
    mock_create.return_value = [mock_invoice]

    scheduler.create_invoices()

    mock_create.assert_called()


def test_create_invoices_invalid_signature(scheduler):
    with patch('starkbank.invoice.create', side_effect=starkbank.error.InvalidSignatureError("Invalid signature")):
        with patch('builtins.print') as mocked_print:
            scheduler.create_invoices()
            mocked_print.assert_called_once_with("Error to create Invoice: Invalid signature")


def test_create_invoices_generic_exception(scheduler):
    with patch('starkbank.invoice.create', side_effect=Exception("Generic error")):
        with patch('builtins.print') as mocked_print:
            scheduler.create_invoices()
            mocked_print.assert_called_once_with("Error Exception: Generic error")


@patch('apscheduler.schedulers.background.BackgroundScheduler')
def test_setup_scheduler(MockScheduler, scheduler):
    with patch('builtins.print') as mocked_print:
        scheduler.setup_scheduler()
        mocked_print.assert_called_once_with("Scheduler Started. Invoices will be created every 3 hours.")
