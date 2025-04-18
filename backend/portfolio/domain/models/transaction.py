from django.db import models

from .portfolio import Portfolio
from .asset import Asset

class Transaction(models.Model):
    """
    Model representing a transaction in the portfolio.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.asset.name} - {self.type} - {self.amount} - {self.date}"