

// Toggle status text
const statusToggle = document.getElementById('status');
const statusText = document.getElementById('statusText');

statusToggle.addEventListener('change', function () {
    statusText.textContent = this.checked ? 'Active' : 'Inactive';
});

// ==========================================
// MOCK DATA FOR PRODUCTS
// ==========================================
const availableProducts = [
    { id: '1', name: 'Smartphone X Pro', image: 'https://via.placeholder.com/40', price: 999 },
    { id: '2', name: 'Laptop Ultra Slim', image: 'https://via.placeholder.com/40', price: 1299 },
    { id: '3', name: 'Wireless Noise Cancelling Headphones', image: 'https://via.placeholder.com/40', price: 299 },
    { id: '4', name: 'Smart Watch Series 5', image: 'https://via.placeholder.com/40', price: 399 },
    { id: '5', name: '4K Ultra HD Monitor', image: 'https://via.placeholder.com/40', price: 499 },
    { id: '6', name: 'Gaming Mouse RGB', image: 'https://via.placeholder.com/40', price: 79 },
    { id: '7', name: 'Mechanical Keyboard', image: 'https://via.placeholder.com/40', price: 149 },
    { id: '8', name: 'USB-C Hub Multiport', image: 'https://via.placeholder.com/40', price: 59 },
];

let selectedProductIds = new Set();

// Elements
const searchBox = document.getElementById('searchBox');
const dropdownOptions = document.getElementById('dropdownOptions');
const productSearchInput = document.getElementById('productSearchInput');
const selectedPreview = document.getElementById('selectedPreview');

// Render Dropdown Options
function renderDropdownOptions(products) {
    dropdownOptions.innerHTML = '';
    if (products.length === 0) {
        dropdownOptions.innerHTML = '<div style="padding:10px; color:#666; text-align:center;">No products found</div>';
        return;
    }

    products.forEach(product => {
        const div = document.createElement('div');
        div.className = `option-item ${selectedProductIds.has(product.id) ? 'selected' : ''}`;
        // Usage of stopPropagation to prevent dropdown close
        div.onclick = (e) => {
            e.stopPropagation();
            toggleProductSelection(product.id);
        };

        div.innerHTML = `
                    <img src="${product.image}" alt="${product.name}" class="product-img">
                    <div class="product-info">
                        <span class="product-name">${product.name}</span>
                        <span class="product-id">ID: ${product.id}</span>
                    </div>
                    ${selectedProductIds.has(product.id) ? '<span style="color:#4f46e5; font-weight:bold;">✓</span>' : ''}
                `;
        dropdownOptions.appendChild(div);
    });
}

// Toggle Selection
function toggleProductSelection(productId) {
    if (selectedProductIds.has(productId)) {
        selectedProductIds.delete(productId);
    } else {
        selectedProductIds.add(productId);
    }

    // Re-render dropdown to update checkboxes/highlighting
    const searchTerm = productSearchInput.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(searchTerm) ||
        p.id.toLowerCase().includes(searchTerm)
    );
    renderDropdownOptions(filtered);

    // Update the preview section
    updateSelectedPreview();

    // Keep focus used to be here, but we want to keep dropdown open which is handled by stopPropagation
    productSearchInput.focus();
}

// Update Selected Preview
function updateSelectedPreview() {
    selectedPreview.innerHTML = '';

    selectedProductIds.forEach(id => {
        const product = availableProducts.find(p => p.id === id);
        if (product) {
            const tag = document.createElement('div');
            tag.className = 'preview-item';
            tag.innerHTML = `
                        <img src="${product.image}" alt="${product.name}" class="preview-img">
                        <div class="preview-info">
                            <span class="preview-name">${product.name}</span>
                        </div>
                        <button type="button" class="remove-btn" onclick="removeTag('${id}', event)">×</button>
                    `;
            selectedPreview.appendChild(tag);
        }
    });
}

