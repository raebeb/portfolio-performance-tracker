from django.db import models


class Asset(models.Model):
    """
    Model representing an asset in the portfolio.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"