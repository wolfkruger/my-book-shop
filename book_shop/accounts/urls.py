from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='my_login'),
    path('logout/', logout_user, name='my_logout'),
    path('profile/', user_profile, name='profile'),
    path('change_user_data/', ChangeUserData.as_view(), name='change_user_data'),
    path('password/', ChangeUserPassword.as_view(), name='change_user_password'),
    path('reset_password/', UserResetPassword.as_view(), name='reset_password'),
    path('reset_password_sent/', UserResetPasswordDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', UserResetPasswordComplete.as_view(), name='password_reset_complete'),
]
