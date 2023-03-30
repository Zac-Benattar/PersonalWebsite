from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/people/', views.PeopleView.as_view(), name='people'),
    path('<int:pk>/tasks/', views.TasksView.as_view(), name='tasks'),
    path('<int:pk>/suggestions/', views.SuggestionsView.as_view(), name='suggestions'),
]


