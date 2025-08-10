from django.urls import path
from . import views

urlpatterns = [
    path('borrow/', views.borrow_book_view, name='borrow_book'),
]
