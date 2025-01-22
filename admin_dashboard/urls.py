from django.urls import path
from . import views
from catalog.views import (
                category_list, category_create, category_edit, category_details, category_delete,
                product_list, product_create, product_details, product_edit, product_delete,
                download_document,view_document
                )


urlpatterns = [
    path('', views.dashboard_view, name='admin_dashboard-dashboard'),
    path('logout/', views.dashboard_logout, name="admin_dashboard-logout"),
    path('categories/', category_list, name='admin_dashboard-category_list'),
    path('categories/add/', category_create, name='admin_dashboard-category_add'),
    path('categories/<int:pk>/edit/', category_edit, name='admin_dashboard-category_edit'),
    path('categories/<int:pk>/', category_details, name='admin_dashboard-category_details'),
    path('categories/<int:pk>/delete/', category_delete, name='admin_dashboard-category_delete'),

    path('products/', product_list, name='admin_dashboard-products_list'),
    path('products/add/', product_create, name='admin_dashboard-product_add'),
    path('products/<int:pk>/', product_details, name='admin_dashboard-product_details'),
    path('products/<int:pk>/edit/', product_edit, name='admin_dashboard-product_edit'),
    path('product/delete/<int:pk>/', product_delete, name='admin_dashboard-product_delete'),
   

    path('document/<int:doc_id>/download/', download_document, name='admin_dashboard-download_document'),
    path('view-document/<int:doc_id>/', view_document, name='admin_dashboard-view_document'),

    path('news_article/', views.news_article_list, name='admin_dashboard-news_article_list'),
    path('news_article/add/', views.news_article_create, name='admin_dashboard-news_article_create'),
    path('news_article/<int:pk>/edit/', views.news_article_edit, name='admin_dashboard-news_article_edit'),
    path('news_article/<int:pk>/',views.news_article_details, name='admin_dashboard-news_article_details'),
    path('news_article/delete/<int:pk>/',views.news_article_delete, name='admin_dashboard-news_article_delete'),


    path('blog_post/', views.blog_post_list, name='admin_dashboard-blog_post_list'),
    path('blog_post/add/', views.blog_post_create, name='admin_dashboard-blog_post_create'),
    path('blog_post/<int:pk>/edit/', views.blog_post_edit, name='admin_dashboard-blog_post_edit'),
    path('blog_post/<int:pk>/',views.blog_post_details, name='admin_dashboard-blog_post_details'),
    path('blog_post/delete/<int:pk>/',views.blog_post_delete, name='admin_dashboard-blog_post_delete'),


    path('job_listing/', views.job_listing_list, name='admin_dashboard-job_listing_list'),
    path('job_listing/add/', views.job_listing_create, name='admin_dashboard-job_listing_create'),
    path('job_listing/<int:pk>/edit/', views.job_listing_edit, name='admin_dashboard-job_listing_edit'),
    path('job_listing/<int:pk>/', views.job_listing_details, name='admin_dashboard-job_listing_details'),
    path('job_listing/delete/<int:pk>/', views.job_listing_delete, name='admin_dashboard-job_listing_delete'),


    
]











