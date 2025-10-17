# 🚀 Deploying Car Parking Detection to Vercel

This guide will help you deploy your car parking detection web application to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally with `npm install -g vercel`
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)

## 🔧 Pre-Deployment Setup

### 1. Prepare Your Files

Make sure you have these files in your project root:
- `vercel.json` - Vercel configuration
- `package.json` - Node.js package configuration
- `requirements-vercel.txt` - Python dependencies
- `api/` directory with Python files
- `templates/` directory with HTML files
- `static/` directory with CSS/JS files
- `CarParkPos` - Your parking space coordinates file

### 2. Mark Parking Spaces (Important!)

Before deploying, you need to mark parking spaces:

```bash
# Run this locally first
python ParkingSpacePicker.py
```

- Left-click to add parking spaces
- Right-click to remove parking spaces
- This creates the `CarParkPos` file needed for detection

## 🚀 Deployment Methods

### Method 1: Vercel CLI (Recommended)

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Deploy from your project directory:**
   ```bash
   vercel
   ```

3. **Follow the prompts:**
   - Link to existing project? (No for first deployment)
   - Project name: `car-parking-detection`
   - Directory: `.` (current directory)
   - Override settings? (No)

4. **Deploy to production:**
   ```bash
   vercel --prod
   ```

### Method 2: GitHub Integration

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Add Vercel deployment files"
   git push origin main
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Configure settings:
     - Framework Preset: `Other`
     - Root Directory: `.`
     - Build Command: (leave empty)
     - Output Directory: (leave empty)

3. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete

## ⚙️ Configuration Details

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

### Key Points:
- **Serverless Functions**: Each API endpoint runs as a separate serverless function
- **File Uploads**: Limited to 4.5MB per request
- **Processing Time**: Maximum 30 seconds per function execution
- **Static Files**: Served from `/static/` directory

## 🔍 Testing Your Deployment

1. **Check the deployment URL:**
   - Vercel will provide a URL like `https://your-project.vercel.app`

2. **Test the application:**
   - Upload an image
   - Process it for parking detection
   - Verify results are displayed

3. **Monitor logs:**
   ```bash
   vercel logs your-project-name
   ```

## 🛠️ Troubleshooting

### Common Issues:

1. **OpenCV Import Errors:**
   - Make sure you're using `opencv-python-headless`
   - Check that all dependencies are in `requirements-vercel.txt`

2. **File Not Found Errors:**
   - Ensure `CarParkPos` file is included in deployment
   - Check file paths are relative

3. **Function Timeout:**
   - Reduce image processing complexity
   - Optimize OpenCV operations

4. **Memory Issues:**
   - Use smaller images
   - Optimize image processing pipeline

### Debug Commands:

```bash
# Check deployment status
vercel ls

# View function logs
vercel logs your-project-name --follow

# Redeploy
vercel --prod
```

## 📊 Performance Optimization

### For Better Performance:

1. **Image Optimization:**
   - Resize images before processing
   - Use JPEG format for smaller file sizes
   - Compress images client-side

2. **Function Optimization:**
   - Minimize imports
   - Use efficient OpenCV operations
   - Cache parking space positions

3. **Frontend Optimization:**
   - Compress CSS/JS files
   - Use CDN for static assets
   - Implement lazy loading

## 🔄 Updates and Maintenance

### Updating Your Deployment:

1. **Make changes locally**
2. **Test thoroughly**
3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Update parking detection"
   git push origin main
   ```
4. **Redeploy:**
   ```bash
   vercel --prod
   ```

### Monitoring:

- Use Vercel Analytics for performance monitoring
- Check function execution times
- Monitor error rates

## 🌐 Custom Domain (Optional)

1. **Add domain in Vercel dashboard**
2. **Configure DNS settings**
3. **Enable SSL certificate**

## 📝 Notes

- **Limitations**: Vercel has a 10-second timeout for hobby plans
- **Scaling**: Pro plans have higher limits
- **Storage**: No persistent storage (use external services for file storage)
- **Environment**: Each function runs in isolation

## 🎉 Success!

Once deployed, your car parking detection application will be available at your Vercel URL. Users can:

- Upload parking lot images
- Process them for parking space detection
- View real-time results
- See statistics about parking occupancy

The application will work seamlessly with your existing parking space coordinates and provide a beautiful, responsive interface for parking detection!
