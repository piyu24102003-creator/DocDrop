# DocDrop - Project Structure Summary

## 📁 Clean Project Structure (After Cleanup)

```
DocDrop/
├── docdrop/                    # 🎯 MAIN APPLICATION (Production Code)
│   ├── accounts/               # User management app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── models.py          # UserProfile, Enquiry
│   │   ├── urls.py
│   │   └── views.py           # Auth, dashboards, user CRUD
│   │
│   ├── documents/              # Document management app
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py          # Document, DocumentRequest
│   │   ├── urls.py
│   │   ├── utils.py           # OCR utilities
│   │   └── views.py           # Upload, download, requests
│   │
│   ├── docdrop/                # Project configuration
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py        # ⚙️ Main settings
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py
│   │
│   ├── templates/              # HTML templates
│   │   ├── admin/             # Owner portal
│   │   ├── auth/              # Login/register
│   │   ├── base/              # Public pages
│   │   ├── documents/         # Document pages
│   │   └── user/              # Client portal
│   │
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── staticfiles/            # Collected static (production)
│   ├── media/                  # 📤 Uploaded documents
│   │   └── documents/
│   │       └── [username]/
│   │
│   ├── .env                    # 🔐 Environment variables (SECRET)
│   ├── .env.example            # Environment template
│   ├── .gitignore              # Git ignore rules
│   ├── db.sqlite3              # 🗄️ Database
│   ├── manage.py               # Django CLI
│   ├── Procfile                # Deployment config
│   ├── render.yaml             # Render deployment
│   ├── requirements.txt        # Python dependencies
│   ├── README.md               # Project readme
│   └── SETUP.md                # Setup instructions
│
├── venv/                       # 🐍 Virtual environment (DO NOT TOUCH)
│
├── DOCUMENTATION.md            # 📚 Complete documentation
├── ARCHITECTURE.md             # 🏗️ Architecture guide
├── PROJECT_SUMMARY.md          # 📋 Project summary
│
└── [Moved Files]               # 🗑️ Temporary/diagnostic files
    ├── admin_list.txt
    ├── pip_list.txt
    ├── error.log
    ├── diag_docs.py
    ├── create_admin.py
    ├── list_admins.py
    ├── reset_db.py
    ├── reset_password.py
    ├── setup_test_scenario.py
    ├── test_db_connection.py
    └── test_db_debug.py
```

---

## 🎯 Core Application Files (What You Need to Know)

### Backend (Python/Django)

#### 1. **accounts/** - User Management
| File | Purpose | Key Functions |
|------|---------|---------------|
| `models.py` | User data structure | `UserProfile`, `Enquiry` |
| `views.py` | Business logic | Login, registration, dashboards, user CRUD |
| `urls.py` | URL routing | Maps URLs to views |
| `context_processors.py` | Global data | Pending requests count |

#### 2. **documents/** - Document Management
| File | Purpose | Key Functions |
|------|---------|---------------|
| `models.py` | Document data structure | `Document`, `DocumentRequest` |
| `views.py` | Document logic | Upload, download, requests, OCR |
| `urls.py` | URL routing | Document-related URLs |
| `utils.py` | Helper functions | OCR text extraction |

#### 3. **docdrop/** - Configuration
| File | Purpose | What It Controls |
|------|---------|------------------|
| `settings.py` | Main config | Database, apps, security, static files |
| `urls.py` | Root routing | Main URL patterns |
| `wsgi.py` | Web server | Production deployment |

---

### Frontend (HTML/CSS/JS)

#### Templates Structure
```
templates/
├── base/base.html              # 🎨 Master template (navbar, footer)
│
├── auth/                       # 🔐 Authentication
│   ├── admin_login.html        # Owner login
│   ├── user_login.html         # Client login
│   └── register_owner.html     # Owner registration
│
├── admin/                      # 👔 Owner Portal
│   ├── dashboard.html          # Statistics, recent uploads
│   ├── user_list.html          # Client list
│   ├── user_detail.html        # Client details + requests
│   ├── create_user.html        # Add client
│   ├── document_list.html      # All documents
│   └── create_request.html     # Request document
│
├── user/                       # 👤 Client Portal
│   ├── dashboard.html          # Client dashboard
│   └── profile.html            # Profile management
│
└── documents/                  # 📄 Document Management
    ├── upload.html             # Upload form + camera
    ├── list.html               # Document list
    ├── req_list_v2.html        # Request list
    ├── text_view.html          # OCR text viewer
    └── delete_confirm.html     # Delete confirmation
```

#### Static Files
- **CSS**: Bootstrap 5 + custom styles
- **JavaScript**: Camera capture, form validation
- **Icons**: Bootstrap Icons

---

### Database (SQLite)

