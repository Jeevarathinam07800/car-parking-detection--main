// Global variables
let currentImageData = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadParkingSpaces();
});

// Setup event listeners
function setupEventListeners() {
    // File upload handling
    const imageInput = document.getElementById('imageInput');
    const uploadArea = document.getElementById('uploadArea');
    
    imageInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => imageInput.click());
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        uploadImage(file);
    }
}

// Handle drag over
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('dragover');
}

// Handle drag leave
function handleDragLeave(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
}

// Handle file drop
function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        uploadImage(files[0]);
    }
}

// Upload image file
function uploadImage(file) {
    if (!file.type.startsWith('image/')) {
        showMessage('Please select a valid image file.', 'error');
        return;
    }
    
    // Show upload progress
    showUploadProgress(true);
    
    // Read file as base64
    const reader = new FileReader();
    reader.onload = function(e) {
        currentImageData = e.target.result.split(',')[1]; // Remove data:image/...;base64, prefix
        
        // Update image info
        updateImageInfo(file);
        showUploadProgress(false);
        showMessage('Image uploaded successfully!', 'success');
    };
    
    reader.onerror = function() {
        showUploadProgress(false);
        showMessage('Failed to read image file.', 'error');
    };
    
    reader.readAsDataURL(file);
}

// Show/hide upload progress
function showUploadProgress(show) {
    const uploadArea = document.getElementById('uploadArea');
    const uploadProgress = document.getElementById('uploadProgress');
    const imageInfo = document.getElementById('imageInfo');
    
    if (show) {
        uploadArea.style.display = 'none';
        uploadProgress.style.display = 'block';
        imageInfo.style.display = 'none';
        
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            document.getElementById('progressFill').style.width = progress + '%';
            document.getElementById('progressText').textContent = 
                progress < 100 ? `Processing... ${Math.round(progress)}%` : 'Complete!';
        }, 200);
    } else {
        uploadArea.style.display = 'block';
        uploadProgress.style.display = 'none';
    }
}

// Update image information
function updateImageInfo(file) {
    const imageInfo = document.getElementById('imageInfo');
    const fileName = document.getElementById('fileName');
    const imageSize = document.getElementById('imageSize');
    
    fileName.textContent = file.name;
    imageSize.textContent = formatFileSize(file.size);
    
    imageInfo.style.display = 'flex';
}

// Process image for parking detection
function processImage() {
    if (!currentImageData) {
        showMessage('Please upload an image first.', 'error');
        return;
    }
    
    const processBtn = document.getElementById('processBtn');
    processBtn.disabled = true;
    processBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    
    fetch('/api/process_frame', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            frame: currentImageData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'error');
        } else {
            updateDetectionResults(data);
            showMessage('Image processed successfully!', 'success');
        }
    })
    .catch(error => {
        console.error('Processing error:', error);
        showMessage('Failed to process image.', 'error');
    })
    .finally(() => {
        processBtn.disabled = false;
        processBtn.innerHTML = '<i class="fas fa-play"></i> Process Image';
    });
}

// Update detection results
function updateDetectionResults(data) {
    const detectionImage = document.getElementById('detectionImage');
    const imagePlaceholder = document.getElementById('imagePlaceholder');
    const freeSpaces = document.getElementById('freeSpaces');
    const occupiedSpaces = document.getElementById('occupiedSpaces');
    const totalSpacesDisplay = document.getElementById('totalSpacesDisplay');
    
    // Update image
    detectionImage.src = 'data:image/jpeg;base64,' + data.image;
    detectionImage.style.display = 'block';
    imagePlaceholder.style.display = 'none';
    
    // Update statistics
    freeSpaces.textContent = data.free_spaces;
    occupiedSpaces.textContent = data.occupied_spaces;
    totalSpacesDisplay.textContent = data.total_spaces;
    
    // Update total spaces counter
    document.getElementById('totalSpaces').textContent = data.total_spaces;
}

// Load parking spaces count
function loadParkingSpaces() {
    fetch('/api/parking_spaces')
    .then(response => response.json())
    .then(data => {
        document.getElementById('totalSpaces').textContent = data.total_spaces;
    })
    .catch(error => {
        console.error('Error loading parking spaces:', error);
    });
}

// Show message to user
function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert message at the top of the main content
    const mainContent = document.querySelector('.main-content');
    mainContent.insertBefore(messageDiv, mainContent.firstChild);
    
    // Auto-remove message after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Export functions for global access
window.processImage = processImage;
