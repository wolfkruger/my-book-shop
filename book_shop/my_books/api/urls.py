from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'books', BooksViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('books/', BooksAPIView.as_view()),
    #path('books/<int:pk>/', BookDetailAPIView.as_view()),

    path('my-cart/', CartViewSet.as_view({'get': 'list'})),
    path('add-to-my-cart/<int:pk>/', CartViewSet.as_view({'post': 'create'}), name='add_to_my_cart_api'),
    path('remove-from-my-cart/', CartViewSet.as_view({'post': 'update'})),
    path('clear-my-cart/', CartViewSet.as_view({'post': 'destroy'})),

    path('my-orders/', OrderViewSet.as_view({'get': 'list'})),
    path('get-order/', OrderViewSet.as_view({'post': 'create'})),

    path('drf-auth/', include('rest_framework.urls')),  # регистрация и аутентификация по сессиям
    path('auth/', include('djoser.urls')),  # регистрация и аутентификация по токенам через Djoser
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('register/', RegisterAPIView.as_view()),  # моя регистрация

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_refresh'),
]
