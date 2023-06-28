from django.core.management.base import BaseCommand
from core.code import RefreshData
import pickle
from core.models import StockInfo

class Command(BaseCommand):
    help = "A command to update database with data from yfinance"
    
    def handle(self, *args, **options):
        t = StockInfo(Name="RELIANCE.NS")
        t.save()