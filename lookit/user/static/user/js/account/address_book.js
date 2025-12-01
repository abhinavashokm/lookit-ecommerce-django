
// DOM Elements
const addAddressBtn = document.getElementById('addAddressBtn');
const addressModal = document.getElementById('addressModal');
const closeModal = document.getElementById('closeModal');
const cancelBtn = document.getElementById('cancelBtn');
const addressForm = document.getElementById('addressForm');
const modalTitle = document.getElementById('modalTitle');
const addressIdInput = document.getElementById('addressId');
const addressGrid = document.getElementById('addressGrid');
const addressLabels = document.querySelectorAll('input[name="addressLabel"]');
const customLabelContainer = document.querySelector('.custom-label');


// Event Listeners
addAddressBtn.addEventListener('click', () => openModal());
closeModal.addEventListener('click', closeModalHandler);
cancelBtn.addEventListener('click', closeModalHandler);

// Toggle custom label input when 'Other' is selected
addressLabels.forEach(radio => {
    radio.addEventListener('change', (e) => {
        if (e.target.value === 'other') {
            customLabelContainer.style.display = 'block';
        } else {
            customLabelContainer.style.display = 'none';
        }
    });
});

// Close modal when clicking outside the modal content
window.addEventListener('click', (e) => {
    if (e.target === addressModal) {
        closeModalHandler();
    }
});

// Functions
function openModal(address = null) {
    if (address) {
        // Edit mode
        modalTitle.textContent = 'Edit Address';
        addressIdInput.value = address.id;
        document.getElementById('fullName').value = address.fullName;
        document.getElementById('phoneNumber').value = address.phoneNumber;
        document.getElementById('addressLine1').value = address.addressLine1;
        document.getElementById('addressLine2').value = address.addressLine2 || '';
        document.getElementById('city').value = address.city;
        document.getElementById('state').value = address.state;
        document.getElementById('postalCode').value = address.postalCode;
        document.getElementById('country').value = address.country;
        
        // Set the address label
        const label = address.customLabel ? 'other' : address.label;
        document.querySelector(`input[name="addressLabel"][value="${label}"]`).checked = true;
        
        // Show custom label if needed
        if (address.customLabel) {
            customLabelContainer.style.display = 'block';
            document.getElementById('customLabel').value = address.customLabel;
        } else {
            customLabelContainer.style.display = 'none';
        }
        
        // Set default checkbox
        document.getElementById('setAsDefault').checked = address.isDefault;
    } else {
        // Add new mode
        modalTitle.textContent = 'Add New Address';
        addressForm.reset();
        addressIdInput.value = '';
        customLabelContainer.style.display = 'none';
        document.getElementById('setAsDefault').checked = false;
    }
    
    addressModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModalHandler() {
    addressModal.style.display = 'none';
    document.body.style.overflow = 'auto';
    addressForm.reset();
}

function getCountryName(countryCode) {
    const countries = {
        'US': 'United States',
        'CA': 'Canada',
        'UK': 'United Kingdom',
        'AU': 'Australia',
        'IN': 'India',
        'JP': 'Japan',
        'DE': 'Germany',
        'FR': 'France',
        'BR': 'Brazil',
        'CN': 'China'
    };
    return countries[countryCode] || countryCode;
}


// ==============================
// Delete Modal Functions
// ==============================
let currentStyleId = null;

function openDeleteModal(address_id) {
    console.log("call is here")
    console.log(address_id)
    const modal = document.getElementById('deleteModal'+address_id);
    if (modal) modal.classList.add('show');
}

function closeDeleteModal(address_id) {
    const modal = document.getElementById('deleteModal'+address_id);
    if (modal) modal.classList.remove('show');
}

// Optional: Close modal when clicking on overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        if (currentStyleId) closeDeleteModal(currentStyleId);
    }
});

// Optional: Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && currentStyleId) {
        closeDeleteModal(currentStyleId);
    }
});

