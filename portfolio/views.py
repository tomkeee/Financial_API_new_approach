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

    queryset=Instrument.objects.filter(profiles=user).order_by('-total_price')

    totals=[]
    for element in queryset:
        data=[]

        obj=element.name
        data.append(obj)

        price=element.total_price
        data.append(price)

        percentage=price/total
        percentage=prettify(percentage)
        data.append(percentage)

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


    # new=Instrument.objects.filter(profiles=user).first()
    # print(new.region)

    totals=[]
    
    total_in = float(list(Instrument.objects.filter(region="In",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_in=[]
    data_in.append(total_in)
    data_in.append("Independent")
    data_in.append(total_in)
    totals.append(data_in)

    total_as = float(list(Instrument.objects.filter(region="AS",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_as=[]
    data_as.append(total_as)
    data_as.append("Asia")
    data_as.append(total_as)
    totals.append(data_as)

    total_rus = float(list(Instrument.objects.filter(region="Rus",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_rus=[]
    data_rus.append(total_rus)
    data_rus.append("Russia Federation")
    data_rus.append(total_rus)
    totals.append(data_rus)

    total_us = float(list(Instrument.objects.filter(region="US",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_us=[]
    data_us.append(total_us)
    data_us.append("United States")
    data_us.append(total_us)
    totals.append(data_us)

    total_eu = float(list(Instrument.objects.filter(region="EU",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_eu=[]
    data_eu.append(total_eu)
    data_eu.append("European Union")
    data_eu.append(total_eu)
    totals.append(data_eu)

    total_af = float(list(Instrument.objects.filter(region="Af",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_af=[]
    data_af.append(total_af)
    data_af.append("Africa")
    data_af.append(total_af)
    totals.append(data_af)

    totals.sort(reverse=True)
    
    for instance in totals:
        if total==0:
            instance[2]="0%"
        else:
            instance[2]=instance[2]/total
            instance[2]=prettify(instance[2])
    
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
        "form":form,
        "form_b":form_b,
        "chart":chart,
         }
    return render(request,"portfolio/region.html",context)





@login_required
def sector_view(request):
    user=request.user
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
    

    totals=[]
    
    total_pm = float(list(Instrument.objects.filter(stake="pm",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_pm=[]
    data_pm.append(total_pm)
    data_pm.append("Precious Metals")
    data_pm.append(total_pm)
    totals.append(data_pm)

    total_eg = float(list(Instrument.objects.filter(stake="Eg",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_eg=[]
    data_eg.append(total_eg)
    data_eg.append("Energy sector")
    data_eg.append(total_eg)
    totals.append(data_eg)

    total_met = float(list(Instrument.objects.filter(stake="Met",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_met=[]
    data_met.append(total_met)
    data_met.append("Metal sector")
    data_met.append(total_met)
    totals.append(data_met)

    total_cs = float(list(Instrument.objects.filter(stake="Cs",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_cs=[]
    data_cs.append(total_cs)
    data_cs.append("Cash")
    data_cs.append(total_cs)
    totals.append(data_cs)

    total_eq = float(list(Instrument.objects.filter(stake="Eq",profiles=user).aggregate(total=Sum('total_price')).values())[0] or 0)
    data_eq=[]
    data_eq.append(total_eq)
    data_eq.append("Equity")
    data_eq.append(total_eq)
    totals.append(data_eq)

    totals.sort(reverse=True)

    for instance in totals:
        if total==0:
            instance[2]="0%"
        else:
            instance[2]=instance[2]/total
            instance[2]=prettify(instance[2])

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
        "form":form,
        "form_b":form_b,
        "chart":chart,
        }
    return render(request,"portfolio/sector.html",context)