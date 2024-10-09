import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import json

from starkbank import Project

from webhook_handler import setup_webhook


class TestWebhookHandler(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

        self.project = MagicMock(spec=Project)

        setup_webhook(self.app, self.project)

    @patch('webhook_handler.starkbank.event.parse')
    @patch('webhook_handler.Invoicer')
    def test_webhook_invoice_paid(self, mock_invoicer_class, mock_event_parse):
        mock_invoice = MagicMock()
        mock_invoice.id = 'inv_123'
        mock_invoice.amount = 200
        mock_event = MagicMock()
        mock_event.subscription = 'invoice'
        mock_event.log.type = 'invoice.paid'
        mock_event.log.invoice = mock_invoice

        mock_event_parse.return_value = mock_event

        mock_invoicer_instance = MagicMock()
        mock_invoicer_class.return_value = mock_invoicer_instance

        payload = json.dumps({
            "subscription": "invoice",
            "log": {
                "type": "invoice.paid",
                "invoice": {
                    "id": "inv_123",
                    "amount": 200,
                    "due": "2024-11-01T00:00:00Z"
                }
            }
        })
        headers = {
            "Content-Type": "application/json",
            "Digital-Signature": "valid_signature"
        }

        response = self.client.post('/webhook', data=payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Webhook Received Successfully'})

        mock_event_parse.assert_called_once_with(
            content=payload,
            signature="valid_signature",
            user=self.project
        )

        mock_invoicer_class.assert_called_once_with(self.project)
        mock_invoicer_instance.handle_invoice_credit.assert_called_once_with(mock_invoice)

    @patch('webhook_handler.starkbank.event.parse')
    def test_webhook_invalid_signature(self, mock_event_parse):
        mock_event_parse.side_effect = Exception("Invalid signature")

        payload = json.dumps({
            "subscription": "invoice",
            "log": {
                "type": "invoice.paid",
                "invoice": {
                    "id": "inv_123",
                    "amount": 200,
                    "due": "2024-11-01T00:00:00Z"
                }
            }
        })
        headers = {
            "Content-Type": "application/json",
            "Digital-Signature": "invalid_signature"
        }

        response = self.client.post('/webhook', data=payload, headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {'error': 'Internal Server Error'})

    @patch('webhook_handler.starkbank.event.parse')
    @patch('webhook_handler.Invoicer')
    def test_webhook_non_invoice_event(self, mock_invoicer_class, mock_event_parse):
        mock_event = MagicMock()
        mock_event.subscription = 'payment'
        mock_event.log.type = 'payment.received'
        mock_event.log.invoice = None

        mock_event_parse.return_value = mock_event

        payload = json.dumps({
            "subscription": "payment",
            "log": {
                "type": "payment.received",
                "invoice": None
            }
        })
        headers = {
            "Content-Type": "application/json",
            "Digital-Signature": "valid_signature"
        }

        response = self.client.post('/webhook', data=payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Webhook Received Successfully'})

        mock_invoicer_class.assert_not_called()

    @patch('webhook_handler.starkbank.event.parse')
    @patch('webhook_handler.Invoicer')
    def test_webhook_exception_handling(self, mock_invoicer_class, mock_event_parse):
        mock_event_parse.side_effect = Exception("Some unexpected error")

        payload = json.dumps({
            "subscription": "invoice",
            "log": {
                "type": "invoice.paid",
                "invoice": {
                    "id": "inv_123",
                    "amount": 200,
                    "due": "2024-11-01T00:00:00Z"
                }
            }
        })
        headers = {
            "Content-Type": "application/json",
            "Digital-Signature": "valid_signature"
        }

        response = self.client.post('/webhook', data=payload, headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {'error': 'Internal Server Error'})

        mock_invoicer_class.assert_not_called()
