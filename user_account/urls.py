from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='account-login-page'),
    path('login/', views.account_login, name='user_account-login-function'),
    path('category/<int:category_id>/', views.category_view, name='user_account-category_view'),
    path('product/<int:category_id>/', views.product_list_view, name='user_account-product_list_view'),
    path('product/detail/<int:product_id>/', views.product_detail_view, name='user_account-product_detail_view'),
   
]