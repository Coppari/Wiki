from django.urls import path
    
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("new",views.newPage, name ="new_page"),
    path('edit_entry/<str:title>/', views.editEntry, name='edit_entry'),
    path('delete_entry/<str:title>/', views.deleteEntry, name='delete_entry'),
    path("random/", views.randomPage, name="random_page"),
]
