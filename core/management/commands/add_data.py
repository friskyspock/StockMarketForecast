from django.core.management.base import BaseCommand
from core.code import RefreshData
import pickle
from core.models import TickerList

class Command(BaseCommand):
    help = "A command to update database with data from yfinance"
    
    def handle(self, *args, **options):
        TickerList.objects.all().delete()
        data = [["WIPRO.NS","Wipro Limited"],["BRITANNIA.NS","Britannia Industries Limited"],["TECHM.NS","Tech Mahindra Limited"],["NESTLEIND.NS","Nestle India Limited"],["MARUTI.NS","Maruti Suzuki India Limited"],["BAJAJFINSV.NS","Bajaj Finserv Ltd."],["HEROMOTOCO.NS","Hero MotoCorp Limited"],["TCS.NS","Tata Consultancy Services Limited"],["ITC.NS","ITC Limited"],["TATACONSUM.NS","Tata Consumer Products Limited"],["KOTAKBANK.NS","Kotak Mahindra Bank Limited"],["ONGC.NS","Oil and Natural Gas Corporation Limited"],["ICICIBANK.NS","ICICI Bank Limited"],["ULTRACEMCO.NS","UltraTech Cement Limited"],["BAJFINANCE.NS","Bajaj Finance Limited"],["COALINDIA.NS","Coal India Limited"],["HINDALCO.NS","Hindalco Industries Limited"],["INDUSINDBK.NS","IndusInd Bank Limited"],["TATASTEEL.NS","Tata Steel Limited"],["APOLLOHOSP.NS","Apollo Hospitals Enterprise Limited"],["LT.NS","Larsen & Toubro Limited"],["TITAN.NS","Titan Company Limited"],["BAJAJ-AUTO.NS","Bajaj Auto Limited"],["ADANIENT.NS","Adani Enterprises Limited"],["MM.NS","MM.NS"],["CIPLA.NS","Cipla Limited"],["RELIANCE.NS","Reliance Industries Limited"],["NTPC.NS","NTPC Limited"],["BHARTIARTL.NS","Bharti Airtel Limited"],["HDFCLIFE.NS","HDFC Life Insurance Company Limited"]]
        for row in data:
            t = TickerList(Symbol=row[0],Name=row[1])
            t.save()