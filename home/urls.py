from django.urls import path
from . import views

urlpatterns = [
    path('charts/', views.home_page, name='home-charts'),
    path('blog/', views.home_page, name='home-blog'),
    path('request-quote/', views.home_page, name='home-request_quote'),
    path('', views.home_page, name='home-page'),  # Assuming the home page is at the root URL
    path('projects/', views.home_page, name='home-projects'),
    path('support/', views.home_page, name='home-support'),
    path('partners/', views.home_page, name='home-partners'),
    path('about/', views.home_page, name='home-about'),
    path('contact/', views.home_page, name='home-contact'),
    path('faq/', views.home_page, name='home-faq'),
    path('careers/', views.home_page, name='home-careers'),
    path('privacy/', views.home_page, name='home-privacy'),
    path('terms/', views.home_page, name='home-terms'),

]
