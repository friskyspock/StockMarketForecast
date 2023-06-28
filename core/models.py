from django.db import models

# Create your models here.
class StockData(models.Model):
    Date = models.DateField()
    Close = models.FloatField()
    LogReturns = models.FloatField()
    Target = models.FloatField()

    class Meta:
        ordering = ('id',)