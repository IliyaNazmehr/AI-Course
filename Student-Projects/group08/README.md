# Face & Eye Detection with Eye Color Recognition

## Overview
This project implements real-time face and eye detection with eye color recognition capabilities. The system uses OpenCV's Haar Cascade classifiers to detect faces and eyes, then applies color analysis to determine eye color (Brown, Blue, or Green).

## ⚠️ Important Note
**This application works exclusively with a webcam.** It captures live video feed from your computer's camera (default camera device 0). You cannot use static images or video files as input.

## Features
- **Real-time Face Detection**: Detects human faces in webcam feed with confidence scoring
- **Eye Detection**: Identifies eyes within detected face regions
- **Eye Color Recognition**: Analyzes and classifies eye color into three categories:
  - Brown (including black eyes)
  - Blue
  - Green
- **Confidence Display**: Shows detection confidence percentage based on face size and proximity
- **Live Visualization**: Real-time display with bounding boxes and color labels

## How It Works
1. **Capture Video**: Continuously captures frames from the connected webcam
2. **Face Detection**: Uses Haar Cascade classifier to identify faces in each frame
3. **Confidence Calculation**: Determines detection confidence based on face area ratio and size
4. **Eye Detection**: Searches for eyes within detected face regions
5. **Color Analysis**: Converts eye region to HSV color space and applies color masks to identify iris color
6. **Display Results**: Draws rectangles around faces, displays confidence percentage, and shows detected eye color

## Requirements
- Python 3.x
- OpenCV (cv2)
- NumPy
- Webcam/Camera device

## Installation
```bash
pip install opencv-python numpy
```

## Usage
1. Ensure your webcam is connected and working
2. Run the script:
```bash
python "main.py"
```
3. Position your face in front of the camera
4. The system will display:
   - Green rectangle around detected face
   - Confidence percentage above the face
   - Detected eye color below the face
5. Press 'q' to quit the application

## Technical Details
- **Face Detection**: Uses `haarcascade_frontalface_default.xml`
- **Eye Detection**: Uses `haarcascade_eye.xml`
- **Color Detection**: HSV-based color masking with focus on iris region
- **Confidence Levels**:
  - 100%: Face area > 15% of frame and width > 150px
  - 90-95%: Face area > 10% of frame
  - 80-90%: Face area > 5% of frame
  - 70-80%: Smaller face areas

## Team Members & Roles

### 👨‍💼 Mahdi
**Role**: Documentation & Project Management
- Created comprehensive README documentation
- Developed requirements.txt file
- Managed project documentation standards

### 👨‍💻 Pourya Seifi
**Role**: Developer
- Wrote the complete codebase
- Implemented face and eye detection algorithms
- Developed eye color recognition system

### 📝 Abbas
**Role**: Code Documentation
- Added useful comments throughout the code
- Improved code readability and maintainability
- Documented function purposes and logic flow

### ⚡ Seyed Javad Hashemi
**Role**: Code Optimization
- Optimized detection parameters for better performance
- Fine-tuned confidence calculation algorithms
- Improved processing efficiency

### 🔬 Morteza Noroozi
**Role**: Research & Testing
- Conducted extensive testing with different face types
- Researched and validated eye color detection accuracy
- Provided feedback for algorithm improvements

## Limitations
- **Webcam Only**: Does not support image files or pre-recorded videos
- Eye color detection accuracy depends on:
  - Lighting conditions
  - Camera quality
  - Distance from camera
  - Eye visibility
- Best results achieved when face is:
  - Well-lit
  - Directly facing the camera
  - Within 0.5-2 meters from webcam

## Troubleshooting
- **No face detected**: Ensure adequate lighting and face the camera directly
- **Incorrect eye color**: Move closer to the camera and ensure eyes are fully visible
- **Camera not opening**: Check if another application is using the webcam
- **Low confidence**: Move closer to the camera to increase detection confidence

## Notes
Demo images in outputs/demo/ are used only to demonstrate eye color detection 
for cases not available in team members.

---
*Developed by Team: Mahdi Poorjahangiri, Pourya Seifi, Abbas Faghihi, Seyed Javad Hashemi ,Morteza Noroozi.

