       /* ============================================
           INITIALIZE UI ON PAGE LOAD
           ============================================ */
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize clear button visibility based on search input value
            const searchInput = document.getElementById('searchInput');
            const clearBtn = document.getElementById('clearBtn');
            if (searchInput && clearBtn) {
                // Show/hide clear button based on input value
                if (searchInput.value.trim().length > 0) {
                    clearBtn.classList.add('show');
                } else {
                    clearBtn.classList.remove('show');
                }
            }
        });

        /* ============================================
           SEARCH FUNCTIONALITY
           ============================================ */
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');
        const clearBtn = document.getElementById('clearBtn');

        // Update clear button visibility based on input value
        searchInput.addEventListener('input', () => {
            if (searchInput.value.trim().length > 0) {
                clearBtn.classList.add('show');
            } else {
                clearBtn.classList.remove('show');
            }
        });

        // Clear search function - just clears the input field
        function clearSearch() {
            searchInput.value = '';
            clearBtn.classList.remove('show');
            searchInput.focus();
        }

        // Escape key to clear search
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && searchInput.value.trim().length > 0) {
                clearSearch();
            }
        });

        // Action functions
        function addNewStyle() {
            alert('Add New Style');
            // Add navigation to add style page
        }

        function editStyle(styleId) {
            alert(`Edit style ID: ${styleId}`);
            // Add navigation to edit style page
        }

        // Modal functionality
        let currentStyleId = null;

        // Delete Modal Functions
        function openDeleteModal(styleId) {
            currentStyleId = styleId;
            const modal = document.getElementById('deleteModal');
            const styleIdElement = document.getElementById('deleteStyleId');
            styleIdElement.textContent = `STY-${String(styleId).padStart(3, '0')}`;
            modal.classList.add('show');
        }

        function closeDeleteModal() {
            const modal = document.getElementById('deleteModal');
            modal.classList.remove('show');
            currentStyleId = null;
        }

        function confirmDelete() {
            if (currentStyleId) {
                alert(`Style STY-${String(currentStyleId).padStart(3, '0')} deleted successfully!`);
                closeDeleteModal();
                // Add actual delete logic here
                // Example: fetch(`/api/styles/${currentStyleId}`, { method: 'DELETE' })
            }
        }

        // Restore Modal Functions
        function openRestoreModal(styleId) {
            currentStyleId = styleId;
            const modal = document.getElementById('restoreModal');
            const styleIdElement = document.getElementById('restoreStyleId');
            styleIdElement.textContent = `STY-${String(styleId).padStart(3, '0')}`;
            modal.classList.add('show');
        }

        function closeRestoreModal() {
            const modal = document.getElementById('restoreModal');
            modal.classList.remove('show');
            currentStyleId = null;
        }

        function confirmRestore() {
            if (currentStyleId) {
                alert(`Style STY-${String(currentStyleId).padStart(3, '0')} restored successfully!`);
                closeRestoreModal();
                // Add actual restore logic here
                // Example: fetch(`/api/styles/${currentStyleId}/restore`, { method: 'POST' })
            }
        }

        // Close modal when clicking overlay
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-overlay')) {
                closeDeleteModal();
                closeRestoreModal();
            }
        });

        // Close modal with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeDeleteModal();
                closeRestoreModal();
            }
        });