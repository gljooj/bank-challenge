import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from services.invoicer import Invoicer
import starkbank

from webhook_handler import setup_webhook


@pytest.fixture
def project_mock():
    return MagicMock(spec=starkbank.Project)


@pytest.fixture
def invoice_mock():
    invoice = MagicMock()
    invoice.amount = 200
    return invoice


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def invoicer(project_mock):
    return Invoicer(project=project_mock)


@patch('starkbank.transfer.create')
def test_handle_invoice_credit(mock_create, project_mock, invoice_mock):
    transfer_mock = MagicMock()
    transfer_mock.id = 'transfer_123'
    transfer_mock.amount = 200
    mock_create.return_value = [transfer_mock]

    invoicer = Invoicer(project_mock)

    invoicer.handle_invoice_credit(invoice_mock)

    mock_create.assert_called_once()

    args, kwargs = mock_create.call_args
    transfer = args[0][0]
    assert transfer.amount == 200
    assert transfer.tax_id == '20.018.183/0001-80'
    assert transfer.bank_code == '20018183'


def test_webhook_invalid_signature(app):
    project = MagicMock()
    setup_webhook(app, project)

    with app.test_client() as client:
        with patch('starkbank.event.parse', side_effect=starkbank.error.InvalidSignatureError("Invalid signature")):
            response = client.post('/webhook', data='{}',
                                   headers={'Digital-Signature': 'invalid_signature'})

            assert response.status_code == 400
            assert response.json == {'error': 'Invalid signature'}


def test_create_invoices_generic_exception(invoicer):
    with patch('builtins.print') as mocked_print:
        invoicer.handle_invoice_credit({})
        mocked_print.assert_called_once_with("Error processing the transfer: 'dict' object has no attribute 'amount'")
