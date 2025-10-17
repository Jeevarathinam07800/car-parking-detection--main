// Static version for Netlify deployment
let currentImage = null;
let parkingSpaces = [];
let isAnalyzing = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadParkingSpaces();
});

// Setup event listeners
function setupEventListeners() {
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
    
    const reader = new FileReader();
    reader.onload = function(e) {
        currentImage = e.target.result;
        updateImageInfo(file);
        showMessage('Image uploaded successfully!', 'success');
        displayImage();
    };
    
    reader.readAsDataURL(file);
}

// Display uploaded image
function displayImage() {
    const canvas = document.getElementById('analysisCanvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = function() {
        // Set canvas size to image size
        canvas.width = img.width;
        canvas.height = img.height;
        
        // Draw image on canvas
        ctx.drawImage(img, 0, 0);
        
        // Show canvas and hide placeholder
        canvas.style.display = 'block';
        document.getElementById('imagePlaceholder').style.display = 'none';
        
        // Add click listener for marking spaces
        canvas.addEventListener('click', markParkingSpace);
    };
    
    img.src = currentImage;
}

// Mark parking space on click
function markParkingSpace(event) {
    const canvas = document.getElementById('analysisCanvas');
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    // Add parking space
    parkingSpaces.push({x: x, y: y, occupied: false});
    
    // Draw parking space marker
    const ctx = canvas.getContext('2d');
    ctx.strokeStyle = '#ff00ff';
    ctx.lineWidth = 2;
    ctx.strokeRect(x - 50, y - 25, 100, 50);
    
    // Update counter
    document.getElementById('totalSpaces').textContent = parkingSpaces.length;
    
    showMessage(`Parking space added at (${Math.round(x)}, ${Math.round(y)})`, 'success');
}

// Analyze image for parking detection
function analyzeImage() {
    if (!currentImage) {
        showMessage('Please upload an image first.', 'error');
        return;
    }
    
    if (parkingSpaces.length === 0) {
        showMessage('Please mark some parking spaces first by clicking on the image.', 'error');
        return;
    }
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    
    // Simulate analysis (in real version, this would use computer vision)
    setTimeout(() => {
        performAnalysis();
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Image';
    }, 2000);
}

// Perform parking space analysis
function performAnalysis() {
    const canvas = document.getElementById('analysisCanvas');
    const ctx = canvas.getContext('2d');
    
    let freeSpaces = 0;
    let occupiedSpaces = 0;
    
    // Analyze each parking space
    parkingSpaces.forEach((space, index) => {
        // Simple analysis based on image data
        const imageData = ctx.getImageData(space.x - 50, space.y - 25, 100, 50);
        const data = imageData.data;
        
        // Calculate average brightness
        let totalBrightness = 0;
        for (let i = 0; i < data.length; i += 4) {
            const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3;
            totalBrightness += brightness;
        }
        const avgBrightness = totalBrightness / (data.length / 4);
        
        // Simple heuristic: darker areas are occupied
        const isOccupied = avgBrightness < 100;
        space.occupied = isOccupied;
        
        if (isOccupied) {
            occupiedSpaces++;
            // Draw red rectangle for occupied
            ctx.strokeStyle = '#ff0000';
            ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';
        } else {
            freeSpaces++;
            // Draw green rectangle for free
            ctx.strokeStyle = '#00ff00';
            ctx.fillStyle = 'rgba(0, 255, 0, 0.3)';
        }
        
        ctx.lineWidth = 3;
        ctx.strokeRect(space.x - 50, space.y - 25, 100, 50);
        ctx.fillRect(space.x - 50, space.y - 25, 100, 50);
        
        // Add text
        ctx.fillStyle = '#000000';
        ctx.font = '12px Arial';
        ctx.fillText(isOccupied ? 'OCCUPIED' : 'FREE', space.x - 30, space.y);
    });
    
    // Update statistics
    document.getElementById('freeSpaces').textContent = freeSpaces;
    document.getElementById('occupiedSpaces').textContent = occupiedSpaces;
    document.getElementById('totalSpacesDisplay').textContent = parkingSpaces.length;
    
    showMessage(`Analysis complete! Found ${freeSpaces} free and ${occupiedSpaces} occupied spaces.`, 'success');
}

// Load parking spaces from localStorage
function loadParkingSpaces() {
    const saved = localStorage.getItem('parkingSpaces');
    if (saved) {
        parkingSpaces = JSON.parse(saved);
        document.getElementById('totalSpaces').textContent = parkingSpaces.length;
    }
}

// Save parking spaces to localStorage
function saveParkingSpaces() {
    localStorage.setItem('parkingSpaces', JSON.stringify(parkingSpaces));
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
window.analyzeImage = analyzeImage;
