from django.urls import path

from . import views

app_name = 'foods'

urlpatterns = [
    path('', views.home, name='home'),
    path('foods/create/', views.food_create, name='create'),
    path('foods/<int:pk>/', views.food_detail, name='detail'),
    path('foods/<int:pk>/edit/', views.food_edit, name='edit'),
    path('foods/<int:pk>/delete/', views.food_delete, name='delete'),
    path('foods/<int:pk>/summary/', views.food_summary, name='summary'),
]
