from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import pickle
from datetime import datetime

from core.models import StockData, StockInfo, TickerList
from core.forms import TickerName, Steps
from core.code import RefreshData

# Create your views here.
def send_data(request):
    data = StockData.objects.all()
    return JsonResponse(list(data.values()),safe=False)

def send_filtered_data(request,start):
    start = datetime.strptime(start,format="%Y-%m-%d")
    data = StockData.objects.all()
    data = data.filter(Date__gte=start)
    return JsonResponse(list(data.values()),safe=False)

def chart(request):
    t = StockInfo.objects.get(id=1)
    name = t.Name
    data = StockData.objects.values()
    new_data = [{'Date':row['Date'].strftime("%Y-%m-%d"),'Close':row['Close'],'Open':row['Open'],'High':row['High'],'Low':row['Low']} for row in data]
    last_month_data = new_data[-30:]
    context = {'name':name,'data':new_data,'last_month_data':last_month_data,'nbar':'chart'}
    return render(request, 'chart.html', context)

def predict(request):
    t = StockInfo.objects.get(id=1)
    updated = t.Updated
    data = StockData.objects.values('Date','Close')
    new_data = [{'Date':row['Date'].strftime("%Y-%m-%d"),'Close':row['Close']} for row in data]
    context = {'updated':updated,'data':new_data,'step_form':Steps,'nbar':'predict'}

    num_steps = request.GET.get('num_steps')
    if num_steps:
        with open('modelclass','rb') as picklefile:
            SMP = pickle.load(picklefile)
        pred_stocks, pred_dates = SMP.predict_future(int(num_steps))
        pred_data = [{'Date':pred_dates[i].strftime("%Y-%m-%d"),'Close':pred_stocks[i]} for i in range(int(num_steps))]
        context['pred_data'] = pred_data

    return render(request,'predict.html',context)

def retrain(request):
    context = {'ticker_form':TickerName,'nbar':'retrain'}
    ticker = request.GET.get('ticker')
    if ticker:
        t = StockInfo.objects.get(id=1)
        t.Symbol = ticker
        tl = TickerList.objects.filter(Symbol__exact=ticker).get()
        t.Name = tl.Name
        t.Updated = timezone.now()
        t.save()
        refresh = RefreshData(ticker)
        refresh.download_data()
        refresh.build_model()
        RMSE = refresh.RMSEontest
        context['rmse'] = RMSE
        with open('modelclass','wb') as picklefile:
            pickle.dump(refresh,picklefile)
    return render(request,'retrain.html',context)