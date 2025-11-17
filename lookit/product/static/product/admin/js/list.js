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

// Toggle dropdown menu
function toggleDropdown(btn) {
    const dropdown = btn.nextElementSibling;
    const isOpen = dropdown.classList.contains('show');

    // Close all other dropdowns
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        if (menu !== dropdown) {
            menu.classList.remove('show');
            menu.classList.remove('above');
            menu.style.visibility = '';
            menu.style.display = '';
        }
    });

    if (!isOpen) {
        // Temporarily show dropdown to measure it
        dropdown.style.visibility = 'hidden';
        dropdown.style.display = 'block';
        dropdown.classList.add('show');

        // Force a reflow to get accurate measurements
        void dropdown.offsetHeight;

        // Get positions
        const btnRect = btn.getBoundingClientRect();
        const dropdownRect = dropdown.getBoundingClientRect();
        const dropdownHeight = dropdownRect.height;
        const gap = 5;

        // Check if dropdown would overflow below
        const spaceBelow = window.innerHeight - btnRect.bottom - gap;
        const spaceAbove = btnRect.top - gap;

        // Position above if not enough space below AND more space above
        if (spaceBelow < dropdownHeight && spaceAbove > spaceBelow) {
            dropdown.classList.add('above');
        } else {
            dropdown.classList.remove('above');
        }

        // Make visible
        dropdown.style.visibility = 'visible';
    } else {
        dropdown.classList.remove('show');
        dropdown.classList.remove('above');
        dropdown.style.visibility = '';
        dropdown.style.display = '';
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.actions-dropdown')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.remove('show');
            menu.classList.remove('above');
            menu.style.visibility = '';
            menu.style.display = '';
        });
    }
});

// Action functions
function viewVariants(productId) {
    alert(`View variants for product ID: ${productId}`);
    closeAllDropdowns();
}

function deactivateProduct(productId) {
    if (confirm(`Are you sure you want to deactivate product ID: ${productId}?`)) {
        alert(`Product ${productId} deactivated`);
        closeAllDropdowns();
    }
}

function editProduct(productId) {
    alert(`Edit product ID: ${productId}`);
    closeAllDropdowns();
}

function deleteProduct(productId) {
    if (confirm(`Are you sure you want to delete product ID: ${productId}? This action cannot be undone.`)) {
        alert(`Product ${productId} deleted`);
        closeAllDropdowns();
    }
}

function closeAllDropdowns() {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.classList.remove('show');
        menu.classList.remove('above');
        menu.style.visibility = '';
        menu.style.display = '';
    });
}