# AI Emotion Recognition Software

This project is an AI-powered emotion recognition system that analyzes facial expressions in real-time to detect human emotions. Built with **TensorFlow** for robust machine learning capabilities, it leverages **Node.js** as a scalable backend to handle data processing and API services. The software is designed for applications in human-computer interaction, mental health monitoring, and interactive user experiences.

### Key Features

- **Real-Time Emotion Detection**: Utilizes deep learning models to identify emotions from facial expressions.
- **TensorFlow Integration**: Employs state-of-the-art neural networks for accurate and efficient inference.
- **Node.js Backend**: Provides a fast, event-driven server environment for seamless performance and scalability.
- **Easy Integration**: Can be incorporated into web or mobile applications via a simple API.

### Potential Use Cases

- Enhancing user engagement in apps and games through emotion-aware interactions.
- Supporting mental health tools by tracking emotional well-being.
- Improving customer experience in service industries with sentiment analysis.

This software is open-source and welcomes contributions to expand its functionality and accessibility.


## 1. Project Overview
- **Type:** Web Application
- **Backend:** Node.js + Express
- **Frontend:** HTML, JavaScript
- **AI Library:** face-api.js (browser-based)
- **Camera:** Webcam (required)

All AI inference runs **inside the browser**, not on the server.

---

## 2. System Requirements
- Windows / macOS / Linux
- **Node.js v18 or newer (LTS recommended)**
- Webcam (built-in or external)
- Modern browser (Chrome, Edge, Firefox)

---

## 3. Install Node.js
1. Go to: https://nodejs.org
2. Download and install the **LTS version**
3. Verify installation:
   
bash
   node -v
   npm -v
---

## 4. Extract the Project

1. Right-click `face-emotion-detection-master.zip`
2. Select **Extract All**
3. Open the extracted folder:

   
   face-emotion-detection-master
  

---

## 5. Open Terminal in Project Folder

### Windows

* Hold **Shift + Right Click**
* Click **Open PowerShell window here**

### macOS / Linux

bash
cd face-emotion-detection-master

---

## 6. Install Project Dependencies

Run:

bash
npm install

This installs:

* express
* ejs
* multer
* pg (optional, database not required unless used)

---

## 7. How to Run the Application

### Start the Server

bash
node server.js

If successful, you will see:

Server running on port 3000

---

### Open the App in Browser

Open your browser and go to:

http://localhost:3000

---

### Allow Webcam Access

* When prompted, click **Allow**
* Emotion detection will start automatically

---

## 8. Stopping the Application

To stop the server:

text
Ctrl + C

---

## 9. Common Issues & Fixes

### Port Already in Use

Edit `server.js`:

js
app.listen(3001)

Then open:

http://localhost:3001

---

# Acknowledgments ✨

This project was developed as part of a university coursework/thesis. We would like to thank the following people for their valuable help and contributions:

## Academic Support
• **Dr. Maryam Hajiesmaeili** – Project supervisor and guidance  
• **Prof. iliya Nazmehr** – Provided feedback and resources  

## Development Support
• **hesam shekarabi**  
• **Bahar Pourvosoughi** 
• **Nava Pourjam**

## Main Contributor
• **Mohamad sadegh Refahiyat** – Main developer
