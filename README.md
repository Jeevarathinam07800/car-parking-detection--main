# 🚗 Car Parking Detection Web Application

A beautiful, modern web application for real-time car parking space detection using OpenCV, Flask, and WebSocket technology. This project provides an intuitive web interface to upload videos, monitor parking spaces, and get live detection results.

## ✨ Features

- 🎨 **Beautiful Modern UI** - Responsive design with gradient backgrounds and smooth animations
- 📤 **Video Upload** - Drag & drop or click to upload parking lot videos
- 👁️ **Live Preview** - Real-time video processing with parking space detection
- 📊 **Live Statistics** - Real-time count of free, occupied, and total parking spaces
- 🔌 **WebSocket Support** - Live updates without page refresh
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile devices
- ⚡ **Real-time Processing** - Fast detection with OpenCV computer vision

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harshbafnaa/car-parking-detection.git
   cd car-parking-detection
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

## 📖 How to Use

### Step 1: Mark Parking Spaces
Before using the web application, you need to mark parking spaces on your parking lot image:

1. Run the original space picker:
   ```bash
   python ParkingSpacePicker.py
   ```
2. Left-click to add parking spaces
3. Right-click to remove parking spaces
4. The coordinates are saved in `CarParkPos` file

### Step 2: Use the Web Application
1. **Upload Video**: Drag and drop or click to upload your parking lot video
2. **Start Detection**: Click the "Start Detection" button
3. **Monitor Results**: Watch the live preview and statistics
4. **Stop Detection**: Click "Stop Detection" when finished

## 🏗️ Project Structure

```
car-parking-detection/
├── app.py                 # Flask web application backend
├── run.py                 # Application startup script
├── main.py                # Original OpenCV detection script
├── ParkingSpacePicker.py  # Original space marking script
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── style.css         # Beautiful CSS styling
│   └── script.js         # Frontend JavaScript
├── uploads/              # Uploaded video files (auto-created)
├── carPark.mp4          # Sample video file
├── carParkImg.png       # Sample parking lot image
└── CarParkPos           # Saved parking space coordinates
```

## 🛠️ Technical Details

### Backend (Flask)
- **Flask**: Web framework for API endpoints
- **Flask-SocketIO**: WebSocket support for real-time communication
- **OpenCV**: Computer vision for parking space detection
- **cvzone**: Enhanced OpenCV utilities
- **NumPy**: Numerical computing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Real-time interaction and WebSocket handling
- **Font Awesome**: Beautiful icons
- **Google Fonts**: Inter font family

### API Endpoints
- `POST /api/upload` - Upload video files
- `POST /api/start_detection` - Start parking detection
- `POST /api/stop_detection` - Stop detection
- `GET /api/parking_spaces` - Get parking space information
- `POST /api/parking_spaces` - Add parking space
- `DELETE /api/parking_spaces/<id>` - Remove parking space

## 🎨 UI Features

- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Responsive Layout**: Adapts to all screen sizes
- **Real-time Updates**: Live statistics and video preview
- **Drag & Drop**: Easy file upload with visual feedback
- **Status Indicators**: Connection status and processing indicators
- **Smooth Animations**: Hover effects and transitions
- **Error Handling**: User-friendly error messages

## 🔧 Configuration

The application uses the following default settings:
- **Server Port**: 5000
- **Host**: 0.0.0.0 (accessible from any IP)
- **Debug Mode**: Enabled for development
- **Parking Space Size**: 107x48 pixels
- **Detection Threshold**: 900 pixels

## 📱 Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Credits

- **Original Inspiration**: [Murtaza's Computer Vision Zone](https://www.computervision.zone/)
- **Course**: [Computer Vision Zone YouTube Course](https://www.youtube.com/watch?v=caKnQlCMIYI)
- **Developer**: [Harsh Bafna](https://github.com/harshbafnaa)
- **Web Interface**: Enhanced with modern Flask and WebSocket technology
