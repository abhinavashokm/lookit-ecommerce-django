// Toggle filters functionality
function toggleFilters() {
    const filtersContainer = document.getElementById('filtersContainer');
    const filterToggle = document.getElementById('filterToggle');
    const icon = filterToggle.querySelector('span:first-child');

    filtersContainer.classList.toggle('show');
    filterToggle.classList.toggle('active');

    // Change icon based on state
    if (filtersContainer.classList.contains('show')) {
        icon.textContent = '🔼';
    } else {
        icon.textContent = '🔽';
    }
}

// Export CSV functionality
document.querySelector('.btn-export').addEventListener('click', () => {
    alert('Exporting user data to CSV...');
    // Add actual CSV export logic here
});

// View user functionality
function viewUser(userId) {
    alert(`Viewing details for user ID: ${userId}`);
    // Add navigation to user details page
}