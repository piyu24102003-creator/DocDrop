from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse_lazy
from .models import UserProfile, Enquiry
from documents.models import Document


def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_admin


def home(request):
    """Landing Page"""
    return render(request, 'base/index.html')


def about(request):
    """About Us Page"""
    return render(request, 'base/about.html')


def contact(request):
    """Contact Us Page with Enquiry Form"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        try:
            Enquiry.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'Thank you for your enquiry. We will get back to you soon!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again later.')

    return render(request, 'base/contact.html')



def register_owner(request):
    """Register a new Owner account"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        designation = request.POST.get('designation')
        
        # Validation
        if User.objects.filter(username=email).exists(): # Username = Email
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'auth/register_owner.html')
            
        try:
            # Create User (Username is Email)
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.is_staff = True # Allow access to Django Admin
            user.save()
            
            # Update Profile
            user.profile.role = 'admin' # Owner
            user.profile.phone = phone
            user.profile.designation = designation
            user.profile.save()
            
            messages.success(request, 'Owner account created successfully! Please login.')
            return redirect('accounts:admin_login')
        except Exception as e:
             messages.error(request, f'Error creating account: {e}')
             
    return render(request, 'auth/register_owner.html')


def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.is_admin:
            return redirect('accounts:admin_dashboard')
        else:
            return redirect('accounts:user_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is admin
            if hasattr(user, 'profile') and user.profile.is_admin:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('accounts:admin_dashboard')
            else:
                messages.error(request, 'This account does not have admin privileges. Please use the user login page.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/admin_login.html')


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.is_admin:
            return redirect('accounts:admin_dashboard')
        else:
            return redirect('accounts:user_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if hasattr(user, 'profile') and user.profile.is_admin:
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('accounts:admin_dashboard')
            else:
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('accounts:user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/user_login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """Dashboard view - redirects based on user role"""
    if is_admin(request.user):
        return redirect('accounts:admin_dashboard')
    else:
        return redirect('accounts:user_dashboard')


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with stats and user management"""
    # Statistics
    # Only show users managed by this admin (Owner)
    total_users = User.objects.filter(profile__managed_by=request.user).count()
    
    # Only show documents from users managed by this admin
    total_documents = Document.objects.filter(user__profile__managed_by=request.user).count()
    
    recent_uploads = Document.objects.filter(
        user__profile__managed_by=request.user
    ).select_related('user').order_by('-uploaded_at')[:10]
    
    # User-wise document counts (filtered by managed_by)
    user_docs = User.objects.filter(profile__managed_by=request.user).annotate(
        doc_count=Count('documents')
    ).order_by('-doc_count')[:10]
    
    # Get admin name
    admin_name = request.user.get_full_name() or request.user.username
    
    context = {
        'total_users': total_users,
        'total_documents': total_documents,
        'recent_uploads': recent_uploads,
        'user_docs': user_docs,
        'admin_name': admin_name,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def user_dashboard(request):
    """User dashboard with their documents"""
    # Redirect admin users to admin dashboard
    if hasattr(request.user, 'profile') and request.user.profile.is_admin:
        return redirect('accounts:admin_dashboard')
    
    user_documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # Get user name
    user_name = request.user.get_full_name() or request.user.username
    
    context = {
        'documents': user_documents,
        'total_documents': user_documents.count(),
        'user_name': user_name,
    }
    return render(request, 'user/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """Admin view: List all users"""
    users = User.objects.filter(profile__managed_by=request.user).select_related('profile').annotate(
        doc_count=Count('documents')
    ).order_by('-date_joined')
    
    context = {
        'users': users,
    }
    return render(request, 'admin/user_list.html', context)


@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    """Admin view: View user details and documents"""
    user = get_object_or_404(User, id=user_id)
    
    # Security: Ensure this user is managed by the current admin
    if user.profile.managed_by != request.user:
        messages.error(request, "You do not have permission to view this user.")
        return redirect('accounts:admin_dashboard')
        
    user_documents = Document.objects.filter(user=user).order_by('-uploaded_at')
    
    context = {
        'view_user': user,
        'documents': user_documents,
        'total_documents': user_documents.count(),
    }
    return render(request, 'admin/user_detail.html', context)


@login_required
@user_passes_test(is_admin)
def create_user(request):
    """Admin view: Create new user"""
    if request.method == 'POST':
        # Username logic: For clients, we use Email as Username
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = 'user' # Clients are always 'user' role
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        username = email # Enforce email as username
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User with this email already exists.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.profile.role = role
            user.profile.managed_by = request.user # Link to Owner
            user.profile.save()
            messages.success(request, f'Client {email} added successfully!')
            return redirect('accounts:user_list')
    
    return render(request, 'admin/create_user.html')


@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    """Admin view: Delete user"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            messages.error(request, 'You cannot delete your own account.')
        else:
            username = user.username
            user.delete()
            messages.success(request, f'User {username} deleted successfully!')
    
    return redirect('accounts:user_list')


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.profile.phone = request.POST.get('phone', '')
        user.save()
        user.profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'user/profile.html')


# Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view"""
    template_name = 'auth/password_reset.html'
    email_template_name = 'auth/password_reset_email.html'
    subject_template_name = 'auth/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def get_success_url(self):
        return reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view"""
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
