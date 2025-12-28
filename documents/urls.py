from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('upload/', views.upload_document, name='upload'),
    path('list/', views.document_list, name='list'),
    path('<int:document_id>/download/', views.download_document, name='download'),
    path('<int:document_id>/preview/', views.preview_document, name='preview'),
    path('<int:document_id>/text/', views.view_text, name='view_text'),
    path('<int:document_id>/delete/', views.delete_document, name='delete'),
    
    # Admin views
    path('admin/list/', views.admin_document_list, name='admin_list'),
]

