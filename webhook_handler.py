from flask import request, jsonify
import starkbank

from services.invoicer import Invoicer


def setup_webhook(app, project):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        try:
            event = starkbank.event.parse(
                content=request.data.decode("utf-8"),
                signature=request.headers.get("Digital-Signature", ""),
                user=project
            )
            print(f"SUBSCRIPTION: {event.subscription}")
            if event.subscription == "invoice":
                print(f"Event Received for payment invoice: {event.log.invoice.id}")
                Invoicer(project).handle_invoice_credit(event.log.invoice)
            print('Webhook Received Successfully')
            return jsonify({'message': 'Webhook Received Successfully'}), 200
        except starkbank.error.InvalidSignatureError:
            print("Assinatura inválida do webhook.")
            return jsonify({'error': 'Invalid signature'}), 400
        except Exception as e:
            print(f"Fail to process webhook: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
