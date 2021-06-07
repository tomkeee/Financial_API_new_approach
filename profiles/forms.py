from django import forms
from django.forms import widgets
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm

User = get_user_model()

class RegisterForm(forms.Form):
    username=forms.CharField()
    email =forms.EmailField()
    password1=forms.CharField(label="Password",widget=forms.PasswordInput())
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput())

    def clean_password2(self):
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("The given passwords do not match")
        return password2

    def clean_email(self):
        email= self.cleaned_data.get("email")
        qs=User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already taken")
        return email

    def clean_username(self):
        username= self.cleaned_data.get("username")
        qs=User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("This user is already taken")
        return username

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    def clean_username(self):
        username=self.cleaned_data.get("username")
        qs= User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("This user does not exist.")
        return username

    def clean_password(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")

        user_qs=User.objects.filter(username__iexact=username)
        if user_qs.exists():
            user_a=user_qs.first()
            if not user_a.check_password(password):
                raise forms.ValidationError("Given password is not correct")
        return password

class EditProfileForm(UserChangeForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control mb-2'}))
    first_name=forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    last_name=forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control mb-2'}))
    username=forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-controlmb mb-2'}))
    
    class Meta:
        model=User
        fields=('username','first_name','last_name','email')


class ChangePasswordForm(PasswordChangeForm):
    old_password=forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control mb-3'}),label="Current password")
    new_password1=forms.CharField(max_length=120,widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}),label="New password")
    new_password2=forms.CharField(max_length=120,widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}),label="Confirm password")
    
    class Meta:
        model=User
        fields=('old_password',"new_password1","new_password2")
