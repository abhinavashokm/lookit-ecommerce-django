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
            }
        });

        // Toggle current dropdown
        dropdown.classList.toggle('show', !isOpen);
    }

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
        });
    }



