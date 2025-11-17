// File upload handler
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const uploadArea = document.getElementById('variantUpload');
        uploadArea.innerHTML = `
<div style="color: #10b981; font-weight: 600; margin-bottom: 10px;">✓ Image selected: ${file.name}</div>
<button type="button" class="upload-btn"
    onclick="event.stopPropagation(); document.getElementById('variantImageInput').click()">Change Image</button>
`;
    }
}

// Drag and drop functionality
const uploadArea = document.getElementById('variantUpload');

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
        document.getElementById('variantImageInput').files = files;
        handleImageUpload({ target: { files: files } });
    }
});

// Form submission
document.getElementById('addVariantForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const isDefault = document.getElementById('defaultVariant').checked;

    // Get form values
    const variantData = {
        colorDisplay: formData.get('colorDisplay'),
        colorBase: formData.get('colorBase'),
        colorCode: formData.get('colorCode'),
        size: formData.get('size'),
        price: formData.get('price'),
        stockQuantity: formData.get('stockQuantity'),
        status: formData.get('status'),
        isDefault: isDefault
    };

    console.log('Variant Data:', variantData);
    alert('Variant added successfully!');
    // Add actual form submission logic here
    // window.location.href = 'view_variants.html';
});

// Color picker functionality
const colorPicker = document.getElementById('colorCode');
const colorValueDisplay = document.getElementById('colorValueDisplay');

colorPicker.addEventListener('input', (e) => {
    const selectedColor = e.target.value.toUpperCase();
    colorValueDisplay.value = selectedColor;
});