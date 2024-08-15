// dashboard.js
$(document).ready(function() {
    // Example: Add a simple confirmation for delete actions
    $('.delete').on('click', function() {
        return confirm('Are you sure you want to delete this book?');
    });
});
