from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_search_view, name='book_list'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('book/create/', views.book_create_view, name='book_create'),
]
