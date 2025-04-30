// static/js/script.js

// Add date formatting filter
function formatDateTime(dateTimeStr) {
    if (!dateTimeStr) return '';
    
    const date = new Date(dateTimeStr);
    return date.toLocaleString();
}

// Add filesize formatting filter
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Handle file input styling
document.addEventListener('DOMContentLoaded', function() {
    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.flash');
    if (flashMessages.length > 0) {
        setTimeout(function() {
            flashMessages.forEach(function(message) {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.remove();
                }, 300);
            });
        }, 3000);
    }
    
    // File input styling
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'No file selected';
            const fileLabel = document.querySelector('.file-input-label');
            if (fileLabel) {
                fileLabel.textContent = fileName;
            }
        });
    }
    
    // Mobile navigation toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.querySelector('nav ul');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('show');
        });
    }
    
    // Handle text selection in notes
    const noteContent = document.getElementById('note-content');
    if (noteContent) {
        noteContent.addEventListener('touchstart', function(e) {
            // Allow default touch behavior for text selection
        });
    }
});

// Custom filters for Jinja templates
// Note: These are actually implemented in the Flask app
// This is just for documentation purposes
const filters = {
    format_datetime: formatDateTime,
    format_size: formatFileSize,
    nl2br: function(text) {
        return text.replace(/\n/g, '<br>');
    }
};