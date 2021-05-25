from .models import Instrument,Stock
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=Instrument)
def post_save_create_watchlistModel(sender,instance,created,**kwargs):
    if created:
        Stock.objects.create(ticker=instance.name)
