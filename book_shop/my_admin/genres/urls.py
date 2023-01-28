from django.urls import path
from .views import *

urlpatterns = [
    path('', all_genres, name='admin_genres'),
    path('add-genre/', AddGenreViewCreate.as_view(), name='admin_add_genre'),
    path('<int:genre_id>/', GenreViewUpdate.as_view(), name='admin_genre_detail'),
    path('delete/<int:genre_id>/', DeleteGenreView.as_view(), name='admin_genre_delete'),
]
