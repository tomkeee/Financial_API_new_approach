from portfolio.views import prettify
from django.shortcuts import render
from django.views.generic import ListView
from instrument.models import Instrument
from django.contrib.auth import get_user_model

class InstrumentInvestments(ListView):
    model=Instrument
    template_name="data/instrumentData.html"

    def get_context_data(self):
        context={}
        total=0
        all_users=len(get_user_model().objects.all())

        data=[]
        tickers=[]

        qs=Instrument.objects.all()
        for instance in qs:
            total += instance.total_price

        for instance in qs:
            if instance.name in tickers:
                index=tickers.index(instance.name)
                data[index][0] += instance.total_price
                data[index][1] += 1

                hodler_per=data[index][1]/all_users
                hodler_per=prettify(hodler_per)
                data[index][2]=hodler_per

                investment_per=data[index][0]/total
                investment_per=prettify(investment_per)
                data[index][3]=investment_per

            else:
                package=[]
                tickers.append(instance.name)
                package.append(instance.total_price)
                package.append(1)

                hodler_per=1/all_users
                hodler_per=prettify(hodler_per)
                package.append(hodler_per)

                investment_per=instance.total_price/total
                investment_per=prettify(investment_per)
                package.append(investment_per)

                package.append(instance.name)

                x=instance.name.replace(" ","_")
                x=x.replace("(","_")
                x=x.replace(")","_")

                package.append(x)

                print(package)
                data.append(package)

        data.sort(reverse=True)

        context['data']=data
        context['total']=total
        context['all_users']=all_users

        return context
    

def RegionInvestments(request):
    qs=Instrument.objects.all()
    total=0
    all_users=len(get_user_model().objects.all())

    data=[]
    regions=[]

    for instance in qs:
        total += instance.total_price
    for instance in qs:
        if instance.region in regions:
            index=regions.index(instance.region)
            data[index][0] += instance.total_price

            investment_per=data[index][0]/total
            investment_per=prettify(investment_per)
            data[index][3]=investment_per

            if instance.profiles.username in data[index][5]:
                pass
            else:
                data[index][1] += 1
                data[index][5].append(instance.profiles.username)

            hodler_per=data[index][1]/all_users
            hodler_per=prettify(hodler_per)
            data[index][2]=hodler_per

        else:
            package=[]
            hodler=[]
            regions.append(instance.region)
            package.append(instance.total_price)
            package.append(1)

            hodler_per=1/all_users
            hodler_per=prettify(hodler_per)
            package.append(hodler_per)

            investment_per=instance.total_price/total
            investment_per=prettify(investment_per)
            package.append(investment_per)

            package.append(instance.region)

            hodler.append(instance.profiles.username)
            package.append(hodler)


            data.append(package)

    data.sort(reverse=True)

    context = {
    "data":data,
    "total":total,
    "all_users":all_users,
    }
    return render(request,"data/regionInvestment.html",context)
    


def SectorInvestments(request):
    qs=Instrument.objects.all()
    total=0
    id=0
    all_users=len(get_user_model().objects.all())

    data=[]
    sectors=[]

    for instance in qs:
        total += instance.total_price
    for instance in qs:
        if instance.sector in sectors:
            index=sectors.index(instance.sector)
            data[index][0] += instance.total_price

            investment_per=data[index][0]/total
            investment_per=prettify(investment_per)
            data[index][3]=investment_per

            if instance.profiles.username in data[index][5]:
                pass
            else:
                data[index][1] += 1
                data[index][5].append(instance.profiles.username)

            hodler_per=data[index][1]/all_users
            hodler_per=prettify(hodler_per)
            data[index][2]=hodler_per

        else:
            package=[]
            hodler=[]
            sectors.append(instance.sector)
            package.append(instance.total_price)
            package.append(1)

            hodler_per=1/all_users
            hodler_per=prettify(hodler_per)
            package.append(hodler_per)

            investment_per=instance.total_price/total
            investment_per=prettify(investment_per)
            package.append(investment_per)

            package.append(instance.sector)

            hodler.append(instance.profiles.username)
            package.append(hodler)


            data.append(package)

    data.sort(reverse=True)

    context = {
        "data":data,
        "total":total,
        "all_users":all_users,
    }
    return render(request,"data/sectorInvestment.html",context)