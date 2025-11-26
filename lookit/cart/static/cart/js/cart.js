
// Quantity controls
document.querySelectorAll('.quantity-btn').forEach(button => {
    button.addEventListener('click', function() {
        const quantityElement = this.parentElement.querySelector('.quantity');
        let quantity = parseInt(quantityElement.textContent);
        
        if (this.textContent === '+' && quantity < 10) {
            quantityElement.textContent = quantity + 1;
        } else if (this.textContent === '-' && quantity > 1) {
            quantityElement.textContent = quantity - 1;
        }
        
        updateCartTotal();
    });
});

// Remove item
document.querySelectorAll('.remove-btn').forEach(button => {
    button.addEventListener('click', function() {
        this.closest('.cart-item').remove();
        updateCartTotal();
    });
});

// Update cart total
function updateCartTotal() {
    let subtotal = 0;
    
    document.querySelectorAll('.cart-item').forEach(item => {
        const price = parseFloat(item.querySelector('.item-price').textContent.replace('$', ''));
        const quantity = parseInt(item.querySelector('.quantity').textContent);
        subtotal += price * quantity;
    });
    
    const tax = subtotal * 0.08; // 8% tax
    const total = subtotal + tax;
    
    document.querySelector('.summary-row:nth-child(2) span:last-child').textContent = `$${subtotal.toFixed(2)}`;
    document.querySelector('.summary-row:nth-child(4) span:last-child').textContent = `$${tax.toFixed(2)}`;
    document.querySelector('.summary-total span:last-child').textContent = `$${total.toFixed(2)}`;
}

// Toggle Coupon Section
const toggleCouponBtn = document.getElementById('toggleCouponBtn');
const couponSection = document.getElementById('couponSection');

if (toggleCouponBtn) {
    toggleCouponBtn.addEventListener('click', () => {
        couponSection.style.display = couponSection.style.display === 'none' ? 'block' : 'none';
        toggleCouponBtn.classList.toggle('active');
    });
}

// Coupon functionality
const couponInput = document.getElementById('couponCode');
const applyCouponBtn = document.getElementById('applyCouponBtn');
const couponMessage = document.getElementById('couponMessage');
let appliedCoupon = null;

// Function to apply coupon
function applyCoupon(code, discount) {
    const validCoupons = ['WELCOME10', 'FREESHIP', 'SUMMER25'];
    
    if (!validCoupons.includes(code)) {
        showCouponMessage('Invalid coupon code', 'error');
        return false;
    }
    
    if (appliedCoupon && appliedCoupon.code === code) {
        showCouponMessage('This coupon is already applied', 'error');
        return false;
    }
    
    appliedCoupon = { code, discount };
    
    // Show applied coupon in the summary
    const appliedCouponRow = document.getElementById('appliedCouponRow');
    const appliedCouponCode = document.getElementById('appliedCouponCode');
    const appliedCouponDiscount = document.getElementById('appliedCouponDiscount');
    
    appliedCouponCode.textContent = code;
    appliedCouponDiscount.textContent = discount;
    appliedCouponRow.style.display = 'flex';
    
    updateOrderSummaryWithCoupon(discount);
    highlightAppliedCoupon(code);
    showCouponMessage(`Coupon ${code} applied successfully!`, 'success');
    return true;
}

// Function to remove coupon
function removeCoupon() {
    if (!appliedCoupon) return;
    
    const couponCode = appliedCoupon.code;
    appliedCoupon = null;
    
    // Hide applied coupon row
    document.getElementById('appliedCouponRow').style.display = 'none';
    
    updateOrderSummaryWithCoupon(0);
    removeCouponHighlight(couponCode);
    showCouponMessage('Coupon removed', 'success');
    couponInput.value = '';
}



// Function to show coupon message
function showCouponMessage(message, type = '') {
    couponMessage.textContent = message;
    couponMessage.className = 'coupon-message ' + (type ? type : '');
}

// Function to highlight applied coupon
function highlightAppliedCoupon(code) {
    document.querySelectorAll('.coupon-item').forEach(item => {
        if (item.dataset.code === code) {
            item.classList.add('applied-coupon');
            const applyBtn = item.querySelector('.apply-coupon-btn');
            applyBtn.textContent = 'Applied';
            applyBtn.disabled = true;
        }
    });
}

// Function to remove coupon highlight
function removeCouponHighlight(code) {
    const couponItem = document.querySelector(`.coupon-item[data-code="${code}"]`);
    if (couponItem) {
        couponItem.classList.remove('applied-coupon');
        const applyBtn = couponItem.querySelector('.apply-coupon-btn');
        applyBtn.textContent = 'Apply';
        applyBtn.disabled = false;
    }
}

// Event listeners for coupon buttons
document.querySelectorAll('.coupon-item .apply-coupon-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const couponItem = this.closest('.coupon-item');
        const code = couponItem.dataset.code;
        const discount = couponItem.dataset.discount;
        
        if (appliedCoupon) {
            if (confirm('Remove current coupon and apply this one instead?')) {
                const discountRow = document.querySelector('.discount-row');
                if (discountRow) discountRow.remove();
                
                if (appliedCoupon) {
                    removeCouponHighlight(appliedCoupon.code);
                }
                
                applyCoupon(code, discount);
            }
        } else {
            applyCoupon(code, discount);
        }
    });
});

// Apply coupon when clicking the apply button
applyCouponBtn.addEventListener('click', () => {
    const code = couponInput.value.trim().toUpperCase();
    if (!code) {
        showCouponMessage('Please enter a coupon code', 'error');
        return;
    }
    
    const couponDiscounts = {
        'WELCOME10': 10,
        'FREESHIP': 5,
        'SUMMER25': 25
    };
    
    if (couponDiscounts[code]) {
        applyCoupon(code, couponDiscounts[code]);
    } else {
        showCouponMessage('Invalid coupon code', 'error');
    }
});

// Allow pressing Enter in the coupon input
couponInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        applyCouponBtn.click();
    }
});
