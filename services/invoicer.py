import os
import starkbank

TRANSFER_DETAILS = {
    "bank_code": os.getenv('TRANSFER_BANK_CODE'),
    "branch": os.getenv('TRANSFER_BRANCH'),
    "account_number": os.getenv('TRANSFER_ACCOUNT'),
    "name": os.getenv('TRANSFER_NAME'),
    "tax_id": os.getenv('TRANSFER_TAX_ID'),
    "account_type": os.getenv('TRANSFER_ACCOUNT_TYPE')
}


class Invoicer:
    def __init__(self, project):
        self.project = project

    def handle_invoice_credit(self, invoice):
        try:

            transfer = starkbank.Transfer(
                amount=invoice.amount,
                tax_id=TRANSFER_DETAILS["tax_id"],
                name=TRANSFER_DETAILS["name"],
                bank_code=TRANSFER_DETAILS["bank_code"],
                branch_code=TRANSFER_DETAILS["branch"],
                account_number=TRANSFER_DETAILS["account_number"],
                tags=[f"invoice:{invoice.id}"],
                rules=[
                    starkbank.transfer.Rule(
                        key="resendingLimit",
                        value=5
                    )
                ],
                account_type=TRANSFER_DETAILS["account_type"]
            )

            created_transfer = starkbank.transfer.create([transfer], user=self.project)[0]

            print(f"Transfer Created by Webhook: {created_transfer.id}, Amount: R${created_transfer.amount / 100:.2f}")
        except Exception as e:
            print(f"Error processing the transfer: {e}")
