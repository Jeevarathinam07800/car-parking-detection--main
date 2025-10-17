#!/usr/bin/env python3
"""
Vercel Deployment Helper Script
Prepares the car parking detection app for Vercel deployment
"""

import os
import shutil
import subprocess
import sys

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check if vercel CLI is installed
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Vercel CLI is installed")
        else:
            print("✗ Vercel CLI not found. Install with: npm install -g vercel")
            return False
    except FileNotFoundError:
        print("✗ Vercel CLI not found. Install with: npm install -g vercel")
        return False
    
    # Check if git is available
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Git is available")
        else:
            print("✗ Git not found")
            return False
    except FileNotFoundError:
        print("✗ Git not found")
        return False
    
    return True

def prepare_files():
    """Prepare files for Vercel deployment"""
    print("\n📁 Preparing files for deployment...")
    
    # Check if required files exist
    required_files = [
        'vercel.json',
        'package.json',
        'requirements-vercel.txt',
        'api/index.py',
        'templates/index-vercel.html',
        'static/style.css',
        'static/script-vercel.js'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - Missing!")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    # Copy Vercel-specific files to standard locations
    print("\n📋 Copying Vercel-specific files...")
    
    # Copy template
    if os.path.exists('templates/index-vercel.html'):
        shutil.copy2('templates/index-vercel.html', 'templates/index.html')
        print("✓ Copied Vercel template to standard location")
    
    # Copy script
    if os.path.exists('static/script-vercel.js'):
        shutil.copy2('static/script-vercel.js', 'static/script.js')
        print("✓ Copied Vercel script to standard location")
    
    # Copy requirements
    if os.path.exists('requirements-vercel.txt'):
        shutil.copy2('requirements-vercel.txt', 'requirements.txt')
        print("✓ Copied Vercel requirements to standard location")
    
    return True

def check_parking_spaces():
    """Check if parking spaces are marked"""
    print("\n🅿️ Checking parking spaces...")
    
    if os.path.exists('CarParkPos'):
        print("✓ CarParkPos file exists")
        try:
            import pickle
            with open('CarParkPos', 'rb') as f:
                posList = pickle.load(f)
            print(f"✓ Found {len(posList)} parking spaces")
            return True
        except Exception as e:
            print(f"✗ Error reading CarParkPos: {e}")
            return False
    else:
        print("⚠ CarParkPos file not found")
        print("  Run 'python ParkingSpacePicker.py' to mark parking spaces first")
        return False

def deploy_to_vercel():
    """Deploy to Vercel"""
    print("\n🚀 Deploying to Vercel...")
    
    try:
        # Check if already logged in
        result = subprocess.run(['vercel', 'whoami'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Please login to Vercel first:")
            subprocess.run(['vercel', 'login'])
        
        # Deploy
        print("Starting deployment...")
        result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment successful!")
            print(result.stdout)
            return True
        else:
            print("❌ Deployment failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚗 Car Parking Detection - Vercel Deployment Helper")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Please install missing tools.")
        sys.exit(1)
    
    # Prepare files
    if not prepare_files():
        print("\n❌ File preparation failed.")
        sys.exit(1)
    
    # Check parking spaces
    if not check_parking_spaces():
        print("\n⚠️ Warning: No parking spaces marked. Detection may not work properly.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Deployment cancelled.")
            sys.exit(1)
    
    # Deploy
    if deploy_to_vercel():
        print("\n🎉 Deployment completed successfully!")
        print("\n📝 Next steps:")
        print("1. Visit your Vercel dashboard to get the deployment URL")
        print("2. Test the application by uploading an image")
        print("3. If parking spaces aren't marked, run ParkingSpacePicker.py locally first")
    else:
        print("\n❌ Deployment failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
