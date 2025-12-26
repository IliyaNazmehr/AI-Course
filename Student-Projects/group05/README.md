# Group 5
⸻

👤 Real-Time Face Detection Using OpenCV and Haar Cascade

📌 Project Overview

This project presents a real-time face detection system developed using classical computer vision techniques. The system employs the Haar Cascade classifier provided by the OpenCV library to detect human faces from a live webcam stream.

The primary objective of this project is to demonstrate a clear understanding of object detection and image processing concepts without utilizing deep learning or neural network-based approaches.

⸻

🎯 Project Objectives
• Implement a real-time face detection system using a webcam
• Understand and apply the Haar Cascade object detection algorithm
• Gain practical experience with OpenCV for image and video processing
• Detect and localize human faces in video frames
• Visualize detection results using bounding boxes

⸻

🧠 Methodology

The face detection process follows a structured pipeline:
1. Capture live video frames from the system webcam
2. Convert each frame from RGB to grayscale to reduce computational cost
3. Load the pre-trained Haar Cascade classifier from an XML file
4. Apply the cascade classifier to detect face regions at multiple scales
5. Draw bounding boxes around detected faces
6. Display the processed video stream in real time

⸻

⚙️ Technologies and Tools
• Python
• OpenCV (cv2)
• Haar Cascade Classifier
• Jupyter Notebook

⸻

📁 Project Structure

Face-Detection/
│── face.ipynb
│── haarcascade_frontalface_default.xml
│── README.md


⸻

🚀 Installation and Execution

1️⃣ Install Required Dependencies

Ensure Python is installed, then run:

pip install opencv-python

2️⃣ Run the Project

Launch Jupyter Notebook and execute the notebook file:

jupyter notebook face.ipynb


⸻

📊 Key Features
• Real-time face detection from live video input
• Efficient and lightweight implementation
• Webcam-based video processing
• No dependency on deep learning frameworks
• Suitable for systems with limited computational resources

⸻

🧪 Algorithm Explanation

The Haar Cascade classifier is a machine learning-based object detection algorithm that uses Haar-like features and a cascade of weak classifiers trained on positive and negative samples. This approach allows rapid and efficient detection, making it well-suited for real-time face detection applications.

⸻

📌 Important Notes
• The file haarcascade_frontalface_default.xml is required for proper execution
• Webcam access must be enabled before running the project
• Press the q key to terminate the program

⸻

🎓 Academic Statement

This project has been developed exclusively for educational purposes and is submitted as part of a university coursework in the field of Artificial Intelligence and Computer Vision.

⸻

🧑‍💻 Author

Niloufar zohdy tale
Aylin emamizade
Mani vazirpour
fatemeh salmani amand
⸻

📄 License

This project is intended for academic and educational use only.
