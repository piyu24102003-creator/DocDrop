# DocDrop - API & Database Reference

## Technical Reference Documentation

**Version:** 1.0.0  
**Last Updated:** January 2, 2026

---

## Database Schema

### Entity Relationship Diagram

```
auth_user (Django Built-in)
├── id (PK)
├── username (email)
├── email
├── password (hashed)
├── first_name
├── last_name
├── is_staff
├── is_active
├── date_joined
└── last_login

accounts_userprofile
├── id (PK)
├── user_id (FK → auth_user) [OneToOne]
├── role (admin/user)
├── phone
├── designation
├── firm_name
├── managed_by_id (FK → auth_user)
├── created_at
└── updated_at
└── owners (M2M → auth_user)

documents_document
├── id (PK)
├── user_id (FK → auth_user) [uploader]
├── target_owner_id (FK → auth_user) [recipient]
├── document_name
├── document_file (FileField)
├── document_type (image/pdf/docx/other)
├── uploaded_at
├── file_size
└── extracted_text (OCR)

documents_documentrequest
├── id (PK)
├── owner_id (FK → auth_user) [requester]
├── client_id (FK → auth_user) [target]
├── document_id (FK → documents_document)
├── title
├── description
├── status (pending/completed/cancelled)
├── created_at
└── updated_at

accounts_passwordresetotp
├── id (PK)
├── user_id (FK → auth_user)
├── otp (6-digit code)
├── created_at
├── expires_at
└── is_used

accounts_enquiry
├── id (PK)
├── name
├── email
├── subject
├── message
├── created_at
└── is_resolved
```

### Table Descriptions

#### auth_user
**Purpose**: Django's built-in user authentication table

**Key Fields**:
- `username`: Email address (used as username)
- `password`: PBKDF2-SHA256 hashed password
- `is_staff`: True for owners, False for clients
- `is_active`: Account active status

**Indexes**:
- Primary key on `id`
- Unique index on `username`
- Index on `email`

#### accounts_userprofile
**Purpose**: Extended user information

**Key Fields**:
- `role`: 'admin' (owner) or 'user' (client)
- `firm_name`: Business name for owners
- `owners`: Many-to-many relationship for multi-owner support

**Relationships**:
- OneToOne with `auth_user`
- ManyToMany with `auth_user` (as owners)

#### documents_document
**Purpose**: Stores uploaded document metadata

**Key Fields**:
- `user_id`: Who uploaded the document
- `target_owner_id`: Who the document is for
- `document_file`: Path to actual file
- `document_type`: Categorization (image/pdf/docx/other)
- `extracted_text`: OCR text for searchability

**File Storage**:
- Path: `media/documents/[username]/[filename]`
- Max size: 10MB
- Allowed types: JPG, PNG, PDF, DOC, DOCX

#### documents_documentrequest
**Purpose**: Document request workflow

**Key Fields**:
- `owner_id`: Who requested the document
- `client_id`: Who should upload the document
- `document_id`: Uploaded document (when completed)
- `status`: pending/completed/cancelled

**Workflow**:
1. Owner creates request → status: pending
2. Client uploads document → status: completed
3. Document linked via `document_id`

#### accounts_passwordresetotp
**Purpose**: OTP-based password reset

**Key Fields**:
- `otp`: 6-digit numeric code
- `expires_at`: Expiration timestamp (10 minutes)
- `is_used`: One-time use flag

**Security**:
- OTP expires after 10 minutes
- Can only be used once
- Automatically cleaned up (future)

---

## URL Routes

### Public Routes

| URL | View | Method | Description |
|-----|------|--------|-------------|
| `/` | `home` | GET | Landing page |
| `/about/` | `about` | GET | About page |
| `/contact/` | `contact` | GET/POST | Contact form |

### Authentication Routes

| URL | View | Method | Auth Required |
|-----|------|--------|---------------|
| `/accounts/register/owner/` | `register_owner` | GET/POST | No |
| `/accounts/admin/login/` | `admin_login` | GET/POST | No |
| `/accounts/login/` | `user_login` | GET/POST | No |
| `/accounts/logout/` | `logout_view` | GET | Yes |
| `/accounts/password-reset/request/` | `password_reset_request` | GET/POST | No |
| `/accounts/password-reset/verify/` | `password_reset_verify_otp` | GET/POST | No |

### Owner (Admin) Routes

| URL | View | Method | Permission |
|-----|------|--------|------------|
| `/accounts/admin/dashboard/` | `admin_dashboard` | GET | Owner |
| `/accounts/admin/users/` | `user_list` | GET | Owner |
| `/accounts/admin/users/create/` | `create_user` | GET/POST | Owner |
| `/accounts/admin/users/<id>/` | `user_detail` | GET | Owner |
| `/accounts/admin/users/<id>/delete/` | `delete_user` | POST | Owner |
| `/documents/admin/list/` | `admin_document_list` | GET | Owner |
| `/documents/admin/request/<user_id>/` | `create_request` | GET/POST | Owner |

