from django.contrib import messages
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
import requests
from .forms import TickerForm,InstrumentForm,StockForm
from django.http import HttpResponseRedirect
from .models import Instrument,Stock
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,CreateView,UpdateView

@login_required
def add_view(request):
    form_add=InstrumentForm(request.POST or None)
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        if form_add.is_valid():
            data=InstrumentForm(request.POST or None)
            obj=data.save(commit=False)
            obj.profiles=request.user
            obj.save()
            return HttpResponseRedirect('/add/')
            
        elif form.is_valid():
            ticker=request.POST['ticker']
            return HttpResponseRedirect(ticker)
        else:
            form=TickerForm()
            form_add=InstrumentForm()

    context={
        "form":form,
        "form_if":form_add,
    }
    return render(request,"instrument/add.html",context)


@login_required
def quote(request):
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            ticker=request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form=TickerForm()
    context={
        "form":form,
    }
    return render(request,'instrument/quote.html',context)


# @login_required
# def ticker(request,tid):
#     form=TickerForm(request.POST or None)
#     if request.method=="POST":
#         if form.is_valid():
#             try:
#                 ticker=request.POST['ticker'].upper()
#                 return redirect(ticker)
#             except KeyError:
#                 ticker="error"
#                 return render(request,'instrument/watchlist.html',{'ticker_wl':ticker})
#     else:
#         form=TickerForm()
#     context={"form":form}
#     context['ticker']=tid
#     context['meta']=get_meta_data(tid)
#     context['price']=get_price_data(tid)
#     # context['fund']=get_fundamentals_data(tid)
#     return render(request,'instrument/ticker.html',context)

@login_required
def list(request):
    user=request.user
    queryset=Instrument.objects.filter(profiles=user).order_by('-total_price')
    context = {
        "qs":queryset
    }
    return render(request,"instrument/list.html",context)

@login_required
def update(request,pk):

    obj=Instrument.objects.get(id=pk)
    form_upd=InstrumentForm(instance=obj)
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        form_upd=InstrumentForm(request.POST,instance=obj)
        if form_upd.is_valid():
            form_upd.save()
            return HttpResponseRedirect('/')
            
        elif form.is_valid():
            ticker=request.POST['ticker']
            return HttpResponseRedirect(ticker)
        else:
            form=TickerForm()
            form_add=InstrumentForm()

    context={
        'object':obj,
        "form_if":form_upd,
        "form":form,

    }
    return render(request,"instrument/update.html",context)

@login_required
def delete(request,pk):
    obj=Instrument.objects.get(id=pk)
    if request.method=="POST":
        obj.delete()
        return redirect("/list/")

    context={'object':obj}
    return render(request,"instrument/delete.html",context)

@login_required
def research(request):
    import requests
    import json

    if request.method=="POST":
        ticker_wl=request.POST['ticker_wl'].upper()
        api_request=requests.get("https://cloud.iexapis.com/stable/stock/" + ticker_wl + "/quote?token="+ API)
        try:
            api=json.loads(api_request.content)
        except:
            api="Error"
        context={
            "ticker_wl":ticker_wl,
            "api":api
        }
        return render(request,'instrument/research.html',context)
        
    else:
        return render(request,'instrument/research.html',{'ticker':"Enter a Ticker symbol above"})

@login_required
def watchlist(request):
    import requests
    import json

    user=request.user
    form=TickerForm(request.POST or None)
    form_add=StockForm(request.POST or None)
    if request.method=="POST":
        if form_add.is_valid():
            data=StockForm(request.POST or None)
            obj=data.save(commit=False)
            obj.profiles=request.user
            obj.save()
            messages.success(request,("Stock has been added!"))
            return redirect('/watchlist/')
        elif form.is_valid():
            ticker=request.POST['ticker']
            return redirect(ticker)
    else:
        ticker=Stock.objects.filter(profiles=user)
        output=[]
        for instance in ticker:
            data=[]
            api_request=requests.get("https://cloud.iexapis.com/stable/stock/" + str(instance) + "/quote?token=pk_19c0b9bac0a84df3b10ec61dd1c2d718")
            try:
                api=json.loads(api_request.content)
                data.append(instance.id)
                data.append(api)
                output.append(data)
            except:
                instance.delete()
                api="Error"

    context={
        "form":form,"form_add":form_add,"ticker":ticker,"output":output
        }

    return render(request,'instrument/watchlist.html',context)

def unfollow(request,pk):
    obj=Stock.objects.get(id=pk)
    obj.delete()
    messages.success(request,("Stock has been unfollowed"))
    return redirect("/watchlist/")
