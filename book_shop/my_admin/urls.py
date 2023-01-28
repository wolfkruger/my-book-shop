from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='admin_index'),
    path('orders/', AllOrdersView.as_view(), name='admin_orders'),
    path('orders/detail/<int:order_id>/', order_detail, name='admin_order_detail'),
    path('orders/complete/<int:order_id>/', complete_order, name='admin_complete_order'),
    path('users/', include('my_admin.users.urls')),
    path('books/', include('my_admin.books.urls')),
    path('authors/', include('my_admin.authors.urls')),
    path('genres/', include('my_admin.genres.urls')),
]
