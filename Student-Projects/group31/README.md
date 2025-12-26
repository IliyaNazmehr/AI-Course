# Group 31
## Project by:
**Shirin Abdolahzade For Dr. Maryam Hajiesmaeili --- Group Number 31 @IAUCTB**
# University Chatbot Project

This is our university group project: a simple chatbot that answers questions about the university and anything else you need!  We built it using Node.js on the backend and the OpenAI API to generate answers. The frontend is clean, academic-style HTML with a chat interface, and it allows switching between different GPT models (GPT-4O-Mini, GPT-4.1-Mini, and GPT-3.5-Turbo). It’s designed to be easy to run and test, perfect for a small project or demo.

## Project Overview
- A fast, local backend that communicates with the OpenAI API to generate human-like responses.
- A responsive, academic-style chat interface.
- Model switching capability to compare responses across GPT models.
- Easy setup and runnable with minimal commands.

## APIs and libraries used
- OpenAI API: For generating AI-driven responses.
- Node.js and Express: Lightweight server to handle API requests and connect the frontend.
- cors: Enables cross-origin requests during development.
- dotenv: Manages environment variables securely (e.g., API keys and port).
- Frontend: Plain HTML/CSS/JavaScript for a minimal, dependency-free UI.

## Why these libraries?
- Node.js and Express provide a simple, well-supported backend suitable for small projects.
- dotenv keeps sensitive keys out of the source code.
- The OpenAI API provides high-quality AI responses without maintaining an in-house model.
- A plain HTML frontend ensures cross-platform compatibility and easy customization for documentation or demos.

## What you need

1. **Node.js** (LTS version) – download and install it from the official site (https://nodejs.org/). Make sure `node -v` and `npm -v` work in your terminal.
2. **OpenAI API Key** – we didn't include our key for security, so you need to get your own and put it in a `.env` file. to get your own API KEY visit OpenAI website and obtain it from there. or click here:
  https://platform.openai.com/api-keys

## Setup

1. Put the folder somewhere on your computer.
2. Make sure you have `background.jpg` in the same folder as `chatbot_frontend.html` (you can replace it with your own image if you want).
3. Open a terminal inside the project folder and run:
Make sure you see the versions of the packages we need, if you get an error regarding the packages not being installed, kindly install them onto your device.
```
node -v
```
```
npm -v
```


This will check all the dependencies (express, cors, dotenv, openai, etc).

## Environment Variables

Create a file called `.env` in the project folder and put your API key in it:

```
OPENAI_API_KEY=KEYHERE
PORT=3000
```

## Running the Project

1. Start the backend server in the terminal INSIDE the folder with the contents:

```
node server.js
```

or, if you have `nodemon`:

```
nodemon server.js
```

You should see:

```
Server listening at http://localhost:3000
```

2. Open `chatbot_frontend.html` in your browser.
3. Type a question, click send, and see the chatbot reply.
4. You can also click the buttons to switch between GPT models (GPT-4O-Mini, GPT-4.1-Mini, GPT-3.5-Turbo).

## Security

- Do not commit .env; use .env.example for guidance.
- Rotate API keys if exposure occurs.
- Validate and sanitize user input on the server.
- Consider enabling logging and access controls for production.
- Use HTTPS in production; keep dependencies up to date.
- Regularly review dependencies for known vulnerabilities and apply updates.


## Notes

* If something goes wrong, restart the server.
* To stop the server, press Ctrl + C.
* To update the server safely, stop it first, save changes, then start it again.

## Included Files

* `server.js` – backend code
* `chatbot_frontend.html` – frontend with chat box and model buttons
* `package.json` – project dependencies
* `README.md` – this file
* `background.jpg` – background image (replace if you want)
* `node_modules` required files/modules
* `HOW_TO_RUN.md` – Simplified Version of the README and its contents
* `package-lock.json`
