from django.urls import path
from . import views, auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('tracking/<int:query_id>/', views.query_tracking, name='query_tracking'),
    path('login/', auth_views.login_view, name='login'),
    path('register/', auth_views.register_view, name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
    # Superuser dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/mark-complete/<int:query_id>/', views.mark_complete, name='mark_complete'),
]