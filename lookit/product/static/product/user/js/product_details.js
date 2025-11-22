
// Image change functionality
const images = [
    '<div style="width: 100%; height: 100%; background: linear-gradient(135deg, #ff6b6b, #ff8e53, #333); display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">Abstract Art Design</div>',
    '<div style="width: 100%; height: 100%; background: linear-gradient(135deg, #4ecdc4, #ff8e53, #f5e6d3); display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold;">Geometric Design</div>'
];

let currentImageIndex = 0;

function changeImage(index) {
    currentImageIndex = index;
    const mainImage = document.getElementById('mainImage');
    mainImage.innerHTML = images[index];

    // Update active thumbnail
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach((thumb, i) => {
        if (i === index) {
            thumb.classList.add('active');
        } else {
            thumb.classList.remove('active');
        }
    });

    // Update modal image if modal is open
    const modal = document.getElementById('imageModal');
    if (modal && modal.classList.contains('active')) {
        updateModalImage();
    }
}

// Modal functionality
function openImageModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.add('active');
    updateModalImage();
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.remove('active');
    document.body.style.overflow = ''; // Restore scrolling
}

function closeImageModalOnBackdrop(event) {
    // Close modal if clicking on the backdrop (not on the image or its children)
    if (event.target.id === 'imageModal') {
        closeImageModal();
    }
}

// Prevent modal from closing when clicking on the image
document.addEventListener('DOMContentLoaded', function () {
    const modalImage = document.getElementById('modalImage');
    if (modalImage) {
        modalImage.addEventListener('click', function (event) {
            event.stopPropagation();
        });
    }
});

function updateModalImage() {
    const modalImageContent = document.getElementById('modalImageContent');
    if (modalImageContent) {
        modalImageContent.innerHTML = images[currentImageIndex];
    }
}

function changeModalImage(direction) {
    currentImageIndex += direction;

    // Loop around
    if (currentImageIndex < 0) {
        currentImageIndex = images.length - 1;
    } else if (currentImageIndex >= images.length) {
        currentImageIndex = 0;
    }

    // Update main image and thumbnails
    changeImage(currentImageIndex);
}

// Keyboard navigation for modal
document.addEventListener('keydown', function (event) {
    const modal = document.getElementById('imageModal');
    if (modal && modal.classList.contains('active')) {
        if (event.key === 'Escape') {
            closeImageModal();
        } else if (event.key === 'ArrowLeft') {
            changeModalImage(-1);
        } else if (event.key === 'ArrowRight') {
            changeModalImage(1);
        }
    }
});

// Size selection
function selectSize(btn) {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

// Like functionality
function toggleLike(button) {
    const likeCount = button.querySelector('.like-count');
    const isLiked = button.classList.contains('liked');

    if (isLiked) {
        button.classList.remove('liked');
        const currentCount = parseInt(likeCount.textContent);
        likeCount.textContent = currentCount - 1;
    } else {
        button.classList.add('liked');
        const currentCount = parseInt(likeCount.textContent);
        likeCount.textContent = currentCount + 1;
    }
}

// Quantity functionality
function increaseQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    let currentValue = parseInt(quantityInput.value);
    if (currentValue < 10) {
        quantityInput.value = currentValue + 1;
    }
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantityInput');
    let currentValue = parseInt(quantityInput.value);
    if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
}