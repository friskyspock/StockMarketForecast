from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

import pickle
import numpy as np
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

def send_filtered_data(request,start):
    start = datetime.strptime(start,format="%Y-%m-%d")
    data = StockData.objects.all()
    data = data.filter(Date__gte=start)
    return JsonResponse(list(data.values()),safe=False)

def chart(request):    
    context = {'ticker_form':TickerName,'nbar':'chart'}
    ticker = request.GET.get('ticker')
    if ticker:
        # updating data into info-database
        t = StockInfo.objects.get(id=1)
        t.Symbol = ticker
        tl = TickerList.objects.filter(Symbol__exact=ticker).get()
        t.Name = tl.Name
        t.Updated = timezone.now()
        t.save()
        # sending ticker name for heading
        context['name'] = t.Name
        # downloading data from yfinance
        data = yf.download(tickers=ticker,start='2020-09-01',end='2023-06-05',progress=False).copy()
        data['Date'] = data.index
        
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