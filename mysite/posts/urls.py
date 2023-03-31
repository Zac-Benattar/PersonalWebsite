from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostIndexView.as_view(), name='index'),
    path('blogpost/<int:pk>/', views.BlogPostDetailView.as_view(), name='blogdetail'),
    path('albumpost/<int:pk>/', views.AlbumPostDetailView.as_view(), name='albumdetail'),
    path('videopost/<int:pk>/', views.VideoPostDetailView.as_view(), name='videodetail'),
]


