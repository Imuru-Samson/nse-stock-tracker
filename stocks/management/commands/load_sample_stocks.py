from django.core.management.base import BaseCommand
from stocks.models import Stock

class Command(BaseCommand):
    help = "Loads sample stock data into the database"

    def handle(self, *args, **kwargs):
        sample_data = [
            {"symbol": "EQTY", "name": "Equity Group Holdings", "price": 40.50},
            {"symbol": "SCOM", "name": "Safaricom Plc", "price": 17.85},
            {"symbol": "KCB", "name": "KCB Group Plc", "price": 31.20},
            {"symbol": "ABSA", "name": "ABSA Bank Kenya", "price": 13.40},
            {"symbol": "COOP", "name": "Co-operative Bank", "price": 11.95},
        ]

        for stock in sample_data:
            Stock.objects.update_or_create(
                symbol=stock["symbol"],
                defaults={"name": stock["name"], "price": stock["price"]}
            )

        self.stdout.write(self.style.SUCCESS("✅ Sample stock data loaded successfully."))
