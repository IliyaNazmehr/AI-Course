// =====================================================
// CALIFORNIA TRAVEL ASSISTANT - CLIENT-SIDE LOGIC
// =====================================================
// Main JavaScript for chat interface functionality
// 
// Responsibilities:
// 1. UI Management: Message display, animations
// 2. Rasa Communication: Send/receive messages to AI backend
// 3. Event Handling: User input and button interactions
// 4. API Integration: External services (OpenWeather, Foursquare, Eventbrite)
//
// Note: This file contains both Rasa integration and fallback legacy APIs
// =====================================================


// API Configuration
const RASA_SERVER_URL = 'http://localhost:5005/webhooks/rest/webhook';
const API_CONFIG = {
    openWeatherMap: {
        apiKey: 'YOUR_OPENWEATHERMAP_API_KEY', // Replace with your key
        baseUrl: 'https://api.openweathermap.org/data/2.5/weather'
    },
    foursquare: {
        clientId: 'YOUR_FOURSQUARE_CLIENT_ID', // Replace with your client ID
        clientSecret: 'YOUR_FOURSQUARE_CLIENT_SECRET', // Replace with your client secret
        baseUrl: 'https://api.foursquare.com/v3/places/search'
    },
    eventbrite: {
        apiKey: 'YOUR_EVENTBRITE_API_KEY', // Replace with your key
        baseUrl: 'https://www.eventbriteapi.com/v3/events/search/'
    }
};

// California cities for reference
const CALIFORNIA_CITIES = [
    'los angeles', 'san francisco', 'san diego', 'sacramento', 
    'san jose', 'fresno', 'long beach', 'oakland', 'bakersfield',
    'anaheim', 'santa ana', 'riverside', 'stockton', 'chula vista',
    'irvine', 'fremont', 'san bernardino', 'modesto', 'fontana',
    'moreno valley', 'santa clarita', 'oxnard', 'huntington beach'
];

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');
const quickActionButtons = document.querySelectorAll('.quick-action-btn');

// Function to add a new message to the chat
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const avatarIcon = isUser ? 'fas fa-user' : 'fas fa-robot';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <div class="message-text">${text}</div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

// Typewriter effect for bot messages
function typeMessage(message, messageElement, delay = 30) {
    const textElement = messageElement.querySelector('.message-text');
    textElement.innerHTML = '';
    
    let i = 0;
    
    function typeChar() {
        if (i < message.length) {
            // Add next character
            textElement.innerHTML += message.charAt(i);
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            i++;
            setTimeout(typeChar, delay);
        } else {
            // Hide typing indicator after completion
            typingIndicator.classList.remove('active');
        }
    }
    
    // Start typing
    typeChar();
}

// Function to extract city from user message
function extractCityFromMessage(message) {
    const lowerMessage = message.toLowerCase();
    
    for (const city of CALIFORNIA_CITIES) {
        if (lowerMessage.includes(city)) {
            // Return formatted city name (first letters uppercase)
            return city.split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
        }
    }
    
    // Check for common abbreviations
    const cityMap = {
        'la': 'Los Angeles',
        'sf': 'San Francisco',
        'sd': 'San Diego',
        'sac': 'Sacramento',
        'sj': 'San Jose'
    };
    
    for (const [abbr, city] of Object.entries(cityMap)) {
        if (lowerMessage.includes(abbr)) {
            return city;
        }
    }
    
    return null;
}

// Function to call OpenWeatherMap API
async function getWeatherData(city) {
    try {
        const response = await fetch(
            `${API_CONFIG.openWeatherMap.baseUrl}?q=${city},CA,US&units=imperial&appid=${API_CONFIG.openWeatherMap.apiKey}`
        );
        
        if (!response.ok) {
            throw new Error(`Weather API error: ${response.status}`);
        }
        
        const data = await response.json();
        return {
            temperature: Math.round(data.main.temp),
            description: data.weather[0].description,
            humidity: data.main.humidity,
            windSpeed: data.wind.speed,
            icon: data.weather[0].icon
        };
    } catch (error) {
        console.error('Weather API error:', error);
        return null;
    }
}

