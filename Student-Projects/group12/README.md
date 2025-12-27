# Group 12
#
🎬Movie Recommendation Bot

### An Artificial Intelligence–Based Movie Recommendation Bot Using External APIs
The Movie Recommendation Bot is an intelligent, web-based recommendation bot
designed to suggest relevant movies to users based on their preferences.
The bot leverages real-time data from The Movie Database (TMDB) API and applies
content-based recommendation logic within a clean, modular, and explainable
software architecture.
---
## 1. Introduction
With the rapid growth of online movie platforms and digital content libraries,
users are often overwhelmed by the vast number of available movies. Identifying
content that aligns with personal interests has become increasingly complex.
The Movie Recommendation Bot addresses this challenge by acting as an autonomous
intelligent agent that processes user input, analyzes movie metadata, and
generates personalized movie recommendations in real time.
This project is implemented as a recommendation bot rather than a static
application, emphasizing automation, autonomy, and decision-making logic.

---

## 2. Problem Statement
Conventional movie discovery approaches rely heavily on manual search and
browsing, which are time-consuming and inefficient. These methods often fail
to capture user intent beyond simple keyword matching.
The goal of this project is to design and implement a bot that:
- Accepts minimal user input
- Understands user preferences
- Filters large-scale movie data
- Produces concise, genre-aware recommendations
- Operates autonomously without human supervision

---

## 3. Project Objectives
The main objectives of the Movie Recommendation Bot are:
- Designing an AI-oriented movie recommendation bot
- Implementing content-based recommendation logic
- Integrating an external movie knowledge API
- Ensuring clear separation between backend logic and UI
- Following software engineering best practices
- Delivering a professional, GitHub-ready project

---

## 4. Why This System Is a Bot
This system qualifies as a bot because it:
- Reacts dynamically to user input
- Operates autonomously after execution
- Communicates with external knowledge sources
- Applies rule-based decision-making logic
- Generates structured and explainable outputs
- Requires no manual control during runtime

---

## 5. Recommendation Strategy
The Movie Recommendation Bot employs a Content-Based Recommendation Strategy.
Key properties of the implemented approach include:
- Similarity-based movie discovery
- Metadata-driven filtering
- Genre-based constraints
- Deterministic and explainable outputs
- No offline training or dataset preparation
The bot relies on similarity data provided by TMDB, ensuring low computational
overhead and continuously up-to-date recommendations.

---

## 6. Scientific & Technical Implementation
The backend of the bot is implemented using Flask, a lightweight Python web
framework responsible for request handling, routing, input validation, and
orchestration of system components.
Movie data is retrieved via the TMDB (The Movie Database) API, which serves
as an external knowledge base. The API provides access to movie metadata,
genre identifiers, ratings, similarity relationships, and poster images.
The backend communicates with TMDB using RESTful HTTP requests and processes
JSON responses in real time. Retrieved movies are filtered based on the
user-selected genre before being returned as structured recommendations.
The frontend is developed using HTML5 with the Jinja2 templating engine
to dynamically render results. CSS3 is used to enhance visual aesthetics,
layout consistency, and overall user experience.
This architecture follows a clear separation of concerns between:
- Logic (Flask backend)
- Structure (HTML)
- Presentation (CSS)

---

## 7. System Architecture Overview
### Input Layer
- User-provided movie title
- Genre selection via predefined TMDB genre IDs
### Processing Layer
- Input validation
- TMDB API requests
- Movie ID extraction
- Similar movie retrieval
- Genre-based filtering
- Result formatting and limiting
### Output Layer
- Movie recommendations
- Poster images
- Ratings
- Movie descriptions

---

## 8. Interaction & Data Flow
1. User accesses the bot interface
2. User enters a favorite movie
3. User selects a preferred genre
4. Bot validates the input
5. TMDB search endpoint is queried
6. Target movie ID is extracted
7. Similar movies are retrieved
8. Movies are filtered by genre
9. Top recommendations are selected
10. Results are rendered dynamically
---
## 9. Technology Stack
### Backend
- Python
- Flask
- Requests
### Frontend
- HTML5
- CSS3
### External API
- TMDB (The Movie Database)
---
## 10. Project Structure
movie-recommendation-bot/
│
├── app.py
│ └── Core bot logic and routing
│
├── requirements.txt
│ └── Bot requirements
│
├── index.html
│ └── Bot user interface
│
├── style.css
│ └── Bot styling
│
├── project.png
│ └── Screenshot of bot output
│
└── README.md

---

## 11. How to Run the Movie Recommendation Bot
This project is executed locally using a Flask development server.
### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Active internet connection (required for TMDB API)
### Step 1: Clone the Repository
```bash
git clone https://github.com/IliyaNazmehr/AI-Course/tree/main/Student-Projects/group12


### Step 2: Install Dependencies
```bash
pip install flask requests
### Step 3: Configure the API Key
Obtain an API key from TMDB and place it inside app.py:
TMDB_API_KEY = "YOUR_TMDB_API_KEY"
### Step 4: Run the Bot
python app.py
### Step 5: Access the Bot Interface
Open your web browser and navigate to:
http://localhost:5001
Once the page loads, enter a movie name, select a genre, and submit the form.
The bot will process the input and display movie recommendations in real time.
---

## Local Deployment Note 
*Due to the absence of a purchased domain and public hosting service,
*this project has been executed and demonstrated locally using localhost.
*The Movie Recommendation Bot runs on a local Flask development server,and all functionalities can be fully tested in this environment.
*A screenshot of the project output and user interface is provided in project.png, which displays the bot running successfully on localhost.

## Future Enhancements
* Secure API key management
* User preference persistence
* Collaborative and hybrid recommendation models
* Machine learning–based recommenders
* Public deployment with a domain
* Chatbot platform integration
* Multi-language support

---

## Educational Value
#This project demonstrates:
* Intelligent bot design
* API-driven recommendation systems
* Content-based filtering concepts
* Clean Flask architecture
* Backend–frontend integration
* Explainable AI logic
* Professional technical documentation

---

## Acknowledgments
* #TMDB for providing movie data
* #Flask open-source community
* #Recommendation system research community
---
## Academic Credentials
*Project Name: Movie Recommendation Bot
*Institution: Islamic Azad University, Tehran Central Branch (IAUCTB)
*Faculty: Faculty of Computer Science & Engineering
*Supervisor: Dr. Maryam Hajiesmaeili

## Group Members
- ## Saba Ghanadzadeh
- ## Roxana Norouzbegi
- Member 3
- Member 4
- ## Negar Habibi
