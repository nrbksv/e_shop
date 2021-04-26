from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import UserRegisterView, UserStatisticsView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('statistics/', UserStatisticsView.as_view(), name='user-statistics'),
]