from django.urls import path
from . import views

urlpatterns = [
    path('categories/new/', views.create_category, name='create_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('categories/', views.category_list, name='category_list'), # для списку категорій
]
