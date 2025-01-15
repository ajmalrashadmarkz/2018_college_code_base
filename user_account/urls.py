from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='account-login-page'),
    path('login/', views.account_login, name='user_account-login-function'),
    
]