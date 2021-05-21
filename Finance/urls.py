"""Finance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from instrument.views import quote,ticker,add_view
from portfolio.views import portfolio_view,region_view,sector_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quote/',quote),
    path('',portfolio_view),
    path('region/',region_view),
    path('sector/',sector_view),
    path('add/',add_view),
    path('quote/<str:tid>/',ticker, name='ticker'),
]
