from django.db import models

# Create your models here.
class StockData(models.Model):
    Open = models.FloatField()
    High = models.FloatField()
    Low = models.FloatField()
    Close = models.FloatField()
    Volume = models.FloatField()
    Date = models.DateField()
    Trend = models.FloatField()
    Seasonal = models.FloatField()
    Residue = models.FloatField()

    class Meta:
        ordering = ('id',)

class StockInfo(models.Model):
    Symbol = models.CharField(max_length=50)
    Name = models.CharField(max_length=100)
    Updated = models.DateField()
    TrainedOn = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

class TickerList(models.Model):
    Symbol = models.CharField(max_length=50)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name