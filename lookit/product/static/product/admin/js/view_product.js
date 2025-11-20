// Delete Modal Functions
function openDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.add('show');
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('show');
}

function confirmDelete() {
    alert('Product deleted successfully!');
    closeDeleteModal();
    // Add actual delete logic here
    // window.location.href = 'product_management.html';
}

// Close modal when clicking overlay
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        closeDeleteModal();
    }
});