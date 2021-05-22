from django import forms
from .models import Instrument
from django.forms import ModelForm


class TickerForm(forms.Form):
    ticker=forms.CharField(required=False,max_length=100,widget=forms.TextInput(attrs={"class":"form-control mr-sm-2","placeholder":"AAPL"}))

class InstrumentForm(ModelForm):
    class Meta:
        model=Instrument
        fields =['profiles','name','price','quantity','region','stake']
        exclude=['profiles']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control mb-4'}),
            'price': forms.NumberInput(attrs={'class':'form-control mb-4'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control mb-4'}),
            'region':forms.Select(attrs={'class':'form-control mb-4'}),
            'stake':forms.Select(attrs={'class':'form-control mb-4'}),
        }

class BarTypeForm(forms.Form):

    CHART_CHOICES=(
    ('#1','Bar chart'),
    ('#2','Pie chart'),
    ('#3','Line chart'),
    )
    
    chart_type=forms.ChoiceField(choices=CHART_CHOICES,label="Select Chart Type")


