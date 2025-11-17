// ============================================
// MAIN CONTENT FUNCTIONALITY
// ============================================

// File upload handlers
function handleThumbnailUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const uploadArea = document.getElementById('thumbnailUpload');
        uploadArea.innerHTML = `
                    <div style="color: #10b981; font-weight: 600; margin-bottom: 10px;">✓ Image selected: ${file.name}</div>
                    <button type="button" class="upload-btn" onclick="event.stopPropagation(); document.getElementById('thumbnailInput').click()">Change Image</button>
                `;
    }
}

function handleAdditionalUpload(event) {
    const files = event.target.files;
    if (files.length > 0) {
        const uploadArea = document.getElementById('additionalUpload');
        const fileNames = Array.from(files).map(f => f.name).join(', ');
        uploadArea.innerHTML = `
                    <div style="color: #10b981; font-weight: 600; margin-bottom: 10px;">✓ ${files.length} image(s) selected</div>
                    <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 10px;">${fileNames}</div>
                    <button type="button" class="upload-btn" onclick="event.stopPropagation(); document.getElementById('additionalInput').click()">Change Images</button>
                `;
    }
}

// Drag and drop functionality
['thumbnailUpload', 'additionalUpload'].forEach(id => {
    const uploadArea = document.getElementById(id);

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            if (id === 'thumbnailUpload') {
                document.getElementById('thumbnailInput').files = files;
                handleThumbnailUpload({ target: { files: files } });
            } else {
                document.getElementById('additionalInput').files = files;
                handleAdditionalUpload({ target: { files: files } });
            }
        }
    });
});

// Form submission
document.getElementById('addProductForm').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Product saved successfully!');
    // Add actual form submission logic here
    // window.location.href = 'product_management.html';
});