from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Authentication
    path('register/owner/', views.register_owner, name='register_owner'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    
    # User Management (Admin only)
    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/create/', views.create_user, name='create_user'),
    path('admin/users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Password Reset
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]