### Client (User) Routes

| URL | View | Method | Permission |
|-----|------|--------|------------|
| `/accounts/user/dashboard/` | `user_dashboard` | GET | Client |
| `/documents/upload/` | `upload_document` | GET/POST | Client |
| `/documents/list/` | `document_list` | GET | Client |
| `/documents/my-requests/` | `my_requests` | GET | Client |

### Shared Routes

| URL | View | Method | Permission |
|-----|------|--------|------------|
| `/accounts/profile/` | `profile` | GET/POST | Any authenticated |
| `/documents/download/<id>/` | `download_document` | GET | Owner/Uploader |
| `/documents/preview/<id>/` | `preview_document` | GET | Owner/Uploader |
| `/documents/text/<id>/` | `view_text` | GET | Owner/Uploader |
| `/documents/delete/<id>/` | `delete_document` | POST | Owner/Uploader |

---

## View Functions Reference

### Authentication Views

#### `register_owner(request)`
**Purpose**: Owner registration

**Method**: GET, POST

**POST Parameters**:
- `name`: Full name
- `email`: Email address (becomes username)
- `password`: Password (min 8 chars)
- `password_confirm`: Password confirmation
- `phone`: Contact number
- `designation`: Business type
- `firm_name`: Company name

**Returns**:
- GET: Registration form
- POST: Redirect to login on success

**Validations**:
- Email uniqueness
- Password match
- Password length (min 8)

#### `admin_login(request)` / `user_login(request)`
**Purpose**: User authentication

**Method**: GET, POST

**POST Parameters**:
- `username`: Email address
- `password`: Password

**Returns**:
- GET: Login form
- POST: Redirect to dashboard on success

**Authentication**:
- Uses Django's `authenticate()` and `login()`
- Creates session
- Redirects based on role

#### `password_reset_request(request)`
**Purpose**: Request password reset OTP

**Method**: GET, POST

**POST Parameters**:
- `email`: User email address

**Process**:
1. Validate email exists
2. Generate 6-digit OTP
3. Create PasswordResetOTP record
4. Send email with OTP
5. Redirect to verification page

#### `password_reset_verify_otp(request)`
**Purpose**: Verify OTP and reset password

**Method**: GET, POST

**POST Parameters**:
- `email`: User email
- `otp`: 6-digit code
- `new_password`: New password
- `confirm_password`: Password confirmation

**Validations**:
- OTP validity (not expired, not used)
- Password match
- Password length

---

### Owner Views

#### `admin_dashboard(request)`
**Purpose**: Owner dashboard

**Method**: GET

**Permission**: Owner only

**Context Data**:
```python
{
    'total_clients': int,
    'total_documents': int,
    'pending_requests': int,
    'recent_uploads': QuerySet[Document],
    'top_uploaders': List[dict]
}
```

#### `user_list(request)`
**Purpose**: List all clients

**Method**: GET

**Permission**: Owner only

**Context Data**:
```python
{
    'users': QuerySet[User],
    # Each user annotated with:
    # - doc_count: number of documents
}
```

#### `create_user(request)`
**Purpose**: Create new client

**Method**: GET, POST

**Permission**: Owner only

**POST Parameters**:
- `email`: Client email (required)
- `first_name`: First name (optional)
- `last_name`: Last name (optional)

**Process**:
1. Check email uniqueness
2. Generate random password
3. Create user account
4. Link to current owner
5. Send welcome email
6. Redirect to user list

#### `user_detail(request, user_id)`
**Purpose**: View client details

**Method**: GET

**Permission**: Owner only (must own client)

**Context Data**:
```python
{
    'view_user': User,
    'documents': QuerySet[Document],
    'user_requests': QuerySet[DocumentRequest],
    'total_documents': int
}
```

#### `create_request(request, user_id)`
**Purpose**: Request document from client

**Method**: GET, POST

**Permission**: Owner only (must own client)

**POST Parameters**:
- `title`: Document title (required)
- `description`: Instructions (optional)

**Process**:
1. Validate client ownership
2. Create DocumentRequest
3. Send email notification to client
4. Redirect to client details

---

### Client Views

#### `user_dashboard(request)`
**Purpose**: Client dashboard

**Method**: GET

**Permission**: Client only

**Context Data**:
```python
{
    'total_documents': int,
    'pending_requests': QuerySet[DocumentRequest],
    'recent_uploads': QuerySet[Document]
}
```

#### `upload_document(request)`
**Purpose**: Upload document

