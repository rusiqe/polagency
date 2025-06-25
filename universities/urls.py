from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    path('', views.university_list, name='university_list'),
    path('programs/', views.program_search, name='program_search'),
    path('<slug:slug>/', views.university_detail, name='university_detail'),
]

