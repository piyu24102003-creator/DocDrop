from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.contrib.auth.models import User
from .models import Document, DocumentRequest
from accounts.views import is_admin


@login_required
def upload_document(request):
    """Upload document view"""
    if request.method == 'POST':
        document_file = request.FILES.get('document_file')
        document_name = request.POST.get('document_name', '')
        
        if not document_file:
            messages.error(request, 'Please select a file to upload.')
            return redirect('documents:upload')
        
        # Validate file type
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
        file_ext = os.path.splitext(document_file.name)[1].lower()
        
        if file_ext not in allowed_extensions:
            messages.error(request, 'Invalid file type. Allowed: JPG, PNG, PDF, DOC, DOCX')
            return redirect('documents:upload')
        
        # Validate file size (10MB max)
        if document_file.size > 10 * 1024 * 1024:
            messages.error(request, 'File size exceeds 10MB limit.')
            return redirect('documents:upload')
        
        # Use filename if document_name not provided
        if not document_name:
            document_name = document_file.name
        
        target_owner_id = request.POST.get('target_owner')
        target_owner = None
        if target_owner_id:
            target_owner = get_object_or_404(User, id=target_owner_id)
            
        document = Document.objects.create(
            user=request.user,
            target_owner=target_owner,
            document_name=document_name,
            document_file=document_file
        )
        
        # Handle Request Completion
        request_id = request.POST.get('request_id')
        if request_id:
            try:
                doc_request = DocumentRequest.objects.get(id=request_id, client=request.user)
                doc_request.status = 'completed'
                doc_request.document = document
                doc_request.save()
                
                # Ensure target_owner is set if it wasn't in POST
                if not document.target_owner:
                    document.target_owner = doc_request.owner
                    document.save()
            except DocumentRequest.DoesNotExist:
                pass
                
        # Perform OCR if it's an image
        if document.document_type == 'image':
            try:
                # Import utility here to avoid circular imports or issues if not needed
                from .utils import perform_ocr
                
                # Check if path exists before calling
                if document.document_file and os.path.exists(document.document_file.path):
                    extracted = perform_ocr(document.document_file.path)
                    if extracted:
                        document.extracted_text = extracted
                        document.save()
            except Exception as e:
                # Log error but don't fail the request (document is already saved)
                print(f"Post-upload OCR failed for document {document.id}: {e}")
        
        messages.success(request, f'Document "{document_name}" uploaded successfully!')
        return redirect('documents:list')
    
    # Pre-select owner if responding to a request
    selected_request = None
    request_id = request.GET.get('request_id')
    if request_id:
        selected_request = get_object_or_404(DocumentRequest, id=request_id, client=request.user)
    
    # List of owners linked to this client
    owners = request.user.profile.owners.all()
    
    context = {
        'selected_request': selected_request,
        'owners': owners,
    }
    return render(request, 'documents/upload.html', context)


@login_required
def document_list(request):
    """List user's documents with search"""
    query = request.GET.get('q', '')
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    
    
    if query:
        from django.db.models import Q
        documents = documents.filter(
            Q(document_name__icontains=query) | 
            Q(extracted_text__icontains=query)
        )
    
    context = {
        'documents': documents,
        'query': query,
    }
    return render(request, 'documents/list.html', context)


@login_required
def download_document(request, document_id):
    """Download document"""
    document = get_object_or_404(Document, id=document_id)
    
    # Check if user has permission (owner or admin)
    if document.user != request.user and not (hasattr(request.user, 'profile') and request.user.profile.is_admin):
        messages.error(request, 'You do not have permission to download this document.')
        return redirect('documents:list')
    
    if document.document_file and os.path.exists(document.document_file.path):
        # Fix: Ensure filename has extension
        filename = document.document_name
        file_ext = os.path.splitext(document.document_file.name)[1]
        if not filename.lower().endswith(file_ext.lower()):
            filename += file_ext
            
        return FileResponse(
            open(document.document_file.path, 'rb'),
            as_attachment=True,
            filename=filename
        )
    else:
        messages.error(request, 'File not found.')
        return redirect('documents:list')


@login_required
def preview_document(request, document_id):
    """Preview document in browser"""
    document = get_object_or_404(Document, id=document_id)
    
    # Check permission
    if document.user != request.user and not (hasattr(request.user, 'profile') and request.user.profile.is_admin):
        raise Http404("Permission denied")
    
    if document.document_file and os.path.exists(document.document_file.path):
        response = FileResponse(open(document.document_file.path, 'rb'))
        # inline content-disposition tells browser to try and open it
        response['Content-Disposition'] = f'inline; filename="{document.document_name}"'
        return response
    else:
        raise Http404("File not found")


@login_required
def view_text(request, document_id):
    """View extracted text"""
    document = get_object_or_404(Document, id=document_id)
    
    # Check permission
    if document.user != request.user and not (hasattr(request.user, 'profile') and request.user.profile.is_admin):
        messages.error(request, 'Permission denied.')
        return redirect('documents:list')
    
    return render(request, 'documents/text_view.html', {'document': document})


@login_required
def delete_document(request, document_id):
    """Delete document"""
    document = get_object_or_404(Document, id=document_id)
    
    # Check if user has permission (uploader, target owner, or superadmin)
    is_uploader = document.user == request.user
    is_target_owner = document.target_owner == request.user
    is_superadmin = request.user.is_superuser
    
    if not (is_uploader or is_target_owner or is_superadmin):
        messages.error(request, 'You do not have permission to delete this document.')
        return redirect('documents:list')
    
    if request.method == 'POST':
        document_name = document.document_name
        if document.document_file and os.path.exists(document.document_file.path):
            os.remove(document.document_file.path)
        document.delete()
        messages.success(request, f'Document "{document_name}" deleted successfully!')
        
        if is_target_owner:
            return redirect('accounts:admin_dashboard')
        else:
            return redirect('documents:list')
    
    return render(request, 'documents/delete_confirm.html', {'document': document})


@login_required
@user_passes_test(is_admin)
def admin_document_list(request):
    """Admin view: List all documents with search"""
    query = request.GET.get('q', '')
    documents = Document.objects.select_related('user').order_by('-uploaded_at')
    
    # Filter by target_owner (Admin/Owner isolation)
    documents = documents.filter(target_owner=request.user)

    if query:
        documents = documents.filter(document_name__icontains=query)
    
    # Filter by user if provided
    user_id = request.GET.get('user_id')
    if user_id:
        documents = documents.filter(user_id=user_id)
    
    context = {
        'documents': documents,
        'query': query,
    }
    return render(request, 'admin/document_list.html', context)


@login_required
@user_passes_test(is_admin)
def create_request(request, user_id):
    """Admin view: Request a document from a client"""
    client = get_object_or_404(User, id=user_id)
    
    # Check if user is linked to this owner
    if request.user not in client.profile.owners.all():
        messages.error(request, "This user is not your client.")
        return redirect('accounts:user_list')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        DocumentRequest.objects.create(
            owner=request.user,
            client=client,
            title=title,
            description=description
        )
        messages.success(request, f'Document request sent to {client.email}')
        return redirect('accounts:user_detail', user_id=user_id)
        
    return render(request, 'admin/create_request.html', {'client': client})


@login_required
def my_requests(request):
    """Client view: List all document requests"""
    requests_list = DocumentRequest.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'documents/req_list_v2.html', {'requests': requests_list})
