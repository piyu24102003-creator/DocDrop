# DocDrop - User Guide

## Complete User Manual

**Version:** 1.0.0  
**Last Updated:** January 2, 2026  
**Audience:** Owners and Clients

---

## Table of Contents

### For Owners (Admins)
1. [Getting Started as Owner](#getting-started-as-owner)
2. [Managing Clients](#managing-clients)
3. [Requesting Documents](#requesting-documents)
4. [Viewing Documents](#viewing-documents)
5. [Dashboard Overview](#owner-dashboard)

### For Clients (Users)
6. [Getting Started as Client](#getting-started-as-client)
7. [Uploading Documents](#uploading-documents)
8. [Responding to Requests](#responding-to-requests)
9. [Managing Your Documents](#managing-your-documents)
10. [Client Dashboard](#client-dashboard)

### For Everyone
11. [Profile Management](#profile-management)
12. [Changing Password](#changing-password)
13. [Tips & Best Practices](#tips--best-practices)
14. [FAQ](#frequently-asked-questions)

---

## Getting Started as Owner

### Registration

1. **Navigate to Registration Page**
   - Go to: http://yoursite.com/accounts/register/owner/
   - Or click "Register as Owner" on homepage

2. **Fill Registration Form**
   - **Full Name**: Your complete name
   - **Firm/Company Name**: Your business name (e.g., "ABC Consultants")
   - **Email**: Your email address (will be your username)
   - **Contact Number**: Your phone number
   - **Designation**: Select from dropdown (Business, Startup, Student, etc.)
   - **Password**: Minimum 8 characters
   - **Confirm Password**: Re-enter password

3. **Submit**
   - Click "Register" button
   - You'll be redirected to login page
   - Success message will appear

### First Login

1. **Go to Owner Login**
   - Navigate to: http://yoursite.com/accounts/admin/login/
   - Or click "Owner Login" on homepage

2. **Enter Credentials**
   - **Username**: Your email address
   - **Password**: Password you set during registration

3. **Access Dashboard**
   - After successful login, you'll see the Owner Dashboard
   - Shows statistics, recent uploads, and quick actions

---

## Managing Clients

### Creating a New Client

1. **Navigate to User Management**
   - From dashboard, click "Manage Users" in navigation
   - Or go to: http://yoursite.com/accounts/admin/users/

2. **Click "Create User"**
   - Green button at top of page
   - Opens client creation form

3. **Fill Client Information**
   - **Email**: Client's email address (required)
     - Will be their username
     - Must be unique
   - **First Name**: Client's first name (optional)
   - **Last Name**: Client's last name (optional)

4. **Submit**
   - Click "Create User" button
   - System automatically:
     - Generates secure random password
     - Creates client account
     - Sends welcome email to client with credentials

5. **Confirmation**
   - Success message appears
   - Client receives email with:
     - Username (their email)
     - Auto-generated password
     - Login link
     - Instructions

### Viewing Client List

1. **Access User List**
   - Click "Manage Users" in navigation
   - Shows all your clients in a table

2. **Information Displayed**
   - Client name
   - Email address
   - Number of documents uploaded
   - Quick action buttons

3. **Actions Available**
   - **View**: See client details
   - **Request**: Request a document
   - **Delete**: Remove client (with confirmation)

### Viewing Client Details

1. **Click on Client Name**
   - From user list, click any client name
   - Opens detailed client page

2. **Information Shown**
   - **Profile Information**
     - Name
     - Email
     - Phone (if provided)
     - Join date
   
   - **Document Requests**
     - All requests sent to this client
     - Request title
     - Status (Pending/Completed)
     - Date created
     - Link to view uploaded document (if completed)
   
   - **Documents Received**
     - All documents uploaded by this client
     - Document name
     - Upload date
     - File type
     - Actions (view, download, delete)

3. **Quick Actions**
   - **Request Document**: Create new request for this client
   - **Back to List**: Return to client list

### Deleting a Client

1. **From Client List**
   - Click red "Delete" button next to client name

2. **Confirmation**
   - Confirm deletion in popup dialog
   - **Warning**: This action cannot be undone!

3. **What Gets Deleted**
   - Client account
   - Client profile
   - **Note**: Documents are preserved (for audit purposes)

---

## Requesting Documents

### Creating a Document Request

1. **Navigate to Client Details**
   - Go to "Manage Users"
   - Click on client name
   - Click "Request Document" button

2. **Fill Request Form**
   - **Title**: Document name (e.g., "PAN Card", "Bank Statement")
     - Be specific and clear
     - Client will see this title
   
   - **Description** (Optional): Additional instructions
     - Example: "Please upload last 6 months bank statement"
     - Example: "Scan both sides of PAN card"

3. **Submit Request**
   - Click "Send Request" button
   - System automatically:
     - Creates request record
     - Sends email notification to client
     - Updates request list

4. **Confirmation**
   - Success message appears
   - Request appears in client's "My Requests"
   - Client receives email notification

### Tracking Requests

1. **View in Client Details**
   - Go to client's detail page
   - "Document Requests" section shows all requests
   - Status indicators:
     - **Pending** (Yellow badge): Awaiting client upload
     - **Completed** (Green badge): Client has uploaded

2. **Request Information**
   - Request title
   - Date sent
   - Current status
   - Link to view document (if completed)

### Viewing Fulfilled Requests

1. **When Client Uploads**
   - Request status automatically changes to "Completed"
   - Document appears in "Documents Received" section
   - You can view/download the document

2. **Accessing Document**
   - Click "View File" link in requests table
   - Or find in "Documents Received" section
   - Download or preview as needed

---

## Viewing Documents

### Accessing All Documents

1. **Navigate to Documents**
   - Click "All Documents" in navigation
   - Shows all documents uploaded by your clients

2. **Document List View**
   - **Document Name**: Original filename
   - **Uploaded By**: Client name
   - **Upload Date**: When it was uploaded
   - **File Type**: Image, PDF, DOCX, etc.
   - **Actions**: View, Download, Delete

### Searching Documents

1. **Use Search Box**
   - Located at top of document list
   - Search by:
     - Document name
     - OCR extracted text (for images)

2. **Search Tips**
   - Enter keywords
   - Press Enter or click Search
   - Results update automatically

### Viewing Document Details

1. **Click "View" Button**
   - Opens document preview page

2. **Information Shown**
   - Document name
   - Uploader name
   - Upload date
   - File size
   - File type

3. **For Images**
   - Image preview
   - OCR extracted text (if available)

4. **For PDFs**
   - PDF preview in browser
   - Download option

### Downloading Documents

1. **Click "Download" Button**
   - From document list or detail page
   - File downloads to your computer
   - Original filename and extension preserved

### Deleting Documents

1. **Click "Delete" Button**
   - Red button in actions column

2. **Confirmation**
   - Confirm deletion
   - **Warning**: Cannot be undone!

3. **What Happens**
   - Document removed from system
   - File deleted from storage
   - Cannot be recovered

---

## Owner Dashboard

### Dashboard Overview

When you login as owner, you see:

1. **Statistics Cards**
   - **Total Clients**: Number of clients you manage
   - **Total Documents**: Documents received from all clients
   - **Pending Requests**: Requests awaiting client upload

2. **Recent Uploads**
   - Last 10 documents uploaded
   - Shows:
     - Document name
     - Client name
     - Upload date
   - Quick actions (view, download)

3. **Top Uploaders**
   - Clients with most documents
   - Document count per client
   - Click to view client details

### Quick Actions

From dashboard, you can:
- Click "Manage Users" → View/manage clients
- Click "All Documents" → See all documents
- Click client name → View client details
- Click document name → View document

---

## Getting Started as Client

### Receiving Welcome Email

When your owner creates your account:

1. **Check Your Email**
   - Subject: "Welcome to DocDrop - Your Account Details"
   - From: DocDrop (owner's email)

2. **Email Contains**
   - Your username (your email address)
   - Auto-generated password
   - Login link
   - Instructions

3. **Important**
   - Save your password securely
   - Change password after first login (recommended)

### First Login

1. **Go to Client Login**
   - Click link in email
   - Or go to: http://yoursite.com/accounts/login/

2. **Enter Credentials**
   - **Username**: Your email address
   - **Password**: From welcome email

3. **Access Dashboard**
   - After login, you see Client Dashboard
   - Shows your documents and pending requests

---

## Uploading Documents

### Method 1: Regular Upload

1. **Navigate to Upload Page**
   - Click "Upload" in navigation
   - Or go to: http://yoursite.com/documents/upload/

2. **Select Target Owner**
   - If you have multiple owners, select one
   - If only one owner, auto-selected

3. **Enter Document Name**
   - Give your document a descriptive name
   - Example: "PAN Card", "Salary Slip - January 2026"

4. **Choose File**
   - Click "Choose File" button
   - Select file from your computer
   - **Supported formats**:
     - Images: JPG, JPEG, PNG
     - Documents: PDF, DOC, DOCX
   - **Maximum size**: 10MB

5. **Upload**
   - Click "Upload Document" button
   - Wait for upload to complete
   - Success message appears

### Method 2: Camera Capture (Mobile/Desktop)

1. **On Upload Page**
   - Click "Use Camera" button
   - Browser asks for camera permission
   - Allow camera access

2. **Capture Photo**
   - Point camera at document
   - Ensure good lighting
   - Document should be clear and readable
   - Click "Capture" button

3. **Review**
   - Preview captured image
   - Retake if needed
   - Click "Use This Photo"

4. **Upload**
   - Enter document name
   - Click "Upload Document"

### Method 3: Upload from Request

1. **View Pending Requests**
   - Go to "Requests" in navigation
   - See list of pending requests

2. **Click "Upload" on Request**
   - Opens upload page
   - Document name pre-filled with request title
   - Target owner pre-selected

3. **Choose File**
   - Select file
   - Upload

4. **Automatic Actions**
   - Request status changes to "Completed"
   - Owner is notified
   - Document linked to request

---

## Responding to Requests

### Viewing Requests

1. **Access Requests**
   - Click "Requests" in navigation
   - Or check "Action Required" on dashboard

2. **Request Information**
   - **Title**: What document is requested
   - **Description**: Additional instructions (if any)
   - **Requested By**: Owner's firm name
   - **Date**: When request was sent
   - **Status**: Pending or Completed

### Uploading for Request

1. **Click "Upload" Button**
   - On the specific request
   - Opens upload page with pre-filled information

2. **Select File**
   - Choose the requested document
   - Ensure it matches what was requested

3. **Upload**
   - Click "Upload Document"
   - Request automatically marked as completed

### Email Notifications

You receive emails when:
- New request is created
- (Future) Reminders for pending requests

---

## Managing Your Documents

### Viewing Your Documents

1. **Access Document List**
   - Click "My Documents" in navigation
   - Shows all documents you've uploaded

2. **Information Displayed**
   - Document name
   - Upload date
   - File type
   - Target owner
   - Actions

### Searching Your Documents

1. **Use Search Box**
   - Enter document name or keywords
   - Press Enter
   - Results filter automatically

### Downloading Your Documents

1. **Click "Download" Button**
   - File downloads to your device
   - Original format preserved

### Deleting Your Documents

1. **Click "Delete" Button**
   - Confirmation dialog appears
   - Confirm deletion
   - **Note**: Owner may still have access (check with owner)

---

## Client Dashboard

### Dashboard Overview

Your dashboard shows:

1. **Statistics**
   - Total documents uploaded
   - Pending requests count

2. **Action Required**
   - Pending document requests
   - Quick upload links
   - Request details

3. **Recent Uploads**
   - Your last uploaded documents
   - Upload dates
   - Quick actions

### Quick Actions

From dashboard:
- Click "Upload" → Upload new document
- Click "Requests" → View all requests
- Click "My Documents" → See all your documents
- Click request title → Upload for that request

---

## Profile Management

### Accessing Profile

1. **Click Your Name**
   - Top right corner of navigation
   - Or go to: http://yoursite.com/accounts/profile/

### Updating Profile Information

1. **Edit Fields**
   - **Email**: Your email address
   - **First Name**: Your first name
   - **Last Name**: Your last name
   - **Phone**: Your contact number
   - **Firm Name** (Owners only): Your company name

2. **Save Changes**
   - Click "Update Profile" button
   - Success message appears

---

## Changing Password

### Using OTP Verification

1. **From Profile Page**
   - Click "Change Password" button
   - Or go to: http://yoursite.com/accounts/password-reset/request/

2. **Enter Your Email**
   - Type your email address
   - Click "Send OTP"

3. **Check Email**
   - You'll receive an email with 6-digit OTP
   - OTP valid for 10 minutes

4. **Enter OTP and New Password**
   - Go to verification page
   - Enter:
     - Your email
     - 6-digit OTP from email
     - New password (min 8 characters)
     - Confirm new password
   - Click "Reset Password"

5. **Login with New Password**
   - Password changed successfully
   - Login with new credentials

### Password Requirements

- Minimum 8 characters
- Can include letters, numbers, special characters
- Must match confirmation
- Cannot be same as old password

### Password Tips

- Use strong, unique passwords
- Don't share your password
- Change password regularly
- Use password manager (recommended)

---

## Tips & Best Practices

### For Owners

1. **Client Management**
   - Use descriptive firm name
   - Keep client information updated
   - Regularly review client list

2. **Document Requests**
   - Be specific in request titles
   - Add clear descriptions
   - Follow up on pending requests

3. **Document Organization**
   - Use consistent naming conventions
   - Regularly review and archive old documents
   - Download important documents for backup

4. **Security**
   - Change password regularly
   - Don't share account credentials
   - Logout when done

### For Clients

1. **Document Uploads**
   - Use clear, descriptive names
   - Ensure documents are readable
   - Upload correct documents for requests

2. **File Quality**
   - Good lighting for camera captures
   - Clear, focused images
   - Proper orientation

3. **Timely Response**
   - Check requests regularly
   - Upload requested documents promptly
   - Contact owner if unclear

4. **Security**
   - Keep login credentials secure
   - Change default password
   - Logout on shared devices

---

## Frequently Asked Questions

### General Questions

**Q: What is DocDrop?**
A: DocDrop is a secure document management system for professional service providers and their clients.

**Q: Is it free?**
A: Contact your service provider for pricing information.

**Q: Is my data secure?**
A: Yes, we use industry-standard security measures including encryption, secure authentication, and role-based access control.

### For Owners

**Q: How many clients can I add?**
A: There's no limit on the number of clients.

**Q: Can I delete documents?**
A: Yes, you can delete documents uploaded by your clients.

**Q: How do I export documents?**
A: Download documents individually. Bulk export feature coming soon.

**Q: Can clients see each other's documents?**
A: No, clients can only see their own documents.

### For Clients

**Q: Can I upload to multiple owners?**
A: Yes, if you're linked to multiple owners, you can upload to any of them.

**Q: What file types are supported?**
A: JPG, JPEG, PNG, PDF, DOC, DOCX (max 10MB each).

**Q: Can I delete uploaded documents?**
A: Yes, but your owner may have already downloaded them.

**Q: How do I know if my upload was successful?**
A: You'll see a success message and the document will appear in "My Documents".

### Technical Questions

**Q: Which browsers are supported?**
A: Chrome, Firefox, Safari, Edge (latest versions).

**Q: Can I use on mobile?**
A: Yes, the site is fully responsive and works on mobile devices.

**Q: What if I forget my password?**
A: Use the "Change Password" feature which sends OTP to your email.

**Q: Why can't I login?**
A: Check your email and password. Contact your owner if issues persist.

---

## Getting Help

### Contact Support

- **Email**: support@docdrop.com (if applicable)
- **Owner Contact**: Contact your service provider directly
- **Documentation**: Refer to this user guide

### Reporting Issues

If you encounter problems:
1. Note the error message
2. Note what you were trying to do
3. Take a screenshot if possible
4. Contact support with details

---

**End of User Guide**

Thank you for using DocDrop! We hope this guide helps you make the most of the platform.
