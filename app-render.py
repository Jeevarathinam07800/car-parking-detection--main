from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import cv2
import pickle
import numpy as np
import base64
import io
import os
import threading
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
posList = []
cap = None
is_processing = False
width, height = 107, 48

# Load existing parking positions
def load_parking_positions():
    global posList
    try:
        with open('CarParkPos', 'rb') as f:
            posList = pickle.load(f)
    except:
        posList = []

def save_parking_positions():
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

def put_text_rect(img, text, pos, scale=1, thickness=2, offset=0, colorR=(255, 255, 255)):
    """Simple text rendering function to replace cvzone"""
    x, y = pos
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = scale
    color = colorR
    thickness = thickness
    
    # Get text size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Draw rectangle background
    cv2.rectangle(img, (x - offset, y - text_height - offset), 
                 (x + text_width + offset, y + offset), color, -1)
    
    # Draw text
    cv2.putText(img, text, (x, y), font, font_scale, (0, 0, 0), thickness)

def check_parking_space(img_pro, img):
    global posList
    space_counter = 0
    
    for pos in posList:
        x, y = pos
        img_crop = img_pro[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)
        
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        put_text_rect(img, str(count), (x, y + height - 3), scale=1,
                      thickness=2, offset=0, colorR=color)
    
    put_text_rect(img, f'Free: {space_counter}/{len(posList)}', (100, 50), scale=3,
                  thickness=5, offset=20, colorR=(0, 200, 0))
    
    return img, space_counter, len(posList)

def process_video():
    global cap, is_processing, posList
    
    if cap is None:
        return
    
    while is_processing:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        success, img = cap.read()
        if not success:
            break
            
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)
        
        processed_img, free_spaces, total_spaces = check_parking_space(img_dilate, img.copy())
        
        # Convert image to base64 for sending to frontend
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Send data to frontend
        socketio.emit('detection_result', {
            'image': img_base64,
            'free_spaces': free_spaces,
            'total_spaces': total_spaces,
            'occupied_spaces': total_spaces - free_spaces
        })
        
        time.sleep(0.1)  # Control frame rate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_video():
    global cap, is_processing
    
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        
        # Create uploads directory if it doesn't exist
        os.makedirs('uploads', exist_ok=True)
        
        file.save(filepath)
        
        # Stop current processing if running
        if is_processing:
            is_processing = False
            if cap:
                cap.release()
        
        # Load new video
        cap = cv2.VideoCapture(filepath)
        
        return jsonify({
            'message': 'Video uploaded successfully',
            'filename': filename,
            'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS)
        })

@app.route('/api/start_detection', methods=['POST'])
def start_detection():
    global is_processing, cap
    
    if cap is None:
        return jsonify({'error': 'No video loaded'}), 400
    
    if not posList:
        return jsonify({'error': 'No parking spaces defined'}), 400
    
    if not is_processing:
        is_processing = True
        thread = threading.Thread(target=process_video)
        thread.daemon = True
        thread.start()
        
        return jsonify({'message': 'Detection started'})
    
    return jsonify({'message': 'Detection already running'})

@app.route('/api/stop_detection', methods=['POST'])
def stop_detection():
    global is_processing
    
    is_processing = False
    return jsonify({'message': 'Detection stopped'})

@app.route('/api/parking_spaces', methods=['GET'])
def get_parking_spaces():
    return jsonify({
        'total_spaces': len(posList),
        'positions': posList
    })

@app.route('/api/parking_spaces', methods=['POST'])
def add_parking_space():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    
    if x is None or y is None:
        return jsonify({'error': 'Missing coordinates'}), 400
    
    posList.append((x, y))
    save_parking_positions()
    
    return jsonify({
        'message': 'Parking space added',
        'total_spaces': len(posList)
    })

@app.route('/api/parking_spaces/<int:index>', methods=['DELETE'])
def remove_parking_space(index):
    global posList
    
    if 0 <= index < len(posList):
        posList.pop(index)
        save_parking_positions()
        return jsonify({
            'message': 'Parking space removed',
            'total_spaces': len(posList)
        })
    
    return jsonify({'error': 'Invalid index'}), 400

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    load_parking_positions()
    socketio.run(app, debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
