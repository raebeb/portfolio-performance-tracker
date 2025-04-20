from django.db import models

from .portfolio import Portfolio
from .asset import Asset

class Holding(models.Model):
    """
    Model representing a holding in a portfolio.
    """
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='holdings')
    quantity = models.DecimalField(max_digits=20, decimal_places=6)


    def __str__(self):
        return f"{self.asset.name} - {self.quantity}"