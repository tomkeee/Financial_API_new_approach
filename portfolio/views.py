from django.shortcuts import render,redirect
from instrument.models import Instrument, Stock
from instrument.forms import TickerForm,BarTypeForm
from django.db.models import Sum, query,Count
from django.http import HttpResponse
from .utils import get_chart,prettify
import pandas as pd

from itertools import chain
from django.contrib.auth.decorators import login_required

@login_required
def portfolio_view(request):  
    user=request.user
    try:
        total=Instrument.objects.filter(profiles=user).aggregate(sum=Sum('total_price'))['sum']
    except:
        total=0

    chart_type="#1"
    form_b=BarTypeForm(request.POST or None)
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        if form_b.is_valid():
                if form_b.is_valid():
                    chart_type=request.POST.get('chart_type') 

        elif form.is_valid():
            ticker=request.POST['ticker']
            return redirect(ticker)
    else:
        form=TickerForm()
        form_b=BarTypeForm()

    queryset=Instrument.objects.filter(profiles=user).order_by('-total_price')

    totals=[]

    
    for element in queryset:
        data={}

        obj=element.name
        data['name']=obj

        price=element.total_price
        data['price']=price

        percentage=price/total
        percentage=prettify(percentage)
        data['percentage']=percentage

        totals.append(data)
    
    context={
        "queryset":queryset,
        "total":total,
        "totals":totals,
        "form":form,
        "form_b":form_b
        }
        
    if len(queryset)>0:
        df=pd.DataFrame(queryset.values())
        df.rename({'total_price':'invested',"name":'Ticker'},axis=1,inplace=True)
        df.sort_values(by=['invested'],ascending=False, inplace=True)
        chart=get_chart(chart_type, df,labels=df['Ticker'],y='invested',x='Ticker')
        context['chart']=chart


    return render(request,"portfolio/portfolio.html",context)


    
@login_required
def region_view(request):
    user=request.user
    total=Instrument.objects.filter(profiles=user).aggregate(sum=Sum('total_price'))['sum']
    chart_type="#1"
    form_b=BarTypeForm(request.POST or None)
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        if form_b.is_valid():
                if form_b.is_valid():
                    chart_type=request.POST.get('chart_type') 

        elif form.is_valid():
            ticker=request.POST['ticker']
            return redirect(ticker)
    else:
        form=TickerForm()
        form_b=BarTypeForm()
    

    queryset=Instrument.objects.filter(profiles=user)
    totals=[]
    regions=[]
    for instance in queryset:
        if instance.region in regions:
            index=regions.index(instance.region)
            totals[index]['invested'] += instance.total_price
            percentage=totals[index]['invested']/total
            percentage=prettify(percentage)
            totals[index]['percentage']=percentage
        else:
            regions.append(instance.region)

            data_new={}
            data_new['invested']=instance.total_price
            data_new['region']=instance.region
            percentage=instance.total_price/total
            percentage=prettify(percentage)
            data_new['percentage']=percentage
            totals.append(data_new)
    totals.sort(key=lambda x: x['invested'], reverse=True)

    if totals:
        df=pd.DataFrame(totals)
        chart=get_chart(chart_type, df,labels=df['region'],y='invested',x='region')
    else:
        chart=""
    
    context={
        "total":total,
        "totals":totals,
        "form":form,
        "form_b":form_b,
        "chart":chart,
         }
    return render(request,"portfolio/region.html",context)


@login_required
def sector_view(request):
    chart_type="#1"
    form_b=BarTypeForm(request.POST or None)
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        if form_b.is_valid():
                if form_b.is_valid():
                    chart_type=request.POST.get('chart_type') 
        elif form.is_valid():
            ticker=request.POST['ticker']
            return redirect(ticker)
    else:
        form=TickerForm()
        form_b=BarTypeForm()
    user=request.user
    try:
        total=Instrument.objects.filter(profiles=user).aggregate(sum=Sum('total_price'))['sum']
    except:
        total=0

    totals=[]    
    sectors=[]

    queryset=Instrument.objects.filter(profiles=user)
    for instance in queryset:
        if instance.sector in sectors:
            index=sectors.index(instance.sector)
            totals[index]['invested'] += instance.total_price
            percentage=totals[index]['invested']/total
            percentage=prettify(percentage)
            totals[index]['percentage']=percentage
        else:
            sectors.append(instance.sector)
            data_new={}
            data_new['invested']=instance.total_price
            data_new['sector']=instance.sector
            percentage=instance.total_price/total
            percentage=prettify(percentage)
            data_new['percentage']=percentage
            totals.append(data_new)
    totals.sort(key=lambda x: x['invested'],reverse=True)

    if totals:
        df=pd.DataFrame(totals)
        chart=get_chart(chart_type, df,labels=df['sector'],y='invested',x='sector')
    else:
        chart=""

    context={
        "total":total,
        "totals":totals,
        "form":form,
        "form_b":form_b,
        "chart":chart,
        }
    return render(request,"portfolio/sector.html",context)

def calculator(request):
    try:
        returns=float(request.POST.get('returns'))
        years = float(request.POST.get('years'))
        invested = float(request.POST.get('invested'))
    except:
        returns=0
        years=0
        invested=0

    value=invested*(1+returns*0.01)**years
    profit=value-invested
    round(profit,2)
    round(value,2)

    context={
        "value":value,
        "profit":profit,
    }

    return render(request,"portfolio/calculator.html",context)
