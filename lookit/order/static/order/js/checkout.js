
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

// Edit address
document.querySelectorAll('.edit-address').forEach(button => {
    button.addEventListener('click', function(e) {
        e.stopPropagation();
        const addressId = this.getAttribute('data-address-id');
        // In a real app, this would open an edit modal or navigate to an edit page
        alert(`Edit address with ID: ${addressId}`);
    });
});

// Modal functionality
const modal = document.getElementById('addAddressModal');
const openModalBtn = document.querySelector('.add-address-btn');
const closeModalBtn = document.querySelector('.close-modal');
const cancelBtn = document.querySelector('.btn-outline');
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

// Close modal when clicking outside the modal content
modal.addEventListener('click', function(e) {
    if (e.target === modal) {
        closeModal();
    }
});


