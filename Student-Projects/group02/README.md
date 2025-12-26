# Group 2

## source code
the following file contains the main n8n workflow used in this project:


{
  "name": "n8n telegram image",
  "nodes": [
    {
      "parameters": {
        "updates": [
          "message"
        ],
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.telegramTrigger",
      "typeVersion": 1.2,
      "position": [
        1376,
        240
      ],
      "id": "72fe64dc-c874-42d4-88f7-fff2656e1b74",
      "name": "Telegram Trigger",
      "webhookId": "a3bceba6-da22-4794-bb44-922f2e9b037b",
      "credentials": {
        "telegramApi": {
          "id": "t9ZuvXhdIxlp5ud9",
          "name": "Telegram account"
        }
      }
    },
    {
      "parameters": {
        "operation": "toBinary",
        "sourceProperty": "data[0].b64_json",
        "options": {}
      },
      "type": "n8n-nodes-base.convertToFile",
      "typeVersion": 1.1,
      "position": [
        1760,
        240
      ],
      "id": "d755aa4a-d790-4846-bf8f-ddae71eb8c3e",
      "name": "Convert to File"
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://router.huggingface.co/nebius/v1/images/generations",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Authorization",
              "value": "Bearer {{$env.HF_API_KEY}}"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "response_format",
              "value": "b64_json"
            },
            {
              "name": "prompt",
              "value": "=\"{{ $json.message.text }}\""
            },
            {
              "name": "model",
              "value": "black-forest-labs/flux-dev"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [
        1584,
        240
      ],
      "id": "31b905da-8265-4d5b-9a41-c8a48a244e67",
      "name": "Create Image"
    },
    {
      "parameters": {
        "operation": "sendPhoto",
        "chatId": "={{ $('Telegram Trigger').item.json.message.chat.id }}",
        "binaryData": true,
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [
        1920,
        240
      ],
      "id": "7e650085-d987-4afa-8ed3-feb3224f5964",
      "name": "Telegram",
      "webhookId": "851fda81-1ae1-4350-a288-5823a7f3507b",
      "credentials": {
        "telegramApi": {
          "id": "t9ZuvXhdIxlp5ud9",
          "name": "Telegram account"
        }
      }
    }
  ],
  "pinData": {},
  "connections": {
    "Telegram Trigger": {
      "main": [
        [
          {
            "node": "Create Image",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Convert to File": {
      "main": [
        [
          {
            "node": "Telegram",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Create Image": {
      "main": [
        [
          {
            "node": "Convert to File",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "449c31cc-e69f-477c-ad32-e8fc055fd361",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "18b1ed7f120aa14586cfdcccaebf39e081615446bc492bc6d7655eb45ce874d5"
  },
  "id": "6Y4YuW6UXAfZc66q",
  "tags": []
}
=======
Telegram AI Image Generator Bot

Implementation using n8n and Hugging Face API


1. Project Overview

This project implements an AI-based Telegram bot capable of generating images from textual prompts using a machine learning image generation model.
The system is developed using n8n workflow automation and integrates external AI services through RESTful APIs.

Users interact with the system via Telegram by sending a text prompt. The bot processes the request, sends it to an image generation API, and returns the generated image to the user.


2. Academic Information
• University: Islamic Azad University, Tehran Central Branch
• Course: Artificial Intelligence


3. Project Team Members

This project was developed by a group of five students:
• Member 1: (Full Name)
• Member 2: (sara ghavidel)
• Member 3: (Full Name)
• Member 4: (Full Name)
• Member 5: (Full Name)


4. Team Members and Responsibilities

Name Responsibility
Fateme Parvane Sekam Workflow design and system architecture
Sara ghavidel  API integration and configuration
amir Hesam sanako Telegram bot setup and testing
Raha  motahari Documentation and report preparation
Zahra doozandeh Debugging, validation, and final testing


5. Project Objectives

The main objectives of this project are:
• Gaining practical experience with workflow automation systems
• Integrating AI-based services via external APIs
• Developing a functional Telegram bot
• Understanding end-to-end AI service pipelines without heavy coding


6. System Architecture

The system follows an event-driven architecture:
1. Telegram receives user input.
2. n8n triggers the workflow.
3. The input text is sent to an AI image generation API.
4. The generated image is returned in Base64 format.
5. The image is converted to a binary file.
6. The final image is sent back to the user via Telegram.


7. Technologies and Tools
• n8n (Workflow Automation)
• Telegram Bot API
• Hugging Face Inference API
• HTTP / REST
• Base64 Image Encoding


8. APIs and External Services

8.1 Telegram Bot API

Used to:
• Receive user messages
• Send generated images to users

8.2 Hugging Face Image Generation API
• Provider: Hugging Face
• Model: black-forest-labs/flux-dev
• Task: Text-to-Image generation
• Response Format: Base64-encoded image


9. n8n Workflow Description

Telegram Trigger
      ↓
HTTP Request (Image Generation API)
      ↓
Convert Base64 to Binary File
      ↓
Telegram Send Photo

Each node performs a single, well-defined task, ensuring modularity, clarity, and ease of maintenance.


10. Project Structure

├── images/
│   ├── result1.png
│   ├── result2.png
├── README.md



11. Sample Results

11.1 Generated Image Example

Sample images generated by the bot are available in the images/ directory.
These images demonstrate the system’s ability to convert textual prompts into visual content.


12. Installation and Execution Guide

12.1 Prerequisites
• Installed n8n
• A Telegram Bot Token (via BotFather)
• A Hugging Face API Token

12.2 Setup Steps
1. Start n8n:

n8n start

2. Import the workflow file:

• Import n8n telegram image.json into n8n

3. Configure credentials:

• Telegram Bot Token
• Hugging Face API Token

4. Activate the workflow



12.3 Running the Bot
1. Open Telegram
2. Send a text prompt to the bot
3. Receive the generated image in response


13. Security Considerations
• API tokens must not be committed to public repositories
• Credentials are managed using n8n’s built-in credential system or environment variables
• Access to sensitive data is restricted and controlled



14. Testing and Evaluation
• Tested with multiple textual prompts
• Verified response time and image quality
• Ensured stable and consistent workflow execution



15. Project Outcomes
• Successful integration of AI-based image generation
• Reliable Telegram bot interaction
• Fully automated workflow with minimal manual intervention



16. Limitations (Free Trial Notice)

⚠️ This project uses third-party services that provide limited free trial access.
As a result:
 • The system may only be available for a limited time
 • Image generation may stop after the trial period ends
 • These limitations depend on the service provider’s policies and are beyond the developers’ control



17. Future Improvements
 • Support for image size and style selection
 • Logging and monitoring of user requests
 • Database integration for image storage
 • User interface and interaction enhancements



18. License

This project was developed for educational purposes only.



19. Acknowledgments

Special thanks to the course instructor and all team members for their contributions.
