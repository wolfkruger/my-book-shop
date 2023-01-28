from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('books/', cache_page(60)(BooksListView.as_view()), name='book_list'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('books/search/', Search.as_view(), name='search'),

    path('add-to-my-cart/<int:book_id>/', add_to_cart, name='add_to_my_cart'),
    path('add-and-del/<int:book_id>/', add_and_del, name='add_and_del'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('confirm-clear-cart/', confirm_clear_cart, name='confirm_clear_cart'),
    path('my-cart/', cart_view, name='my_cart'),

    path('order/<int:book_id>/', get_order, name='order'),
    path('confirm_order/<int:book_id>/', confirm_order, name='confirm_order'),
    path('my-orders', MyOrdersView.as_view(), name='my_orders'),

    path('admin/', to_admin, name='admin'),
]