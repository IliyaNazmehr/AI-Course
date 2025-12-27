# Group 23
# 🌴 California Travel Assistant - Chatbot 🤖

## ℹ️ Project Information


* 🎓 **Course:** Artificial intelligence
* 👩‍🏫 **Instructor:** Dr. Maryam Haji Esmaeili 
* 🏫 **Institution:** Tehran Markaz Islamic Azad University
* 📅 **Date:** December 2025
* 🚥 **Status:** ✅ Completed
* 👥 **Group Members:** Fatemeh Mahoori 


---

[![Rasa](https://img.shields.io/badge/Rasa-2.8.x-blueviolet.svg)](https://rasa.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A sophisticated chatbot designed to assist travelers with comprehensive California tourism information. This intelligent assistant integrates weather data, place recommendations, event information, and travel planning capabilities through multiple external APIs.

---

## 📸 Project Showcase


<img width="1124" height="777" alt="run 2" src="https://github.com/user-attachments/assets/35d1fabf-30dc-48cb-9267-95547d53cee7" />


---

## 🌟 Features

### 🌤 **1. Weather Information** (OpenWeather API)
- Real-time current weather conditions
- Temperature, humidity, and forecasts
- Weather alerts and severe weather warnings
- Multi-day weather forecasts

### 📍 **2. Places & Attractions** (Foursquare API)
- Search for restaurants, hotels, cafes, museums, etc.
- Find places near specific landmarks
- Filter results by amenities (outdoor seating, pet-friendly, etc.)
- Detailed place information including ratings and addresses

### 🎟️ **3. Events & Activities** (Eventbrite API)
- Search events by date range
- Filter events by price (free/paid)
- Check event capacity and availability
- Get ticket information and purchase details

### 🧠 **4. Intelligent Combinations**
- Weather-based activity recommendations
- Event weather impact analysis
- Personalized suggestions based on preferences
- Trip itinerary planning

### 🌟 **5. Safety & Practical Information**
- Emergency services location
- Seasonal activities guide
- Travel tips and practical information
- City comparisons for better decision making
    
---

## Core RASA Files

| File | Purpose | Key Components |
|------|---------|----------------|
| `nlu.yml` | Natural Language Understanding training data | - 50+ intent definitions<br>- 1000+ training examples<br>- Entity synonyms and lookup tables<br>- Regex patterns for date/time extraction |
| `rules.yml` | Conversation flow rules | - Basic interaction rules (greet, goodbye)<br>- Slot filling rules<br>- Fallback handling<br>- Service-specific rules |
| `stories.yml` | Conversation stories for training | - Sample conversation paths<br>- Success scenarios<br>- User journey templates |
| `domain.yml` | Bot domain configuration | - Intent definitions<br>- Entity declarations<br>- Slot configurations<br>- Response templates<br>- Action listings |
| `config.yml` | ML pipeline configuration | - DIET classifier settings<br>- Policy configurations<br>- Fallback thresholds<br>- Training parameters |
| `credentials.yml` | Channel credentials | - REST API configuration<br>- SocketIO for web interface<br>- Rasa X integration |




### **Custom Action Server** (`actions.py`)

This is the brain of the chatbot, containing all business logic:

| Section | Purpose | Key Actions |
|---------|---------|-------------|
| **Weather Actions** | Handle weather-related queries | `action_get_weather`, `action_get_temperature`, `action_get_forecast` |
| **Places Actions** | Manage location-based searches | `action_search_places_by_category`, `action_get_place_details` |
| **Events Actions** | Process event-related requests | `action_search_events_by_date_range`, `action_get_event_ticket_info` |
| **Combination Actions** | Provide integrated recommendations | `action_weather_based_recommendations`, `action_event_weather_impact` |
| **Personalization** | Deliver customized suggestions | `action_personalized_recommendations`, `action_create_itinerary` |
| **Utility Actions** | Support and helper functions | `action_validate_city`, `action_reset_slots`, fallback handlers |




### **Frontend Interface**

| File | Purpose | Technologies |
|------|---------|--------------|
| `index.html` | Main web interface | HTML5, Font Awesome icons, Google Fonts |
| `style.css` | Styling and animations | CSS3 with custom variables, responsive design |
| `script.js` | Client-side logic | Vanilla JavaScript, Socket.IO for real-time updates |




### **Configuration Files**

| File | Purpose |
|------|---------|
| `endpoints.yml` | Server endpoint configurations |
| `requirements.txt` | Python dependencies (not shown but required) |


---

## 🔧 API Integrations

### **1. OpenWeather API**
- **Usage**: Fetch real-time weather data
- **Key Functions**: `_call_openweather_api()`
- **Data Retrieved**: Temperature, humidity, conditions, alerts
- **Location**: California cities only

### **2. Foursquare API**
- **Usage**: Search for points of interest
- **Key Functions**: `_call_foursquare_api()`
- **Data Retrieved**: Places, categories, ratings, addresses
- **Features**: Category filtering, proximity search, amenity filters

### **3. Eventbrite API**
- **Usage**: Find local events and activities
- **Key Functions**: `_call_eventbrite_api()`
- **Data Retrieved**: Events, dates, venues, ticket info
- **Filters**: Date range, price, capacity

---

## 🏷️ Tech Stack 

* **Framework:** Rasa Open Source (2.8.x)
* **Backend:** Python 3.8+
* **Libraries:** `requests`, `urllib3`, `rasa-sdk`
* **Frontend:** HTML5, CSS3, Vanilla JS, Socket.IO 4.7.2
* **UI Elements:** Font Awesome 6.4.0, Google Fonts (Poppins)

---

## 📦 Dependencies

To run this project, you need to install the following Python libraries. It is recommended to use a virtual environment.

### **Python Libraries** (`requirements.txt`)
```python
rasa==2.8.27             # Core RASA framework
rasa-sdk==2.8.10         # SDK for custom actions
requests==2.31.0         # HTTP requests for API calls
python-dateutil==2.8.2   # Date parsing and manipulation
sqlalchemy==2.0.23       # Database for conversation tracking

```

## 📁 Project Structure

### **🌳 File Tree**

```python
california-travel-assistant/
├── 📂 data/
│   ├── 📄 nlu.yml          # Natural Language Understanding training data
│   ├── 📄 rules.yml        # Conversation flow rules
│   └── 📄 stories.yml      # Training conversation stories
├── 📂 actions/             # Custom Action Server Directory
│   └── 🐍 actions.py       # Main Python logic for API integrations
├── 📄 domain.yml           # Bot domain configuration (Slots, Actions, Responses)
├── 📄 config.yml           # Machine Learning pipeline & policies configuration
├── 📄 credentials.yml      # Authentication & Channel credentials
├── 📄 endpoints.yml        # Server endpoint configurations (Action server & Tracker)
├── 📄 requirements.txt     # List of Python dependencies
│
└── 📂 frontend/            # Web Interface Files
    ├── 🌐 index.html       # Responsive HTML5 chat interface
    ├── 🎨 style.css        # California-themed CSS styling
    └── ⚡ script.js        # Frontend logic & Socket.IO communication
```


---

# California Travel Assistant Chatbot - Complete Guide

## 📋 Project Overview

This is an AI-powered conversational chatbot designed to assist travelers with comprehensive California tourism information. The chatbot integrates multiple external APIs (OpenWeather, Foursquare, Eventbrite) to provide real-time weather data, place recommendations, event information, and personalized travel planning.

## 🏗️ Project Architecture

### **Frontend Layer**

```python
├── index.html # Main web interface with California-themed design
├── style.css # Responsive styling with animations
└── script.js # Client-side logic with Socket.IO integration
```

### **RASA Conversational AI Layer**

```python
├── nlu.yml # Natural Language Understanding training data
├── domain.yml # Bot domain configuration
├── stories.yml # Conversation flow examples
├── rules.yml # Business logic rules
├── config.yml # Machine learning pipeline configuration
└── credentials.yml # Channel authentication settings
```

### **Backend & Integration Layer**

```python
├── actions.py # Custom action server with business logic
├── endpoints.yml # Server endpoint configurations
└── requirements.txt # Python dependencies
```

---

## 📁 Detailed File Explanations

### **1. Natural Language Understanding (nlu.yml)**
This file contains the training data for intent recognition and entity extraction.

**Key Sections:**
- **Intents**: 50+ user intentions with 1000+ training examples
- **Entities**: City names, place categories, date ranges, filters
- **Synonyms**: Alternative terms (LA = Los Angeles, SF = San Francisco)
- **Regex Patterns**: For dates, phone numbers, price ranges
- **Lookup Tables**: California cities, activity types, landmarks

**Purpose**: Teaches the bot to understand user queries like "What's the weather in Los Angeles?" or "Find Italian restaurants in San Francisco."

### **2. Domain Configuration (domain.yml)**
Defines the chatbot's universe - everything it needs to know about.

**Components:**
- **Intents**: All possible user intentions
- **Entities**: Information to extract from user messages
- **Slots**: Memory variables (city, date_range, preferences)
- **Responses**: Predefined bot responses
- **Actions**: Custom Python functions and utterance actions

**Purpose**: Creates a comprehensive knowledge base for the chatbot.

### **3. Conversation Rules (rules.yml)**
Handles specific conversation patterns that should always follow the same path.

**Example Rules:**
- When user says "hello" → respond with greeting
- When asking for weather without city → ask for city
- When user says "thank you" → respond appropriately

**Purpose**: Ensures consistent behavior for common interactions.

### **4. Conversation Stories (stories.yml)**
Training examples for complex, multi-turn conversations.

**Example Story:**

```text
**User:** "What's the weather in Los Angeles?"  
**Bot:** Shows weather information

**User:** "Find restaurants there"  
**Bot:** Shows restaurant recommendations
```

**Purpose**: Teaches the bot how to handle multi-step conversations.

### **5. Machine Learning Configuration (config.yml)**
Defines the NLP pipeline and training policies.

**Key Components:**
- **DIET Classifier**: For intent and entity recognition
- **TED Policy**: For dialogue management
- **Rule Policy**: For rule-based conversations
- **Fallback Classifier**: For handling low-confidence predictions

**Purpose**: Configures how the AI model learns and makes decisions.

### **6. Custom Actions (actions.py)**
The brain of the chatbot - contains all business logic and API integrations.

**Main Functions:**
- **API Handlers**: Connect to OpenWeather, Foursquare, Eventbrite
- **Weather Actions**: Get current weather, forecasts, alerts
- **Place Actions**: Search for restaurants, hotels, attractions
- **Event Actions**: Find events, get ticket information
- **Personalization**: Generate customized recommendations
- **Error Handling**: Graceful fallbacks and user-friendly messages

**Purpose**: Executes all complex operations and external API calls.

## Core Libraries & Dependencies

### **Required Libraries**

| Library | Purpose |
|---------|---------|
| `rasa_sdk` | Framework for building Rasa custom actions |
| `requests` | HTTP requests to external APIs (OpenWeather, Foursquare, Eventbrite) |
| `datetime` | Date and time manipulation for event handling |
| `urllib.parse` | URL encoding for API parameters |
| `logging` | Application logging and error tracking |
| `random` | Mock data generation for development |
| `json` | JSON data parsing |

#### **1. API Configuration Class**

```python
class APIConfig
```
- Centralized API configuration for weather, places, and events services
- Stores API keys, endpoints, and default parameters
- Designed to be populated from `credentials.yml` in production


#### **2. Mock Data & Action Overview**

#### 🛠️ 1. MockData Class
- 📝 Provides synthetic data for development/testing when APIs are unavailable  
- 🎯 Generates realistic mock responses for weather, places, and events  
- ⚡ Ensures chatbot functionality during API quota exhaustion or offline development


#### 🚀 2. Action Categories

##### ☀️ Weather Actions
- **ActionGetWeather:** Current weather conditions  
- **ActionGetTemperature:** Specific temperature queries  
- **ActionGetHumidity:** Humidity level reporting  
- **ActionGetForecast:** Short-term weather outlook  
- **ActionGetWeatherAlerts:** Severe weather warnings  

##### 🏙️ Places Actions
- **ActionSearchPlacesByCategory:** Category-based POI search  
- **ActionSearchPlacesNearLocation:** Landmark proximity searches  
- **ActionSearchPlacesWithFilters:** Feature-filtered place searches  
- **ActionGetPlaceDetails:** Comprehensive place metadata  

##### 🎉 Events Actions
- **ActionSearchEventsByDateRange:** Time-based event discovery  
- **ActionSearchEventsByPrice:** Budget-friendly event filtering  
- **ActionSearchEventsWithCapacity:** Event availability checking  
- **ActionGetEventTicketInfo:** Ticketing and pricing details  

##### 🔗 Combination Actions
- **ActionWeatherBasedRecommendations:** Weather-aware activity suggestions  
- **ActionEventWeatherImpact:** Weather risk analysis for events  
- **ActionPersonalizedRecommendations:** User-profile-based suggestions  

##### 🗺️ Trip Planning Actions
- **ActionCreateItinerary:** Custom travel schedule generation  
- **ActionCompareLocations:** Comparative analysis between destinations  
- **ActionGetPracticalInfo:** Operational details (hours, pricing, transport)  
- **ActionGetSeasonalActivities:** Time-of-year specific suggestions  

##### ⚙️ Utility Actions
- **ActionValidateCity:** California city validation  
- **ActionSaveUserPreferences:** User preference persistence  
- **ActionResetSlots:** Conversation state clearing  
- **ActionDefaultFallback:** Primary fallback handler  
- **ActionTwoStageFallback:** Ambiguity resolution mechanism  



#### 🧰 3. Helper Functions

##### 🌐 API Call Functions
- `_call_openweather_api()`: OpenWeather API integration  
- `_call_foursquare_api()`: Foursquare Places API v3 integration  
- `_call_eventbrite_api()`: Eventbrite event discovery  

##### 🛡️ Utility Functions
- `get_slot_value()`: Safe slot value retrieval  
- `validate_city()`: California city validation  
- `format_weather_response()`: Weather data formatting  
- `format_place_response()`: Place information formatting  
- `format_event_response()`: Event data formatting



### **7. Web Interface (index.html, style.css, script.js)**
Modern, responsive web interface for interacting with the chatbot.

**Features:**
- Real-time messaging with Socket.IO
- California-themed design with animated stickers
- Quick action buttons for common queries
- Typing indicators and message timestamps
- Mobile-responsive layout

**Purpose**: Provides an intuitive user interface for the chatbot.

#### 📄 index.html — User Interface Structure

**Responsibilities:**
- Defines the chat layout and visual structure
- Contains the chat header, message area, input box, and quick action buttons
- Loads external libraries and local assets

**Key Features:**
- California-themed UI (sun, palm tree, sea)
- Chat header with bot identity and online status
- Message container for user & bot messages
- Typing indicator for realistic conversation flow
- Quick action buttons for common queries
- Fully responsive layout

**Technologies Used:**
- HTML5
- Font Awesome (icons)
- Google Fonts (Poppins)


## 🎨 style.css — Styling & Animations

**Responsibilities:**
- Defines the visual identity of the chatbot
- Ensures responsive behavior across devices
- Adds animations and interactive feedback

**Key Design Elements:**
- CSS Variables for centralized theming
- Gradient backgrounds and soft shadows
- Distinct styles for user vs bot messages
- Typing indicator animation
- Hover effects and smooth transitions
- Mobile-friendly responsive design

**UI/UX Highlights:**
- Clear separation between user and bot messages
- Readable typography and spacing
- Subtle decorative stickers for branding
- Smooth message appearance animations



## ⚙️ script.js — Client-Side Logic

**Responsibilities:**
- Handles user input and message rendering
- Communicates with the Rasa backend
- Manages typing effects and UI updates
- Integrates with external APIs (optional)



### 🔌 Rasa Integration

The frontend communicates with the Rasa server using REST API:

```javascript
POST http://localhost:5005/webhooks/rest/webhook
```


## 🔄 Workflow

1. User types a message
2. Message is sent to Rasa via `fetch`
3. Rasa processes the message (NLU + Core + Actions)
4. Bot responses are returned as JSON
5. Responses are rendered in the chat UI

---

## 🧠 Model Training Process

### **Step 1: Data Preparation**

```python
┌─────────────────────────────────────────────┐
│ 1. Define intents in nlu.yml │
│ 2. Create entity synonyms and patterns │
│ 3. Write conversation stories │
│ 4. Define business rules │
└─────────────────────────────────────────────┘
```

### **Step 2: Configuration Setup**

Configure the ML pipeline in `config.yml`:
- Choose appropriate NLU components (DIETClassifier)
- Set training policies (TEDPolicy, RulePolicy)
- Configure fallback thresholds
- Set training epochs and batch sizes

### **Step 3: Training Execution**

```bash
# Train both NLU and dialogue management models
rasa train

# Expected output:
# ✓ Training NLU model...
# ✓ Training Core model...
# ✓ Models trained successfully and saved to 'models/'
```

### **Step 4: Model Evaluation**

```bash
# Test NLU model performance
rasa test nlu --nlu data/nlu.yml

# Test dialogue management
rasa test core --stories data/stories.yml

# Cross-validation for better evaluation
rasa test --cross-validation
```

### **Step 5: Model Optimization**

Based on test results:

- Add more training examples for low-confidence intents
- Adjust pipeline components in `config.yml`
- Fine-tune hyperparameters (epochs, batch size)
- Update stories and rules based on conversation failures

---

# 🔄 Complete Project Workflow

## Phase 1: Setup & Configuration
* **Install dependencies:** Run `pip install -r requirements.txt` to set up the Python environment.
* **Obtain API Keys:** Register and get keys for:
    * OpenWeather
    * Foursquare
    * Eventbrite
* **Configuration:** Securely add your API keys into `actions.py`.
* **Environment:** Finalize the development environment setup.


## Phase 2: Model Training & Development
1.  **NLU Definition:** Define intents and entities based on specific use cases.
2.  **Data Creation:** Generate diverse training examples for robust intent recognition.
3.  **Stories:** Write conversation stories to handle complex dialogue flows.
4.  **Custom Actions:** Program the logic for each intent in the actions server.
5.  **Training:** Execute `rasa train` to build the model.
6.  **Local Testing:** Use `rasa shell` to interact with the bot and debug.


## Phase 3: Integration & Deployment
1.  **Action Server:** Start the custom action server: `rasa run actions`.
2.  **Rasa Server:** Launch the main server: `rasa run --enable-api --cors "*"`.
3.  **UI Connection:** Configure the web interface/frontend to communicate with the Rasa API.
4.  **E2E Testing:** Verify end-to-end functionality from the user interface.
5.  **Production:** Deploy the stack to your production environment.


## Phase 4: Monitoring & Improvement
* **Logging:** Collect and review user conversation logs.
* **Analysis:** Identify frequently misunderstood intents or failed stories.
* **Optimization:** Add more training examples to address weak points.
* **Iteration:** Retrain the model and redeploy.
* **Feedback Loop:** Continuously update the bot based on real-world user feedback.

---

### 🚀 **Implementation Guide**


📦 **Step 1: Install Python Dependencies**  

Install all required libraries using `requirements.txt`:

```bash
pip install -r requirements.txt
```

🧩 **Step 2: Configure API Keys**

Update the API configuration in actions.py :
```python
class APIConfig:
    OPENWEATHER_API_KEY = "your_openweather_api_key"
    FOURSQUARE_API_KEY = "your_foursquare_api_key"
    EVENTBRITE_TOKEN = "your_eventbrite_token"
```

🧠 **Step 3: Train the AI Model**

Train the Rasa NLU and Core models using your data.
```bash
rasa train
```

⚡ **Step 4: Run the Assistant**  

You will need two separate terminals to run the bot:

- **Terminal 1 (Action Server):** Runs the Python logic for APIs.
```bash
rasa run actions
```
- **Terminal 2 (Rasa Server):** Runs the main bot engine.
```bash
rasa run --enable-api --cors "*"
```

🌐 **Step 5: Launch the Interface**  

Once both servers are running, simply open the `index.html` file in your web browser to start chatting , or serve it locally!
```bash
python -m http.server 8000
```

---

## 🔄 End-to-End Example: How Rasa Files Work Together

### 🧑 User Input
The user types the following message in the chatbot:

> **"What's the weather in Los Angeles?"**

---

### 🧠 Step 1: `nlu.yml` — Understanding the Message

- Rasa NLU receives the user message.
- The model uses training data in `nlu.yml` to:
  - Detect the **intent** → `ask_weather`
  - Extract the **entity** → `city = Los Angeles`
- If synonyms are defined (e.g., `LA → Los Angeles`), the city name is normalized.

✅ Output of this step:
```text
Intent: ask_weather
Entity: city = Los Angeles
```

## 🧭 Step 2: `rules.yml` and `stories.yml` — Deciding What to Do Next

Rasa Core now decides how to respond.

It checks:

- **`rules.yml`** → Are there any fixed rules for this intent?
- **`stories.yml`** → What is the best next action based on learned conversation flows?

The model decides to execute a custom action:

- **`ActionGetWeather`**


## ⚙️ Step 3: `actions.py` — Executing Business Logic

`ActionGetWeather` is executed from `actions.py`.

Inside the action:

- The `city` slot is read (**Los Angeles**)
- The OpenWeather API is called via `_call_openweather_api()`
- If APIs are unavailable, **MockData** is used instead


## 🌐 Step 4: External API or MockData

- The weather service returns raw data (temperature, condition, humidity)
- Helper functions format the data:
  - `format_weather_response()`

**Example formatted result:**
```text
"It's currently 22°C and sunny in Los Angeles."
```

## 💬 Step 5: Sending the Response to the User

- The formatted message is sent back to Rasa
- Rasa delivers the response to the frontend (web interface)
- The user sees the answer in the chat window

---

## 📸 System Architecture & Date Flow


<img width="2755" height="2712" alt="diagram_1" src="https://github.com/user-attachments/assets/c4aed3a8-b5c9-42a8-9951-960c1fbcb05e" />


---

## 🧩 File Interaction Summary

| Step | File Involved | Responsibility |
|------|--------------|----------------|
| 1 | `nlu.yml` | Understand intent & extract entities |
| 2 | `rules.yml` / `stories.yml` | Decide next action |
| 3 | `actions.py` | Execute logic & API calls |
| 4 | APIs / MockData | Fetch or simulate data |
| 5 | Frontend | Display response to user |

---

## ⚠️ Current Limitations & Future Work
- Limited to California cities only
- API rate limits may affect response speed
- Event availability depends on Eventbrite coverage

**Group Members:** Fatemeh Mohammad Beigi
