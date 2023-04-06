from django.urls import path
from django.shortcuts import get_object_or_404
from . import views
from .models import Post
import re


app_name = 'posts'
urlpatterns = [
    path('', views.PostIndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('account/', views.AccountView.as_view(), name='account'),
]
