
// Photo Upload Functionality
document.addEventListener('DOMContentLoaded', function () {
    const profileImage = document.getElementById('profileImage');
    const profileImageInput = document.getElementById('profileImageInput');
    const changePhotoBtn = document.getElementById('changePhotoBtn');
    const imageUploadOverlay = document.getElementById('imageUploadOverlay');

    // Function to handle file selection
    function handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        // Check if the file is an image
        if (!file.type.match('image.*')) {
            alert('Please select a valid image file (JPEG, PNG, etc.)');
            return;
        }

        // Check file size (max 2MB)
        if (file.size > 2 * 1024 * 1024) {
            alert('Image size should be less than 2MB');
            return;
        }

        // Create a FileReader to read the image file
        const reader = new FileReader();

        reader.onload = function (e) {
            // Set the source of the profile image to the selected file
            profileImage.src = e.target.result;

            // Here you would typically upload the image to your server
            // For example:
            // uploadImageToServer(file);
        };

        // Read the image file as a data URL
        reader.readAsDataURL(file);
    }

    // Click event for the change photo button
    if (changePhotoBtn) {
        changePhotoBtn.addEventListener('click', function () {
            profileImageInput.click();
        });
    }

    // Click event for the image container (for the overlay)
    if (imageUploadOverlay) {
        imageUploadOverlay.addEventListener('click', function () {
            profileImageInput.click();
        });
    }

    // Change event for the file input
    if (profileImageInput) {
        profileImageInput.addEventListener('change', handleFileSelect);
    }
});

// Copy referral code functionality
const copyBtn = document.querySelector('.action-icon-btn[title="Copy"]');
if (copyBtn) {
    copyBtn.addEventListener('click', function () {
        const referralCode = document.querySelector('.referral-code').textContent;
        navigator.clipboard.writeText(referralCode).then(function () {
            // Visual feedback
            const originalSvg = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>';
            setTimeout(function () {
                copyBtn.innerHTML = originalSvg;
            }, 2000);
        });
    });
}



// Password Change Modal Functionality
document.addEventListener('DOMContentLoaded', function () {
    // Modal elements
    const modal = document.getElementById('passwordModal');
    const openModalBtn = document.querySelector('.change-password-btn');
    const closeModalBtns = document.querySelectorAll('.close-modal, .modal-overlay');
    const form = document.getElementById('changePasswordForm');
    const newPasswordInput = document.getElementById('newPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const passwordMatch = document.getElementById('passwordMatch');
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');

    // Toggle password visibility
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const input = this.previousElementSibling;
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    });


    // Event listeners
    if (openModalBtn) {
        openModalBtn.addEventListener('click', function (e) {
           // e.preventDefault();
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    }

    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (e.target === this || e.target.classList.contains('close-modal')) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
                form.reset();
                passwordMatch.textContent = '';
                passwordMatch.className = 'password-match';

                // Reset password visibility
                document.querySelectorAll('.toggle-password i').forEach(icon => {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                });
                document.querySelectorAll('.password-input input').forEach(input => {
                    input.type = 'password';
                });
            }
        });
    });

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
            form.reset();
            passwordMatch.textContent = '';
            passwordMatch.className = 'password-match';
        }
    });


});



// OTP Verification Functionality
document.addEventListener('DOMContentLoaded', function () {
    const otpModal = document.getElementById('otpModal');
    const otpInputs = document.querySelectorAll('.otp-input');
    const verifyOtpBtn = document.getElementById('verifyOtpBtn');
    const resendOtpBtn = document.getElementById('resendOtp');
    const countdownElement = document.getElementById('countdown');
    const closeModalBtns = document.querySelectorAll('.close-modal');
    const saveChangesBtn = document.querySelector('.save-changes-btn');

    let countdown = 30;
    let countdownInterval;

    // Start the countdown timer
    function startCountdown() {
        countdown = 30;
        countdownElement.textContent = countdown;
        resendOtpBtn.disabled = true;

        clearInterval(countdownInterval);
        countdownInterval = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;

            if (countdown <= 0) {
                clearInterval(countdownInterval);
                resendOtpBtn.disabled = false;
            }
        }, 1000);
    }

    // Handle OTP input
    otpInputs.forEach((input, index) => {
        // Focus on the first input when modal opens
        if (index === 0) {
            input.focus();
        }

        // Move to next input on number input
        input.addEventListener('input', (e) => {
            if (e.target.value && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        // Handle backspace
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });

    // Verify OTP
    verifyOtpBtn.addEventListener('click', () => {
        const otp = Array.from(otpInputs).map(input => input.value).join('');

        if (otp.length !== 6) {
            alert('Please enter a valid 6-digit OTP');
            return;
        }

        // Here you would verify the OTP with your backend
        console.log('Verifying OTP:', otp);

        // Simulate API call
        verifyOtpBtn.disabled = true;
        verifyOtpBtn.textContent = 'Verifying...';

        // In a real application, you would verify the OTP with your backend here
        // For this example, we'll simulate a successful verification
        setTimeout(() => {
            // Simulate successful verification
            alert('Email verified successfully! Your changes have been saved.');
            otpModal.classList.remove('active');
            document.body.style.overflow = '';
            resetOtpForm();

            // Submit the form with the stored form data
            if (editProfileForm && formData) {
                // In a real application, you would send the form data to your server
                console.log('Submitting form with data:', Object.fromEntries(formData));
                // Uncomment the line below to actually submit the form
                // editProfileForm.submit();

                // For demo purposes, show the form data in the console
                const formDataObj = {};
                formData.forEach((value, key) => {
                    formDataObj[key] = value;
                });
                console.log('Form data:', formDataObj);

                // Show success message
                alert('Profile updated successfully!');
            }
        }, 1500);
    });

    // Resend OTP
    resendOtpBtn.addEventListener('click', () => {
        // Here you would typically resend the OTP via your backend
        console.log('Resending OTP...');
        startCountdown();
        alert('A new verification code has been sent to your email.');
    });

    // Close modal
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (e.target === this || e.target.classList.contains('close-modal')) {
                otpModal.classList.remove('active');
                document.body.style.overflow = '';
                resetOtpForm();
            }
        });
    });

    // Reset OTP form
    function resetOtpForm() {
        otpInputs.forEach(input => {
            input.value = '';
        });
        if (otpInputs.length > 0) {
            otpInputs[0].focus();
        }
        verifyOtpBtn.disabled = false;
        verifyOtpBtn.textContent = 'Verify & Save Changes';
        clearInterval(countdownInterval);
        resendOtpBtn.disabled = true;
        countdownElement.textContent = '30';
    }

    // Show OTP modal when save changes is clicked
    const editProfileForm = document.querySelector('.edit-profile-form');
    let formData = null;

});
