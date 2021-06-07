from django.http.response import HttpResponse
import requests


headers={
    'Content-Type':'application/json',
    'Authorization':'Token b99cd927b1bcb1633db60f62b5420be17ee12eb8'
}

def get_meta_data(ticker):
    url="https://api.tiingo.com/tiingo/daily/{}".format(ticker)
    response=requests.get(url,headers=headers)
    return response.json()
    

def get_price_data(ticker):
    url="https://api.tiingo.com/tiingo/daily/{}/prices".format(ticker)
    response=requests.get(url,headers=headers)
    return response.json()[0]

API="pk_19c0b9bac0a84df3b10ec61dd1c2d718"
