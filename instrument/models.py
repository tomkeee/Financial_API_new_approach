from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your models here.
REGION_CATEGORY= (
        ('In','Independent'),
        ('EU','Europe'),
        ('Af','Africa'),
        ('US','United States'),
        ('AS','Asia'),
        ('Rus','Russia'),
)
STAKE_CATEGORY=(
        ('pm','Precious Metals'),
        ('Eg','Energy'),
        ('Met','Metals'),
        ('Eq','Equity'),
        ('Cs','Cash'),
)


User=get_user_model()

class Instrument(models.Model):
    profiles=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=120)
    price=models.FloatField(default=0)
    quantity =models.PositiveIntegerField(default=0)
    region=models.CharField(max_length=3, choices=REGION_CATEGORY, default='In')
    stake=models.CharField(max_length=3, choices=STAKE_CATEGORY, default="pm")
    
    total_price=models.FloatField(blank=True,default=0)

    def save(self,*args,**kwargs):
        self.total_price=0+self.price * self.quantity
        self.total_price=round(self.total_price,2)
        return super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.name}, quantity: {self.quantity}"

    def get_absolute_url(self):
        return reverse("update", kwargs={"pk": self.id})


class Stock(models.Model):
    ticker=models.CharField(max_length=10)

    def __str__(self):
        return self.ticker
