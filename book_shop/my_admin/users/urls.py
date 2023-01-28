from django.urls import path
from .views import *

urlpatterns = [
    path('', UserList.as_view(), name='admin_users'),
    path('add-user/', AddUserView.as_view(), name='admin_add_user'),
    path('search-user/', Search.as_view(), name='admin_search_user'),
    path('user/<int:user_id>/', UserDetail.as_view(), name='admin_user'),
    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='admin_user_delete'),
]
