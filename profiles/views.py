from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


from .forms import RegisterForm
User = get_user_model()
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('registraion/login')

def login_view(request):
    error_message=None
    form_b= AuthenticationForm()
    if request.method=="POST":
        form_b=AuthenticationForm(data=request.POST)
        if form_b.is_valid():
            username=form_b.cleaned_data.get("username")
            password=form_b.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('/')
        else:
            error_message="Ups ... something went wrong"
    context={
        'form':form_b,
        'error_message':error_message,
    }
    return render(request,"registration/login.html",context)

def register_view(request):
    form=RegisterForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get("password1")
        password2=form.cleaned_data.get("password2")
        try:
            user=User.objects.create_user(username,email,password)
        except:
            user=None
        if user !=None:
            login(request,user)
            return redirect("/")
        else:
            request.session['register_error']=1

    return render(request,"registration/register.html",{"form":form})