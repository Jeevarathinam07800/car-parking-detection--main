// Global variables
let isDetectionRunning = false;
let pollingInterval = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadParkingSpaces();
});

// Setup event listeners
function setupEventListeners() {
    // File upload handling
    const videoInput = document.getElementById('videoInput');
    const uploadArea = document.getElementById('uploadArea');
    
    videoInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => videoInput.click());
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        uploadVideo(file);
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
        uploadVideo(files[0]);
    }
}

// Upload video file
function uploadVideo(file) {
    if (!file.type.startsWith('video/')) {
        showMessage('Please select a valid video file.', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('video', file);
    
    // Show upload progress
    showUploadProgress(true);
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'error');
        } else {
            showMessage(data.message, 'success');
            updateVideoInfo(data);
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        showMessage('Upload failed. Please try again.', 'error');
    })
    .finally(() => {
        showUploadProgress(false);
    });
}

// Show/hide upload progress
function showUploadProgress(show) {
    const uploadArea = document.getElementById('uploadArea');
    const uploadProgress = document.getElementById('uploadProgress');
    const videoInfo = document.getElementById('videoInfo');
    
    if (show) {
        uploadArea.style.display = 'none';
        uploadProgress.style.display = 'block';
        videoInfo.style.display = 'none';
        
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
                progress < 100 ? `Uploading... ${Math.round(progress)}%` : 'Processing...';
        }, 200);
    } else {
        uploadArea.style.display = 'block';
        uploadProgress.style.display = 'none';
    }
}

// Update video information
function updateVideoInfo(data) {
    const videoInfo = document.getElementById('videoInfo');
    const fileName = document.getElementById('fileName');
    const videoDuration = document.getElementById('videoDuration');
    const videoFPS = document.getElementById('videoFPS');
    
    fileName.textContent = data.filename;
    videoDuration.textContent = `${Math.round(data.total_frames / data.fps)}s`;
    videoFPS.textContent = `${data.fps.toFixed(1)} FPS`;
    
    videoInfo.style.display = 'flex';
}

// Start detection
function startDetection() {
    fetch('/api/start_detection', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'error');
        } else {
            isDetectionRunning = true;
            updateDetectionControls();
            showMessage(data.message, 'success');
            
            // Start polling for results
            startPolling();
        }
    })
    .catch(error => {
        console.error('Start detection error:', error);
        showMessage('Failed to start detection.', 'error');
    });
}

// Stop detection
function stopDetection() {
    fetch('/api/stop_detection', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        isDetectionRunning = false;
        updateDetectionControls();
        showMessage(data.message, 'success');
        
        // Stop polling
        stopPolling();
        
        // Hide detection image
        const detectionImage = document.getElementById('detectionImage');
        const videoPlaceholder = document.getElementById('videoPlaceholder');
        detectionImage.style.display = 'none';
        videoPlaceholder.style.display = 'block';
    })
    .catch(error => {
        console.error('Stop detection error:', error);
        showMessage('Failed to stop detection.', 'error');
    });
}

// Start polling for detection results
function startPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
    
    pollingInterval = setInterval(() => {
        fetch('/api/get_result')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log('No result available yet');
            } else {
                updateDetectionResults(data);
            }
        })
        .catch(error => {
            console.error('Polling error:', error);
        });
    }, 100); // Poll every 100ms
}

// Stop polling
function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

// Update detection controls
function updateDetectionControls() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    
    if (isDetectionRunning) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
}

// Update detection results
function updateDetectionResults(data) {
    const detectionImage = document.getElementById('detectionImage');
    const videoPlaceholder = document.getElementById('videoPlaceholder');
    const freeSpaces = document.getElementById('freeSpaces');
    const occupiedSpaces = document.getElementById('occupiedSpaces');
    const totalSpacesDisplay = document.getElementById('totalSpacesDisplay');
    
    // Update image
    detectionImage.src = 'data:image/jpeg;base64,' + data.image;
    detectionImage.style.display = 'block';
    videoPlaceholder.style.display = 'none';
    
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
window.startDetection = startDetection;
window.stopDetection = stopDetection;
