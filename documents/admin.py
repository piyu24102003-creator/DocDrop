from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'user', 'document_type', 'file_size', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('document_name', 'user__username', 'user__email')
    readonly_fields = ('uploaded_at', 'file_size')
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('Document Information', {
            'fields': ('user', 'document_name', 'document_file', 'document_type')
        }),
        ('Metadata', {
            'fields': ('file_size', 'uploaded_at')
        }),
    )
