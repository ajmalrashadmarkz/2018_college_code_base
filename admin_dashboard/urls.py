from django.urls import path
from . import views



urlpatterns = [
    path('account/', views.dashboard_view, name='admin_dashboard-dashboard'), 
    path('logout/', views.dashboard_logout, name="admin_dashboard-logout"),

    path('survey/', views.survey_list, name='admin_dashboard-survey_list'),
    path('survey/add/', views.survey_create, name='admin_dashboard-survey_create'),
    path('survey/<int:pk>/edit/', views.survey_edit, name='admin_dashboard-survey_edit'),
    path('survey/<int:pk>/', views.survey_details, name='admin_dashboard-survey_details'),
    path('survey/delete/<int:pk>/', views.survey_delete, name='admin_dashboard-survey_delete'),

    path('submission/', views.submission_list, name='admin_dashboard-submission_list'),
    path('submission/add/', views.submission_create, name='admin_dashboard-submission_create'),
    path('submission/<int:pk>/edit/', views.submission_edit, name='admin_dashboard-submission_edit'),
    path('submission/<int:pk>/', views.submission_details, name='admin_dashboard-submission_details'),
    path('submission/delete/<int:pk>/', views.submission_delete, name='admin_dashboard-submission_delete'),

]