from .views import add_view,instrument_list,update,delete, research, watchlist,unfollow
from django.urls import path

urlpatterns=[
    path('add/',add_view,name="add"),
    path('investments/',instrument_list,name='instrument_list'),
    path('update/<int:pk>/',update, name="update"),
    path('delete/<int:pk>/',delete, name="delete"),
    path('research/',research,name="research"),
    path('watchlist/',watchlist,name="watchlist"),
    path('unfollow/<int:pk>/',unfollow, name="unfollow"),
]