from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "landing-page"),
    # path("survey/<int:id>/", views.show_survey, name="show-survey"),
    path("survey/<int:id>/", views.show_survey, name="show-survey"),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('login_page/', views.login_page, name='account-login-page'),
    path('login/', views.account_login, name='user_account-login-function'),
    
]