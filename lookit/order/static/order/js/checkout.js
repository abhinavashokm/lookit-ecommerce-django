// Address selection
document.querySelectorAll('.address-option').forEach(option => {
    option.addEventListener('click', function(e) {
        // Don't trigger for buttons inside the address option
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            return;
        }
        
        document.querySelectorAll('.address-option').forEach(opt => {
            opt.classList.remove('selected');
        });
        this.classList.add('selected');
        const radio = this.querySelector('input[type="radio"]');
        if (radio) {
            radio.checked = true;
        }
    });
});


// Modal functionality
const modal = document.getElementById('addAddressModal');
const openModalBtn = document.querySelector('.add-address-btn');
const closeModalBtn = document.getElementById('closeAddModel');
const cancelBtn = document.getElementById('btn-outline');
const addressForm = document.getElementById('addressForm');

function openModal() {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = window.innerWidth - document.documentElement.clientWidth + 'px';
}

function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    addressForm.reset();
}

// Open modal when clicking add address button
openModalBtn.addEventListener('click', openModal);

// Close modal when clicking close button or cancel
closeModalBtn.addEventListener('click', closeModal);
cancelBtn.addEventListener('click', closeModal);

let editModal = null
let closeEditModalBtn = null
let cancelEditBtn = null
let editAddressForm = null

function openEditModal(address_id) {
    editModal = document.getElementById('editAddressModal'+address_id);
    editAddressForm = document.getElementById('addressForm'+address_id);

    editModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = window.innerWidth - document.documentElement.clientWidth + 'px';
}

function closeEditModal() {
    editModal.classList.remove('active');
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    editAddressForm.reset();
}


// Close modal when clicking outside the modal content
modal.addEventListener('click', function(e) {
    if (e.target === modal) {
        closeModal();
    }
});


