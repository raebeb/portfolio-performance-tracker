from django.db import models

from .asset import Asset

class Price(models.Model):
    """
    Model representing a price for an asset.
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('asset', 'date')

    def __str__(self):
        return f"{self.asset.name} - {self.date} - {self.price}"