const fileUpload = document.getElementById('fileUpload');
const fileInput = document.getElementById('productImages');
const uploadText = document.getElementById('uploadText');
const uploadIcon = document.getElementById('uploadIcon');

// Clicking the upload area triggers file input
fileUpload.addEventListener('click', () => fileInput.click());

// When user selects files
fileInput.addEventListener('change', function (e) {
  const files = e.target.files;

  // Restrict max 3 files
  if (files.length > 3) {
    alert('You can only upload a maximum of 3 images.');
    fileInput.value = ''; // Clear the input
    uploadIcon.className = 'fas fa-cloud-upload-alt'; // Reset icon
    uploadIcon.style.color = ''; // Reset color
    uploadText.textContent = 'Upload images to show the reason for return';
    return;
  }

  // Update UI based on selection
  if (files.length > 0) {
    uploadIcon.className = 'fas fa-check-circle';
    uploadIcon.style.color = '#4CAF50';
    uploadText.textContent = `${files.length} file(s) selected — click to change`;
  } else {
    uploadIcon.className = 'fas fa-cloud-upload-alt';
    uploadIcon.style.color = '';
    uploadText.textContent = 'Upload images to show the reason for return';
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


// //can upload only 3 images max
// const fileInput = document.getElementById('productImages');

// fileInput.addEventListener('change', function () {
//     if (this.files.length > 3) {
//         alert('You can only upload a maximum of 3 images.');
//         this.value = ''; // Clear selected files
//     }
// });
