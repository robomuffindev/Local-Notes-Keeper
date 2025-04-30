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