// Function to call Foursquare API
async function getPlacesData(city, query = 'restaurants', limit = 5) {
    try {
        const response = await fetch(
            `${API_CONFIG.foursquare.baseUrl}?near=${city},CA&query=${query}&limit=${limit}`,
            {
                headers: {
                    'Authorization': API_CONFIG.foursquare.apiKey,
                    'Accept': 'application/json'
                }
            }
        );
        
        if (!response.ok) {
            throw new Error(`Foursquare API error: ${response.status}`);
        }
        
        const data = await response.json();
        return data.results.map(place => ({
            name: place.name,
            address: place.location.address || 'Address not available',
            category: place.categories[0]?.name || 'Unknown category'
        }));
    } catch (error) {
        console.error('Foursquare API error:', error);
        return null;
    }
}

// Function to call Eventbrite API
async function getEventsData(city, limit = 5) {
    try {
        const response = await fetch(
            `${API_CONFIG.eventbrite.baseUrl}?location.address=${city},CA&location.within=10mi&expand=venue&token=${API_CONFIG.eventbrite.apiKey}`
        );
        
        if (!response.ok) {
            throw new Error(`Eventbrite API error: ${response.status}`);
        }
        
        const data = await response.json();
        return data.events.map(event => ({
            name: event.name.text,
            date: event.start.local ? new Date(event.start.local).toLocaleDateString() : 'Date not available',
            venue: event.venue ? event.venue.name : 'Venue not specified'
        }));
    } catch (error) {
        console.error('Eventbrite API error:', error);
        return null;
    }
}

// Main function to process user message and generate response
async function processUserMessage(userMessage) {
    const city = extractCityFromMessage(userMessage);
    const lowerMessage = userMessage.toLowerCase();
    
    // Show typing indicator
    typingIndicator.classList.add('active');
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Default response if no city found
    if (!city) {
        const defaultResponses = [
            "I can help you with weather, restaurants, and events in California cities. Which city are you interested in?",
            "Please specify a California city. For example: 'What's the weather in Los Angeles?' or 'Find restaurants in San Francisco'",
            "I specialize in California travel information. Try asking about a specific city like San Diego, San Francisco, or Los Angeles."
        ];
        
        const randomResponse = defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
        
        setTimeout(() => {
            const botMessageElement = addMessage('', false);
            typeMessage(randomResponse, botMessageElement);
        }, 1000);
        
        return;
    }
    
    // Process based on user query
    let botResponse = `Information for ${city}, California:\n\n`;
    let apiData = null;
    
    if (lowerMessage.includes('weather') || lowerMessage.includes('temperature') || lowerMessage.includes('forecast')) {
        // Get weather data
        apiData = await getWeatherData(city);
        
        if (apiData) {
            botResponse += `🌤️ Weather: ${apiData.description}\n`;
            botResponse += `🌡️ Temperature: ${apiData.temperature}°F\n`;
            botResponse += `💧 Humidity: ${apiData.humidity}%\n`;
            botResponse += `💨 Wind Speed: ${apiData.windSpeed} mph\n`;
        } else {
            botResponse += "Sorry, I couldn't fetch weather data at the moment. Please try again later.";
        }
        
    } else if (lowerMessage.includes('restaurant') || lowerMessage.includes('food') || lowerMessage.includes('eat') || lowerMessage.includes('dining')) {
        // Get restaurant data
        apiData = await getPlacesData(city, 'restaurants');
        
        if (apiData && apiData.length > 0) {
            botResponse += `🍽️ Top ${apiData.length} restaurants in ${city}:\n\n`;
            apiData.forEach((place, index) => {
                botResponse += `${index + 1}. ${place.name}\n`;
                botResponse += `   📍 ${place.address}\n`;
                botResponse += `   🏷️ ${place.category}\n\n`;
            });
        } else {
            botResponse += "Sorry, I couldn't find restaurant information for that city.";
        }
        
    } else if (lowerMessage.includes('event') || lowerMessage.includes('activity') || lowerMessage.includes('things to do')) {
        // Get event data
        apiData = await getEventsData(city);
        
        if (apiData && apiData.length > 0) {
            botResponse += `🎭 Upcoming events in ${city}:\n\n`;
            apiData.forEach((event, index) => {
                botResponse += `${index + 1}. ${event.name}\n`;
                botResponse += `   📅 ${event.date}\n`;
                botResponse += `   🏟️ ${event.venue}\n\n`;
            });
        } else {
            botResponse += "Sorry, I couldn't find events for that city.";
        }
        
    } else if (lowerMessage.includes('hotel') || lowerMessage.includes('accommodation') || lowerMessage.includes('stay') || lowerMessage.includes('lodging')) {
        // Get hotel data
        apiData = await getPlacesData(city, 'hotels');
        
        if (apiData && apiData.length > 0) {
            botResponse += `🏨 Hotels in ${city}:\n\n`;
            apiData.forEach((place, index) => {
                botResponse += `${index + 1}. ${place.name}\n`;
                botResponse += `   📍 ${place.address}\n`;
                botResponse += `   🏷️ ${place.category}\n\n`;
            });
        } else {
            botResponse += "Sorry, I couldn't find hotel information for that city.";
        }
        
    } else {
        // General city information
        const cityResponses = {
            'Los Angeles': "Los Angeles is known for Hollywood, beautiful beaches, and diverse culture. Don't miss Santa Monica Pier, Griffith Observatory, and the Getty Center!",
            'San Francisco': "San Francisco is famous for the Golden Gate Bridge, Alcatraz Island, and historic cable cars. Try the seafood at Fisherman's Wharf!",
            'San Diego': "San Diego has perfect weather, beautiful beaches, and the world-famous San Diego Zoo. Balboa Park is a must-visit!",
            'Sacramento': "Sacramento is California's capital with rich history. Visit the State Capitol Museum and Old Sacramento Waterfront."
        };
        
        botResponse += cityResponses[city] || `${city} is a beautiful California city with lots to explore! You can ask me about weather, restaurants, or events here.`;
        
        // Also show weather as default
        const weatherData = await getWeatherData(city);
        if (weatherData) {
            botResponse += `\n\nCurrent weather: ${weatherData.temperature}°F, ${weatherData.description}`;
        }
    }
    
    // Add bot message with typing effect
    setTimeout(() => {
        const botMessageElement = addMessage('', false);
        typeMessage(botResponse, botMessageElement, 20);
    }, 1500);
}

