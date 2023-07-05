from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

import pickle
import numpy as np
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose

from core.models import StockData, StockInfo, TickerList
from core.forms import TickerName, Steps
from core.code import EnsembleModel

# Create your views here.
def send_data(request):
    data = StockData.objects.all()
    return JsonResponse(list(data.values()),safe=False)

def send_info(request):
    data = StockInfo.objects.all()
    return JsonResponse(list(data.values()),safe=False)

def chart(request):    
    datapoints = StockData.objects.all()
    context = {'ticker_form':TickerName,'datapoints':datapoints,'nbar':'chart'}
    ticker = request.GET.get('ticker')
    if ticker:
        # updating data into info-database
        t = StockInfo.objects.get(id=1)
        t.Symbol = ticker
        tl = TickerList.objects.filter(Symbol__exact=ticker).get()
        t.Name = tl.Name
        t.Updated = timezone.now()
        t.save()
        # downloading data from yfinance
        data = yf.download(tickers=ticker,start='2020-09-01',end='2023-06-05',progress=False).copy()
        data['Date'] = data.index
        data['DateString'] = data['Date'].dt.strftime("%Y-%m-%d")
        
        data.index = 1+np.arange(data.shape[0])
        data.index.names = ['id']
        # seasonal decomposition of data
        decompose = seasonal_decompose(data['Close'],model='additive',period=5)
        data['Trend'] = decompose.trend
        data['Seasonal'] = decompose.seasonal
        data['Residue'] = decompose.resid
        # calculating moving average and bollinger bands
        n = 20 # no. of moving average
        m = 2 # no. of steps std
        data['MovAvg'] = data['Adj Close'].rolling(n).mean().fillna(method='bfill')
        sigma = data['Adj Close'].rolling(n).std().fillna(method='bfill')
        data['BollTop'] = data['MovAvg'] + (m * sigma)
        data['BollBottom'] = data['MovAvg'] - (m * sigma)
        # calculating RSI
        data['RSI'] = RSI(data)
        # calculating MACD
        data = computeMACD(data,12,26,9)

        data.drop('Adj Close',axis=1,inplace=True)
        engine = create_engine('sqlite:///db.sqlite3')
        data.to_sql(StockData._meta.db_table, if_exists='replace', con=engine)
    return render(request, 'chart.html', context)

def predict(request):
    t = StockInfo.objects.get(id=1)
    updated = t.Updated
    context = {'updated':updated,'step_form':Steps,'nbar':'predict'}

    num_steps = request.GET.get('num_steps')
    if num_steps:
        with open('modelclass','rb') as picklefile:
            SMP = pickle.load(picklefile)
        pred_stocks, pred_dates = SMP.predict_future(int(num_steps))
        pred_data = [{'Date':pred_dates[i].strftime("%Y-%m-%d"),'Close':pred_stocks[i]} for i in range(int(num_steps))]
        context['pred_data'] = pred_data

    return render(request,'predict.html',context)

def retrain(request):
    u = StockInfo.objects.get(id=1)
    u.TrainedOn = u.Symbol
    u.save()
    data = StockData.objects.values_list('Date','Close')
    dates = np.array([row[0] for row in data])
    array = np.array([row[1] for row in data])
    refresh = EnsembleModel(array,dates)
    with open('modelclass','wb') as picklefile:
        pickle.dump(refresh,picklefile)
    return HttpResponse("""<html><script>window.location.replace('/predict');</script></html>""")


def about(request):
    context = {'nbar':'about'}
    return render(request,'about.html',context)

## Other functions
def RSI(data, window=14, adjust=False):
    delta = data['Close'].diff(1).dropna()
    loss = delta.copy()
    gains = delta.copy()

    gains[gains < 0] = 0
    loss[loss > 0] = 0

    gain_ewm = gains.ewm(com=window - 1, adjust=adjust).mean()
    loss_ewm = abs(loss.ewm(com=window - 1, adjust=adjust).mean())

    RS = gain_ewm / loss_ewm
    RSI = 100 - 100 / (1 + RS)

    return RSI

def computeMACD (df, n_fast, n_slow, n_smooth):
    data = df['Adj Close']
    
    fastEMA = data.ewm(span=n_fast, min_periods=n_slow).mean()
    slowEMA = data.ewm(span=n_slow, min_periods=n_slow).mean()
    MACD = pd.Series(fastEMA-slowEMA, name = 'MACD')
    MACDsig = pd.Series(MACD.ewm(span=n_smooth, min_periods=n_smooth).mean(), name='MACDsig')
    MACDhist = pd.Series(MACD - MACDsig, name = 'MACDhist')
    #df = df.join(MACD)
    #df = df.join(MACDsig)
    df = df.join(MACDhist)
    
    return df