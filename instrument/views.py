from django.shortcuts import render,redirect
from .tiingo import get_meta_data,get_price_data
from .forms import TickerForm,InstrumentForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def add_view(request):
    form_if=InstrumentForm(request.POST or None)
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        if form_if.is_valid():
            form_if.save(commit=False)
            form_if.user=request.user
            form_if.save()
            form_if=InstrumentForm()

        elif form.is_valid():
            ticker=request.POST['ticker']
            return HttpResponseRedirect(ticker)
        else:
            form=TickerForm()
            form_if=InstrumentForm()
    context={
        "form":form,
        "form_if":form_if,
    }
    return render(request,"instrument/add.html",context)



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

def ticker(request,tid):
    form=TickerForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            ticker=request.POST['ticker']
            return redirect(ticker)
    else:
        form=TickerForm()
    context={"form":form}
    context['ticker']=tid
    context['meta']=get_meta_data(tid)
    context['price']=get_price_data(tid)
    # context['fund']=get_fundamentals_data(tid)
    return render(request,'instrument/ticker.html',context)