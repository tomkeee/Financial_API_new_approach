from django.db import models
from django.db.models.fields import DateField, DateTimeField
from django.urls import reverse
from PIL import Image
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
    
class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Article(models.Model):
    title=models.CharField(max_length=120)
    body=RichTextField(blank=True,null=True)
    category=models.CharField(max_length=120,default="coding")
    image=models.ImageField(upload_to='blogpage',default="no_picture.png")
    date=models.DateField(auto_now_add=True)
    likes=models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        img= Image.open(self.image.path)
        if img.width > 230 or img.height>180:
            output_size = (230, 179)
            img.thumbnail(output_size)
            img.save(self.image.path)
    def __str__(self):
        return f"{self.title} on {self.date}"

    def get_absolute_url(self):
        # return reverse("detail", kwargs={"pk": self.pk})
        return reverse("list")
    
class Comment(models.Model):
    article=models.ForeignKey(Article,related_name="comments",on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    body=models.TextField()
    date=DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.article.title,self.date.strftime("%Y-%m-%d %H:%M"))