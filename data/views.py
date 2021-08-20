from django.http import request
from portfolio.views import prettify
from django.shortcuts import render
from django.views.generic import ListView
from instrument.models import Instrument
from django.contrib.auth import get_user_model

from django.db.models import Sum

from .serializers import InstrumentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    list_of_id = []
    for session in active_sessions:
        data = session.get_decoded()
        list_of_id.append(data.get('_auth_user_id', None))
    return User.objects.filter(id__in=list_of_id)

class InstrumentInvestments(ListView):
    model=Instrument
    template_name="data/instrumentData.html"

    def get_context_data(self,**kwargs):

        context=super().get_context_data(**kwargs)
        total=0
        all_users=len(get_user_model().objects.all())

        data=[]
        tickers=[]

        qs=Instrument.objects.all()
        total=qs.aggregate(sum=Sum('total_price'))['sum']


        for instance in qs:
            if instance.name in tickers:
                index=tickers.index(instance.name)
                data[index]['invested'] += instance.total_price
                data[index]['hodlers'] += 1

                hodler_per=data[index]['hodlers']/all_users
                hodler_per=prettify(hodler_per)
                data[index]['holders_per']=hodler_per

                investment_per=data[index]['invested']/total
                investment_per=prettify(investment_per)
                data[index]['investment_per']=investment_per

            else:
                package={}
                tickers.append(instance.name)
                package['invested']=instance.total_price
                package['hodlers']=1

                hodler_per=1/all_users
                hodler_per=prettify(hodler_per)
                package['holders_per']=hodler_per

                investment_per=instance.total_price/total
                investment_per=prettify(investment_per)
                package['investment_per']=investment_per

                package['name']=instance.name

                x=instance.name.replace(" ","_")
                x=x.replace("(","_")
                x=x.replace(")","_")
                package['name_as_id']=x

                data.append(package)
        data.sort(key=lambda x:x['invested'], reverse=True)

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

    total = qs.aggregate(sum=Sum('total_price'))['sum']
    for instance in qs:
        if instance.region in regions:
            index=regions.index(instance.region)
            data[index]['invested'] += instance.total_price

            investment_per=data[index]['invested']/total
            investment_per=prettify(investment_per)
            data[index]['investment_per']=investment_per

            if instance.profiles.username in data[index]['hodlers']:
                pass
            else:
                data[index]['hodlers_num'] += 1
                data[index]['hodlers']=instance.profiles.username

            hodler_per=data[index]['hodlers_num']/all_users
            hodler_per=prettify(hodler_per)
            data[index]['hodlers_per']=hodler_per

        else: 
            package={}
            hodler=[]
            regions.append(instance.region)

            package['invested']=instance.total_price
            package['hodlers_num']=1

            hodler_per=1/all_users
            hodler_per=prettify(hodler_per)
            package['hodlers_per']=hodler_per

            investment_per=instance.total_price/total
            investment_per=prettify(investment_per)
            package['investment_per']=investment_per

            package['region']=instance.region
            region_id=instance.region.replace(" ","_")
            package['region_for_id']=region_id

            hodler.append(instance.profiles.username)
            package['hodlers']=hodler
            data.append(package)


    data.sort(key=lambda x:x['invested'], reverse=True)

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

    total=qs.aggregate(sum=Sum('total_price'))['sum']

    for instance in qs:
        if instance.sector in sectors:
            index=sectors.index(instance.sector)
            data[index]['invested'] += instance.total_price

            investment_per=data[index]['invested']/total
            investment_per=prettify(investment_per)
            data[index]['hodler_per']=investment_per

            if instance.profiles.username in data[index]['hodlers']:
                pass
            else:
                data[index]['hodlers_num'] += 1
                data[index]['hodlers']=instance.profiles.username

            hodler_per=data[index]['hodlers_num']/all_users
            hodler_per=prettify(hodler_per)
            data[index]['hodler_per']=hodler_per

        else:
            package={}
            hodler=[]
            sectors.append(instance.sector)
            package['invested']=instance.total_price
            package['hodlers_num']=1

            hodler_per=1/all_users
            hodler_per=prettify(hodler_per)
            package['hodler_per']=hodler_per

            investment_per=instance.total_price/total
            investment_per=prettify(investment_per)
            package['investment_per']=investment_per

            package['sector']=instance.sector
            sector_id=instance.sector.replace(" ","_")
            package['sector_id']=sector_id

            hodler.append(instance.profiles.username)
            package['hodlers']=instance.profiles.username


            data.append(package)
    data.sort(key=lambda x:x['invested'],reverse=True)

    context = {
        "data":data,
        "total":total,
        "all_users":all_users,
    }
    return render(request,"data/sectorInvestment.html",context)

def ClientsData(request):
    active_users=get_current_users()
    context={
        "active_users":len(active_users)
    }

    return render(request,"data/usersData.html",context)

@api_view(['GET'])
def InstrumentsAPI(request):
    instruments=Instrument.objects.all()
    serializer=InstrumentSerializer(instruments,many=True) 
    return Response(serializer.data)

@api_view(["GET"])
def InstrumentAPI(request,pk):
    instrument=Instrument.objects.get(id=pk)
    serializer=InstrumentSerializer(instrument,many=False)
    return Response(serializer.data)

