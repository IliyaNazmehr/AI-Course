# Person Guesser From Image

An intelligent Telegram bot that analyzes images with multiple people and plays an interactive guessing game! The bot uses advanced AI-powered face detection and analysis to identify various facial attributes, then challenges users to a guessing game where it tries to identify which person the user is thinking of through strategic yes/no questions.

> **University Course Project**  
> This project was developed as part of an AI course assignment by Group 24.  
> **[Islamic Azad University Central Tehran Branch](https://ctb.iau.ir/en)**  
> Faculty of Convergent and Quantum Sciences and Technologies

## Team Members

**Group 24**

- Mohammad Amin Jafarian ([@BaziForYou](https://github.com/BaziForYou))
- Mohammad Hossein Meftah ([@MHKEY81](https://github.com/MHKEY81))
- Sabrineh Pourmarashi ([@puormarashisabrineh](https://github.com/puormarashisabrineh))
- Sarina Soleimany Rad ([@SarinaRad](https://github.com/SarinaRad))
- Ilia Asghari ([@ilia-ast](https://github.com/ilia-ast))


## Features

### Advanced Face Analysis
- **Multi-face Detection**: Detects and analyzes up to 20 faces in a single image
- **Eye Color Analysis**: Detailed eye color identification with RGB/HSL/HEX values
- **Hair Color Detection**: Accurate hair color analysis using advanced clustering algorithms
- **Skin Tone Classification**: Comprehensive skin tone analysis including Fitzpatrick scale
- **Facial Expression Recognition**: Detects emotions with confidence scores (happy, sad, neutral, angry, etc.)
- **Head & Gaze Direction**: Tracks where each person is looking and head orientation
- **Eye State Detection**: Identifies if eyes are open, closed, or blinking
- **Mouth State Analysis**: Detects if mouth is open/closed with percentage measurements
- **Distance Estimation**: Calculates approximate distance from camera
- **Hand Gesture Recognition**: Detects and identifies hand gestures in the image
- **Body Posture Analysis**: Analyzes body positioning and posture

### Interactive Guessing Game
- **AI-Powered Questions**: Uses OpenAI API to generate strategic yes/no questions
- **Smart Question Strategy**: AI asks about distinctive features to narrow down candidates
- **Maximum Questions Limit**: Configurable question limit (default: 20 questions)
- **Guess Verification**: User confirms if the AI's guess is correct or wrong
- **Retry Mechanism**: If wrong, AI continues with remaining questions
- **Detailed Analysis Summary**: Shows comprehensive facial analysis after correct guess
- **Annotated Image Output**: Visual representation of all detected faces with bounding boxes

### Timeout Management System
- **State-Specific Timeouts**: Different timeout limits for each game phase
  - Naming phase: 1 minute
  - Question phase: 2 minutes per question
  - Guess verification: 2 minutes
- **Total Game Timeout**: Automatic game expiration based on maximum questions
- **Automatic Cleanup**: Expired games are automatically removed
- **Session Tracking**: Tracks last response time and game start time

### Clean Architecture
- **Modular Handler Functions**: Separate handlers for different game states
- **State Machine**: Clean state transitions (analyzing → naming → playing → guessVerify)
- **Error Handling**: Comprehensive error handling throughout the application
- **Session Management**: UUID-based game session tracking

## Getting Started

### Prerequisites

- **Docker**: Version 20.x or higher (for Docker installation)
- **Docker Compose**: Version 2.x or higher (recommended for Docker)
- **Node.js**: Version 18.x or higher (for source installation)
- **npm**: Version 8.x or higher (for source installation)
- **Telegram Bot Token**: Obtain from [@BotFather](https://t.me/botfather)
- **OpenAI API Key**: Required for the AI guessing game logic
- **OpenAI-compatible API Endpoint**: Can use OpenAI, Azure OpenAI, or other compatible services

### Installation

#### Method 1: Docker Installation (Recommended)

1. **Get the source code**
   
   Download or clone this repository to your local machine, then navigate to the project directory in your terminal.

2. **Create environment file**
   
   Create a `.env` file in the root directory with all required variables (see Configuration section below)

3. **Build and start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

5. **Stop the bot**
   ```bash
   docker-compose down
   ```

**Docker Features:**
- Smart npm install: Validates existing `node_modules` if copied, only reinstalls if needed
- Auto-restart: Container automatically restarts unless manually stopped
- Latest Node.js: Uses the latest stable Node.js version
- Optimized build: Includes all necessary system dependencies for canvas and TensorFlow

**Alternative: Using Docker directly (without Compose)**

1. **Build the image**
   ```bash
   docker build -t person-guesser-bot .
   ```

2. **Run the container**
   ```bash
   docker run -d --name person-guesser-bot --env-file .env --restart unless-stopped person-guesser-bot
   ```

3. **View logs**
   ```bash
   docker logs -f person-guesser-bot
   ```

4. **Stop the container**
   ```bash
   docker stop person-guesser-bot
   docker rm person-guesser-bot
   ```

#### Method 2: Source Installation (Alternative)

1. **Get the source code**
   
   Download or clone this repository to your local machine, then navigate to the project directory in your terminal.

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   
   Create a `.env` file in the root directory (see Configuration section below for required variables)

4. **Configure environment variables** (see Configuration section below)

5. **Start the bot**
   ```bash
   npm start
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here

# OpenAI API Configuration
API_KEY=your_openai_api_key_here
API_URL=https://api.openai.com/v1
API_MODEL=gpt-5-mini

# Game Configuration
MAX_QUESTIONS=20
```

### Environment Variables Explained

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Your Telegram bot token from @BotFather | ✅ Yes | - |
| `API_KEY` | OpenAI or compatible API key | ✅ Yes | - |
| `API_URL` | Base URL for OpenAI-compatible API | ✅ Yes | - |
| `API_MODEL` | AI model to use for chat completions | ✅ Yes | - |
| `MAX_QUESTIONS` | Maximum questions allowed per game | ❌ No | 20 |

## How to Use

### Starting a Game

1. **Start the bot**: Send `/start` command to the bot
2. **Upload an image**: Send an image (JPG or PNG) with at least 2 people
3. **Wait for analysis**: The bot will analyze all faces in the image
4. **Name the people**: Assign names to each detected person (letters only)
5. **Think of a person**: Choose one person from the image mentally
6. **Answer questions**: Respond to AI's yes/no questions with buttons
7. **Verify guess**: Confirm if AI's guess is correct or wrong
8. **See results**: View detailed analysis summary if guess is correct

### Available Commands

- `/start` - Start the bot and see welcome message
- `/cancel` - Cancel the current game session

### Game Flow

```
Upload Image → Image Analysis → Face Naming → Start Game
     ↓
Answer Yes/No/Unsure Questions ↔ AI Asks Strategic Questions
     ↓
AI Makes a Guess → Verify Correct/Wrong
     ↓
Correct: Show Detailed Analysis | Wrong: Continue with Remaining Questions
```

## Demo Video

<video src="https://github.com/user-attachments/assets/f63bd147-35b6-4ad2-b56e-3287c2d80eda" controls></video>

## Project Structure

```
Person_Gusser_From_Image/
├── index.js              # Main bot application with Telegraf handlers
├── imageAnalyze.js       # Face detection and analysis using Human.js
├── apiChat.js            # OpenAI API integration and game logic
├── package.json          # Node.js dependencies and scripts
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose orchestration file
├── .env                  # Environment configuration (not in repo)
└── README.md             # Project documentation
```

## Core Components

### 1. Image Analysis Engine (`imageAnalyze.js`)

- Uses **@vladmandic/human** library for face/body/hand detection
- Implements advanced color analysis algorithms:
  - K-means clustering for dominant color extraction
  - RGB to HSL conversion for color classification
  - Euclidean distance for nearest color name matching
- Extracts facial features from specific regions (iris, skin, hair)
- Applies polygon-based masking to isolate target areas
- Generates debug visualizations for color analysis

### 2. AI Chat System (`apiChat.js`)

- Initializes guessing game with analyzed face data
- Manages conversation context with OpenAI API
- Implements strict rules for AI question generation:
  - Must ask about observable attributes only
  - Cannot ask about individual names (minimum 3 people for group questions)
  - Must track question numbers and eliminated candidates
- Formats data efficiently to reduce token usage
- Handles JSON-formatted AI responses

### 3. Telegram Bot (`index.js`)

**State Management:**
- `analyzing` - Processing uploaded image
- `naming` - User assigning names to detected faces
- `playing` - Active Q&A game session
- `guessVerify` - Waiting for guess verification

**Modular Handlers:**
- `handleCancelCallback()` - Game cancellation
- `sendGuessMessage()` - Display AI's guess with verification buttons
- `sendNextQuestion()` - Present next question with Yes/No/Unsure buttons
- `handlePlayingState()` - Process user answers and get AI response
- `handleMaxQuestionsReached()` - Force final guess at question limit
- `handleCorrectGuess()` - Display detailed analysis summary
- `handleWrongGuess()` - Handle retry logic or game end
- `handleGuessVerifyState()` - Route to correct/wrong handlers

**Timeout System:**
- Validates game sessions against multiple timeout criteria
- Automatically cleans up expired games
- Notifies users when sessions expire

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Node.js** | Runtime environment |
| **Docker** | Containerization platform |
| **Telegraf** | Telegram Bot API framework |
| **@vladmandic/human** | Face/body/hand detection and analysis |
| **TensorFlow.js** | Machine learning backend for Human.js |
| **Canvas** | Image manipulation and processing |
| **OpenAI API** | AI-powered question generation and game logic |
| **ml-kmeans** | K-means clustering for color analysis |
| **color-name-list** | Comprehensive named color database |
| **colornamer** | Simple color name identification |
| **dotenv** | Environment variable management |
| **uuid** | Unique game session identifiers |


## Privacy & Data

- **No Data Storage**: All game data is stored in memory only
- **Automatic Cleanup**: Games are deleted after completion or timeout
- **No Image Persistence**: Images are processed and discarded
- **Session-Based**: Each user has isolated game sessions

## Acknowledgments

- [@vladmandic/human](https://github.com/vladmandic/human) - Excellent face detection library
- [Telegraf](https://github.com/telegraf/telegraf) - Powerful Telegram bot framework
- [OpenAI](https://openai.com/) - AI-powered conversation capabilities
- [TensorFlow.js](https://www.tensorflow.org/js) - Machine learning in JavaScript

## Example Output

After a successful guess, the bot provides detailed analysis:

```
Detailed Analysis Summary:

┌─ Basic Information
│  • Age: ~24 years old
│  • Gender: female (98% confidence)
│
├─ Emotions
│  • Primary Emotion: neutral (85% confidence)
│  • All Emotions:
│     - neutral: 85%
│     - happy: 10%
│
├─ Eye Details
│  • Eye Color: Greyish Blue (blue)
│    Category: blue
│    Confidence: 78%
│  • Eye State: Both eyes open
│
├─ Hair Details
│  • Hair Color: Wheatberry (blonde)
│    Category: blonde
│    Confidence: 82%
│
├─ Skin Details
│  • Skin Tone: fair
│  • Undertone: neutral
│  • Fitzpatrick: Type II
│  • Confidence: 91%
│
├─ Mouth State
│  • Mouth: slightly open (15%)
│
├─ Direction & Position
│  • Head Direction: looking at camera
│  • Gaze Direction: looking at camera
│  • Distance: 1.2m (medium distance)
└─────────────
```

---
