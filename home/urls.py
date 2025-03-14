from django.urls import path
from . import views
from django.urls import path, re_path

urlpatterns = [
    path('charts/', views.home_page, name='home-charts'),
    path('blog/', views.home_page, name='home-blog'),
    #path('request-quote/', views.home_page, name='home-request_quote'),
    #path('projects/', views.about_page, name='home-projects'),

    # Quick Links
    path('', views.home_page, name='home-page'),  
    path('about/', views.about_page, name='home-about'),
    path('resources/', views.resources_page, name='home-resources'),
    path('news/', views.news_page, name='home-news'),

    # Company Links
    path('contact/', views.contact_page, name='home-contact'),
    path('careers/', views.careers_page, name='home-careers'),
    
    


    #JobApplication -ContactUs-NewsLetter
    path('careers/submit/', views.submit_application, name='submit_application'),
    path('contact/submit/', views.submit_contact, name='submit_contact'),
    path('newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
   
    path('partners/', views.partners_page, name='home-partners'),
    path('support/', views.support_page, name='home-support'),
    path('privacy/', views.policy_page, name='home-privacy'),
    path('terms/', views.terms_page, name='home-terms'),
    path('e-guides/', views.guide_page, name='home-e_books'),

    path('projects/', views.about_page, name='home-projects'),
    # path('projects/<int:pk>/', views.project_detail, name='home-project_detail'),
    path('projects/<slug:slug>/', views.project_detail, name='home-project_detail'),

    
    path('blog/<slug:slug>/', views.blog_detail, name='home-blog_detail'),

    path('news/<slug:slug>/', views.news_detail, name='home-news_detail'),

    path('request-quote/', views.request_quote, name='home-request_quote'),
    path('submit-enquiry/', views.submit_customer_enquiry, name='submit_customer_enquiry'),
    path('submit-question/',  views.submit_question, name='submit_question'),
    path('partner-application/', views.partner_application, name='partner_application'),

    #path('category/<int:category_id>/', views.category_view, name='user_account-category_view'),
    path('category/<int:category_id>/', views.category_by_id, name='user_account-category_by_id'),
    path('<slug:category_slug>/', views.category_view, name='user_account-category_view'),
    path('product-list/<slug:category_slug>/', views.product_list_view, name='user_account-product_list_view'), 
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail_view, name='user_account-product_detail_view'),

    # re_path(r'^(?P<php_filename>[\w-]+\.php)$', views.php_to_category_redirect),
    re_path(r'^(?P<php_filename>[\w-]+\.php)$', views.php_to_new_url_redirect),
]
