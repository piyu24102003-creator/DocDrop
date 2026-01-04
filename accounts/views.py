from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse_lazy
from .models import UserProfile, Enquiry
from documents.models import Document, DocumentRequest


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
        password_confirm = request.POST.get('password_confirm')
        phone = request.POST.get('phone')
        designation = request.POST.get('designation')
        
        # Password confirmation validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'auth/register_owner.html')
        
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
            user.profile.firm_name = request.POST.get('firm_name')
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
    clients = User.objects.filter(profile__owners=request.user)
    total_users = clients.count()
    
    # Only show documents from users managed by this admin OR uploaded specifically to this admin
    total_documents = Document.objects.filter(
        models.Q(user__in=clients, target_owner=request.user) | 
        models.Q(user=request.user)
    ).count()
    
    recent_uploads = Document.objects.filter(
        models.Q(user__in=clients, target_owner=request.user) | 
        models.Q(user=request.user)
    ).select_related('user').order_by('-uploaded_at')[:10]
    
    # User-wise document counts (filtered by managed_by)
    user_docs = User.objects.filter(profile__owners=request.user).annotate(
        doc_count=Count('documents', filter=models.Q(documents__target_owner=request.user))
    ).order_by('-doc_count')[:10]
    
    # Pending requests
    pending_requests = DocumentRequest.objects.filter(owner=request.user, status='pending').count()
    
    # Get admin name
    admin_name = request.user.get_full_name() or request.user.username
    
    context = {
        'total_users': total_users,
        'total_documents': total_documents,
        'recent_uploads': recent_uploads,
        'user_docs': user_docs,
        'admin_name': admin_name,
        'pending_requests': pending_requests,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def user_dashboard(request):
    """User dashboard with their documents"""
    # Redirect admin users to admin dashboard
    if hasattr(request.user, 'profile') and request.user.profile.is_admin:
        return redirect('accounts:admin_dashboard')
    
    # Get documents specifically for this user or sent to this user by others
    user_documents = Document.objects.filter(
        models.Q(user=request.user) | models.Q(target_owner=request.user)
    ).order_by('-uploaded_at')
    
    # Get user name
    user_name = request.user.get_full_name() or request.user.username
    
    # Get pending requests for this client
    pending_requests = DocumentRequest.objects.filter(client=request.user, status='pending')
    
    context = {
        'documents': user_documents,
        'total_documents': user_documents.count(),
        'user_name': user_name,
        'pending_requests': pending_requests,
        'pending_count': pending_requests.count(),
    }
    return render(request, 'user/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """Admin view: List all users linked to this owner"""
    users = User.objects.filter(profile__owners=request.user).select_related('profile').annotate(
        doc_count=Count('documents', filter=models.Q(documents__target_owner=request.user))
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
    
    # Security: Ensure this user is linked to the current administrator
    if request.user not in user.profile.owners.all():
        messages.error(request, "You do not have permission to view this user.")
        return redirect('accounts:admin_dashboard')
        
    user_documents = Document.objects.filter(user=user, target_owner=request.user).order_by('-uploaded_at')
    user_requests = DocumentRequest.objects.filter(client=user, owner=request.user).order_by('-created_at')
    
    context = {
        'view_user': user,
        'documents': user_documents,
        'user_requests': user_requests,
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
        role = 'user' # Clients are always 'user' role
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        username = email # Enforce email as username
        
        if User.objects.filter(username=username).exists():
            # If user exists, check if they are already a client
            user = User.objects.get(username=username)
            if user.profile.role == 'user':
                if request.user in user.profile.owners.all():
                    messages.info(request, f'User {email} is already your client.')
                else:
                    user.profile.owners.add(request.user)
                    user.profile.save()
                    messages.success(request, f'User {email} has been added to your client list!')
                return redirect('accounts:user_list')
            else:
                messages.error(request, 'This email belongs to an administrator account.')
        else:
            # Generate random password
            from .utils import generate_random_password, send_client_welcome_email
            password = generate_random_password()
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.profile.role = role
            user.profile.owners.add(request.user)
            user.profile.save()
            
            # Send welcome email with credentials
            try:
                send_client_welcome_email(user, password, request.user)
                messages.success(request, f'Client {email} added successfully! Welcome email sent with login credentials.')
            except Exception as e:
                messages.warning(request, f'Client {email} added successfully, but email could not be sent: {str(e)}')
            
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
        # Profile update logic
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.profile.phone = request.POST.get('phone', '')
        if user.profile.is_admin:
            user.profile.firm_name = request.POST.get('firm_name', '')
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


def password_reset_request(request):
    """Request password reset OTP"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate OTP
            from .utils import generate_otp, send_password_reset_otp
            from .models import PasswordResetOTP
            from django.utils import timezone
            from datetime import timedelta
            
            otp = generate_otp()
            expires_at = timezone.now() + timedelta(minutes=10)
            
            # Create OTP record
            PasswordResetOTP.objects.create(
                user=user,
                otp=otp,
                expires_at=expires_at
            )
            
            # Send OTP email
            try:
                send_password_reset_otp(user, otp)
                messages.success(request, f'OTP has been sent to {email}. Please check your email.')
                return redirect('accounts:password_reset_verify')
            except Exception as e:
                messages.error(request, f'Failed to send OTP email: {str(e)}')
        except User.DoesNotExist:
            # Don't reveal if email exists or not (security)
            messages.success(request, 'If an account with this email exists, an OTP has been sent.')
            return redirect('accounts:password_reset_verify')
    
    return render(request, 'auth/password_reset_request.html')


def password_reset_verify_otp(request):
    """Verify OTP and reset password"""
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Password confirmation check
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/password_reset_otp.html')
        
        try:
            user = User.objects.get(email=email)
            from .models import PasswordResetOTP
            
            # Get latest unused OTP
            otp_record = PasswordResetOTP.objects.filter(
                user=user,
                otp=otp,
                is_used=False
            ).first()
            
            if otp_record and otp_record.is_valid():
                # Reset password
                user.set_password(new_password)
                user.save()
                
                # Mark OTP as used
                otp_record.is_used = True
                otp_record.save()
                
                messages.success(request, 'Password reset successful! Please login with your new password.')
                return redirect('accounts:user_login')
            else:
                messages.error(request, 'Invalid or expired OTP. Please request a new one.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email address.')
    
    return render(request, 'auth/password_reset_otp.html')
