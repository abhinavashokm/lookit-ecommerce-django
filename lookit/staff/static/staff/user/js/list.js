/* ============================================
       FILTERS FUNCTIONALITY
       ============================================ */
// Toggle filters functionality
function toggleFilters() {
    const filtersContainer = document.getElementById('filtersContainer');
    const filterToggle = document.getElementById('filterToggle');

    filtersContainer.classList.toggle('show');
    filterToggle.classList.toggle('active');
}

// Custom dropdown functionality
function toggleDropdown(button, event) {
    if (event) {
        event.stopPropagation();
    }
    const dropdown = button.nextElementSibling;
    const isActive = button.classList.contains('active');

    // Close all other dropdowns
    closeAllDropdowns();

    // Toggle current dropdown
    if (!isActive) {
        button.classList.add('active');
        dropdown.classList.add('show');
    } else {
        button.classList.remove('active');
        dropdown.classList.remove('show');
    }
}

function selectOption(item, buttonId, event) {
    if (event) {
        event.stopPropagation();
    }
    const button = document.getElementById(buttonId);
    const dropdown = button.nextElementSibling;
    const text = item.textContent;
    const value = item.getAttribute('data-value');

    // Update button text
    button.querySelector('.dropdown-text').textContent = text;
    button.classList.add('has-value');

    // Update selected state
    const allItems = dropdown.querySelectorAll('.dropdown-item');
    allItems.forEach(i => i.classList.remove('selected'));
    item.classList.add('selected');

    // Store the value on the button
    button.setAttribute('data-value', value);

    // Close dropdown
    button.classList.remove('active');
    dropdown.classList.remove('show');
}

function closeAllDropdowns() {
    const allButtons = document.querySelectorAll('.dropdown-button');
    const allMenus = document.querySelectorAll('.dropdown-menu');

    allButtons.forEach(btn => btn.classList.remove('active'));
    allMenus.forEach(menu => menu.classList.remove('show'));
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-dropdown')) {
        closeAllDropdowns();
    }
});

// Reset filters functionality
document.querySelector('.btn-reset')?.addEventListener('click', () => {
    const allButtons = document.querySelectorAll('.dropdown-button');
    allButtons.forEach(button => {
        // Get the default placeholder text from the button id
        const buttonId = button.id;
        let defaultText = 'Status';
        if (buttonId === 'roleDropdownBtn') {
            defaultText = 'Filter by Role';
        } else if (buttonId === 'dateDropdownBtn') {
            defaultText = 'Joined Date';
        }

        button.querySelector('.dropdown-text').textContent = defaultText;
        button.classList.remove('has-value');
        button.removeAttribute('data-value');

        // Clear selected state
        const dropdown = button.nextElementSibling;
        const allItems = dropdown.querySelectorAll('.dropdown-item');
        allItems.forEach(item => item.classList.remove('selected'));
    });

    closeAllDropdowns();
});

/* ============================================
   TABLE FUNCTIONALITY
   ============================================ */
// View user functionality
function viewUser(userId) {
    alert(`Viewing details for user ID: ${userId}`);
    // Add navigation to user details page
}