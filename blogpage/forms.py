from django import forms
from .models import Article,Category, Comment

        
choice=[]
category= Category.objects.all().values_list('name','name')
for instance in category:
    choice.append(instance)

class AddForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=["title",'category','body','image']

        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            'category':forms.Select(choices=choice,attrs={"class":"form-control"}),
            "body":forms.Textarea(attrs={"class":"form-control"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name','body']

        widgets={
            'name':forms.TextInput(attrs={'class':"form-control"}),
            'body':forms.Textarea(attrs={'class':"form-control"}),
        }