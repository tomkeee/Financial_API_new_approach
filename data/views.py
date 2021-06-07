from django.shortcuts import render
from django.views.generic import ListView
from instrument.models import Instrument

from django.contrib.auth import get_user_model

# def InstrumentInvestments(request):
#     qs=Instrument.objects.all()
#     total=0
#     all_users=len(get_user_model().objects.all())

#     data=[]
#     tickers=[]

#     id=0
#     for instance in qs:
#         total += instance.total_price
#         if instance.name in tickers:
#             index=tickers.index(instance.name)
#             data[index]['investment'] += instance.total_price
#             data[index]['hodler'] += 1
#             data[index]['hodler_per']=data[index]['hodler']/all_users



#         else:
#             package={}
#             tickers.append(instance.name)
#             id+=1
#             package['id']=id
#             package['ticker']=instance.name
#             package['investment']=instance.total_price
#             package['hodler']=1
#             hodler_per=1/all_users
#             round(hodler_per,2)
#             package['hodler_per']=hodler_per

#             data.append(package)

#     context = {
#         "data":data,
#         "total":total,
#         "all_users":all_users,
#     }
#     return render(request,"data/instrumentData.html",context)

class InstrumentInvestments(ListView):
    model=Instrument
    template_name="data/instrumentData.html"

    def get_context_data(self):
        context={}
        qs=Instrument.objects.all()
        total=0
        id=0
        all_users=len(get_user_model().objects.all())

        data=[]
        tickers=[]

        for instance in qs:
            total += instance.total_price
        for instance in qs:
            if instance.name in tickers:
                index=tickers.index(instance.name)
                data[index]['investment'] += instance.total_price
                data[index]['hodler'] += 1
                data[index]['hodler_per']=data[index]['hodler']/all_users

                investment_per=data[index]['investment']/total
                investment_per=(round(investment_per,2) *100)
                data[index]['investment_per']=investment_per

            else:
                package={}
                tickers.append(instance.name)
                id+=1
                package['id']=id
                package['ticker']=instance.name
                package['investment']=instance.total_price
                package['hodler']=1
                hodler_per=1/all_users
                round(hodler_per,2)
                package['hodler_per']=hodler_per

                investment_per=instance.total_price/total
                investment_per=(round(investment_per,2) *100)
                package['investment_per']=investment_per

                data.append(package)

        context['data']=data
        context['total']=total
        context['all_users']=all_users

        return context
    

def RegionInvestments(request):
    qs=Instrument.objects.all()
    total=0
    id=0
    all_users=len(get_user_model().objects.all())

    data=[]
    regions=[]

    for instance in qs:
        total += instance.total_price
    
    for instance in qs:
        if instance.region in regions:
            index=regions.index(instance.region)

            data[index]['investment'] += instance.total_price

            investment_per=data[index]['investment']/total
            investment_per=(100*round(investment_per,2))
            data[index]['investment_per']=investment_per


            if instance.profiles.username in data[index]['hodler']:
                data[index]['hodler_num']= data[index]['hodler_num']
            else:
                data[index]['hodler_num'] += 1
                data[index]['hodler'] += [instance.profiles.username]

            hodler_per=data[index]['hodler_num']/all_users
            hodler_per=(round(hodler_per,2) * 100)
            data[index]['hodler_per']=hodler_per

        else:
            package={}
            regions.append(instance.region)
            id += 1
            package['id']=id
            package['region']=instance.region
            package['hodler']=[instance.profiles.username]
            package['hodler_num']=1
            package['investment']=instance.total_price

            hodler_per=1/all_users
            hodler_per = (round(hodler_per,2) * 100)
            package['hodler_per']=hodler_per

            investment_per=instance.total_price/total
            investment_per=(100*round(investment_per,2))
            package['investment_per']=investment_per
            
            data.append(package)

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
        if instance.stake in sectors:
            index=sectors.index(instance.stake)

            data[index]['investment'] += instance.total_price

            investment_per=data[index]['investment']/total
            investment_per=(100*round(investment_per,2))
            data[index]['investment_per']=investment_per


            if instance.profiles.username in data[index]['hodler']:
                data[index]['hodler_num']= data[index]['hodler_num']
            else:
                data[index]['hodler_num'] += 1
                data[index]['hodler'] += [instance.profiles.username]

            hodler_per=data[index]['hodler_num']/all_users
            hodler_per=(round(hodler_per,2) * 100)
            data[index]['hodler_per']=hodler_per

        else:
            package={}
            sectors.append(instance.stake)
            id += 1
            package['id']=id
            package['sector']=instance.stake
            package['hodler']=[instance.profiles.username]
            package['hodler_num']=1
            package['investment']=instance.total_price

            hodler_per=1/all_users
            hodler_per=(round(hodler_per,2) * 100)
            package['hodler_per']=hodler_per

            investment_per=instance.total_price/total
            investment_per=(100*round(investment_per,2))
            package['investment_per']=investment_per
            
            data.append(package)

    context = {
        "data":data,
        "total":total,
        "all_users":all_users,
    }
    return render(request,"data/sectorInvestment.html",context)