from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.views import generic
from .forms import EditProfileForm,ChangePasswordForm,RegisterForm

User=get_user_model()

def logout_view(request):
    logout(request)
    return redirect('/login')

def login_view(request):
    error_message=None
    form_b= AuthenticationForm()
    print(form_b)
    print(request.COOKIES)
    print(request.session.session_key)

    if request.method=="POST":
            form_b=AuthenticationForm(data=request.POST)
            if form_b.is_valid():
                username=form_b.cleaned_data.get("username")
                password=form_b.cleaned_data.get('password')
                user = authenticate(username=username,password=password)
                print("Cleaned data ",form_b.cleaned_data)
                print("The user: ",user)
                if user is not None:
                    login(request,user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('/')
            else:
                error_message="Ups ... something went wrong"
        # else:
            # return HttpResponse("Validation error has occured")
        
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

class UserEditView(generic.UpdateView):
    form_class=EditProfileForm
    template_name="registration/edit.html"
    success_url='/'

    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class=ChangePasswordForm
    success_url=reverse_lazy('main')
    