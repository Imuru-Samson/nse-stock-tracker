from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_fetched = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)  # ⏱️ Add this
    def __str__(self):
        return f"{self.symbol} - {self.price}"
