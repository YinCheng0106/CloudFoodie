from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('foods/<int:food_pk>/reviews/create/', views.review_create, name='create'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='delete'),
]
