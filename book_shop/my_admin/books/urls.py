from django.urls import path
from .views import *

urlpatterns = [
    path('', AllBooks.as_view(), name='admin_books'),
    path('<int:book_id>/', BookViewUpdate.as_view(), name='admin_book_detail'),
    path('delete/<int:book_id>/', DeleteBookView.as_view(), name='admin_book_delete'),
    path('search/', Search.as_view(), name='admin_search'),
    path('add-book/', AddBookViewCreate.as_view(), name='admin_add_book'),
]
