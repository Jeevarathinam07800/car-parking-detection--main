from flask import Flask, render_template, request, jsonify, send_file
import cv2
import pickle
import cvzone
import numpy as np
import base64
import io
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Global variables
posList = []
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
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                          thickness=2, offset=0, colorR=color)
    
    cvzone.putTextRect(img, f'Free: {space_counter}/{len(posList)}', (100, 50), scale=3,
                      thickness=5, offset=20, colorR=(0, 200, 0))
    
    return img, space_counter, len(posList)

def process_frame(frame_data):
    """Process a single frame for parking detection"""
    try:
        # Decode base64 image
        img_bytes = base64.b64decode(frame_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return None
        
        # Process the image
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
        img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 25, 16)
        img_median = cv2.medianBlur(img_threshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        img_dilate = cv2.dilate(img_median, kernel, iterations=1)
        
        processed_img, free_spaces, total_spaces = check_parking_space(img_dilate, img.copy())
        
        # Convert back to base64
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return {
            'image': img_base64,
            'free_spaces': free_spaces,
            'total_spaces': total_spaces,
            'occupied_spaces': total_spaces - free_spaces
        }
    except Exception as e:
        print(f"Error processing frame: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parking_spaces', methods=['GET'])
def get_parking_spaces():
    load_parking_positions()
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
    
    load_parking_positions()
    posList.append((x, y))
    save_parking_positions()
    
    return jsonify({
        'message': 'Parking space added',
        'total_spaces': len(posList)
    })

@app.route('/api/parking_spaces/<int:index>', methods=['DELETE'])
def remove_parking_space(index):
    global posList
    
    load_parking_positions()
    if 0 <= index < len(posList):
        posList.pop(index)
        save_parking_positions()
        return jsonify({
            'message': 'Parking space removed',
            'total_spaces': len(posList)
        })
    
    return jsonify({'error': 'Invalid index'}), 400

@app.route('/api/process_frame', methods=['POST'])
def process_frame_endpoint():
    """Process a single frame for parking detection"""
    try:
        data = request.get_json()
        frame_data = data.get('frame')
        
        if not frame_data:
            return jsonify({'error': 'No frame data provided'}), 400
        
        result = process_frame(frame_data)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to process frame'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_parking_positions()
    app.run(debug=True)
