

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


// Update wishlist count to work with the current HTML structure
function updateWishlistCount() {
    const items = document.querySelectorAll('.wishlist-card');
    const countElements = document.querySelectorAll('.wishlist-count');
    const itemText = items.length === 1 ? 'item' : 'items';
    countElements.forEach(el => {
        el.textContent = `(${items.length} ${itemText})`;
    });
}


// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateWishlistCount();
    checkIfEmpty();
});


//FOR ADDING VARIANT ID TO MOVE TO CART  REQUEST          
document.getElementById("moveToCartForm").addEventListener("submit", function (event) {
// Step 1: Temporarily block submission
event.preventDefault();

const sizeOptions = document.getElementById('sizeOptions')


// Step 2: Add a new field dynamically
const form = event.target;
const hidden = document.createElement("input");
hidden.type = "hidden";
hidden.name = "variant_id";
hidden.value = sizeOptions.value; // You can compute something dynamically here
form.appendChild(hidden);

// Step 3: Continue form submission (resume normal behavior)
form.submit();
});