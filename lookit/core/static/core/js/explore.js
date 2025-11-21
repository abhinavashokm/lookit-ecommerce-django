// Mobile Filter Toggle
const filterToggleBtn = document.getElementById('filterToggleBtn');
const mobileFilterSidebar = document.getElementById('mobileFilterSidebar');

if (filterToggleBtn && mobileFilterSidebar) {
    filterToggleBtn.addEventListener('click', function () {
        mobileFilterSidebar.classList.toggle('expanded');
        filterToggleBtn.classList.toggle('active');
    });
}

// Filter Functions
function handleFilterSubmit(event) {
    event.preventDefault();
    applyFilters();
}

function clearFilters() {
    // Clear searchable dropdowns
    const stylesInput = document.getElementById('stylesInput');
    const stylesValue = document.getElementById('stylesValue');
    const stylesInputMobile = document.getElementById('stylesInputMobile');
    const stylesValueMobile = document.getElementById('stylesValueMobile');

    if (stylesInput && stylesValue) {
        stylesInput.value = '';
        stylesValue.value = '';
        stylesInput.placeholder = 'All Styles';
    }

    if (stylesInputMobile && stylesValueMobile) {
        stylesInputMobile.value = '';
        stylesValueMobile.value = '';
        stylesInputMobile.placeholder = 'All Styles';
    }

    // Clear other filters
    document.getElementById('color').value = '';
    document.getElementById('size').value = '';

    // Clear desktop price range
    const priceRangeMin = document.getElementById('priceRangeMin');
    const priceRangeMax = document.getElementById('priceRangeMax');
    if (priceRangeMin && priceRangeMax) {
        priceRangeMin.value = 500;
        priceRangeMax.value = 2500;
    }

    // Clear mobile price range
    const priceRangeMinMobile = document.getElementById('priceRangeMinMobile');
    const priceRangeMaxMobile = document.getElementById('priceRangeMaxMobile');
    if (priceRangeMinMobile && priceRangeMaxMobile) {
        priceRangeMinMobile.value = 500;
        priceRangeMaxMobile.value = 2500;
    }

    updatePriceDisplay(false);
    updatePriceDisplay(true);
}

function applyFilters() {
    // Filter logic would go here
    console.log('Filters applied');
}

// Search Functions
const searchInput = document.getElementById('searchInput');
const searchClearBtn = document.getElementById('searchClearBtn');
const searchForm = document.getElementById('searchForm');

if (searchInput && searchClearBtn) {
    // Show/hide clear button based on input value
    searchInput.addEventListener('input', function () {
        if (this.value.trim().length > 0) {
            searchClearBtn.classList.add('visible');
        } else {
            searchClearBtn.classList.remove('visible');
        }
    });

    // Check initial state
    if (searchInput.value.trim().length > 0) {
        searchClearBtn.classList.add('visible');
    }
}

function clearSearch() {
    if (searchInput) {
        searchInput.value = '';
        searchInput.focus();
        if (searchClearBtn) {
            searchClearBtn.classList.remove('visible');
        }
    }
}

function handleSearch(event) {
    event.preventDefault();
    const searchValue = searchInput.value.trim();
    // Search logic would go here
    console.log('Searching for:', searchValue);
    // You can implement the actual search functionality here
}

