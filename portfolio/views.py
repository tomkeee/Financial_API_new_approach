from django.shortcuts import render,redirect
from instrument.models import Instrument
from instrument.forms import TickerForm,BarTypeForm
from django.db.models import Sum, query
from django.http import HttpResponse
from instrument.tiingo import get_meta_data,get_price_data
from .utils import get_chart
import pandas as pd

from django.contrib.auth.decorators import login_required


# Create your views here.
def prettify(number):
    return '{:.2%}'.format(number)
@login_required
def portfolio_view(request):
    user=request.user
    print(user)
    total=float(list(Instrument.objects.filter(profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
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
    for element in queryset:
        element=element.price
        totals.append(element)

    percentage=[]
    for instance in totals:
        instance=instance/total
        instance=prettify(instance)
        percentage.append(instance)

    context={
        "queryset":queryset,
        "total":total,
        "totals":totals,
        "percentage":percentage,
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
    total=float(list(Instrument.objects.filter(profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    chart_type="#3"
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
    
    total_in = float(list(Instrument.objects.filter(region="In").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_in)

    total_as = float(list(Instrument.objects.filter(region="AS").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_as)

    total_rus = float(list(Instrument.objects.filter(region="Rus").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_rus)

    total_us = float(list(Instrument.objects.filter(region="US").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_us)

    total_eu = float(list(Instrument.objects.filter(region="EU").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_eu)

    total_af = float(list(Instrument.objects.filter(region="Af").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_af)


    percentage=[]
    for instance in totals:
        if total==0:
            instance="0%"
            percentage.append(instance)
        else:
            instance=instance/total
            instance=prettify(instance)
            percentage.append(instance)
    
    table=[]
    table.append({"region":"Independent","invested":total_in})
    table.append({"region":"Asia","invested":total_as})
    table.append({"region":"Russia","invested":total_rus})
    table.append({"region":"US","invested":total_us})
    table.append({"region":"Europe","invested":total_eu})
    table.append({"region":"Africa","invested":total_af})


    df=pd.DataFrame(table)
    df.sort_values(by=['invested'],ascending=False, inplace=True)
    chart=get_chart(chart_type, df,labels=df['region'],y='invested',x='region')
    
    context={
        "total":total,
        "totals":totals,
        "percentage":percentage,
        "form":form,
        "form_b":form_b,
        "chart":chart
        }
    return render(request,"portfolio/region.html",context)





@login_required
def sector_view(request):
    user=request.user
    total=float(list(Instrument.objects.filter(profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    chart_type="#3"
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
    

    totals=[]
    
    total_pm = float(list(Instrument.objects.filter(stake="pm").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_pm)

    total_eg = float(list(Instrument.objects.filter(stake="Eg").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_eg)

    total_met = float(list(Instrument.objects.filter(stake="Met").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_met)

    total_eq = float(list(Instrument.objects.filter(stake="Eq").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_eq)
    
    total_cs = float(list(Instrument.objects.filter(stake="Cs").aggregate(total=Sum('total_price')).values())[0] or 0)
    totals.append(total_cs)

    percentage=[]

    for instance in totals:
        if total==0:
            instance="0%"
            percentage.append(instance)
        else:
            instance=instance/total
            instance=prettify(instance)
            percentage.append(instance)
#
    table=[]
    table.append({"sector":"Precious metal","invested":total_pm})
    table.append({"sector":"Energy","invested":total_eg})
    table.append({"sector":"Equity","invested":total_eq})
    table.append({"sector":"Cash","invested":total_cs})
    table.append({"sector":"Metals","invested":total_met})


    df=pd.DataFrame(table)
    df.sort_values(by=['invested'],ascending=False, inplace=True)
    chart=get_chart(chart_type, df,labels=df['sector'],y='invested',x='sector')
#
    context={
        "total":total,
        "totals":totals,
        "percentage":percentage,
        "form":form,
        "form_b":form_b,
        "chart":chart,
        }
    return render(request,"portfolio/sector.html",context)