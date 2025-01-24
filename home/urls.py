from django.urls import path
from . import views

urlpatterns = [
    path('charts/', views.home_page, name='home-charts'),
    path('blog/', views.home_page, name='home-blog'),
    path('request-quote/', views.home_page, name='home-request_quote'),
    path('privacy/', views.home_page, name='home-privacy'),
    path('terms/', views.home_page, name='home-terms'),
    path('projects/', views.home_page, name='home-projects'),

    # Quick Links
    path('', views.home_page, name='home-page'),  
    path('about/', views.about_page, name='home-about'),
    path('resources/', views.resources_page, name='home-resources'),
    path('news/', views.news_page, name='home-news'),

    # Company Links
    path('contact/', views.contact_page, name='home-contact'),
    path('careers/', views.careers_page, name='home-careers'),
    path('support/', views.home_page, name='home-support'),
    path('partners/', views.home_page, name='home-partners'),
    

    path('category/<int:category_id>/', views.category_view, name='user_account-category_view'),
    path('product/<int:category_id>/', views.product_list_view, name='user_account-product_list_view'),
    path('product/detail/<int:product_id>/', views.product_detail_view, name='user_account-product_detail_view'),
   

]
