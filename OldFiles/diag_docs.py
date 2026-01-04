from django.contrib.auth.models import User
from documents.models import Document, DocumentRequest
import os

print("--- Document Data Diagnostic ---")
docs = Document.objects.all().order_by('-uploaded_at')[:10]
for d in docs:
    target_name = d.target_owner.username if d.target_owner else "NONE"
    request_info = "NONE"
    try:
        req = DocumentRequest.objects.get(document=d)
        request_info = f"Req ID: {req.id}, Owner: {req.owner.username}, Status: {req.status}"
    except:
        pass
    print(f"ID: {d.id}, File: {d.document_name}, Uploader: {d.user.username}, Target: {target_name}, Request: {request_info}")
