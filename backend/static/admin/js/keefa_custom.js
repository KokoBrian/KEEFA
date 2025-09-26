// keefa_custom.js

document.addEventListener('DOMContentLoaded', function() {
    // 1. Auto-focus the search bar for quick access
    // This targets the search input field in the top navigation bar
    var searchInput = document.getElementById('search-input'); 
    
    // Check if the search input exists before attempting to focus
    if (searchInput) {
        searchInput.focus();
    }

    // 2. Example: Add a click listener to all sidebar links for analytics or custom behavior
    document.querySelectorAll('.nav-sidebar a.nav-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            // console.log('Sidebar link clicked:', event.target.textContent);
            // You can add custom logic here, like a confirmation prompt for destructive actions
        });
    });
});