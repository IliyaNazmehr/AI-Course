# 🧠 NexMind – Digital Mental Health Assistant

## 📘 Artificial Intelligence Course Project

---

## 🧾 Project Information

Project Title: NexMind – Digital Mental Health Assistant  
Course Name: Artificial Intelligence  
University Name: Rafsanjani Complex, Islamic Azad University  
Instructor: Dr. Maryam Haji Esmaeili  

### 👥 Team Members
- Leader: [Reyhane Salehi ] – [40110130117462]
- [Mina Heidary ] – [40110130117384]
- [Donya ghorbani] – [40110130117415]
- [mohammad saleh imani]_[40110130117572]
- [Abtin nikoobonyad rad ] – [40010130117039]

---

## 🌱 Project Overview

NexMind is an AI-powered conversational system designed as a digital mental health assistant.  
The system focuses on emotional awareness, empathetic dialogue, and supportive interaction 💬💛.

The system does not provide medical diagnosis, therapy, or clinical treatment.  
Its purpose is to encourage emotional expression, reflection, and general well-being support in a non-clinical and ethical manner.

---

## 🎯 Project Objectives

- Design and implement an AI-based conversational assistant  
- Detect emotional signals from user input  
- Apply a multi-agent decision-making architecture  
- Combine rule-based responses with AI-generated responses  
- Develop a full-stack system with clear separation of concerns  
- Follow ethical and safety-aware AI design principles ⚖️  

---

## 🏗️ System Architecture

The project follows a three-tier architecture:

1. Frontend (Client Side)  
2. Backend (Server Side)  
3. AI Logic Layer  

---

### 💻 Frontend (Client Side)

- Implemented using React
- Provides a chat-based user interface
- Handles user input and message visualization
- Communicates with the backend via HTTP requests
- Supports both Persian (RTL) and English (LTR) text direction 🌍

---

### ⚙️ Backend (Server Side)

- Implemented using FastAPI
- Exposes a RESTful API endpoint (/generate)
- Handles request validation and response formatting
- Acts as an interface between frontend and AI logic
- Manages CORS configuration for cross-origin communication 🔗

---

### 🤖 AI Logic Layer

- Implemented in Python
- Uses a multi-agent architecture
- Maintains limited conversation memory
- Applies safety checks and ethical constraints
- Decides between rule-based and AI-generated responses

---

## 🧩 Multi-Agent Design

The AI logic consists of multiple specialized agents:

Emotion Analyzer Agent  
Detects emotional keywords from user input using a transparent rule-based approach 😊😟😡  

Confidence Agent  
Estimates the confidence level of detected emotions 📊  

Strategy Agent  
Decides whether to use rule-based responses or AI-generated responses 🧠  

Safety Agent  
Detects potentially harmful or sensitive content and ensures safe responses 🚨  

Affection and Name Detection Agent  
Adjusts tone and response style when the assistant is directly addressed 💬💖  

---

## 🌐 AI Model and API Usage

The project integrates a Language Model API to generate dynamic responses when rule-based logic is insufficient.

Reasons for using a Language Model API:
- Natural and context-aware response generation  
- Ability to handle open-ended emotional expressions  
- Improved conversational flexibility  
- Effective integration with multi-agent systems  

Rule-based responses are prioritized when emotional confidence is high,  
while AI-generated responses are used as a fallback mechanism.

---

## 🛠️ Libraries and Technologies Used

### Frontend:
- React  
- JavaScript (ES6)  
- Fetch API  
- CSS and utility-based styling 🎨  

### 🖥️ Backend:
- FastAPI  
- Pydantic  
- Uvicorn  
- Python Requests  
- python-dotenv  
- CORS Middleware  

---

## 🔌 API Specification

Endpoint:  
POST /generate

Request Body:
`json
{
  "prompt": "User input message"
}

Response:
{
  "response": "Generated assistant reply"
}


## 📎 Software Engineering Principles Applied

- Separation of concerns
- Modular architecture
- Clean and readable code structure
- Scalability and extensibility
- Ethical and safety-aware AI design


## 📎 System Limitations

- The system does not provide medical or clinical advice
- Emotion detection is keyword-based and may not capture all nuances
- Conversation memory is intentionally limited
- The assistant is designed for general emotional support only


## ✨ How to Run the Project
Backend:

pip install -r requirements.txt  

uvicorn server:app --reload


Frontend:

npm install  

npm start



## ⚜️ Screenshots

### Chat Interface
![Chat Interface](asset/1.png)

### Running Chat Interface
![Backend Communication](asset/2.png)

### AI Responding to Stress
![AI Responses](asset/3.png)

### AI Guidance
![UI Example](asset/4.png)

### Emotional Reflection
![Final Demo](asset/5.png)

## Conclusion


NexMind demonstrates the practical application of artificial intelligence concepts, multi-agent systems, and full-stack software engineering.  

The project emphasizes emotional awareness, safety, and modular AI design within an ethical framework.
