from django.shortcuts import render

import numpy as np
import yfinance as yf
from sqlalchemy import create_engine

from core.models import StockData
from core.forms import TickerName, Steps
from core.code import StockMarketPrediction

def download_data(ticker):
    data = yf.download(tickers=ticker,start='2013-01-01',end='2023-06-05',progress=False)[['Close']].copy()
    data['Date'] = data.index
    data = data[['Date','Close']]
    data.index = 1+np.arange(data.shape[0])
    data.index.names = ['id']
    data['LogReturns'] = np.log(1 + data['Close'].pct_change())
    data['Target'] = data['Close'].shift(-1)

    engine = create_engine('sqlite:///db.sqlite3')

    data.to_sql(StockData._meta.db_table, if_exists='replace', con=engine)

# Create your views here.
def chart(request):
    ticker = request.GET.get('ticker')
    if ticker:
        download_data(ticker)
    data = StockData.objects.values('Date','Close')
    new_data = [{'x':row['Date'].strftime("%Y-%m-%d"),'y':row['Close']} for row in data]
    context = {'data':new_data, 'ticker_form':TickerName}
    return render(request, 'chart.html', context)

def predict(request):
    data = StockData.objects.values('Date','Close')
    new_data = [{'Date':row['Date'].strftime("%Y-%m-%d"),'Close':row['Close']} for row in data]
    context = {'data':new_data,'step_form':Steps}

    num_steps = request.GET.get('num_steps')
    if num_steps:
        x_data = np.array([row['Date'] for row in data])
        y_data = np.array([row['Close'] for row in data])
        SMP = StockMarketPrediction(x_data,y_data)
        pred_stocks, pred_dates = SMP.predict_future(int(num_steps))
        pred_data = [{'Date':pred_dates[i].strftime("%Y-%m-%d"),'Close':pred_stocks[i]} for i in range(int(num_steps))]
        context['pred_data'] = pred_data

    return render(request,'predict.html',context)