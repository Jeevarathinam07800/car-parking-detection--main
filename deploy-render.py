#!/usr/bin/env python3
"""
Render.com Deployment Helper Script
Prepares the car parking detection app for Render deployment
"""

import os
import subprocess
import sys

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    # Check if git is available
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("+ Git is available")
        else:
            print("- Git not found")
            return False
    except FileNotFoundError:
        print("- Git not found")
        return False
    
    return True

def check_files():
    """Check if required files exist"""
    print("\nChecking required files...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/style.css',
        'static/script.js',
        'render.yaml'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"+ {file}")
        else:
            print(f"- {file} - Missing!")
            missing_files.append(file)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    
    return True

def check_parking_spaces():
    """Check if parking spaces are marked"""
    print("\nChecking parking spaces...")
    
    if os.path.exists('CarParkPos'):
        print("+ CarParkPos file exists")
        try:
            import pickle
            with open('CarParkPos', 'rb') as f:
                posList = pickle.load(f)
            print(f"+ Found {len(posList)} parking spaces")
            return True
        except Exception as e:
            print(f"- Error reading CarParkPos: {e}")
            return False
    else:
        print("! CarParkPos file not found")
        print("  Run 'python ParkingSpacePicker.py' to mark parking spaces first")
        return False

def prepare_git():
    """Prepare Git repository for deployment"""
    print("\nPreparing Git repository...")
    
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Initializing Git repository...")
            subprocess.run(['git', 'init'], check=True)
        
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--cached', '--quiet'], capture_output=True)
        if result.returncode != 0:
            subprocess.run(['git', 'commit', '-m', 'Prepare for Render deployment'], check=True)
            print("+ Changes committed to Git")
        else:
            print("+ No changes to commit")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"- Git error: {e}")
        return False

def show_deployment_instructions():
    """Show deployment instructions"""
    print("\nRender Deployment Instructions")
    print("=" * 50)
    print("\n1. Go to https://render.com")
    print("2. Sign up for a free account")
    print("3. Connect your GitHub account")
    print("4. Push your code to GitHub:")
    print("   git remote add origin https://github.com/yourusername/your-repo.git")
    print("   git push -u origin main")
    print("\n5. Create New Web Service:")
    print("   - Click 'New +' -> 'Web Service'")
    print("   - Connect your GitHub repository")
    print("   - Configure settings:")
    print("     * Name: car-parking-detection")
    print("     * Environment: Python 3")
    print("     * Build Command: pip install -r requirements.txt")
    print("     * Start Command: python app.py")
    print("     * Instance Type: Free")
    print("\n6. Deploy!")
    print("   - Click 'Create Web Service'")
    print("   - Wait 5-10 minutes for deployment")
    print("   - Your app will be available at: https://your-app-name.onrender.com")
    
    print("\nTips:")
    print("• Free tier sleeps after 15 min inactivity")
    print("• First request may take 30-60 seconds (wake-up time)")
    print("• Upgrade to Starter ($7/month) for always-on service")
    print("• Check logs in Render dashboard if issues occur")

def main():
    """Main deployment preparation function"""
    print("Car Parking Detection - Render Deployment Helper")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\nRequirements not met. Please install Git.")
        sys.exit(1)
    
    # Check files
    if not check_files():
        print("\nFile check failed.")
        sys.exit(1)
    
    # Check parking spaces
    if not check_parking_spaces():
        print("\nWarning: No parking spaces marked.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Deployment preparation cancelled.")
            sys.exit(1)
    
    # Prepare Git
    if not prepare_git():
        print("\nGit preparation failed.")
        sys.exit(1)
    
    # Show instructions
    show_deployment_instructions()
    
    print("\nYour project is ready for Render deployment!")
    print("\nNext steps:")
    print("1. Push to GitHub")
    print("2. Connect to Render")
    print("3. Deploy!")
    print("4. Test your real-time video processing!")

if __name__ == "__main__":
    main()