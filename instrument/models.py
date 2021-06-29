from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your models here.
REGION_CATEGORY= (
        ('Independent','Independent'),
        ('Europe','Europe'),
        ('Africa','Africa'),
        ('United States','United States'),
        ('Asia','Asia'),
        ('Russia','Russia'),
)
STAKE_CATEGORY=(
        ('Precious Metals','Precious Metals'),
        ('Energy','Energy'),
        ('Metals','Metals'),
        ('Equity','Equity'),
        ('Cash','Cash'),
)

User=get_user_model()

class Instrument(models.Model):
    profiles=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=120)
    price=models.FloatField()
    quantity =models.PositiveIntegerField()
    region=models.CharField(max_length=13, choices=REGION_CATEGORY)
    sector=models.CharField(max_length=15, choices=STAKE_CATEGORY)
    created=models.DateTimeField(auto_now_add=True)
    
    total_price=models.FloatField(blank=True)

    def save(self,*args,**kwargs):
        self.total_price=0+self.price * self.quantity
        self.total_price=round(self.total_price,2)
        return super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.name}, quantity: {self.quantity}"

    def get_absolute_url(self):
        return reverse("update", kwargs={"pk": self.id})


class Stock(models.Model):
    profiles=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    ticker=models.CharField(max_length=120)

    def __str__(self):
        return self.ticker
