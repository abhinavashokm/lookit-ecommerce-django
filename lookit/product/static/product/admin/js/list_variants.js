// Helper function to properly close a dropdown
function closeDropdown(dropdown) {
    dropdown.classList.remove('show');
    dropdown.style.top = '';
    dropdown.style.right = '';
    dropdown.style.visibility = '';
    dropdown.style.display = '';
}

// Close all dropdowns
function closeAllDropdowns() {
    document.querySelectorAll('.actions-dropdown').forEach(d => {
        closeDropdown(d);
    });
}

// Toggle actions dropdown
function toggleActionsDropdown(event, variantId) {
    event.stopPropagation();
    const dropdown = document.getElementById(`actions-${variantId}`);
    const allDropdowns = document.querySelectorAll('.actions-dropdown');
    const button = event.currentTarget;

    // Close all other dropdowns
    allDropdowns.forEach(d => {
        if (d.id !== `actions-${variantId}`) {
            closeDropdown(d);
        }
    });

    // Toggle current dropdown
    const isOpen = dropdown.classList.contains('show');

    if (!isOpen) {
        // Temporarily show dropdown to measure it (hidden from view)
        dropdown.style.visibility = 'hidden';
        dropdown.style.display = 'block';
        dropdown.style.top = '-9999px';
        dropdown.style.right = '0';
        dropdown.classList.add('show');

        // Force a reflow to get accurate measurements
        void dropdown.offsetHeight;

        // Get actual dimensions
        const dropdownRect = dropdown.getBoundingClientRect();
        const dropdownHeight = dropdownRect.height;
        const dropdownWidth = dropdownRect.width;

        // Calculate button position
        const rect = button.getBoundingClientRect();
        const gap = 5;

        // Position below button by default
        let top = rect.bottom + gap;
        let right = window.innerWidth - rect.right;

        // Check if dropdown would go off bottom of screen
        if (top + dropdownHeight > window.innerHeight - gap) {
            // Position above button instead
            top = rect.top - dropdownHeight - gap;
            // If still goes off top, position at bottom of screen
            if (top < gap) {
                top = window.innerHeight - dropdownHeight - gap;
            }
        }

        // Adjust horizontal position if needed
        if (right + dropdownWidth > window.innerWidth - gap) {
            right = window.innerWidth - rect.left - dropdownWidth;
            if (right < gap) {
                right = gap;
            }
        }

        // Apply final positioning
        dropdown.style.top = `${top}px`;
        dropdown.style.right = `${right}px`;
        dropdown.style.visibility = 'visible';
    } else {
        closeDropdown(dropdown);
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    // Don't close if clicking on the dropdown itself or the button
    if (!e.target.closest('.actions-cell') && !e.target.closest('.actions-dropdown')) {
        closeAllDropdowns();
    }
});

// Close dropdowns on scroll
let scrollTimeout;
window.addEventListener('scroll', () => {
    // Clear any existing timeout
    clearTimeout(scrollTimeout);

    // Close dropdowns immediately
    closeAllDropdowns();
}, true);

// Close dropdowns on resize
let resizeTimeout;
window.addEventListener('resize', () => {
    // Debounce resize events
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        closeAllDropdowns();
    }, 100);
});

// Update stock
function updateStock(variantId, change) {
    const stockElement = document.getElementById(`stock-${variantId}`);
    let currentStock = parseInt(stockElement.textContent);
    currentStock = Math.max(0, currentStock + change);
    stockElement.textContent = currentStock;

    // Add actual API call here to update stock
    console.log(`Updated stock for variant ${variantId} to ${currentStock}`);
}

// Set default variant
function setDefault(variantId) {
    // Remove default class from all rows
    document.querySelectorAll('.variants-table tbody tr').forEach(row => {
        row.classList.remove('default-variant');
        const colorCell = row.querySelector('.color-cell');
        if (colorCell) {
            const existingBadge = colorCell.querySelector('.default-badge');
            if (existingBadge) {
                existingBadge.remove();
            }
        }
    });

    // Add default class to selected row
    const stockElement = document.getElementById(`stock-${variantId}`);
    if (stockElement) {
        const selectedRow = stockElement.closest('tr');
        if (selectedRow) {
            selectedRow.classList.add('default-variant');
            const colorCell = selectedRow.querySelector('.color-cell');
            if (colorCell) {
                const defaultBadge = document.createElement('span');
                defaultBadge.className = 'default-badge';
                defaultBadge.textContent = 'Default';
                colorCell.appendChild(defaultBadge);
            }
        }
    }

    // Close dropdown
    const dropdown = document.getElementById(`actions-${variantId}`);
    closeDropdown(dropdown);

    // Add actual API call here
    alert(`Variant ${variantId} set as default`);
}

// Edit variant
function editVariant(variantId) {
    const dropdown = document.getElementById(`actions-${variantId}`);
    closeDropdown(dropdown);
    alert(`Edit variant ${variantId}`);
    // Add navigation to edit page or open modal
}

// Deactivate variant
function deactivateVariant(variantId) {
    const dropdown = document.getElementById(`actions-${variantId}`);
    closeDropdown(dropdown);
    const stockElement = document.getElementById(`stock-${variantId}`);
    if (stockElement) {
        const row = stockElement.closest('tr');
        if (row) {
            const statusBadge = row.querySelector('.status-badge');
            if (statusBadge) {
                statusBadge.textContent = 'Inactive';
                statusBadge.className = 'status-badge status-inactive';
            }
        }
    }
    alert(`Variant ${variantId} deactivated`);
    // Add actual API call here
}

// Delete variant
function deleteVariant(variantId) {
    const dropdown = document.getElementById(`actions-${variantId}`);
    closeDropdown(dropdown);
    if (confirm('Are you sure you want to delete this variant?')) {
        const stockElement = document.getElementById(`stock-${variantId}`);
        if (stockElement) {
            const row = stockElement.closest('tr');
            if (row) {
                row.remove();
            }
        }
        alert(`Variant ${variantId} deleted`);
        // Add actual API call here
    }
}

// Add variant
function addVariant() {
    window.location.href = 'add_variant.html';
}

// Pagination functionality
function changePage(page) {
    const buttons = document.querySelectorAll('.pagination-btn');
    let targetPage = page;

    if (page === 'prev') {
        // Previous button
        const currentPage = document.querySelector('.pagination-btn.active');
        const currentIndex = Array.from(buttons).indexOf(currentPage);
        if (currentIndex > 1) {
            targetPage = parseInt(buttons[currentIndex - 1].textContent);
        } else {
            return; // Already on first page
        }
    } else if (page === 'next') {
        // Next button
        const currentPage = document.querySelector('.pagination-btn.active');
        const currentIndex = Array.from(buttons).indexOf(currentPage);
        if (currentIndex < buttons.length - 2) {
            targetPage = parseInt(buttons[currentIndex + 1].textContent);
        } else {
            return; // Already on last page
        }
    }

    // Remove active class from all buttons
    buttons.forEach(btn => btn.classList.remove('active'));

    // Add active class to target page button
    buttons.forEach((btn, index) => {
        if (parseInt(btn.textContent) === targetPage) {
            btn.classList.add('active');
        }
    });

    // Update previous/next button states
    const activeButton = document.querySelector('.pagination-btn.active');
    const activeIndex = Array.from(buttons).indexOf(activeButton);
    buttons[0].disabled = activeIndex === 1; // First page
    buttons[buttons.length - 1].disabled = activeIndex === buttons.length - 2; // Last page

    // Add actual API call here to fetch page data
    console.log(`Loading page ${targetPage}`);
}