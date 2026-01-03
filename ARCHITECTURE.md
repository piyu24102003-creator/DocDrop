# DocDrop - Complete Architecture Analysis

## 🏗️ Project Architecture Overview

DocDrop follows the **Model-View-Template (MVT)** architecture pattern of Django, with a clear separation between Backend, Frontend, and Database layers.

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│  (Browser - HTML/CSS/JavaScript)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Templates (Django Template Engine)                    │  │
│  │ - base/         → Public pages                        │  │
│  │ - auth/         → Login/Registration                  │  │
│  │ - admin/        → Owner portal                        │  │
│  │ - user/         → Client portal                       │  │
│  │ - documents/    → Document management                 │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Static Files                                          │  │
│  │ - CSS (Bootstrap 5)                                   │  │
│  │ - JavaScript (Camera API, Form Validation)           │  │
│  │ - Images/Icons (Bootstrap Icons)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND LAYER                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Django Apps                                           │  │
│  │                                                       │  │
│  │ 1. ACCOUNTS APP                                       │  │
│  │    ├── Models: UserProfile, Enquiry                  │  │
│  │    ├── Views: Authentication, User Management        │  │
│  │    ├── URLs: /accounts/*                             │  │
│  │    └── Context Processors: Global variables          │  │
│  │                                                       │  │
│  │ 2. DOCUMENTS APP                                      │  │
│  │    ├── Models: Document, DocumentRequest             │  │
│  │    ├── Views: Upload, Download, Requests             │  │
│  │    ├── URLs: /documents/*                            │  │
│  │    └── Utils: OCR processing                         │  │
│  │                                                       │  │
│  │ 3. DOCDROP (Core)                                     │  │
│  │    ├── settings.py → Configuration                   │  │
│  │    ├── urls.py → URL routing                         │  │
│  │    └── wsgi.py → WSGI application                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Middleware & Security                                 │  │
│  │ - Authentication Middleware                           │  │
│  │ - CSRF Protection                                     │  │
│  │ - Session Management                                  │  │
│  │ - Security Headers                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ SQLite Database (db.sqlite3)                          │  │
│  │                                                       │  │
│  │ Tables:                                               │  │
│  │ - auth_user                                           │  │
│  │ - accounts_userprofile                                │  │
│  │ - accounts_enquiry                                    │  │
│  │ - documents_document                                  │  │
│  │ - documents_documentrequest                           │  │
│  │ - django_session                                      │  │
│  │ - django_migrations                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ File Storage                                          │  │
│  │ media/documents/[username]/[files]                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 BACKEND ARCHITECTURE

### 1. **Accounts App** (`accounts/`)

**Purpose**: User authentication, profile management, and user administration

#### Models (`accounts/models.py`)
```python
UserProfile
├── user (OneToOne → User)
├── role (admin/user)
├── phone
├── designation
├── firm_name
└── owners (ManyToMany → User)

Enquiry
├── name
├── email
├── subject
└── message
```

#### Views (`accounts/views.py`)
| View Function | URL | Purpose |
|---------------|-----|---------|
| `home()` | `/` | Landing page |
| `about()` | `/about/` | About page |
| `contact()` | `/contact/` | Contact form |
| `register_owner()` | `/accounts/register/owner/` | Owner registration |
| `admin_login()` | `/accounts/admin/login/` | Owner login |
| `user_login()` | `/accounts/login/` | Client login |
| `logout_view()` | `/accounts/logout/` | Logout |
| `admin_dashboard()` | `/accounts/admin/dashboard/` | Owner dashboard |
| `user_dashboard()` | `/accounts/user/dashboard/` | Client dashboard |
| `user_list()` | `/accounts/admin/users/` | List clients |
| `user_detail()` | `/accounts/admin/users/<id>/` | Client details |
| `create_user()` | `/accounts/admin/users/create/` | Create client |
| `delete_user()` | `/accounts/admin/users/<id>/delete/` | Delete client |
| `profile()` | `/accounts/profile/` | Profile management |

#### Context Processors (`accounts/context_processors.py`)
```python
pending_requests_processor()
└── Adds 'pending_requests_count' to all templates
```

#### Key Features
- ✅ Dual login system (Owner/Client)
- ✅ Multi-owner client linking
- ✅ Role-based dashboards
- ✅ User CRUD operations
- ✅ Profile management with firm details

---

### 2. **Documents App** (`documents/`)

**Purpose**: Document upload, management, and request workflow

#### Models (`documents/models.py`)
```python
Document
├── user (ForeignKey → User) # Uploader
├── target_owner (ForeignKey → User) # Recipient
├── document_name
├── document_file (FileField)
├── document_type (image/pdf/docx/other)
├── uploaded_at
├── file_size
└── extracted_text (OCR)

DocumentRequest
├── owner (ForeignKey → User) # Requester
├── client (ForeignKey → User) # Target
├── title
├── description
├── status (pending/completed/cancelled)
├── document (ForeignKey → Document)
├── created_at
└── updated_at
```

#### Views (`documents/views.py`)
| View Function | URL | Purpose |
|---------------|-----|---------|
| `upload_document()` | `/documents/upload/` | Upload document |
| `document_list()` | `/documents/list/` | List user documents |
| `download_document()` | `/documents/download/<id>/` | Download document |
| `preview_document()` | `/documents/preview/<id>/` | Preview document |
| `view_text()` | `/documents/text/<id>/` | View OCR text |
| `delete_document()` | `/documents/delete/<id>/` | Delete document |
| `admin_document_list()` | `/documents/admin/list/` | Owner document list |
| `create_request()` | `/documents/admin/request/<user_id>/` | Request document |
| `my_requests()` | `/documents/my-requests/` | View requests |

#### Utils (`documents/utils.py`)
```python
perform_ocr(image_path)
└── Extracts text from images using Tesseract
```

#### Key Features
- ✅ File upload with validation (type, size)
- ✅ Camera capture integration
- ✅ OCR text extraction
- ✅ Document search (name + OCR text)
- ✅ Request workflow (Owner → Client)
- ✅ Automatic request completion
- ✅ Target owner assignment

---

### 3. **Core Configuration** (`docdrop/`)

#### Settings (`docdrop/settings.py`)
```python
# Key Configurations
INSTALLED_APPS = [
    'accounts',
    'documents',
    ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]

TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
    'OPTIONS': {
        'context_processors': [
            'accounts.context_processors.pending_requests_processor',
            ...
        ]
    }
}]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

#### URL Routing (`docdrop/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('documents/', include('documents.urls')),
    path('media/', serve, {'document_root': MEDIA_ROOT}),
]
```

---

## 🎨 FRONTEND ARCHITECTURE

### Template Structure

```
templates/
├── base/
│   ├── base.html          # Master template (navbar, footer)
│   ├── index.html         # Landing page
│   ├── about.html         # About page
│   └── contact.html       # Contact form
│
├── auth/
│   ├── admin_login.html   # Owner login
│   ├── user_login.html    # Client login
│   ├── register_owner.html # Owner registration
│   └── password_reset.html # Password reset
│
├── admin/                  # Owner Portal
│   ├── dashboard.html     # Owner dashboard
│   ├── user_list.html     # Client list
│   ├── user_detail.html   # Client details + requests
│   ├── create_user.html   # Add client
│   ├── document_list.html # All documents
│   └── create_request.html # Request document
│
├── user/                   # Client Portal
│   ├── dashboard.html     # Client dashboard
│   └── profile.html       # Profile management
│
└── documents/
    ├── upload.html        # Upload form + camera
    ├── list.html          # Document list
    ├── req_list_v2.html   # Request list
    ├── text_view.html     # OCR text viewer
    └── delete_confirm.html # Delete confirmation
```

### Template Inheritance Flow

```
base.html (Master)
├── Navbar (dynamic based on user role)
├── Messages (Django messages framework)
├── Content Block ({% block content %})
└── Footer

All other templates extend base.html:
{% extends 'base/base.html' %}
{% block content %}
    <!-- Page-specific content -->
{% endblock %}
```

### Frontend Technologies

| Technology | Usage |
|------------|-------|
| **Bootstrap 5.3** | Responsive grid, components, utilities |
| **Bootstrap Icons** | Icon library |
| **Vanilla JavaScript** | Camera API, form validation, file handling |
| **Django Template Language** | Server-side rendering, loops, conditionals |
| **CSS Custom Properties** | Theme customization |

### Key Frontend Features

1. **Responsive Design**
   - Mobile-first approach
   - Breakpoints: sm, md, lg, xl
   - Collapsible navbar

2. **Camera Integration**
   ```javascript
   navigator.mediaDevices.getUserMedia({
       video: { facingMode: 'environment' }
   })
   ```

3. **Dynamic Forms**
   - CSRF token inclusion
   - File validation (client-side)
   - Real-time feedback

4. **Role-Based UI**
   ```django
   {% if user.profile.is_admin %}
       <!-- Owner-specific content -->
   {% else %}
       <!-- Client-specific content -->
   {% endif %}
   ```

---

## 🗄️ DATABASE ARCHITECTURE

### Entity Relationship Diagram

```
┌─────────────────┐
│   auth_user     │
│─────────────────│
│ id (PK)         │
│ username        │◄────────┐
│ email           │         │
│ password        │         │
│ first_name      │         │
│ last_name       │         │
│ is_staff        │         │
│ is_active       │         │
│ date_joined     │         │
└────────┬────────┘         │
         │                  │
         │ 1:1              │
         ▼                  │
┌─────────────────────┐     │
│ accounts_userprofile│     │
│─────────────────────│     │
│ id (PK)             │     │
│ user_id (FK)        │     │
│ role                │     │
│ phone               │     │
│ designation         │     │
│ firm_name           │     │
│ created_at          │     │
└──────────┬──────────┘     │
           │                │
           │ M:M            │
           │ (owners)       │
           └────────────────┘

┌─────────────────────┐
│ documents_document  │
│─────────────────────│
│ id (PK)             │
│ user_id (FK) ───────┼──► auth_user (uploader)
│ target_owner_id(FK)─┼──► auth_user (recipient)
│ document_name       │
│ document_file       │
│ document_type       │
│ uploaded_at         │
│ file_size           │
│ extracted_text      │
└──────────┬──────────┘
           │
           │ 1:1
           ▼
┌──────────────────────────┐
│ documents_documentrequest│
│──────────────────────────│
│ id (PK)                  │
│ owner_id (FK) ───────────┼──► auth_user (requester)
│ client_id (FK) ──────────┼──► auth_user (target)
│ document_id (FK)         │
│ title                    │
│ description              │
│ status                   │
│ created_at               │
│ updated_at               │
└──────────────────────────┘

┌─────────────────┐
│ accounts_enquiry│
│─────────────────│
│ id (PK)         │
│ name            │
│ email           │
│ subject         │
│ message         │
│ created_at      │
└─────────────────┘
```

### Relationships Explained

1. **User ↔ UserProfile** (One-to-One)
   - Every user has exactly one profile
   - Profile stores role and additional info

2. **UserProfile ↔ User (owners)** (Many-to-Many)
   - A client can have multiple owners
   - An owner can have multiple clients
   - Self-referential relationship through User model

3. **User → Document** (One-to-Many as uploader)
   - A user can upload many documents
   - Each document has one uploader

4. **User → Document** (One-to-Many as target_owner)
   - An owner can receive many documents
   - Each document has one target owner

5. **User → DocumentRequest** (One-to-Many as owner)
   - An owner can create many requests
   - Each request has one owner

6. **User → DocumentRequest** (One-to-Many as client)
   - A client can receive many requests
   - Each request targets one client

7. **DocumentRequest → Document** (One-to-One)
   - A request can be fulfilled by one document
   - A document can fulfill one request

### Database Queries (Common Patterns)

```python
# Get all clients of an owner
clients = User.objects.filter(profile__owners=request.user)

# Get all documents sent to an owner
docs = Document.objects.filter(target_owner=request.user)

# Get pending requests for a client
requests = DocumentRequest.objects.filter(
    client=request.user,
    status='pending'
)

# Get documents with OCR text search
docs = Document.objects.filter(
    Q(document_name__icontains=query) |
    Q(extracted_text__icontains=query)
)

# Get owner's clients with document counts
users = User.objects.filter(
    profile__owners=request.user
).annotate(
    doc_count=Count('documents',
        filter=Q(documents__target_owner=request.user)
    )
)
```

---

## 🔄 REQUEST FLOW EXAMPLES

### 1. **Client Upload Flow**

```
Client Browser
    │
    ├─► GET /documents/upload/
    │   └─► documents/views.py::upload_document()
    │       ├─► Check authentication
    │       ├─► Get owners list
    │       ├─► Check for request_id in URL
    │       └─► Render upload.html
    │
    ├─► POST /documents/upload/
    │   └─► documents/views.py::upload_document()
    │       ├─► Validate file (type, size)
    │       ├─► Get target_owner from form
    │       ├─► Create Document object
    │       ├─► Save file to media/documents/[username]/
    │       ├─► If request_id exists:
    │       │   ├─► Update DocumentRequest status
    │       │   ├─► Link document to request
    │       │   └─► Auto-set target_owner if missing
    │       ├─► If image: Run OCR
    │       └─► Redirect to document list
    │
    └─► GET /documents/list/
        └─► documents/views.py::document_list()
            ├─► Query user's documents
            ├─► Apply search filter if provided
            └─► Render list.html
```

### 2. **Owner Request Flow**

```
Owner Browser
    │
    ├─► GET /accounts/admin/users/15/
    │   └─► accounts/views.py::user_detail()
    │       ├─► Check admin permission
    │       ├─► Get client details
    │       ├─► Get client's documents
    │       ├─► Get requests sent to client
    │       └─► Render user_detail.html
    │
    ├─► GET /documents/admin/request/15/
    │   └─► documents/views.py::create_request()
    │       ├─► Check admin permission
    │       ├─► Verify client ownership
    │       └─► Render create_request.html
    │
    ├─► POST /documents/admin/request/15/
    │   └─► documents/views.py::create_request()
    │       ├─► Get title and description
    │       ├─► Create DocumentRequest
    │       │   ├─► owner = request.user
    │       │   ├─► client = User(id=15)
    │       │   └─► status = 'pending'
    │       └─► Redirect to user_detail
    │
    └─► Client receives notification
        └─► GET /documents/my-requests/
            └─► documents/views.py::my_requests()
                ├─► Query requests for client
                └─► Render req_list_v2.html
```

### 3. **Authentication Flow**

```
User Browser
    │
    ├─► GET /accounts/login/
    │   └─► accounts/views.py::user_login()
    │       └─► Render user_login.html
    │
    ├─► POST /accounts/login/
    │   └─► accounts/views.py::user_login()
    │       ├─► authenticate(username, password)
    │       ├─► If valid:
    │       │   ├─► login(request, user)
    │       │   ├─► Create session
    │       │   └─► Redirect based on role:
    │       │       ├─► Admin → admin_dashboard
    │       │       └─► User → user_dashboard
    │       └─► If invalid:
    │           └─► Show error message
    │
    └─► All subsequent requests include session cookie
        └─► @login_required decorator checks authentication
```

---

## 📊 FUNCTIONALITY MATRIX

| Feature | Owner | Client | Implementation |
|---------|-------|--------|----------------|
| **Authentication** |
| Register | ✅ | ❌ | `accounts/views.py::register_owner()` |
| Login | ✅ | ✅ | `accounts/views.py::admin_login()`, `user_login()` |
| Logout | ✅ | ✅ | `accounts/views.py::logout_view()` |
| Password Reset | ✅ | ✅ | Django auth views |
| **User Management** |
| Create Client | ✅ | ❌ | `accounts/views.py::create_user()` |
| View Clients | ✅ | ❌ | `accounts/views.py::user_list()` |
| View Client Details | ✅ | ❌ | `accounts/views.py::user_detail()` |
| Delete Client | ✅ | ❌ | `accounts/views.py::delete_user()` |
| Update Profile | ✅ | ✅ | `accounts/views.py::profile()` |
| **Document Management** |
| Upload Document | ❌ | ✅ | `documents/views.py::upload_document()` |
| View Own Documents | ❌ | ✅ | `documents/views.py::document_list()` |
| View Client Documents | ✅ | ❌ | `documents/views.py::admin_document_list()` |
| Download Document | ✅ | ✅ | `documents/views.py::download_document()` |
| Preview Document | ✅ | ✅ | `documents/views.py::preview_document()` |
| Delete Document | ✅ | ✅ | `documents/views.py::delete_document()` |
| Search Documents | ✅ | ✅ | Query in list views |
| View OCR Text | ✅ | ✅ | `documents/views.py::view_text()` |
| Camera Capture | ❌ | ✅ | JavaScript in `upload.html` |
| **Request System** |
| Create Request | ✅ | ❌ | `documents/views.py::create_request()` |
| View Requests | ❌ | ✅ | `documents/views.py::my_requests()` |
| Upload via Request | ❌ | ✅ | `upload_document()` with request_id |
| Track Request Status | ✅ | ✅ | `user_detail.html`, `req_list_v2.html` |
| **Dashboard** |
| View Statistics | ✅ | ✅ | `admin_dashboard()`, `user_dashboard()` |
| Recent Uploads | ✅ | ✅ | Both dashboards |
| Pending Alerts | ✅ | ✅ | Context processor |

---

## 🔐 SECURITY IMPLEMENTATION

### 1. **Authentication & Authorization**
```python
# Decorator-based protection
@login_required
def upload_document(request):
    ...

@user_passes_test(is_admin)
def admin_dashboard(request):
    ...

# View-level checks
if document.user != request.user and not is_admin(request.user):
    return HttpResponseForbidden()
```

### 2. **CSRF Protection**
```html
<form method="post">
    {% csrf_token %}
    ...
</form>
```

### 3. **File Validation**
```python
# Type validation
allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx']
if file_ext not in allowed_extensions:
    return error

# Size validation
if document_file.size > 10 * 1024 * 1024:  # 10MB
    return error
```

### 4. **SQL Injection Prevention**
```python
# Django ORM automatically escapes queries
Document.objects.filter(user=request.user)  # Safe
```

### 5. **XSS Protection**
```django
<!-- Auto-escaping in templates -->
{{ user_input }}  <!-- Automatically escaped -->
{{ user_input|safe }}  <!-- Only when explicitly needed -->
```

---

## 📈 PERFORMANCE CONSIDERATIONS

### Database Optimization
```python
# Use select_related for foreign keys
Document.objects.select_related('user', 'target_owner')

# Use prefetch_related for many-to-many
User.objects.prefetch_related('profile__owners')

# Annotate for counts
User.objects.annotate(doc_count=Count('documents'))
```

### File Storage
- User-specific directories prevent conflicts
- Original filenames preserved
- File size limits prevent storage abuse

### Caching Opportunities
```python
# Future enhancement
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def document_list(request):
    ...
```

---

**Last Updated**: January 1, 2026
**Author**: DocDrop Development Team
