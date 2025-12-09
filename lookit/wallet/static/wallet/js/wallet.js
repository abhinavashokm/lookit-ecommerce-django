
// Add Money Modal
const addMoneyBtn = document.querySelector('.add-money-btn');
const addMoneyModal = document.getElementById('addMoneyModal');
const closeModalBtn = document.getElementById('closeModal');
const amountInput = document.getElementById('amountInput');
const amountOptions = document.querySelectorAll('.amount-option');
const proceedToPayBtn = document.getElementById('proceedToPayBtn');

// Open modal when Add Money button is clicked
if (addMoneyBtn) {
    addMoneyBtn.addEventListener('click', () => {
        addMoneyModal.classList.add('active');
        document.body.style.overflow = 'hidden';
        setTimeout(() => amountInput.focus(), 100);
    });
}

// Close modal functions
function closeModal() {
    addMoneyModal.classList.remove('active');
    document.body.style.overflow = '';
}

if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);

// Close modal when clicking outside the modal content
addMoneyModal.addEventListener('click', (e) => {
    if (e.target === addMoneyModal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && addMoneyModal.classList.contains('active')) {
        closeModal();
    }
});

// Handle amount selection from quick options
amountOptions.forEach(option => {
    option.addEventListener('click', () => {
        const amount = option.textContent.replace('₹', '').trim();
        amountInput.value = amount;
        validateAmount();
    });
});

// Validate amount input
function validateAmount() {
    const amount = parseFloat(amountInput.value);
    if (amount && amount > 0) {
        addMoneySubmitBtn.disabled = false;
    } else {
        addMoneySubmitBtn.disabled = true;
    }
}

// Add input validation
if (amountInput) {
    amountInput.addEventListener('input', validateAmount);

    // Prevent negative numbers
    amountInput.addEventListener('keydown', (e) => {
        if (e.key === '-' || e.key === 'e' || e.key === 'E') {
            e.preventDefault();
        }
    });
}

// Handle form submission
if (proceedToPayBtn) {
    proceedToPayBtn.addEventListener('click', () => {
        const amount = parseFloat(amountInput.value);

        if (amount && amount > 0) {
            // Here you would typically handle the payment processing
            console.log(`Proceeding to pay ₹${amount}`);

            // Show success message (you can replace this with actual payment processing)
            alert(`Proceeding to payment of ₹${amount}`);

            // Close the modal after a short delay
            setTimeout(closeModal, 1000);
        }
    });
}
