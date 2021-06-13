from django import forms
from .models import Instrument,Stock
from django.forms import ModelForm, widgets

# region_category= []
# sector_category=[]

# regions=Region.objects.all().values_list('region','region')
# for item in regions:
#     if item in region_category:
#         pass
#     else:
#         region_category.append(item)

# sectors=Sector.objects.all().values_list('sector','sector')
# for item in sectors:
#     if item in sector_category:
#         pass
#     else:
#         sector_category.append(item)


class TickerForm(forms.Form):
    ticker=forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={"class":"form-control mr-sm-2","placeholder":"AAPL"}))


class InstrumentForm(ModelForm):
    class Meta:
        model=Instrument
        fields =['name','price','quantity','region','sector']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control mb-2'}),
            'price': forms.NumberInput(attrs={'class':'form-control mb-2'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control mb-2'}),
            'region':forms.Select(attrs={'class':'form-control mb-2'}),
            'sector':forms.Select(attrs={'class':'form-control mb-4'}),
        }

class BarTypeForm(forms.Form):

    CHART_CHOICES=(
    ('#1','Bar chart'),
    ('#2','Pie chart'),
    ('#3','Line chart'),
    )
    
    chart_type=forms.ChoiceField(choices=CHART_CHOICES,label="Select Chart Type")

class StockForm(ModelForm):
    class Meta:
        model=Stock
        fields=['ticker']
        widgets={
            'ticker':forms.TextInput(attrs={'class':'form-control mr-2'})
        }