**Method**: GET, POST

**Permission**: Client only

**GET Parameters** (optional):
- `request_id`: Pre-fill from document request

**POST Parameters**:
- `document_name`: Document name
- `document_file`: File upload
- `target_owner`: Owner ID
- `request_id`: Request ID (if responding to request)

**Process**:
1. Validate file (type, size)
2. Save file to media/documents/[username]/
3. Create Document record
4. If image: Run OCR
5. If request_id: Update request status
6. Redirect to document list

**File Validation**:
- Allowed extensions: .jpg, .jpeg, .png, .pdf, .doc, .docx
- Max size: 10MB

#### `my_requests(request)`
**Purpose**: View document requests

**Method**: GET

**Permission**: Client only

**Context Data**:
```python
{
    'requests': QuerySet[DocumentRequest]
    # Filtered by client=request.user
}
```

---

### Shared Views

#### `profile(request)`
**Purpose**: View/edit profile

**Method**: GET, POST

**Permission**: Any authenticated user

**POST Parameters**:
- `first_name`: First name
- `last_name`: Last name
- `email`: Email
- `phone`: Phone number
- `firm_name`: Firm name (owners only)

#### `download_document(request, document_id)`
**Purpose**: Download document

**Method**: GET

**Permission**: Owner (if target_owner) or Uploader

**Returns**: FileResponse with original filename

**Security**:
- Verifies user has permission
- Returns 403 if unauthorized

#### `delete_document(request, document_id)`
**Purpose**: Delete document

**Method**: POST

**Permission**: Owner (if target_owner) or Uploader

**Process**:
1. Verify permission
2. Delete file from filesystem
3. Delete database record
4. Redirect to document list

---

## Email Templates

### Client Welcome Email

**Template**: `templates/emails/client_welcome.html`

**Variables**:
```python
{
    'user': User object,
    'password': str (plain text password),
    'owner': User object (owner who created account),
    'login_url': str (domain)
}
```

**Sent When**: Owner creates new client

### Password Reset OTP Email

**Template**: `templates/emails/password_reset_otp.html`

**Variables**:
```python
{
    'user': User object,
    'otp': str (6-digit code)
}
```

**Sent When**: User requests password reset

---

## Utility Functions

### `generate_random_password(length=12)`
**Location**: `accounts/utils.py`

**Purpose**: Generate secure random password

**Returns**: str (random password)

**Algorithm**:
- Includes uppercase, lowercase, digits, special characters
- Ensures at least one of each type
- Shuffles characters

### `generate_otp(length=6)`
**Location**: `accounts/utils.py`

**Purpose**: Generate numeric OTP

**Returns**: str (6-digit code)

### `send_client_welcome_email(user, password, owner)`
**Location**: `accounts/utils.py`

**Purpose**: Send welcome email to new client

**Parameters**:
- `user`: User object (client)
- `password`: str (plain text password)
- `owner`: User object (owner who created account)

**Process**:
1. Render HTML email template
2. Send via SMTP
3. Raise exception on failure

### `send_password_reset_otp(user, otp)`
**Location**: `accounts/utils.py`

**Purpose**: Send OTP for password reset

**Parameters**:
- `user`: User object
- `otp`: str (6-digit code)

### `perform_ocr(image_path)`
**Location**: `documents/utils.py`

**Purpose**: Extract text from image

**Parameters**:
- `image_path`: str (path to image file)

**Returns**: str (extracted text)

**Dependencies**: Tesseract OCR

---

## Security Considerations

### Password Security
- **Hashing**: PBKDF2-SHA256 with 260,000 iterations
- **Minimum Length**: 8 characters
- **Storage**: Never stored in plain text
- **Transmission**: HTTPS only

### Session Security
- **Cookie Settings**:
  - `SESSION_COOKIE_HTTPONLY = True`
  - `SESSION_COOKIE_SECURE = True` (production)
  - `SESSION_COOKIE_SAMESITE = 'Lax'`
- **Timeout**: 2 weeks (default)

### CSRF Protection
- **Token Generation**: Automatic on all forms
- **Validation**: Middleware checks all POST requests
- **Exemptions**: None (all forms protected)

### File Upload Security
- **Type Validation**: Whitelist of allowed extensions
- **Size Limit**: 10MB maximum
- **Path Sanitization**: User-specific directories
- **Virus Scanning**: Not implemented (future enhancement)

### SQL Injection Prevention
- **ORM Usage**: All queries use Django ORM
- **Raw SQL**: Avoided (parameterized if necessary)

### XSS Prevention
- **Template Auto-escaping**: Enabled by default
- **User Input**: Always escaped in templates
- **Safe Filter**: Used only when necessary

---

**End of API & Database Reference**
