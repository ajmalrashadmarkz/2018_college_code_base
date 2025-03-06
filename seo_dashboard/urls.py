from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [    
    path('', views.dashboard_view, name='seo_dashboard-dashboard'),
    path('logout/', views.dashboard_logout, name="seo_dashboard-logout"),
    path('categories/', views.category_list, name='seo_dashboard-category_list'),
    path('categories/<int:pk>/edit/', views.category_edit, name='seo_dashboard-category_edit'),
    path('categories/<int:pk>/', views.category_details, name='seo_dashboard-category_details'),
    

    path('products/', views.product_list, name='seo_dashboard-products_list'),
    path('products/<int:pk>/', views.product_details, name='seo_dashboard-product_details'),
    path('products/<int:pk>/edit/', views.product_edit, name='seo_dashboard-product_edit'),

    path('old_url_redirect/', views.old_url_redirect_list, name='seo_dashboard-old_url_redirect_list'),
    path('old_url_redirect/add/', views.old_url_redirect_create, name='seo_dashboard-old_url_redirect_create'),
    path('old_url_redirect/<int:pk>/edit/', views.old_url_redirect_edit, name='seo_dashboard-old_url_redirect_edit'),
    path('old_url_redirect/<int:pk>/', views.old_url_redirect_details, name='seo_dashboard-old_url_redirect_details'),
    path('old_url_redirect/delete/<int:pk>/', views.old_url_redirect_delete, name='seo_dashboard-old_url_redirect_delete'),

]







    

