// Sort Products Function
function sortProducts(sortType) {
    // Remove active class from all sort buttons
    document.querySelectorAll('.sort-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active class to clicked button
    event.target.classList.add('active');

    // Sort logic would go here
    console.log('Sorting by:', sortType);

    // Example: You would implement actual sorting logic here
    // const products = Array.from(document.querySelectorAll('.product-card'));
    // products.sort((a, b) => {
    //     if (sortType === 'price-low') {
    //         return parsePrice(a) - parsePrice(b);
    //     } else if (sortType === 'price-high') {
    //         return parsePrice(b) - parsePrice(a);
    //     } else if (sortType === 'name-az') {
    //         return getProductName(a).localeCompare(getProductName(b));
    //     } else if (sortType === 'name-za') {
    //         return getProductName(b).localeCompare(getProductName(a));
    //     }
    // });
    // const productGrid = document.querySelector('.product-grid');
    // products.forEach(product => productGrid.appendChild(product));
}

// Price Range Slider (Dual Handle) - Desktop
const priceRangeMin = document.getElementById('priceRangeMin');
const priceRangeMax = document.getElementById('priceRangeMax');
const priceRangeActive = document.getElementById('priceRangeActive');
const priceRangeWrapper = document.querySelector('.filter-sidebar:not(#mobileFilterSidebar) .price-range-wrapper');

// Price Range Slider (Dual Handle) - Mobile
const priceRangeMinMobile = document.getElementById('priceRangeMinMobile');
const priceRangeMaxMobile = document.getElementById('priceRangeMaxMobile');
const priceRangeActiveMobile = document.getElementById('priceRangeActiveMobile');
const priceRangeWrapperMobile = document.querySelector('#mobileFilterSidebar .price-range-wrapper');

function updatePriceDisplay(isMobile = false) {
    const minSlider = isMobile ? priceRangeMinMobile : priceRangeMin;
    const maxSlider = isMobile ? priceRangeMaxMobile : priceRangeMax;
    const activeLine = isMobile ? priceRangeActiveMobile : priceRangeActive;
    const wrapper = isMobile ? priceRangeWrapperMobile : priceRangeWrapper;
    const minDisplay = isMobile ? document.getElementById('priceMinDisplayMobile') : document.getElementById('priceMinDisplay');
    const maxDisplay = isMobile ? document.getElementById('priceMaxDisplayMobile') : document.getElementById('priceMaxDisplay');

    if (!minSlider || !maxSlider) return;

    const minValue = parseInt(minSlider.value);
    const maxValue = parseInt(maxSlider.value);
    const maxRange = parseInt(minSlider.max);

    // Ensure min doesn't exceed max
    if (minValue > maxValue) {
        minSlider.value = maxValue;
    }

    // Ensure max doesn't go below min
    if (maxValue < minValue) {
        maxSlider.value = minValue;
    }

    const finalMin = parseInt(minSlider.value);
    const finalMax = parseInt(maxSlider.value);

    if (minDisplay && maxDisplay) {
        minDisplay.textContent = `₹${finalMin.toLocaleString('en-IN')}`;
        maxDisplay.textContent = `₹${finalMax.toLocaleString('en-IN')}`;
    }

    // Update the colored active range line
    if (activeLine && wrapper) {
        const wrapperWidth = wrapper.offsetWidth;
        const minPercent = (finalMin / maxRange) * 100;
        const maxPercent = (finalMax / maxRange) * 100;

        activeLine.style.left = minPercent + '%';
        activeLine.style.width = (maxPercent - minPercent) + '%';
    }
}

// Desktop price range
if (priceRangeMin && priceRangeMax) {
    priceRangeMin.addEventListener('input', () => updatePriceDisplay(false));
    priceRangeMax.addEventListener('input', () => updatePriceDisplay(false));
}

// Mobile price range
if (priceRangeMinMobile && priceRangeMaxMobile) {
    priceRangeMinMobile.addEventListener('input', () => updatePriceDisplay(true));
    priceRangeMaxMobile.addEventListener('input', () => updatePriceDisplay(true));
}

// Initialize price display for both
updatePriceDisplay(false);
updatePriceDisplay(true);

// Update on window resize
window.addEventListener('resize', () => {
    updatePriceDisplay(false);
    updatePriceDisplay(true);
});

// Searchable Dropdown Functionality
function initSearchableDropdown(dropdownId, inputId, valueId, searchId) {
    const dropdown = document.getElementById(dropdownId);
    const input = document.getElementById(inputId);
    const hiddenInput = document.getElementById(valueId);
    const searchInput = document.getElementById(searchId);
    const options = dropdown.querySelectorAll('.searchable-dropdown-option');

    if (!dropdown || !input || !hiddenInput || !searchInput) return;

    // Toggle dropdown
    input.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.classList.toggle('open');
        if (dropdown.classList.contains('open')) {
            searchInput.focus();
        }
    });

    // Search functionality
    searchInput.addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        options.forEach(option => {
            const text = option.getAttribute('data-text').toLowerCase();
            if (text.includes(searchTerm)) {
                option.classList.remove('hidden');
            } else {
                option.classList.add('hidden');
            }
        });
    });

    // Select option
    options.forEach(option => {
        option.addEventListener('click', function () {
            const value = this.getAttribute('data-value');
            const text = this.getAttribute('data-text');

            input.value = text;
            hiddenInput.value = value;

            // Update selected state
            options.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');

            // Close dropdown
            dropdown.classList.remove('open');
            searchInput.value = '';

            // Reset hidden options
            options.forEach(opt => opt.classList.remove('hidden'));
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
            searchInput.value = '';
            options.forEach(opt => opt.classList.remove('hidden'));
        }
    });
}

// Initialize searchable dropdowns
initSearchableDropdown('stylesDropdown', 'stylesInput', 'stylesValue', 'stylesSearch');
initSearchableDropdown('stylesDropdownMobile', 'stylesInputMobile', 'stylesValueMobile', 'stylesSearchMobile');