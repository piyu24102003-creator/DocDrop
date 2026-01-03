from django.db import models
from django.contrib.auth.models import User
import os


def document_upload_path(instance, filename):
    """Generate upload path for documents"""
    # Upload to: media/documents/username/filename
    return f'documents/{instance.user.username}/{filename}'


class Document(models.Model):
    """Document model for storing user uploaded files"""
    DOCUMENT_TYPE_CHOICES = [
        ('image', 'Image'),
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    target_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_documents')
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to=document_upload_path)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(default=0)  # Size in bytes
    extracted_text = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.document_name} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        """Override save to set file size and detect document type"""
        if self.document_file:
            # Set file size
            self.file_size = self.document_file.size
            
            # Detect document type from extension
            ext = os.path.splitext(self.document_file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                self.document_type = 'image'
            elif ext == '.pdf':
                self.document_type = 'pdf'
            elif ext in ['.doc', '.docx']:
                self.document_type = 'docx'
            else:
                self.document_type = 'other'
        
        super().save(*args, **kwargs)
    
    def get_file_size_display(self):
        """Return human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"


class DocumentRequest(models.Model):
    """Model for owners to request documents from clients"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name='request')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} from {self.owner.username} to {self.client.username}"
