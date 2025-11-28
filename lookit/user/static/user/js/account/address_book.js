
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

// Sample data - in a real app, this would come from a server
let addresses = [
    {
        id: 1,
        fullName: 'John Doe',
        phoneNumber: '+1 (555) 123-4567',
        addressLine1: '123 Main Street, Apartment 4B',
        addressLine2: '',
        city: 'New York',
        state: 'NY',
        postalCode: '10001',
        country: 'US',
        label: 'home',
        customLabel: '',
        isDefault: true
    },
    {
        id: 2,
        fullName: 'John Doe',
        phoneNumber: '+1 (555) 987-6543',
        addressLine1: '456 Business Avenue, Floor 10',
        addressLine2: '',
        city: 'New York',
        state: 'NY',
        postalCode: '10022',
        country: 'US',
        label: 'work',
        customLabel: '',
        isDefault: false
    },
    {
        id: 3,
        fullName: 'John Doe (Parents)',
        phoneNumber: '+1 (555) 456-7890',
        addressLine1: '789 Family Street, House #12',
        addressLine2: '',
        city: 'Suburbia',
        state: 'NJ',
        postalCode: '07001',
        country: 'US',
        label: 'other',
        customLabel: "Parents' House",
        isDefault: false
    }
];

// Event Listeners
addAddressBtn.addEventListener('click', () => openModal());
closeModal.addEventListener('click', closeModalHandler);
cancelBtn.addEventListener('click', closeModalHandler);
addressForm.addEventListener('submit', handleFormSubmit);

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

// Event delegation for edit and delete buttons
addressGrid.addEventListener('click', (e) => {
    // Edit button
    if (e.target.closest('.edit-address')) {
        const addressId = parseInt(e.target.closest('.edit-address').dataset.id);
        const address = addresses.find(addr => addr.id === addressId);
        if (address) {
            openModal(address);
        }
    }
    
    // Delete button
    if (e.target.closest('.delete-address')) {
        if (confirm('Are you sure you want to delete this address?')) {
            const addressId = parseInt(e.target.closest('.delete-address').dataset.id);
            deleteAddress(addressId);
        }
    }
    
    // Set default button
    if (e.target.closest('.set-default')) {
        const addressId = parseInt(e.target.closest('.set-default').dataset.id);
        setDefaultAddress(addressId);
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

function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        id: addressIdInput.value ? parseInt(addressIdInput.value) : Date.now(),
        fullName: document.getElementById('fullName').value,
        phoneNumber: document.getElementById('phoneNumber').value,
        addressLine1: document.getElementById('addressLine1').value,
        addressLine2: document.getElementById('addressLine2').value,
        city: document.getElementById('city').value,
        state: document.getElementById('state').value,
        postalCode: document.getElementById('postalCode').value,
        country: document.getElementById('country').value,
        label: document.querySelector('input[name="addressLabel"]:checked').value,
        customLabel: document.querySelector('input[name="addressLabel"]:checked').value === 'other' 
            ? document.getElementById('customLabel').value 
            : '',
        isDefault: document.getElementById('setAsDefault').checked
    };
    
    // In a real app, you would save this to a server
    if (addressIdInput.value) {
        // Update existing address
        const index = addresses.findIndex(addr => addr.id === formData.id);
        if (index !== -1) {
            addresses[index] = formData;
        }
    } else {
        // Add new address
        addresses.push(formData);
    }
    
    // If this is set as default, update other addresses
    if (formData.isDefault) {
        setDefaultAddress(formData.id);
    }
    
    // Update the UI
    renderAddresses();
    
    // Close the modal
    closeModalHandler();
    
    // Show success message
    alert('Address saved successfully!');
}

function deleteAddress(id) {
    const address = addresses.find(addr => addr.id === id);
    if (!address) return;
    
    // Don't allow deleting the default address
    if (address.isDefault) {
        alert('Cannot delete the default address. Please set another address as default first.');
        return;
    }
    
    // In a real app, you would make an API call to delete from the server
    addresses = addresses.filter(addr => addr.id !== id);
    
    // Update the UI
    renderAddresses();
    
    // Show success message
    alert('Address deleted successfully!');
}

function setDefaultAddress(id) {
    // In a real app, you would make an API call to update on the server
    addresses = addresses.map(addr => ({
        ...addr,
        isDefault: addr.id === id
    }));
    
    // Update the UI
    renderAddresses();
}

function renderAddresses() {
    // Sort addresses with default first, then by ID
    const sortedAddresses = [...addresses].sort((a, b) => {
        if (a.isDefault) return -1;
        if (b.isDefault) return 1;
        return a.id - b.id;
    });
    
    // Clear the grid
    addressGrid.innerHTML = '';
    
    // Add each address to the grid
    sortedAddresses.forEach(address => {
        const addressCard = document.createElement('div');
        addressCard.className = `address-card ${address.isDefault ? 'default' : ''}`;
        
        const labelIcon = address.label === 'work' ? 'building' : 'home';
        const labelText = address.customLabel || 
            (address.label === 'home' ? 'Home' : 
                address.label === 'work' ? 'Work' : 'Address');
        
        addressCard.innerHTML = `
            <div class="address-card-header">
                <div class="address-card-title">
                    <i class="fas fa-${labelIcon}"></i>
                    <span>${labelText}</span>
                    ${address.isDefault ? '<span class="default-badge">Default</span>' : ''}
                </div>
                <div class="address-actions">
                    ${!address.isDefault ? `
                        <button class="address-action-btn set-default" data-id="${address.id}" 
                                title="Set as default">
                            <i class="fas fa-check-circle"></i>
                        </button>
                    ` : ''}
                    <button class="address-action-btn edit-address" data-id="${address.id}" 
                            title="Edit address">
                        <i class="far fa-edit"></i>
                    </button>
                    <button class="address-action-btn delete-address" data-id="${address.id}" 
                            title="Delete address" ${address.isDefault ? 'disabled' : ''}>
                        <i class="far fa-trash-alt"></i>
                    </button>
                </div>
            </div>
            <div class="address-details">
                <p>${address.fullName}</p>
                <p>${address.addressLine1}</p>
                ${address.addressLine2 ? `<p>${address.addressLine2}</p>` : ''}
                <p>${address.city}, ${address.state}, ${address.postalCode}</p>
                <p>${getCountryName(address.country)}</p>
                <p class="address-phone">
                    <i class="fas fa-phone-alt"></i> ${address.phoneNumber}
                </p>
            </div>
        `;
        
        addressGrid.appendChild(addressCard);
    });
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

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    renderAddresses();
});