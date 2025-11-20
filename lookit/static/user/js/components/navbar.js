// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const nav = document.querySelector('nav');

if (mobileMenuBtn && mobileMenu) {
    // Toggle menu on button click
    mobileMenuBtn.addEventListener('click', function () {
        mobileMenu.classList.toggle('active');
        // Change icon when menu is open
        if (mobileMenu.classList.contains('active')) {
            mobileMenuBtn.textContent = '✕';
        } else {
            mobileMenuBtn.textContent = '☰';
        }
    });

    // Close menu when clicking on a link
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function () {
            mobileMenu.classList.remove('active');
            mobileMenuBtn.textContent = '☰';
        });
    });

    // Close menu when clicking outside
    if (nav) {
        document.addEventListener('click', function (event) {
            if (!nav.contains(event.target) && mobileMenu.classList.contains('active')) {
                mobileMenu.classList.remove('active');
                mobileMenuBtn.textContent = '☰';
            }
        });
    }
}