#### Core Tables
```
db.sqlite3
├── auth_user                   # Django users
├── accounts_userprofile        # Extended user info
├── documents_document          # Uploaded files
├── documents_documentrequest   # Document requests
└── accounts_enquiry            # Contact form submissions
```

#### Key Relationships
```
User ←→ UserProfile (1:1)
User → Document (1:Many as uploader)
User → Document (1:Many as target_owner)
User → DocumentRequest (1:Many as owner)
User → DocumentRequest (1:Many as client)
DocumentRequest → Document (1:1)
```

---

## 🔄 How Data Flows

### Example: Client Uploads Document

```
1. Client Browser
   ↓
2. GET /documents/upload/
   ↓
3. documents/views.py::upload_document()
   ├─ Check authentication
   ├─ Get owners list
   └─ Render upload.html
   ↓
4. Client fills form + uploads file
   ↓
5. POST /documents/upload/
   ↓
6. documents/views.py::upload_document()
   ├─ Validate file (type, size)
   ├─ Create Document object
   ├─ Save to media/documents/[username]/
   ├─ If image: Run OCR
   └─ Save to database
   ↓
7. Redirect to /documents/list/
   ↓
8. documents/views.py::document_list()
   ├─ Query user's documents
   └─ Render list.html
   ↓
9. Client sees uploaded document
```

### Example: Owner Requests Document

```
1. Owner Browser
   ↓
2. GET /accounts/admin/users/15/
   ↓
3. accounts/views.py::user_detail()
   ├─ Get client details
   ├─ Get client's documents
   └─ Render user_detail.html
   ↓
4. Owner clicks "Request Document"
   ↓
5. GET /documents/admin/request/15/
   ↓
6. documents/views.py::create_request()
   └─ Render create_request.html
   ↓
7. Owner fills form (title, description)
   ↓
8. POST /documents/admin/request/15/
   ↓
9. documents/views.py::create_request()
   ├─ Create DocumentRequest
   │   ├─ owner = current user
   │   ├─ client = User(id=15)
   │   └─ status = 'pending'
   └─ Save to database
   ↓
10. Client sees request in /documents/my-requests/
```

---

## 🗂️ Files Moved to Parent Directory

These files were used during development/debugging and are not needed for production:

### Diagnostic Files
- `diag_docs.py` - Database diagnostic script
- `test_db_connection.py` - Database connection test
- `test_db_debug.py` - Database debug script
- `error.log` - Error log file

### Utility Scripts
- `create_admin.py` - Admin creation script
- `list_admins.py` - List admins script
- `reset_db.py` - Database reset script
- `reset_password.py` - Password reset script
- `setup_test_scenario.py` - Test data creation

### Info Files
- `admin_list.txt` - Admin list output
- `pip_list.txt` - Package list output

**These files are safe to delete or keep in parent directory for reference.**

---

## 🚀 Quick Start Commands

### Development
```bash
# Navigate to project
cd C:\Users\deepb\Desktop\DocDrop\docdrop

# Activate virtual environment
..\venv\Scripts\activate

# Run server
python manage.py runserver

# Access application
http://127.0.0.1:8000/
```

### Database Management
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

---

## 📊 Functionality Overview

### Owner (Admin) Can:
✅ Register with firm details  
✅ Login to owner portal  
✅ Create and manage clients  
✅ View all client documents  
✅ Request documents from clients  
✅ Download client documents  
✅ View statistics and analytics  
✅ Track request status  

### Client (User) Can:
✅ Login to client portal  
✅ Upload documents to owners  
✅ Use camera to capture documents  
✅ View their uploaded documents  
✅ Respond to document requests  
✅ Download their documents  
✅ View pending requests  
✅ Update profile  

---

## 🔐 Important Files (DO NOT DELETE)

### Critical Configuration
- `.env` - Environment variables (SECRET_KEY, DEBUG, etc.)
- `settings.py` - Django configuration
- `db.sqlite3` - Database (contains all data)
- `requirements.txt` - Python dependencies

### Critical Directories
- `media/` - Uploaded documents (user data)
- `templates/` - HTML templates
- `accounts/` - User management app
- `documents/` - Document management app
- `venv/` - Virtual environment

---

## 📚 Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `DOCUMENTATION.md` | Complete project docs | Full reference |
| `ARCHITECTURE.md` | Technical architecture | Understanding structure |
| `PROJECT_SUMMARY.md` | Quick overview | Quick reference |
| `README.md` | Getting started | First time setup |
| `SETUP.md` | Setup instructions | Installation |

---

## 🎯 Next Steps

1. **Read ARCHITECTURE.md** for deep technical understanding
2. **Read DOCUMENTATION.md** for complete feature reference
3. **Test the application** to see all features in action
4. **Review code** in `accounts/views.py` and `documents/views.py`
5. **Explore templates** to understand UI structure

---

**Last Updated**: January 1, 2026  
**Project Status**: ✅ Production Ready  
**Clean Structure**: ✅ Completed
