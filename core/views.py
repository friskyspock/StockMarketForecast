from django.shortcuts import render
import pickle

from core.models import StockData, StockInfo
from core.forms import TickerName, Steps
from core.code import RefreshData

# Create your views here.
def retrain(request):
    context = {'ticker_form':TickerName,'nbar':'retrain'}
    ticker = request.GET.get('ticker')
    if ticker:
        t = StockInfo.objects.get(id=1)
        t.Name = ticker
        t.save()
        refresh = RefreshData(ticker)
        refresh.download_data()
        refresh.build_model()
        with open('modelclass','wb') as picklefile:
            pickle.dump(refresh,picklefile)
    return render(request,'retrain.html',context)

def chart(request):
    name = StockInfo.objects.get(id=1)
    data = StockData.objects.values('Date','Close')
    new_data = [{'x':row['Date'].strftime("%Y-%m-%d"),'y':row['Close']} for row in data]
    context = {'name':name,'data':new_data,'nbar':'chart'}
    return render(request, 'chart.html', context)

def predict(request):
    data = StockData.objects.values('Date','Close')
    new_data = [{'Date':row['Date'].strftime("%Y-%m-%d"),'Close':row['Close']} for row in data]
    context = {'data':new_data,'step_form':Steps,'nbar':'predict'}

    num_steps = request.GET.get('num_steps')
    if num_steps:
        with open('modelclass','rb') as picklefile:
            SMP = pickle.load(picklefile)
        pred_stocks, pred_dates = SMP.predict_future(int(num_steps))
        pred_data = [{'Date':pred_dates[i].strftime("%Y-%m-%d"),'Close':pred_stocks[i]} for i in range(int(num_steps))]
        context['pred_data'] = pred_data

    return render(request,'predict.html',context)