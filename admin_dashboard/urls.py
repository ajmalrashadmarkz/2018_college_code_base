from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name = "landing-page"),
    # path("survey/<int:id>/", views.show_survey, name="show-survey"),
    path("survey/<int:id>/", views.show_survey, name="show-survey"),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('account/admin/', views.dashboard_view, name='admin_dashboard-dashboard'), 
    path('logout/', views.dashboard_logout, name="admin_dashboard-logout"),
]