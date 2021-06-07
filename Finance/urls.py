from django.contrib import admin
from django.urls import path,include
from instrument.views import quote,add_view,list,update,delete, research, watchlist,unfollow
from portfolio.views import portfolio_view,region_view,sector_view
from profiles.views import login_view,logout_view,register_view
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from profiles.views import login_view,logout_view,UserEditView,PasswordsChangeView

urlpatterns = [
    path("blog/",include('blogpage.urls')),

    path('admin/', admin.site.urls),
    path('register/',register_view),
    path('login/',login_view,name='login'),
    path('logout/',logout_view),
    path('edit/',UserEditView.as_view()),
    path('password/',PasswordsChangeView.as_view(template_name='registration/changePassword.html')),

    path('quote/',quote),
    path('research/',research),
    path('watchlist/',watchlist),
    path('unfollow/<int:pk>/',unfollow, name="unfollow"),

    path('add/',add_view),
    path('list/',list),
    path('update/<int:pk>/',update, name="update"),
    path('delete/<int:pk>/',delete, name="delete"),

    path('',portfolio_view,name='main'),
    path('region/',region_view),
    path('sector/',sector_view),

    path('summary/',include('portfolio.urls')),
    path('data/',include('data.urls')),



]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)