
// Handle file upload UI
document.getElementById('fileUpload').addEventListener('click', function () {
    document.getElementById('productImages').click();
});

document.getElementById('productImages').addEventListener('change', function (e) {
    const files = e.target.files;
    if (files.length > 0) {
        const fileUpload = document.getElementById('fileUpload');
        fileUpload.innerHTML = `
            <i class="fas fa-check-circle" style="color: #4CAF50;"></i>
            <p>${files.length} file(s) selected</p>
            <small>Click to change</small>
        `;
    }
});

// Handle address card selection
document.querySelectorAll('.address-card').forEach(card => {
    card.addEventListener('click', function (e) {
        // Don't uncheck if clicking on the radio button directly
        if (e.target.tagName !== 'INPUT') {
            const radio = this.querySelector('input[type="radio"]');
            radio.checked = true;
            // Remove selected class from all cards and add to this one
            document.querySelectorAll('.address-card').forEach(c => {
                c.classList.remove('selected-address');
            });
            this.classList.add('selected-address');
        }
    });
});

// // Add click handler for the "Add New Address" button
// document.querySelector('.add-address-btn')?.addEventListener('click', function () {
//     // Here you could open a modal or navigate to an address addition page
//     alert('Add new address functionality would open here');
//     // Example: window.location.href = '/add-address?returnTo=return';
// });

// // Form submission
// document.getElementById('returnForm').addEventListener('submit', function (e) {
//     e.preventDefault();
//     // Get the selected address
//     const selectedAddress = document.querySelector('input[name="pickupAddress"]:checked');
//     if (!selectedAddress) {
//         alert('Please select a pickup address');
//         return;
//     }

//     // Here you would typically collect all form data and submit it
//     const formData = {
//         returnReason: document.getElementById('returnReason').value,
//         comments: document.getElementById('comments').value,
//         pickupAddress: selectedAddress.value,
//         refundMode: document.getElementById('refundMode').value,
//         // Add other form fields as needed
//     };

//     console.log('Form data:', formData);
//     alert('Your return request has been submitted successfully!');
//     // window.location.href = 'return-confirmation.html';
// });
