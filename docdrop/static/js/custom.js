// Custom JavaScript for DocDrop

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// File upload validation
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('document_file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Check file size (10MB)
                const maxSize = 10 * 1024 * 1024; // 10MB in bytes
                if (file.size > maxSize) {
                    alert('File size exceeds 10MB limit. Please choose a smaller file.');
                    e.target.value = '';
                    return;
                }
                
                // Check file type
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf', 
                                     'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Invalid file type. Allowed: JPG, PNG, PDF, DOC, DOCX');
                    e.target.value = '';
                    return;
                }
            }
        });
    }
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

