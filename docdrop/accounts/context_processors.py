from documents.models import DocumentRequest

def pending_requests_processor(request):
    """Provides pending document request count to all templates"""
    if request.user.is_authenticated and not (hasattr(request.user, 'profile') and request.user.profile.is_admin):
        pending_count = DocumentRequest.objects.filter(client=request.user, status='pending').count()
        return {'global_pending_requests': pending_count}
    return {'global_pending_requests': 0}
