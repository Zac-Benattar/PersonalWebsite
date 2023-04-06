from django.urls import path
from django.shortcuts import get_object_or_404
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostIndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('myaccount/', views.MyAccountView.as_view(), name='myaccount'),
]
