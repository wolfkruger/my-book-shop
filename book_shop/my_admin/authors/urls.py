from django.urls import path
from .views import *

urlpatterns = [
    path('', all_authors, name='admin_authors'),
    path('add-author/', AddAuthorViewCreate.as_view(), name='admin_add_author'),
    path('<int:author_id>/', AuthorViewUpdate.as_view(), name='admin_author_detail'),
    path('delete/<int:author_id>/', DeleteAuthorView.as_view(), name='admin_author_delete'),
]
