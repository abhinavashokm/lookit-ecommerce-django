
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

// Remove address
document.querySelectorAll('.remove-address').forEach(button => {
    button.addEventListener('click', function(e) {
        e.stopPropagation();
        if (confirm('Are you sure you want to remove this address?')) {
            const addressOption = this.closest('.address-option');
            addressOption.style.opacity = '0';
            setTimeout(() => {
                addressOption.remove();
            }, 300);
        }
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

// Handle form submission
addressForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = {
        fullName: document.getElementById('fullName').value,
        phone: document.getElementById('phone').value,
        altPhone: document.getElementById('altPhone').value,
        address: document.getElementById('address').value,
        city: document.getElementById('city').value,
        zipCode: document.getElementById('zipCode').value,
        state: document.getElementById('state').value,
        addressType: document.getElementById('addressType').value,
        isDefault: document.getElementById('defaultAddress').checked
    };

    // Here you would typically send this data to your backend
    console.log('Form submitted:', formData);
    
    // For demo purposes, just close the modal
    closeModal();
    
    // Show success message with animation
    const successMsg = document.createElement('div');
    successMsg.className = 'success-message';
    successMsg.innerHTML = '<i class="fas fa-check-circle"></i> Address saved successfully!';
    document.body.appendChild(successMsg);
    
    // Animate in
    setTimeout(() => {
        successMsg.style.opacity = '1';
        successMsg.style.transform = 'translateY(0)';
    }, 10);
    
    // Remove after animation
    setTimeout(() => {
        successMsg.style.opacity = '0';
        successMsg.style.transform = 'translateY(20px)';
        setTimeout(() => {
            successMsg.remove();
        }, 300);
    }, 3000);
});

// Add success message styles
const style = document.createElement('style');
style.textContent = `
    .success-message {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        background: #4CAF50;
        color: white;
        padding: 12px 24px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.95rem;
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 1100;
    }
    
    .success-message i {
        font-size: 1.1em;
    }
`;
document.head.appendChild(style);

// Continue to payment
document.querySelector('.checkout-btn').addEventListener('click', function() {
    // In a real app, this would navigate to the payment page
    alert('Proceeding to payment');
});
