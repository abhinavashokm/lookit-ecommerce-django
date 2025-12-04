
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
function openModal() {
    addressModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModalHandler() {
    addressModal.style.display = 'none';
    document.body.style.overflow = 'auto';
    addressForm.reset();
}

function openEditAddressModal(address_id){
    const editAddressModal = document.getElementById('editAddressModal'+address_id);
    editAddressModal.style.display = 'block'
    document.body.style.overflow = 'hidden';
}

function closeEditAddressModal(address_id){
    const editAddressModal = document.getElementById('editAddressModal'+address_id);
    editAddressModal.style.display = 'none'
    document.body.style.overflow = 'auto';
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

