from .models import Instrument,Stock
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save,sender=Instrument)
def post_save_create_watchlistModel(sender,instance,created,**kwargs):
    if created:
        Stock.objects.create(ticker=instance.name, profiles=instance.profiles)