// Function to get current time
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}


// Function to send user message
function sendUserMessage() {
    const message = messageInput.value.trim();
    
    if (message === '') return;
    
    // Add user message to UI
    addMessage(message, true);
    
    // Clear input field
    messageInput.value = '';
    
    // NEW: Send the message to Rasa Server
    talkToRasa(message);
}

// function to communicate with Rasa Model
async function talkToRasa(userMessage) {
    try {
        const response = await fetch(RASA_SERVER_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender: "user123", // Unique ID for the user session
                message: userMessage
            })
        });

        const botResponses = await response.json();
        
        // Display each response from Rasa
        if (botResponses && botResponses.length > 0) {
            botResponses.forEach(res => {
                if (res.text) {
                    addMessage(res.text, false); // false means it's a bot message
                }
                if (res.image) {
                    // If your model sends images (like the stickers)
                    addImageMessage(res.image); 
                }
            });
        }
    } catch (error) {
        console.error("Connection Error:", error);
        addMessage("I'm sorry, I can't reach my server right now.", false);
    }
}

// Event listeners
sendButton.addEventListener('click', sendUserMessage);

messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendUserMessage();
    }
});

// Quick action buttons
quickActionButtons.forEach(button => {
    button.addEventListener('click', function() {
        const message = this.getAttribute('data-message');
        messageInput.value = message;
        sendUserMessage();
    });
});

// Add initial welcome message
window.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        const welcomeMessage = "I can help you plan your California trip! Ask me about weather, restaurants, hotels, or events in any California city.";
        const botMessageElement = addMessage('', false);
        typeMessage(welcomeMessage, botMessageElement, 40);
    }, 1500);
    
    // Animation for stickers
    const sun = document.getElementById('sun');
    const palm = document.getElementById('palm-tree');
    
    // Sun animation
    setInterval(() => {
        sun.style.transform = `scale(${1 + Math.sin(Date.now() / 2000) * 0.05})`;
    }, 50);
    
    // Palm tree animation
    setInterval(() => {
        palm.style.transform = `translateX(${Math.sin(Date.now() / 3000) * 5}px)`;
    }, 50);
});

// API Test Function (for debugging)
async function testAPIs() {
    console.log('Testing APIs...');
    
    // Test weather API
    const weather = await getWeatherData('Los Angeles');
    console.log('Weather API Test:', weather);
    
    // Test Foursquare API
    const places = await getPlacesData('San Francisco', 'restaurants', 3);
    console.log('Foursquare API Test:', places);
    
    // Note: Eventbrite API requires specific authentication setup
}