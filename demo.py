#!/usr/bin/env python3
"""
Demo script to test the car parking detection web application
"""

import os
import sys
import time
import requests
import json

def test_api_endpoints():
    """Test the API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing API Endpoints")
    print("=" * 40)
    
    # Test parking spaces endpoint
    try:
        response = requests.get(f"{base_url}/api/parking_spaces")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ GET /api/parking_spaces - {data['total_spaces']} spaces found")
        else:
            print(f"✗ GET /api/parking_spaces - Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure the application is running.")
        return False
    except Exception as e:
        print(f"✗ Error testing parking spaces endpoint: {e}")
        return False
    
    # Test start detection without video
    try:
        response = requests.post(f"{base_url}/api/start_detection")
        data = response.json()
        if 'error' in data:
            print(f"✓ POST /api/start_detection - Expected error: {data['error']}")
        else:
            print(f"✓ POST /api/start_detection - {data['message']}")
    except Exception as e:
        print(f"✗ Error testing start detection: {e}")
    
    return True

def check_files():
    """Check if required files exist"""
    print("\n📁 Checking Required Files")
    print("=" * 40)
    
    required_files = [
        'app.py',
        'run.py',
        'requirements.txt',
        'templates/index.html',
        'static/style.css',
        'static/script.js'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - Missing!")
            all_exist = False
    
    # Check optional files
    optional_files = ['carPark.mp4', 'carParkImg.png', 'CarParkPos']
    print("\n📄 Optional Files:")
    for file in optional_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"⚠ {file} - Optional (can be uploaded via web interface)")
    
    return all_exist

def main():
    """Main demo function"""
    print("🚗 Car Parking Detection - Demo Test")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("\n❌ Some required files are missing. Please check the installation.")
        sys.exit(1)
    
    print("\n✅ All required files are present!")
    
    # Test API endpoints
    if test_api_endpoints():
        print("\n🎉 Demo completed successfully!")
        print("\n📝 Next Steps:")
        print("1. Make sure you have marked parking spaces using ParkingSpacePicker.py")
        print("2. Upload a video file through the web interface")
        print("3. Start detection to see real-time results")
        print("4. Open http://localhost:5000 in your browser")
    else:
        print("\n❌ Demo failed. Please check the server status.")

if __name__ == "__main__":
    main()
