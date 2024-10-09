import starkbank
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import random


class Scheduler:
    def __init__(self, project):
        self.project = project
        self.scheduler = BackgroundScheduler()

    def create_invoices(self):
        num_invoices = random.randint(8, 12)
        invoices = []

        for _ in range(num_invoices):
            invoice = starkbank.Invoice(
                amount=2 + _,
                descriptions=[{'key': 'Arya', 'value': 'Not today'}],
                due=datetime.now() + timedelta(days=random.randint(1, 30)),
                expiration=123456789,
                fine=2.5,
                interest=1.3,
                name="Not Stark",
                tags=['Supply', 'Invoice #1234'],
                tax_id="20.018.183/0001-80",
                rules=[
                    {
                        'key': 'allowedTaxIds',
                        'value': [
                            '012.345.678-90',
                            '45.059.493/0001-73'
                        ]
                    }
                ]
            )
            invoices.append(invoice)

        try:
            created_invoices = starkbank.invoice.create(invoices, user=self.project)
            for invoice in created_invoices:
                print(f"Invoice created: {invoice.id}, Amount: R${invoice.amount / 100:.2f}, Due: {invoice.due}")
        except starkbank.error.InvalidSignatureError as e:
            print(f"Error to create Invoice: {e}")
        except Exception as e:
            print(f"Error Exception: {e}")

    def setup_scheduler(self):
        self.scheduler.add_job(
            self.create_invoices,
            'interval',
            hours=3,
            next_run_time=datetime.now()
        )
        self.scheduler.start()
        print("Scheduler Started. Invoices will be created every 3 hours.")
