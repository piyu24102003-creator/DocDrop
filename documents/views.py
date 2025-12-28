from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
import os
from .models import Document
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
        
        document = Document.objects.create(
            user=request.user,
            document_name=document_name,
            document_file=document_file
        )
        
        # Perform OCR if it's an image
        if document.document_type == 'image':
            from .utils import perform_ocr
            try:
                # We need the full path. save() might not have written to disk yet if using some storages,
                # but with default FileSystemStorage it should be there.
                full_path = document.document_file.path
                extracted = perform_ocr(full_path)
                if extracted:
                    document.extracted_text = extracted
                    document.save()
            except Exception as e:
                # Log error but don't fail the upload
                print(f"OCR failed for document {document.id}: {e}")
        
        messages.success(request, f'Document "{document_name}" uploaded successfully!')
        return redirect('documents:list')
    
    return render(request, 'documents/upload.html')


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
    
    # Check if user has permission (owner or admin)
    if document.user != request.user and not (hasattr(request.user, 'profile') and request.user.profile.is_admin):
        messages.error(request, 'You do not have permission to delete this document.')
        return redirect('documents:list')
    
    if request.method == 'POST':
        document_name = document.document_name
        # Delete file from filesystem
        if document.document_file and os.path.exists(document.document_file.path):
            os.remove(document.document_file.path)
        document.delete()
        messages.success(request, f'Document "{document_name}" deleted successfully!')
        
        if hasattr(request.user, 'profile') and request.user.profile.is_admin:
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
    
    # Filter by managed_by (Admin/Owner isolation)
    documents = documents.filter(user__profile__managed_by=request.user)

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
