from django.urls import path
from .views import ArticleListView,ArticleDetailView,ArticleCreateView,ArticleUpdateView,ArticleDeleteView,CategoryView,LikeView,CommentView

urlpatterns = [
    path("",ArticleListView.as_view(),name="list"),
    path("article/<int:pk>/",ArticleDetailView.as_view(),name="detail-article"),
    path('article/comment/<int:pk>/',CommentView.as_view(),name='comment-article'),
    path("article/update/<int:pk>/",ArticleUpdateView.as_view(),name="update-article"),
    path("article/add/",ArticleCreateView.as_view(),name="create-article"),
    path('article/delete/<int:pk>/',ArticleDeleteView.as_view(),name="delete-article"),
    path('category/<str:cat>/',CategoryView,name='category'),
    path('like/<int:pk>/',LikeView,name='like-article'),

]
