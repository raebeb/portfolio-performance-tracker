from django.db import models


class Portfolio(models.Model):
    """
    Model representing a portfolio.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"