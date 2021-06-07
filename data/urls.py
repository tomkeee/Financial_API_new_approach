from django.urls import path
from .views import InstrumentInvestments

urlpatterns =[
    path('',InstrumentInvestments,name="instrumentInvestment")
]