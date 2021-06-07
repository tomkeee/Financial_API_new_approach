from django.shortcuts import render
from django.views.generic import ListView
from instrument.models import Instrument
# Create your views here.
def InstrumentInvestments(request):
    qs=Instrument.objects.all()

    data=[]

    tickers=[]
    invested=[]

    for instance in qs:
        if instance.name in tickers:
            index=tickers.index(instance.name)
            data[index]['investment'] += instance.total_price
            data[index]['hodler'] += 1

        else:
            package={}
            tickers.append(instance.name)
            invested.append(instance.total_price)
            
            package['ticker']=instance.name
            package['investment']=instance.total_price
            package['hodler']=1

            data.append(package)

    context = {"data":data}
    return render(request,"data/instrumentData.html",context)