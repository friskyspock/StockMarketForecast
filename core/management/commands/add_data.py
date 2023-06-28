import yfinance as yf
import numpy as np
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from core.models import StockData

class Command(BaseCommand):
    help = "A command to update database with data from yfinance"
    
    def handle(self, *args, **options):
        data = yf.download(tickers="RELIANCE.NS",start='2013-01-01',end='2023-06-05',progress=False)[['Close']].copy()
        data['Date'] = data.index
        data = data[['Date','Close']]
        data.index = 1+np.arange(data.shape[0])
        data.index.names = ['id']
        data['LogReturns'] = np.log(1 + data['Close'].pct_change())
        data['Target'] = data['Close'].shift(-1)

        engine = create_engine('sqlite:///db.sqlite3')

        data.to_sql(StockData._meta.db_table, if_exists='replace', con=engine)