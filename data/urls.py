from django.urls import path
from .views import InstrumentInvestments,RegionInvestments,SectorInvestments

urlpatterns =[
    path('',InstrumentInvestments.as_view(),name="instrumentInvestment"),
    path('regions/',RegionInvestments,name="regionInvestments"),
    path('sectors/',SectorInvestments,name="sectorInvestments"),
]