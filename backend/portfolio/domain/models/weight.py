from django.db import models

from .asset import Asset
from .portfolio import Portfolio


class Weight(models.Model):
    """
    Model representing the weight of an asset in a portfolio.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='weights')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='weights')
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('asset', 'portfolio')

    def __str__(self):
        return f"{self.asset.name} - {self.portfolio.name} - {self.weight}"