// Remove Tag Callback (from preview)
window.removeTag = function (id, event) {
    event.stopPropagation(); // Prevent affecting other elements
    selectedProductIds.delete(id);

    // Re-filter dropdown to consistent state
    const searchTerm = productSearchInput.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(searchTerm) ||
        p.id.toLowerCase().includes(searchTerm)
    );
    renderDropdownOptions(filtered);

    updateSelectedPreview();
};

// Event Listeners for Search
productSearchInput.addEventListener('focus', () => {
    dropdownOptions.classList.add('show');
    const searchTerm = productSearchInput.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(searchTerm) ||
        p.id.toLowerCase().includes(searchTerm)
    );
    renderDropdownOptions(filtered);
});

// Prevent dropdown click from closing it
dropdownOptions.addEventListener('click', (e) => {
    e.stopPropagation();
});

productSearchInput.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdownOptions.classList.add('show');
});

productSearchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const filtered = availableProducts.filter(p =>
        p.name.toLowerCase().includes(term) ||
        p.id.toLowerCase().includes(term)
    );
    renderDropdownOptions(filtered);
    dropdownOptions.classList.add('show');
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('searchableDropdown');
    if (dropdown && !dropdown.contains(e.target)) {
        dropdownOptions.classList.remove('show');
    }
});

// ==========================================
// EXISTING LOGIC ADAPTED
// ==========================================

// Handle Scope Change
const offerScopeSelect = document.getElementById('offerScope');
const productSelectRow = document.getElementById('productSelectRow');
const categorySelectRow = document.getElementById('categorySelectRow');
const categorySelect = document.getElementById('categorySelect');

offerScopeSelect.addEventListener('change', function () {
    const scope = this.value;

    // Reset visibility
    productSelectRow.style.display = 'none';
    categorySelectRow.style.display = 'none';
    categorySelect.required = false;

    if (scope === 'product') {
        productSelectRow.style.display = 'flex';
        // Note: we can't set 'required' on a div, we handle validation on submit
    } else if (scope === 'category') {
        categorySelectRow.style.display = 'flex';
        categorySelect.required = true;
    }
});

// Set minimum end date based on start date
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');

startDateInput.addEventListener('change', function () {
    endDateInput.min = this.value;
    if (endDateInput.value && endDateInput.value < this.value) {
        endDateInput.value = this.value;
    }
});

// Set default start date to today
const today = new Date().toISOString().split('T')[0];
startDateInput.min = today;
startDateInput.value = today;

// // Form submission
// document.getElementById('offerForm').addEventListener('submit', function (e) {
//     e.preventDefault();

//     // Custom Validation for Product Scope
//     const scope = document.getElementById('offerScope').value;
//     if (scope === 'product' && selectedProductIds.size === 0) {
//         alert('Please select at least one product.');
//         return;
//     }

//     // Get form values
//     const formData = {
//         offerTitle: document.getElementById('offerTitle').value,
//         scope: scope,
//         selectedProducts: Array.from(selectedProductIds),
//         selectedCategory: document.getElementById('categorySelect').value,
//         discountPercentage: document.getElementById('discountPercentage').value,
//         startDate: document.getElementById('startDate').value,
//         endDate: document.getElementById('endDate').value,
//         status: document.getElementById('status').checked ? 'active' : 'inactive'
//     };

//     console.log('Form submitted:', formData);
//     alert('Offer saved successfully!');
// });

//SELECT 2 SCRIPT
// Initialize Select2 for type field
    $(document).ready(function () {
        $('#categorySelect').select2({
            placeholder: 'Select Type',
            allowClear: false,
            width: '100%',
            minimumResultsForSearch: 0,
            dropdownAutoWidth: false
        });

        // Make search input appear inside the field
        $('#categorySelect').on('select2:open', function () {
            $('.select2-search__field').attr('placeholder', 'Type to search...');
        });

        // Update Select2 styling when value changes
        $('#categorySelect').on('select2:select', function () {
            $(this).next('.select2-container').find('.select2-selection__rendered').css('color', '#1f2937');
        });

        // Set initial styling for Select2
        if ($('#categorySelect').val() === '' || $('#categorySelect').val() === null) {
            $('#categorySelect').next('.select2-container').find('.select2-selection__rendered').css('color', '#9ca3af');
        }
    });