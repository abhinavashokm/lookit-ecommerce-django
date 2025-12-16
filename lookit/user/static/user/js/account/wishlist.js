

// Remove item from wishlist
const removeButtons = document.querySelectorAll('.remove-btn');
removeButtons.forEach(button => {
    button.addEventListener('click', function() {
        const row = this.closest('tr');
        row.style.opacity = '0';
        setTimeout(() => {
            row.remove();
            updateWishlistCount();
            checkIfEmpty();
        }, 300);
    });
});

// Add event listeners to size dropdowns
document.querySelectorAll('.size-dropdown').forEach(dropdown => {
    const addToCartBtn = dropdown.closest('.wishlist-card').querySelector('.btn-primary');
    
    // Disable add to cart by default if no size is selected
    if (!dropdown.value) {
        addToCartBtn.disabled = true;
    }
    
    dropdown.addEventListener('change', function() {
        if (this.value) {
            addToCartBtn.disabled = false;
            this.style.borderColor = ''; // Reset border color when a size is selected
        } else {
            addToCartBtn.disabled = true;
        }
    });
});

// Update wishlist count
function updateWishlistCount() {
    const items = document.querySelectorAll('.wishlist-table tbody tr');
    const countElements = document.querySelectorAll('.wishlist-count');
    countElements.forEach(el => {
        el.textContent = `(${items.length})`;
    });
}

// Check if wishlist is empty and show empty state
function checkIfEmpty() {
    const items = document.querySelectorAll('.wishlist-table tbody tr');
    const emptyState = document.querySelector('.empty-state');
    const wishlistContent = document.querySelector('.wishlist-table-container');
    
    if (items.length === 0 && emptyState && wishlistContent) {
        wishlistContent.style.display = 'none';
        emptyState.style.display = 'block';
    }
}

// Clear wishlist
document.getElementById('clearWishlistBtn')?.addEventListener('click', function() {
    if (confirm('Are you sure you want to clear your wishlist?')) {
        const wishlistGrid = document.querySelector('.wishlist-grid');
        if (wishlistGrid) {
            wishlistGrid.innerHTML = '';
            updateWishlistCount();
            checkIfEmpty();
        }
    }
});

// Update wishlist count to work with the current HTML structure
function updateWishlistCount() {
    const items = document.querySelectorAll('.wishlist-card');
    const countElements = document.querySelectorAll('.wishlist-count');
    const itemText = items.length === 1 ? 'item' : 'items';
    countElements.forEach(el => {
        el.textContent = `(${items.length} ${itemText})`;
    });
}

// Check if wishlist is empty and show empty state
function checkIfEmpty() {
    const items = document.querySelectorAll('.wishlist-card');
    const emptyState = document.querySelector('.empty-state');
    const wishlistContent = document.querySelector('.wishlist-grid');
    
    if (items.length === 0) {
        if (emptyState) emptyState.style.display = 'flex';
        if (wishlistContent) wishlistContent.style.display = 'none';
    } else {
        if (emptyState) emptyState.style.display = 'none';
        if (wishlistContent) wishlistContent.style.display = 'grid';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateWishlistCount();
    checkIfEmpty();
});
