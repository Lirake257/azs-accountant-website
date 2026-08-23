from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from reports import views
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='reports/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard_redirect, name='home'),
    path('accountant/', views.accountant_dashboard, name='accountant_dashboard'),
    path('chief/', views.chief_dashboard, name='chief_dashboard'),
]