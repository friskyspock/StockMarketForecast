from django.db import models

# Create your models here.
class StockData(models.Model):
    Date = models.DateField()
    Close = models.FloatField()
    LogReturns = models.FloatField()
    Target = models.FloatField()

    class Meta:
        ordering = ('id',)

class StockInfo(models.Model):
    Symbol = models.CharField(max_length=50)
    Name = models.CharField(max_length=100)
    Updated = models.DateField()

    def __str__(self):
        return self.Name

class TickerList(models.Model):
    Symbol = models.CharField(max_length=50)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name