
// Show selected tab content
function showTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab content
    document.getElementById(tabId).classList.add('active');
    
    // Add active class to clicked tab
    event.currentTarget.classList.add('active');
}

// Format card number with spaces
function formatCardNumber(input) {
    // Remove all non-digit characters
    let value = input.value.replace(/\D/g, '');
    
    // Add space after every 4 digits
    value = value.replace(/(\d{4})(?=\d)/g, '$1 ');
    
    // Update input value
    input.value = value.trim();
}

// Format expiry date with slash
function formatExpiryDate(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length > 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    
    input.value = value;
}

// Handle form submission
document.getElementById('cardForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Here you would typically validate the form and process the payment
    alert('Processing your payment...');
    // In a real application, you would make an API call to your payment processor here
});

// Handle Cash on Delivery order
function placeCODOrder() {
    alert('Your order has been placed successfully! You will pay ₹839 at the time of delivery.');
    // In a real application, you would submit the order to your backend here
}
