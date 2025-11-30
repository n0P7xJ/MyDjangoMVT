from django.urls import path
from . import views

app_name = 'dishes'

urlpatterns = [
    path('', views.dish_list, name='list'),                  # /dishes/ - список страв
    path('add/', views.dish_create, name='add'),             # /dishes/add/ - створити страву
    path('<int:pk>/edit/', views.dish_update, name='edit'),  # /dishes/1/edit/ - редагувати
    path('<int:pk>/delete/', views.dish_delete, name='delete'), # /dishes/1/delete/ - видалити
]
