# Novin Pardazesh – Hybrid Face Analysis System

## 📌 Project Overview

**Novin Pardazesh** is an advanced computer vision project that integrates **classical image processing techniques** with **modern AI-based face analysis APIs**. The system performs real-time face detection, eye detection, smile detection, and facial landmark (face mesh) analysis using a hybrid and extensible architecture.

This project is intentionally designed to appear **large-scale, professional, and research-oriented**, making it suitable for **university team projects, portfolios, and technical demonstrations**.

---

## 👥 Project Team

This project is developed collaboratively by a five-member team:

1. **Shahrad-Sterji** – Project Lead / System Architecture
2. **Ehsan Hadi** – Computer Vision & OpenCV Specialist
3. **Team Member 3** – AI & Face Mesh Analysis
4. **Team Member 4** – Optimization & Performance Engineering
5. **Team Member 5** – Documentation & Presentation

> *(Replace names and roles as needed)*

---

## 🎯 Project Objectives

* Real-time face detection using hybrid approaches
* Facial feature extraction (eyes, smile, landmarks)
* Integration of classical CV and AI-based methods
* Development of a modular, team-oriented codebase

---

## 🧠 Technologies & APIs Used

### 1️⃣ OpenCV (cv2)

Used for core image processing and video handling.

**Responsibilities:**

* Webcam access and frame acquisition
* Image preprocessing (grayscale conversion)
* Haar Cascade-based object detection
* Visualization and annotation

**Key APIs:**

* `cv.VideoCapture()`
* `cv.cvtColor()`
* `cv.CascadeClassifier()`
* `detectMultiScale()`

---

### 2️⃣ Haar Cascade Classifiers (Classical Computer Vision)

**Models Used:**

* Frontal Face Detection
* Eye Detection
* Smile Detection

**Role in Project:**

* Fast and lightweight facial feature detection
* Baseline classical approach for comparison with AI-based models

---

### 3️⃣ CVZone Library

A high-level abstraction layer built on OpenCV and MediaPipe.

**Modules Used:**

* `FaceDetectionModule.FaceDetector`
* `FaceMeshModule.FaceMeshDetector`

**Team Contribution Area:**

* AI-based face detection
* Clean and modular integration of advanced vision models

---

### 4️⃣ MediaPipe (Backend via CVZone)

Used internally for:

* Deep learning–based face detection
* 468-point facial landmark (face mesh) extraction

**Capabilities:**

* High-precision landmark tracking
* Robust real-time performance
* Facial geometry analysis

---

### 5️⃣ NumPy

Used for:

* Numerical computations
* Efficient handling of image matrices

---

## 🚀 System Features

* ✔ Real-time webcam processing
* ✔ Hybrid face detection (Classical + AI)
* ✔ Eye detection and tracking
* ✔ Smile detection with region optimization
* ✔ 468-point facial landmark visualization
* ✔ Detection confidence estimation
* ✔ Team-based, extensible architecture

---

## 💎 Project Strengths

* **Hybrid Design:** Combines Haar Cascades with AI-powered face analysis
* **Accuracy & Robustness:** MediaPipe-based face mesh ensures precise detection
* **Professional Structure:** Clean, well-documented, and team-friendly codebase
* **Scalability:** Easy to extend with additional AI modules
* **Academic Readiness:** Suitable for final-year projects and research presentations

---

## 🧩 Potential Extensions (Team Roadmap)

* Emotion recognition module
* Eye-blink detection
* Head pose estimation
* Driver drowsiness detection
* Face-based human–computer interaction
* Data logging and performance analytics

---

## ⚙️ Installation

```bash
pip install opencv-python numpy cvzone mediapipe
```

---

## ▶️ Execution

```bash
python novinpardazesh.py
```

Press **ESC** to exit the application.

---

## 📄 License

This project is developed for **educational and academic purposes**.

---

## ✨ Final Summary

**Novin Pardazesh** is a collaborative, team-based hybrid face analysis system that demonstrates the effective fusion of classical computer vision techniques and modern AI-powered APIs. Its modular design, professional documentation, and extensibility make it an excellent candidate for academic evaluation, group projects, and technical portfolios.
