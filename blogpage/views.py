from django.urls import reverse_lazy,reverse
from django.shortcuts import render,get_object_or_404
from .models import Article,Comment,Category
from .forms import AddForm,CommentForm
from django.http import HttpResponseRedirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
import requests
from .data import API

# Create your views here.
def LikeView(request,pk):
    article=get_object_or_404(Article, id=request.POST.get('article_id'))
    article.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail-article',args=[str(pk)]))

    

class ArticleListView(ListView):
    model=Article
    template_name="blogpage/list.html"

    def get_context_data(self, **kwargs):

        context={}
        context['object_list']=Article.objects.all()
##########################################################  time  ############################################################
        parameters = {"api_key":"32e4642a881d4783377e387aadb6d8cf0d0ea229", "format": "json"}
        url = "https://api.getgeoapi.com/v2/ip/check"

        try:
            api=requests.get(url, parameters)
            api=api.json()
            api=api['time']['time'][0:10]
        except:
            api="Error"

        context['api']=api
##########################################################  exchange rate  #############################################################
        url2 = "https://currency-exchange.p.rapidapi.com/exchange"

        querystring_up = {"to":"PLN","from":"USD","q":"1.0"}
        querystring_uh = {"to":"HKD","from":"USD","q":"1.0"}
        querystring_uc = {"to":"CNY","from":"USD","q":"1.0"}

        headers = {
            'x-rapidapi-key': "0e94fa3e43msh9c5023219d374e8p1e2723jsnab5c586bdfd9",
            'x-rapidapi-host': "currency-exchange.p.rapidapi.com"
            }

        u_p = requests.request("GET", url2, headers=headers, params=querystring_up).json()
        u_h = requests.request("GET", url2, headers=headers, params=querystring_uh).json()
        u_c = requests.request("GET", url2, headers=headers, params=querystring_uc).json()


        u_p=round(u_p,2)
        u_h=round(u_h,2)
        u_c=round(u_c,2)
        
        context['u_p']=u_p
        context['u_h']=u_h
        context['u_c']=u_c

##########################################################  BTC   #############################################################
        url3 = "https://bitcoinaverage-global-bitcoin-index-v1.p.rapidapi.com/indices/global/ticker/BTCUSD"

        headers = {
            'x-rapidapi-key': "0e94fa3e43msh9c5023219d374e8p1e2723jsnab5c586bdfd9",
            'x-rapidapi-host': "bitcoinaverage-global-bitcoin-index-v1.p.rapidapi.com"
            }

        btc = requests.request("GET", url3, headers=headers).json()

        btc_price=btc['last']

        btc_change=btc['changes']['percent']['day']

        context['btc_change']=btc_change
        context['btc_price']=btc_price
        return context


def CategoryView(request,cat):
    posts=Article.objects.filter(category=cat.replace('-',' '))
    context={
        'category':cat.replace('-',' '),
        "posts":posts,
    }
    return render(request,'blogpage/categories.html',context)

class ArticleDetailView(DetailView):
    model=Article
    template_name="blogpage/detail.html"

    def get_context_data(self,*args, **kwargs):

        context=super(ArticleDetailView,self).get_context_data(*args,**kwargs)

        data=get_object_or_404(Article,id=self.kwargs['pk'])
        total_likes=data.total_likes()
        context["total_like"] = total_likes
        return context

class ArticleCreateView(CreateView):
    model=Article
    template_name="blogpage/add.html"
    form_class=AddForm

class ArticleUpdateView(UpdateView):
    model=Article
    template_name="blogpage/add.html"
    form_class=AddForm

class ArticleDeleteView(DeleteView):
    model=Article
    template_name="blogpage/delete.html"
    success_url=reverse_lazy('list')

class CommentView(CreateView):
    model=Comment
    template_name="blogpage/add_comment.html"
    form_class=CommentForm
    success_url="/"

    def form_valid(self,form):
            form.instance.article_id=self.kwargs['pk']
            return super().form_valid(form)