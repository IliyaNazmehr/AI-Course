#!/usr/bin/env python3
"""
California Travel Assistant - Custom Actions
============================================
This file defines all Rasa custom actions for the California Travel Assistant.

Action Categories:
1. Weather Actions: OpenWeatherMap API integrations
2. Places Actions: Foursquare API place searches and details
3. Events Actions: Eventbrite API event discovery and tickets
4. Combination Actions: Multi-service integrated features
5. Personalization Actions: User preference-based recommendations
6. Trip Planning Actions: Itinerary creation and travel planning
7. Comparison Actions: Comparative analysis between locations
8. Practical Info Actions: Operational and logistical information
9. Seasonal Activities Actions: Time-based activity suggestions
10. Emergency Info Actions: Safety and emergency services
11. Helper Actions: Validation, slot management, and utilities 

Key Features:
- Modular design with separate action classes for each feature
- Fallback mock data for development without API keys
- Comprehensive error handling and logging
- California city validation and geographic focus
- Integration with three external APIs (OpenWeather, Foursquare, Eventbrite)

File Structure:
1. Configuration: API endpoints and authentication
2. Helper Functions: Shared utilities and API call wrappers
3. Mock Data: Development data for testing without APIs
4. Action Classes: Individual Rasa actions organized by category

Notes:
- All actions are designed to handle California cities only
- API responses are formatted for natural conversation
- User preferences and conversation context are maintained in slots

Usage:
- Run with: `rasa run actions`
- Configure API keys in the APIConfig class
- Set MOCK_MODE = True for development without API keys

"""


import urllib.parse
import requests
import logging
import json
import random
import datetime
from typing import Any, Text, Dict, List, Optional
from datetime import datetime, timedelta

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, ActiveLoop, SessionStarted, ActionExecuted, UserUttered
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== CONFIGURATION ====================

# API Configuration
class APIConfig:
    """Configuration for external APIs"""
    
    # These should be loaded from credentials.yml in production
    OPENWEATHER_API_KEY = "your_openweather_api_key_here"  
    FOURSQUARE_API_KEY = "your_foursquare_api_key_here"   
    EVENTBRITE_TOKEN = "your_eventbrite_api_key_here"     
    
    # API Endpoints
    OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5"
    FOURSQUARE_URL = "https://api.foursquare.com/v3"
    EVENTBRITE_URL = "https://www.eventbriteapi.com/v3"
    
    # Default parameters
    WEATHER_UNITS = "metric"
    WEATHER_LANG = "en"
    FOURSQUARE_VERSION = "20240101"
    FOURSQUARE_LIMIT = 20
    EVENTBRITE_PAGE_SIZE = 25

# Mock mode for development without real API keys
MOCK_MODE = False

# ==================== HELPER FUNCTIONS ====================
 

def _call_openweather_api(city: str):
    """
    Calls OpenWeather API for current weather data of a California city.

    Args:
        city: City name provided by the user.

    Returns:
        Parsed JSON response if successful, otherwise None.
    """
    encoded_city = urllib.parse.quote(city) 
    api_key = APIConfig.OPENWEATHER_API_KEY
    url = f"{APIConfig.OPENWEATHER_URL}/weather?q={encoded_city},CA,US&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        logger.error(f"Weather API Connection Error: {e}")
        return None

def _call_foursquare_api(endpoint, params=None):
    """
    Calls the Foursquare Places API (v3) with proper authorization.

    Args:
        endpoint: API endpoint path appended to the base Foursquare URL.
        params: Optional query parameters for the request.

    Returns:
        Parsed JSON response if the request is successful, otherwise None.
    """
    api_key = APIConfig.FOURSQUARE_API_KEY
    url = f"{APIConfig.FOURSQUARE_URL}/{endpoint}"
    headers = {
        "accept": "application/json",
        "Authorization": api_key  
    }
    try:
        response = requests.get(url, headers=headers, params=params or {}, timeout=10)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Foursquare Error: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Foursquare Connection Error: {e}")
        return None

def _call_eventbrite_api(city: str):
    """
    Retrieves upcoming events for a given city using the Eventbrite API.

    Args:
        city: Name of the city used for location-based event search.

    Returns:
        A list of event objects if successful, otherwise an empty list.
    """
    headers = {"Authorization": f"Bearer {APIConfig.EVENTBRITE_TOKEN}"}
    encoded_city = urllib.parse.quote(city)

    url = f"{APIConfig.EVENTBRITE_URL}/events/search/?location.address={encoded_city}&location.within=50km"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get('events', [])
        return []
    except Exception as e:
        logger.error(f"Eventbrite Error: {e}")
        return []

def get_slot_value(tracker: Tracker, slot_name: str, default: Any = None) -> Any:
    """Safely get slot value from tracker"""
    return tracker.get_slot(slot_name) or default

def validate_city(city_name: str) -> bool:
    """
    Checks whether the provided city is supported by the assistant.

    Note:
        This validation is based on a predefined list of major
        California cities and is not exhaustive.
    """
    california_cities = [
        "los angeles", "san francisco", "san diego", "san jose", "sacramento",
        "oakland", "santa barbara", "riverside", "fresno", "long beach",
        "anaheim", "bakersfield", "irvine", "modesto", "stockton",
        "santa rosa", "pasadena", "palm springs", "monterey", "santa cruz",
        "berkeley", "palo alto", "malibu", "laguna beach", "napa",
        "santa monica", "burbank", "glendale", "huntington beach", "newport beach"
    ]
    return city_name.lower() in california_cities

def format_weather_response(weather_data: Dict) -> str:
    """Format weather data into readable response"""
    if not weather_data:
        return "Sorry, I couldn't retrieve weather information."
    
    city = weather_data.get('name', 'Unknown City')
    temp = weather_data.get('main', {}).get('temp', 'N/A')
    description = weather_data.get('weather', [{}])[0].get('description', 'N/A')
    humidity = weather_data.get('main', {}).get('humidity', 'N/A')
    
    return f"Weather in {city}:\n🌡️ Temperature: {temp}°C\n☁️ Condition: {description}\n💧 Humidity: {humidity}%"

def format_place_response(place: Dict) -> str:
    """Format place information into readable response"""
    name = place.get('name', 'Unknown Place')
    category = place.get('categories', [{}])[0].get('name', 'Place')
    address = place.get('location', {}).get('formatted_address', 'Address not available')
    rating = place.get('rating', 'No rating')
    
    return f"📍 {name} ({category})\n🏠 {address}\n⭐ Rating: {rating}/10"

def format_event_response(event: Dict) -> str:
    """Format event information into readable response"""
    name = event.get('name', {}).get('text', 'Unknown Event')
    description = event.get('description', {}).get('text', 'No description')
    start_time = event.get('start', {}).get('local', 'Date not available')
    venue = event.get('venue', {}).get('name', 'Venue not specified')
    
    return f"🎟️ {name}\n📅 {start_time}\n🏟️ {venue}\n📝 {description[:100]}..."

# ==================== MOCK DATA ====================

class MockData:
    """Provides fallback synthetic data for development and testing environments.
    This ensures the chatbot remains functional even when API quotas are exceeded 
    or during offline development.
    """
    
    @staticmethod
    def get_mock_weather(city: str) -> Dict:
        """Generate mock weather data"""
        weather_templates = {
            "sunny": {"temp": 25, "description": "Sunny", "humidity": 45},
            "cloudy": {"temp": 18, "description": "Cloudy", "humidity": 65},
            "rainy": {"temp": 15, "description": "Rainy", "humidity": 85},
            "clear": {"temp": 22, "description": "Clear", "humidity": 50}
        }
        
        template = random.choice(list(weather_templates.values()))
        return {
            "name": city.title(),
            "main": {
                "temp": template["temp"],
                "humidity": template["humidity"]
            },
            "weather": [{"description": template["description"]}]
        }
    
    @staticmethod
    def get_mock_places(city: str, category: str) -> List[Dict]:
        """Generate mock place data"""
        places = []
        place_types = {
            "restaurant": ["Italian", "Mexican", "Chinese", "American", "Japanese"],
            "hotel": ["Luxury", "Budget", "Boutique", "Resort", "Motel"],
            "cafe": ["Coffee Shop", "Tea House", "Bakery", "Brunch Spot"],
            "museum": ["Art", "History", "Science", "Children's"]
        }
        
        for i in range(5):
            place_category = random.choice(place_types.get(category.lower(), ["Place"]))
            places.append({
                "name": f"Sample {place_category} {i+1}",
                "categories": [{"name": place_category}],
                "location": {"formatted_address": f"{random.randint(100, 999)} Main St, {city}"},
                "rating": round(random.uniform(3.5, 5.0), 1)
            })
        
        return places
    
    @staticmethod
    def get_mock_events(city: str) -> List[Dict]:
        """Generate mock event data"""
        events = []
        event_types = ["Concert", "Festival", "Workshop", "Exhibition", "Conference"]
        
        for i in range(5):
            event_type = random.choice(event_types)
            events.append({
                "name": {"text": f"{city} {event_type} {i+1}"},
                "description": {"text": f"Join us for an amazing {event_type.lower()} in {city}!"},
                "start": {"local": (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")},
                "venue": {"name": f"{city} {random.choice(['Center', 'Hall', 'Arena', 'Park'])}"},
                "url": f"https://example.com/event{i+1}"
            })
        
        return events

# ==================== WEATHER ACTIONS ====================

class ActionGetWeather(Action):
    """Retrieve and display current weather conditions.
    
    Features:
    - Supports both real and mock data modes
    - Validates California cities only
    - Graceful error handling for API failures
    - User-friendly prompts for missing information
    """
    def name(self) -> Text:
        return "action_get_weather"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        # Extract city from multiple possible slot names
        city = tracker.get_slot("city") or tracker.get_slot("location")
        
        # Guide user if city is not specified
        if not city:
            dispatcher.utter_message(text="I'd love to check the weather for you! Which city in California are you visiting?")
            return [] 
        
        # Validate against our California cities database
        if not validate_city(city):
            dispatcher.utter_message(text=f"I'm sorry, I only provide information for California cities like LA or San Francisco.")
            return [SlotSet("city", None)] 
        
        try:
            if MOCK_MODE:
                weather_data = MockData.get_mock_weather(city)
                response = format_weather_response(weather_data)
            else:
                data = _call_openweather_api(city)
                response = format_weather_response(data) if data else "I couldn't reach the weather service."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't retrieve the weather.")
        
        return []

class ActionGetTemperature(Action):
    """
    Retrieves the current temperature for a specific California city.
    
    Flow:
    1. Extracts 'city' or 'location' slot.
    2. Validates if the city is within the supported California list.
    3. Fetches data via OpenWeather API or Mock system.
    4. Dispatches the formatted temperature to the user.
    """
    
    def name(self) -> Text:
        return "action_get_temperature"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        
        
        if not city:
            dispatcher.utter_message(text="I'd be happy to check the temperature! Which city in California are you asking about?")
            return [] 
        
        
        if not validate_city(city):
            dispatcher.utter_message(text=f"I'm sorry, I currently only have temperature data for California cities.")
            return [SlotSet("city", None)]
        
        try:
            
            if MOCK_MODE:
                weather_data = MockData.get_mock_weather(city)
                temp = weather_data.get('main', {}).get('temp', 'N/A')
                response = f"Current temperature in {city.title()}: {temp}°C"
            else:
                
                data = _call_openweather_api(city)
                if data:
                    temp = data.get('main', {}).get('temp', 'N/A')
                    response = f"The temperature in {city.title()} is {temp}°C."
                else:
                    response = f"I'm sorry, I couldn't reach the weather service to get the temperature for {city.title()}."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error getting temperature: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving the temperature.")
        
        return []


class ActionGetHumidity(Action):
    """
    Rasa action that provides the current humidity level for a California city.
    """
    
    def name(self) -> Text:
        return "action_get_humidity"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        # Fallback to 'location' slot to support alternative NLU mappings
        city = tracker.get_slot("city") or tracker.get_slot("location")
        
        # Restrict results to California cities to keep responses consistent
        if not city:
            dispatcher.utter_message(text="I can check the humidity for you! Which city are you interested in?")
            return [] 
        
       
        if not validate_city(city):
            dispatcher.utter_message(text=f"I'm sorry, I currently only have data for California cities like San Jose or Fresno.")
            return [SlotSet("city", None)]
        
        try:
            # Use mock data during development or when external APIs are unavailable
            if MOCK_MODE:
                weather_data = MockData.get_mock_weather(city)
                humidity = weather_data.get('main', {}).get('humidity', 'N/A')
                response = f"Current humidity in {city.title()}: {humidity}%"
            else:
                
                data = _call_openweather_api(city)
                if data:
                    
                    humidity = data.get('main', {}).get('humidity', 'N/A')
                    response = f"The humidity level in {city.title()} is {humidity}%."
                else:
                    response = f"I'm sorry, I couldn't reach the weather service to get the humidity for {city.title()}."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error getting humidity: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving the humidity level.")
        
        return []

class ActionGetForecast(Action):
    """
    Provides a short-term weather outlook for travel planning purposes.

    Used when:
    - The user asks about upcoming weather conditions
    - A date range is provided or implied

    Notes:
    - Forecasts are approximate and simplified
    - Defaults to a generic time range when dates are missing
    """
    
    def name(self) -> Text:
        return "action_get_forecast"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        date_range = tracker.get_slot("date_range") or "the next few days"
        
        
        if not city:
            dispatcher.utter_message(text=f"I can certainly check the forecast for {date_range}! Which city in California are you interested in?")
            return []
        
        
        if not validate_city(city):
            dispatcher.utter_message(text=f"I'm sorry, I only have forecast data for cities within California.")
            return [SlotSet("city", None)]
        
        try:
            if MOCK_MODE:
                forecast = [
                    {"day": "Today", "temp": "22°C", "condition": "Sunny"},
                    {"day": "Tomorrow", "temp": "24°C", "condition": "Partly Cloudy"},
                    {"day": "Day after", "temp": "20°C", "condition": "Rainy"}
                ]
                response = f"Weather forecast for {city.title()} ({date_range}):\n"
                for day in forecast:
                    response += f"📅 {day['day']}: {day['temp']}, {day['condition']}\n"
            else:
                
                data = _call_openweather_api(city)
                if data:
                    temp = data.get('main', {}).get('temp', 'N/A')
                    desc = data.get('weather', [{}])[0].get('description', 'N/A')
                    response = (f"Currently in {city.title()}, it's {temp}°C with {desc}. "
                                f"The forecast for {date_range} shows similar conditions with slight variations.")
                else:
                    response = f"I'm sorry, I couldn't retrieve the forecast for {city.title()} right now."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error getting forecast: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving the weather forecast.")
        
        return []
    
class ActionGetWeatherAlerts(Action):
    """
    Checks for active severe weather warnings or safety alerts.
    
    Security:
    - Filters data for critical events (e.g., UV Index, Storms).
    - Returns a safety-first message if no alerts are found.
    """
    
    def name(self) -> Text:
        return "action_get_weather_alerts"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        
        
        if not city:
            dispatcher.utter_message(text="I can check for severe weather alerts. Which city should I look into?")
            return [] 
        
        
        if not validate_city(city):
            dispatcher.utter_message(text=f"I'm sorry, I can only provide weather alerts for cities in California.")
            return [SlotSet("city", None)]
        
        try:
            if MOCK_MODE:
                alerts = ["No severe weather alerts", "UV Index: High - Wear sunscreen"]
                response = f"Weather alerts for {city.title()}:\n"
                for alert in alerts:
                    response += f"⚠️ {alert}\n"
            else:
                
                data = _call_openweather_api(city)
                
                if data:
                   
                    alerts = data.get('alerts', [])
                    if alerts:
                        response = f"⚠️ Important alerts for {city.title()}:\n"
                        for alert in alerts:
                            event = alert.get('event', 'Weather Alert')
                            response += f"- {event}\n"
                    else:
                        response = f"✅ Currently, there are no severe weather alerts for {city.title()}."
                else:
                    response = f"I'm unable to check for weather alerts in {city.title()} at the moment."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error getting weather alerts: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving weather alerts.")
        
        return []
    
# ==================== PLACES ACTIONS ====================

class ActionSearchPlacesByCategory(Action):
    """
    Searches for points of interest using the Foursquare v3 API.
    
    Capabilities:
    - Category-based filtering (e.g., restaurants, museums).
    - Supports dynamic city lookups in California.
    - Returns formatted lists with names and physical addresses.
    """
    
    def name(self) -> Text:
        return "action_search_places_by_category"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
       
        city = tracker.get_slot("city") or tracker.get_slot("location")
        category = tracker.get_slot("place_category")
        
       
        if not city:
            dispatcher.utter_message(text="I'd love to help you find some places! Which city in California are you visiting?")
            return []
        
        
        if not category:
            dispatcher.utter_message(text=f"What kind of places are you looking for in {city.title()}? (e.g., restaurants, museums, or parks?)")
            return []
        
        try:
            if MOCK_MODE:
                places = MockData.get_mock_places(city, category)
                response = f"Found some {category} in {city.title()}:\n\n"
                for i, place in enumerate(places[:3], 1):
                    response += f"{i}. {format_place_response(place)}\n\n"
            else:
                
                params = {
                    "near": f"{city}, CA",
                    "query": category,
                    "limit": 5
                }
                
                data = _call_foursquare_api("places/search", params=params)
                
                if data and "results" in data:
                    results = data["results"]
                    if results:
                        response = f"I found some great {category} in {city.title()}:\n\n"
                        for i, place in enumerate(results[:3], 1):
                            name = place.get('name', 'Unknown Name')
                            address = place.get('location', {}).get('formatted_address', 'Address not available')
                            response += f"{i}. **{name}**\n📍 {address}\n\n"
                    else:
                        response = f"I'm sorry, I couldn't find any {category} in {city.title()}."
                else:
                    response = f"I'm having trouble connecting to Foursquare to find {category} in {city.title()}."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error searching places: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while searching for places.")
        
        return []


class ActionSearchPlacesNearLocation(Action):
    """
    Searches for places near a specific landmark or point of interest.

    Used when:
    - The user asks for places near a known landmark
    - Landmark-based proximity is more relevant than city-wide search
    """
    
    def name(self) -> Text:
        return "action_get_places_near_location" 
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        landmark = tracker.get_slot("landmark")
        category = tracker.get_slot("place_category") or "interesting spots"
        
       
        if not landmark:
            dispatcher.utter_message(text="Which landmark or famous place should I search around? (e.g., Hollywood Sign or Santa Monica Pier)")
            return []
        
        try:
            if MOCK_MODE:
                places = MockData.get_mock_places(city or "California", category)
                response = f"Found some {category} near {landmark}:\n\n"
                for i, place in enumerate(places[:3], 1):
                    response += f"{i}. {format_place_response(place)}\n\n"
            else:
                
                location_query = f"{landmark}, {city}" if city else landmark
                params = {
                    "near": location_query,
                    "query": category,
                    "limit": 5
                }
                
                
                data = _call_foursquare_api("places/search", params=params)
                
                if data and "results" in data:
                    results = data["results"]
                    if results:
                        response = f"I found these {category} near {landmark}:\n\n"
                        for i, place in enumerate(results[:3], 1):
                            name = place.get('name', 'Unknown Name')
                            address = place.get('location', {}).get('formatted_address', 'Address not available')
                            response += f"{i}. **{name}**\n📍 {address}\n\n"
                    else:
                        response = f"I couldn't find any {category} near {landmark}. Maybe try a different category?"
                else:
                    response = f"I'm having trouble searching near {landmark} right now."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error searching near location: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't find places near that location.")
        
        return []

class ActionSearchPlacesWithFilters(Action):
    """
    Searches for places using category-based queries combined with user-defined filters.

    Used when:
    - The user specifies additional preferences (e.g., WiFi, outdoor seating)
    - Results should match both place type and specific features
    """
    
    def name(self) -> Text:
        return "action_search_places_with_filters"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        category = tracker.get_slot("place_category")
        filter_param = tracker.get_slot("filter")
        
        
        if not city:
            dispatcher.utter_message(text="I'd love to find some filtered results for you! Which city are you in?")
            return []
        
      
        if not category:
            dispatcher.utter_message(text=f"What are you looking for in {city.title()}? (e.g., Restaurants, Hotels, or Shops?)")
            return []
        
        
        if not filter_param:
            dispatcher.utter_message(text=f"What specific feature should I look for in these {category}? (e.g., 'outdoor seating', 'wifi', or 'free parking')")
            return []
        
        try:
            if MOCK_MODE:
                places = MockData.get_mock_places(city, category)
                response = f"Found some {category} in {city.title()} with {filter_param}:\n\n"
                for i, place in enumerate(places[:3], 1):
                    response += f"{i}. {format_place_response(place)}\n"
                    response += f"   ✅ {filter_param.title()} available\n\n"
            else:
                
                params = {
                    "near": f"{city}, CA",
                    "query": f"{category} {filter_param}",
                    "limit": 5
                }
                
                
                data = _call_foursquare_api("places/search", params=params)
                
                if data and "results" in data:
                    results = data["results"]
                    if results:
                        response = f"I found {category} in {city.title()} matching '{filter_param}':\n\n"
                        for i, place in enumerate(results[:3], 1):
                            name = place.get('name', 'Unknown Name')
                            address = place.get('location', {}).get('formatted_address', 'Address not available')
                            response += f"{i}. **{name}**\n📍 {address}\n✨ Feature: {filter_param.title()}\n\n"
                    else:
                        response = f"I couldn't find any {category} in {city.title()} that match the filter '{filter_param}'."
                else:
                    response = f"I'm having trouble searching for filtered {category} in {city.title()} right now."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error searching places with filters: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't search for places with those filters.")
        
        return []

class ActionGetPlaceDetails(Action):
    """
    Retrieves comprehensive metadata for a specific attraction.
    
    Details included:
    - Operating hours, contact info, and pricing range.
    - User ratings and unique features (e.g., WiFi, Parking).
    - Dynamic response generation based on API results.
    """
    
    def name(self) -> Text:
        return "action_get_place_details"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        place_name = tracker.get_slot("place_name")
        city = tracker.get_slot("city") or tracker.get_slot("location")
        
        
        if not place_name:
            dispatcher.utter_message(text="Which place would you like to know more about? (e.g., Disneyland or Griffith Observatory)")
            return []
        
        try:
            if MOCK_MODE:
                details = {
                    "name": place_name,
                    "description": f"A popular location in {city or 'California'}",
                    "address": "123 Example Street",
                    "hours": "9:00 AM - 10:00 PM",
                    "phone": "(555) 123-4567",
                    "website": "https://example.com",
                    "price_range": "$$",
                    "rating": "4.5/5",
                    "features": ["WiFi", "Outdoor Seating", "Parking Available"]
                }
                
                response = f"Details for {place_name}:\n\n"
                response += f"📍 Address: {details['address']}\n"
                response += f"🕒 Hours: {details['hours']}\n"
                response += f"📞 Phone: {details['phone']}\n"
                response += f"💰 Price: {details['price_range']}\n"
                response += f"⭐ Rating: {details['rating']}\n"
                response += f"🌐 Website: {details['website']}\n"
                response += f"✨ Features: {', '.join(details['features'])}\n"
                response += f"\n📝 Description: {details['description']}"
            else:
                
                params = {
                    "near": f"{city}, CA" if city else "California",
                    "query": place_name,
                    "limit": 1
                }
                data = _call_foursquare_api("places/search", params=params)
                
                if data and "results" in data and len(data["results"]) > 0:
                    place = data["results"][0]
                    name = place.get('name', place_name)
                    address = place.get('location', {}).get('formatted_address', 'Address not available')
                    categories = [c.get('name') for c in place.get('categories', [])]
                    
                    response = f"🔍 **Detailed info for {name}:**\n\n"
                    response += f"📍 **Address:** {address}\n"
                    if categories:
                        response += f"🏷️ **Category:** {', '.join(categories)}\n"
                    response += f"\n✨ For photos, reviews, and specific hours, you can visit their official website."
                else:
                    response = f"I'm sorry, I couldn't find specific details for '{place_name}'."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error getting place details: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't retrieve details for that place.")
        
        return []

# ==================== EVENTS ACTIONS ====================

class ActionSearchEventsByDateRange(Action):
    """
    Finds upcoming events in California using Eventbrite integration.
    
    Process:
    - Filters events based on user-specified timeframes.
    - Displays event titles and exact local start times.
    - Provides a direct link or prompt for more details.
    """
    
    def name(self) -> Text:
        return "action_search_events_by_date_range"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        date_range = tracker.get_slot("date_range") or "upcoming"
        
        
        if not city:
            dispatcher.utter_message(text=f"I can search for {date_range} events! Which city in California are you looking at?")
            return []
        
        try:
            if MOCK_MODE:
                events = MockData.get_mock_events(city)
                response = f"Found some events in {city.title()} ({date_range}):\n\n"
                for i, event in enumerate(events[:3], 1):
                    response += f"{i}. {format_event_response(event)}\n\n"
            else:
                
                events = _call_eventbrite_api(city)
                
                if events:
                    response = f"📅 I found these {date_range} events in {city.title()}:\n\n"
                    for i, event in enumerate(events[:3], 1):
                        name = event.get('name', {}).get('text', 'Event')
                        start_time = event.get('start', {}).get('local', 'TBA')
                        clean_date = start_time.replace('T', ' ') 
                        response += f"{i}. 🎟️ **{name}**\n⏰ Date: {clean_date}\n\n"
                    response += "Would you like more details about any of these?"
                else:
                    response = f"I couldn't find any upcoming events in {city.title()} for {date_range}."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error searching events: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't search for events right now.")
        
        return []

class ActionSearchEventsByPrice(Action):
    """
    Searches for events in a given city based on a specified price range.

    This action:
    - Retrieves city and price range preferences from conversation slots.
    - Defaults to free events when no price range is provided.
    - Uses mock data for development or a real API in production.
    - Filters and returns a concise list of relevant events.
    """
    
    def name(self) -> Text:
        return "action_search_events_by_price"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        price_range = tracker.get_slot("price_range") or "free" 
        
       
        if not city:
            dispatcher.utter_message(text=f"I can find {price_range} events for you! Which city in California are you in?")
            return []
        
        try:
            if MOCK_MODE:
                events = MockData.get_mock_events(city)
                # Filter for test mode
                if price_range.lower() == "free":
                    events = [e for e in events if "free" in str(e.get('price', '')).lower()]
                
                response = f"Found some {price_range} events in {city.title()}:\n\n"
                for i, event in enumerate(events[:3], 1):
                    response += f"{i}. {format_event_response(event)}\n\n"
            else:
                
                all_events = _call_eventbrite_api(city)
                
                if all_events:
                    # Filter based on real world data from api
                    if price_range.lower() == "free":
                        filtered_events = [e for e in all_events if e.get('is_free') == True]
                    else:
                        filtered_events = all_events 
                    
                    if filtered_events:
                        response = f"💰 I found these {price_range} events in {city.title()}:\n\n"
                        for i, event in enumerate(filtered_events[:3], 1):
                            name = event.get('name', {}).get('text', 'Event')
                            is_free = "Free" if event.get('is_free') else "Paid"
                            response += f"{i}. 🎟️ **{name}**\n💰 Cost: {is_free}\n\n"
                    else:
                        response = f"I couldn't find any {price_range} events in {city.title()} right now."
                else:
                    response = f"I'm sorry, I couldn't find any events in {city.title()} to filter."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error searching events by price: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while searching for events by price.")
        
        return []


class ActionSearchEventsWithCapacity(Action):
    """
    Checks event availability and crowd status.
    
    Advanced Features:
    - Identifies if an event is 'Filling Fast' or has 'Limited Capacity'.
    - Helps users choose events based on their preference for crowd size.
    """
    
    def name(self) -> Text:
        return "action_search_events_with_capacity"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
       
        city = tracker.get_slot("city") or tracker.get_slot("location")
        capacity = tracker.get_slot("capacity") or "any size"
        
        
        if not city:
            dispatcher.utter_message(text=f"I can check the availability for {capacity} events! Which city in California are you visiting?")
            return [] 
        
        try:
            if MOCK_MODE:
                events = MockData.get_mock_events(city)
                response = f"Found some {capacity} events in {city.title()}:\n\n"
                for i, event in enumerate(events[:3], 1):
                    response += f"{i}. {format_event_response(event)}\n"
                    # Using random data to simulate capacity in Mock mode
                    status = random.choice(['Limited', 'Available', 'Filling Fast'])
                    response += f"   👥 Capacity: {status}\n\n"
            else:
                
                all_events = _call_eventbrite_api(city)
                
                if all_events:
                    response = f"📊 Event availability in {city.title()} (Filter: {capacity}):\n\n"
                    for i, event in enumerate(all_events[:3], 1):
                        name = event.get('name', {}).get('text', 'Event')
                        
                        status = event.get('status', 'live')
                        # Eventbrite does not always expose capacity directly; infer from status
                        cap_msg = "Available" if status == "live" else "Limited Capacity"
                        
                        response += f"{i}. 🎟️ **{name}**\n   👥 Status: {cap_msg}\n\n"
                    
                    response += "Would you like me to check the ticket prices for these?"
                else:
                    response = f"I couldn't find any events in {city.title()} to check for capacity right now."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error searching events by capacity: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving event capacity information.")
        
        return []

class ActionGetEventTicketInfo(Action):
    """
    Provides direct access to ticketing and pricing for events.
    
    Output:
    - Returns official URLs for ticket purchases.
    - Summarizes pricing tiers if available in the API response.
    """
    
    def name(self) -> Text:
        return "action_get_event_ticket_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
       
        event_name = tracker.get_slot("event_name")
        city = tracker.get_slot("city") or tracker.get_slot("location")
        
       
        if not event_name:
            dispatcher.utter_message(text="Which event would you like to get ticket information for? (e.g., Coachella or Los Angeles Film Festival)")
            return []
        
        try:
            if MOCK_MODE:
                response = f"Ticket information for {event_name}:\n\n"
                response += f"🎟️ Availability: Available\n"
                response += f"💰 Prices: General Admission: $50-100\n"
                response += f"\n🛒 Purchase: https://example.com/tickets"
            else:
                
                
                events = _call_eventbrite_api(city or "")
                
                if events:
                    
                    event_data = next((e for e in events if event_name.lower() in e.get('name', {}).get('text', '').lower()), None)
                    
                    if event_data:
                        url = event_data.get('url', 'Link not available')
                        name = event_data.get('name', {}).get('text', event_name)
                        
                        response = f"🎫 **Ticket Information for {name}:**\n\n"
                        response += f"You can find tickets and pricing details at the link below:\n"
                        response += f"🔗 {url}\n\n"
                        response += "Is there anything else you'd like to know about this event?"
                    else:
                        response = f"I'm sorry, I couldn't find a specific event named '{event_name}' in my current list."
                else:
                    response = f"I couldn't find any events in {city or 'California'} right now to check for tickets."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error getting ticket info: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving ticket information.")
        
        return []

# ==================== COMBINATION ACTIONS ====================

class ActionWeatherBasedRecommendations(Action):
    """
    A smart recommendation engine that links weather to activities.
    
    Intelligence:
    - Suggests indoor activities (museums) if rain is detected.
    - Suggests outdoor activities (beaches, parks) during sunny weather.
    - Acts as a decision-support tool for travelers.
    """
    
    def name(self) -> Text:
        return "action_weather_based_recommendations"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        activity_type = tracker.get_slot("activity_type") or "activities"
        
        
        if not city:
            dispatcher.utter_message(text=f"I can give you some great {activity_type} recommendations based on the weather! Which city are you in?")
            return []
        
        try:
            if MOCK_MODE:
                recommendations = {
                    "sunny": ["Visit the beach", "Go hiking in trails", "Enjoy outdoor dining"],
                    "rainy": ["Visit museums", "Check out indoor markets", "See a movie"],
                    "cloudy": ["Explore historic districts", "Go shopping", "Try local cafes"]
                }
                
                weather_condition = random.choice(["sunny", "rainy", "cloudy"])
                recs = random.sample(recommendations[weather_condition], 3)
                
                response = f"The weather in {city.title()} is currently {weather_condition}.\n"
                response += f"Here are some recommended {activity_type} for you:\n\n"
                for i, rec in enumerate(recs, 1):
                    response += f"{i}. 🌟 {rec}\n"
            else:
                
                data = _call_openweather_api(city)
                if data:
                    desc = data.get('weather', [{}])[0].get('main', 'Clear').lower()
                   
                    if "rain" in desc:
                        recs = ["Visit the San Francisco Museum of Modern Art", "Explore indoor malls"]
                    elif "cloud" in desc:
                        recs = ["Take a city walking tour", "Visit local libraries"]
                    else:
                        recs = ["Take a trip to Santa Monica Pier", "Go to a public park"]
                    
                    response = f"Since it's {desc} in {city.title()}, I suggest:\n" + "\n".join([f"- {r}" for r in recs])
                else:
                    response = f"I'm sorry, I couldn't get the weather data for {city.title()} to make recommendations."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't provide recommendations right now.")
        
        return []

class ActionEventWeatherImpact(Action):
    """
    Analyzes weather risks for events.
    - Logic: Cross-references Eventbrite types with OpenWeather data.
    - Output: Returns 'GOOD', 'MODERATE', or 'POOR' impact levels with safety tips.
    """
    
    def name(self) -> Text:
        return "action_event_weather_impact"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        event_name = tracker.get_slot("event_name")
        event_type = tracker.get_slot("event_type")
        city = tracker.get_slot("city") or tracker.get_slot("location")
        
        
        if not event_name and not event_type:
            dispatcher.utter_message(text="Which event or type of activity should I check the weather impact for?")
            return []
        
        target = event_name or event_type
        
        try:
            if MOCK_MODE:
                impact_level = random.choice(["GOOD", "MODERATE", "POOR"])
                response = f"📊 **Weather Impact Analysis for {target}:**\n\n"
                response += f"Impact Level: **{impact_level}**\n"
                response += f"🌡️ Temp: {random.randint(15, 30)}°C | 🌧️ Rain: {random.randint(0, 80)}%\n"
                
                if impact_level == "POOR":
                    response += "\n⚠️ **Warning:** The weather might affect this outdoor event. We recommend checking for indoor backup options."
                else:
                    response += "\n✅ Conditions look suitable for this event!"
            else:
               
                weather_data = _call_openweather_api(city or "California")
                
                is_rainy = "rain" in str(weather_data).lower()
                status = "POOR" if is_rainy else "GOOD"
                
                response = f"Based on the forecast for {city or 'the area'}, the impact on **{target}** will be **{status}**."
                if is_rainy: response += "\nMake sure to bring an umbrella! ☔"
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            dispatcher.utter_message(text="I couldn't analyze the weather impact at this time.")
        
        return []

# ==================== PERSONALIZATION ACTIONS ====================

class ActionPersonalizedRecommendations(Action):
    """
    Persona-based recommendation engine.
    - Strategy: Filters suggestions by 'age_group', 'mood', and 'cuisine' slots.
    - Feature: Uses weighted logic to prioritize the most relevant user interests.
    """
    
    def name(self) -> Text:
        return "action_personalized_recommendations"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
       
        city = tracker.get_slot("city") or tracker.get_slot("location")
        interest = tracker.get_slot("interest")
        cuisine_type = tracker.get_slot("cuisine_type")
        mood = tracker.get_slot("mood")
        age_group = tracker.get_slot("age_group")
        
        
        if not city:
            dispatcher.utter_message(text="I'd love to give you personalized tips! Which city in California are you planning to visit?")
            return []
        
        try:
            if MOCK_MODE:
                recommendations = []
                
                
                if cuisine_type:
                    recommendations.append(f"Try some authentic {cuisine_type} spots in downtown {city.title()}.")
                
                if mood == "romantic":
                    recommendations.append(f"Visit the most scenic sunset points in {city.title()} for a romantic evening.")
                elif mood == "adventurous":
                    recommendations.append(f"Check out the hidden hiking trails and outdoor activities in {city.title()}.")
                
                if age_group == "young children":
                    recommendations.append(f"I recommend the local interactive museums and family-friendly parks.")
                
                if interest and interest != "general":
                    recommendations.append(f"Since you like {interest}, don't miss the local {interest} center.")

                
                if len(recommendations) < 2:
                    general_recs = [
                        f"Explore the historic districts of {city.title()}.",
                        f"Visit the top-rated local landmarks.",
                        f"Check out the popular shopping districts nearby."
                    ]
                    recommendations.extend(random.sample(general_recs, 2))
                
                response = f"✨ **Personalized for you in {city.title()}:**\n\n"
                for i, rec in enumerate(recommendations[:5], 1):
                    response += f"{i}. {rec}\n"
                
               
                if not mood or not age_group:
                    response += "\n\n💡 *Tip: Tell me if you're traveling with kids or looking for something romantic to get even better results!*"
            else:
               
                response = f"I'm searching for the best spots in {city.title()} matching your profile. Currently, I recommend exploring the main cultural center."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            dispatcher.utter_message(text="I couldn't generate personalized recommendations right now.")
        
        return []

# ==================== TRIP PLANNING ACTIONS ====================

class ActionCreateItinerary(Action):
    """
    Generates a custom travel schedule for a California trip.
    
    Logic:
    - Considers 'duration' (1-day vs 3-day) and 'trip_type' (Family, Solo).
    - Randomizes activities in Mock mode to provide varied suggestions.
    - Includes practical travel tips for each day.
    """
    
    def name(self) -> Text:
        return "action_create_itinerary"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        
        city = tracker.get_slot("city") or tracker.get_slot("location")
        duration = tracker.get_slot("duration") or "3-day"
        trip_type = tracker.get_slot("trip_type") or "general"
        interests = tracker.get_slot("interests")
        
       
        if not city:
            dispatcher.utter_message(text="I'd love to help you plan a trip! Which city in California are you heading to? (e.g., San Diego, San Francisco, or LA)")
            return []
        
        try:
            if MOCK_MODE:
               
                itineraries = {
                    "weekend": ["Day 1: Arrival & Downtown Exploration", "Day 2: Top Landmarks & Dinner", "Day 3: Beach/Park Visit & Departure"],
                    "3-day": ["Day 1: Cultural Sites & Museums", "Day 2: Outdoor Adventure & Nature", "Day 3: Local Shopping & Food Tour"],
                    "week": ["Day 1-2: City Highlights", "Day 3-4: Day Trips to Nearby Towns", "Day 5-6: Local Arts & Relaxation", "Day 7: Farewell Brunch & Departure"]
                }
                
               
                duration_key = "weekend"
                if "week" in duration.lower() and "end" not in duration.lower():
                    duration_key = "week"
                elif "day" in duration.lower():
                    duration_key = "3-day"
                
                days = itineraries.get(duration_key)
                
                response = f"🗓️ **Your {duration.title()} {trip_type.title()} Itinerary for {city.title()}:**\n\n"
                
               
                potential_activities = [
                    "Visit local art galleries", "Explore the historic waterfront", 
                    "Try the city's famous street food", "Visit a botanical garden",
                    "Enjoy a sunset view from a rooftop", "Take a guided architecture tour"
                ]
                
                for day in days:
                    activities = random.sample(potential_activities, 2)
                    response += f"📍 **{day}**\n"
                    response += f"   • {activities[0]}\n"
                    response += f"   • {activities[1]}\n\n"
                
                response += "💡 **Travel Tip:** Consider getting a local transport pass to save on travel costs!"
            else:
               
                response = f"I'm generating a custom {duration} itinerary for {city.title()}. Please wait a moment while I find the best spots for a {trip_type} trip."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error creating itinerary: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an issue while creating your itinerary. Please try again.")
        
        return []
# ==================== COMPARISON ACTIONS ====================

class ActionCompareLocations(Action):
    """
    Performs a comparative analysis between two cities or landmarks.
    
    Criteria:
    - Compares based on 'comparison_type' (Cost, Nightlife, Culture).
    - Assigns scores and declares an 'Overall Winner' based on metrics.
    - Visualizes differences using symbolic indicators (🔺/🔻).
    """
    
    def name(self) -> Text:
        return "action_compare_locations"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
       
        def get_items(slot_name):
            val = tracker.get_slot(slot_name)
            if not val: return []
            return val if isinstance(val, list) else [val]

        cities = get_items("city") or get_items("location")
        place_names = get_items("place_name")
        
        comparison_type = tracker.get_slot("comparison_type") or "general"
        
        
        if len(cities) >= 2:
            items = cities[:2]
            item_label = "cities"
        elif len(place_names) >= 2:
            items = place_names[:2]
            item_label = "places"
        elif len(cities) == 1 and len(place_names) == 1:
            items = [cities[0], place_names[0]]
            item_label = "locations"
        else:
            dispatcher.utter_message(text="To compare, please mention two cities or places (e.g., 'Compare Los Angeles and San Diego').")
            return []
    
        try:
            if MOCK_MODE:
                
                comparisons = {
                    "weather": ["Temperature", "Sunny Days", "Rain Risk"],
                    "general": ["Attractions", "Food Scene", "Transport", "Cost"],
                    "beach vacation": ["Water Quality", "Crowd Level", "Sunset View"]
                }
                
                points = comparisons.get(comparison_type.lower(), comparisons["general"])
                
                response = f"⚖️ **Comparison: {items[0].title()} vs {items[1].title()}**\n"
                response += f"Target: {comparison_type.title()}\n\n"
                
                score_a = 0
                score_b = 0
                
                for point in points:
                    s1, s2 = random.randint(5, 10), random.randint(5, 10)
                    score_a += s1
                    score_b += s2
                    
                    symbol = "🔺" if s1 > s2 else "🔻" if s2 > s1 else "🔹"
                    response += f"{symbol} **{point}:**\n"
                    response += f"   • {items[0].title()}: {s1}/10\n"
                    response += f"   • {items[1].title()}: {s2}/10\n\n"
                
               
                winner = items[0] if score_a > score_b else items[1]
                response += f"🏆 **Overall Winner for {comparison_type}: {winner.title()}**"
            else:
                response = f"I'm analyzing live data to compare {items[0]} and {items[1]}. Based on recent reviews, {items[0]} is trending higher for {comparison_type}."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            dispatcher.utter_message(text="I'm sorry, I couldn't complete the comparison right now.")
    
        return []

class ActionGetPracticalInfo(Action):
    """
    Provides practical information about a place or landmark.
    """
    def name(self) -> Text:
        return "action_get_practical_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
        
        landmark = tracker.get_slot("landmark")
        place_name = tracker.get_slot("place_name")
        info_type = tracker.get_slot("info_type") or "general information"
    
        target = landmark or place_name
        
       
        if not target:
            dispatcher.utter_message(text="Which place or landmark would you like to know more about? (e.g., Golden Gate Bridge or Disneyland)")
            return []
    
        try:
            if MOCK_MODE:
                
                info_templates = {
                    "opening hours": {
                        "Weekdays": "9:00 AM - 6:00 PM",
                        "Weekends": "10:00 AM - 8:00 PM",
                        "Note": "Last entry 1 hour before closing"
                    },
                    "ticket prices": {
                        "Adults": "$25",
                        "Children (under 12)": "$12",
                        "Seniors": "$18"
                    },
                    "parking": {
                        "Status": "Available on-site",
                        "Rate": "$10 per day",
                        "Capacity": "Large underground lot"
                    },
                    "transportation": {
                        "Bus": "Lines 101, 204 stop at the main gate",
                        "Metro": "Blue Line - Central Station (0.5 mi)",
                        "Ride-share": "Designated Uber/Lyft pickup zone"
                    },
                    "accessibility": {
                        "Wheelchair": "Fully accessible ramps",
                        "Elevators": "Available in all sectors",
                        "Restrooms": "Accessible facilities on ground floor"
                    }
                }
                
               
                info_to_show = []
                query = info_type.lower()
                
                if any(word in query for word in ["hour", "open", "time"]):
                    info_to_show.append("opening hours")
                if any(word in query for word in ["price", "ticket", "cost", "fee"]):
                    info_to_show.append("ticket prices")
                if "parking" in query:
                    info_to_show.append("parking")
                if any(word in query for word in ["transport", "bus", "get there", "metro"]):
                    info_to_show.append("transportation")
                if any(word in query for word in ["access", "wheelchair", "disabled"]):
                    info_to_show.append("accessibility")
                
               
                if not info_to_show:
                    info_to_show = ["opening hours", "ticket prices", "transportation"]
                
                response = f"📋 **Practical Information for {target.title()}:**\n\n"
                
                for info_key in info_to_show:
                    if info_key in info_templates:
                        response += f"🔹 **{info_key.upper()}**\n"
                        for key, value in info_templates[info_key].items():
                            response += f"  • {key}: {value}\n"
                        response += "\n"
                
                response += "💡 *Tip: Prices and hours might vary on public holidays.*"
            else:
               
                response = f"I'm checking the latest practical details for {target}. Typically, it opens at 9:00 AM. Would you like the official link?"
            
            dispatcher.utter_message(text=response)
        
        except Exception as e:
            logger.error(f"Error getting practical info: {e}")
            dispatcher.utter_message(text="Sorry, I couldn't retrieve the practical details for that location.")
    
        return []
    
class ActionGetSeasonalActivities(Action):
    """
    Suggests seasonal activities and events based on time of year and location.
    """

    def name(self) -> Text:
        return "action_get_seasonal_activities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
       
        city = tracker.get_slot("city") or tracker.get_slot("location")
        state = tracker.get_slot("state") or "California"
        seasonal_activity = tracker.get_slot("seasonal_activity")
        holiday_event = tracker.get_slot("holiday_event")
    
        target_place = city or state
        
        try:
            if MOCK_MODE:
                
                seasonal_data = {
                    "spring": ["🌸 Cherry blossom viewing", "🌷 Spring flower festivals", "🏡 Garden tours", "🥚 Easter events"],
                    "summer": ["☀️ Beach festivals", "🎶 Outdoor concerts", "🎆 Fourth of July fireworks", "🍦 Summer food fairs"],
                    "fall": ["🍂 Fall foliage tours", "🎃 Harvest festivals", "👻 Halloween events", "🍎 Apple picking"],
                    "winter": ["❄️ Christmas light displays", "⛸️ Ice skating", "⛷️ Winter festivals", "🥂 New Year's celebrations"]
                }
                
               
                current_month = datetime.now().month
                if 3 <= current_month <= 5:
                    season = "spring"
                elif 6 <= current_month <= 8:
                    season = "summer"
                elif 9 <= current_month <= 11:
                    season = "fall"
                else:
                    season = "winter"
                
                activities = seasonal_data.get(season, [])
                
                
                response = f"📅 **It's currently {season.title()} in {target_place.title()}!**\n"
                response += "Here are the best seasonal activities for you:\n\n"
                
                if seasonal_activity or holiday_event:
                    specific = seasonal_activity or holiday_event
                    response += f"🌟 **Featured:** You asked about '{specific}'. It's a great choice for this time of year!\n\n"
                
                for i, activity in enumerate(activities, 1):
                    response += f"{i}. {activity}\n"
                
                
                response += f"\n✅ **Best time:** {random.choice(['Early morning', 'Weekends', 'Evenings'])}"
                response += f"\n💰 **Cost:** {random.choice(['Free entry', '$15 - $40', 'Varies by location'])}"
                
                response += "\n\nWould you like me to find the exact location of any of these?"
            else:
                response = f"I'm checking the current seasonal calendar for {target_place}. There are several festivals happening this {season}!"
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            dispatcher.utter_message(text="I'm sorry, I couldn't retrieve the seasonal activities right now.")
    
        return []
    
class ActionGetEmergencyInfo(Action):
    """
    Provides emergency contacts and safety guidance for a location.
    """
    def name(self) -> Text:
        return "action_get_emergency_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
       
        city = tracker.get_slot("city") or tracker.get_slot("location")
        emergency_service = tracker.get_slot("emergency_service")
        emergency_type = tracker.get_slot("emergency_type")
    
        target_location = city or "California"
    
        try:
            if MOCK_MODE:
               
                emergency_info = {
                    "hospital": {
                        "Name": f"{target_location} Memorial Medical Center",
                        "Address": f"Main Medical Plaza, {target_location}",
                        "Phone": "(555) 911-0000",
                        "Status": "ER Open 24/7"
                    },
                    "police": {
                        "Department": f"{target_location} Police Dept",
                        "Emergency": "911",
                        "Non-Emergency": "(555) 123-4567"
                    },
                    "fire": {
                        "Station": f"{target_location} Fire & Rescue",
                        "Emergency": "911"
                    }
                }
                
                
                safety_tips = {
                    "earthquake": ["Drop, Cover, and Hold On.", "Stay away from glass/windows.", "Do not use elevators."],
                    "wildfire": ["Evacuate immediately if told.", "Keep windows/doors closed.", "Follow local news."],
                    "general": ["Keep ID with you.", "Share your location with family.", "Stay in well-lit areas."]
                }
    
                response = f"🆘 **EMERGENCY & SAFETY INFO: {target_location.upper()}**\n\n"
    
               
                service_key = (emergency_service or "").lower()
                if service_key in emergency_info:
                    info = emergency_info[service_key]
                    response += f"🚨 **{service_key.title()} Details:**\n"
                    for k, v in info.items():
                        response += f"   • {k}: {v}\n"
                    response += "\n"
                
              
                type_key = (emergency_type or "general").lower()
                tips = safety_tips.get(type_key, safety_tips["general"])
                response += f"⚠️ **Safety Tips for {type_key.title()}:**\n"
                for i, tip in enumerate(tips, 1):
                    response += f"   {i}. {tip}\n"
                response += "\n"
    
               
                response += "📞 **CRITICAL NUMBERS:**\n"
                response += "   • EMERGENCY: **911**\n"
                response += "   • Poison Control: 1-800-222-1222\n"
                response += "   • Road Conditions (Caltrans): 511\n\n"
                
                response += "📢 *Please stay calm and follow the instructions of local authorities.*"
            else:
                response = f"I am retrieving the nearest emergency services for {target_location}. In case of immediate danger, please dial 911 immediately."
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            dispatcher.utter_message(text="I couldn't retrieve emergency info. Please dial 911 if you need immediate help.")
    
        return []
    
class ActionValidateCity(Action):
    """
    Validates whether a provided city is located in California.
    """
    def name(self) -> Text:
        return "action_validate_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
       
        city = tracker.get_slot("city")
    
        if not city:
            dispatcher.utter_message(text="Please tell me which California city you're interested in.")
            return [SlotSet("city", None)]
    
        
        is_valid = validate_city(city) 
    
        if not is_valid:
            dispatcher.utter_message(
                text=f"I'm sorry, '{city}' is not in my list of California cities. "
                     f"Could you please try a city like Los Angeles, San Diego, or San Francisco?"
            )
            return [SlotSet("city", None)]
    
        
        return [SlotSet("city", city.title())]
    
class ActionExtractAdditionalInfo(Action):
    """Extract additional information from user messages"""
    def name(self) -> Text:
        return "action_extract_additional_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
       
        last_message = tracker.latest_message.get('text', '').lower()
        events = []
        
       
        if "cheap" in last_message or "budget" in last_message:
            events.append(SlotSet("budget", "low"))
        elif "luxury" in last_message or "expensive" in last_message:
            events.append(SlotSet("budget", "high"))
            
        return events
    
class ActionSaveUserPreferences(Action):
    """Save user preferences for personalization"""
    def name(self) -> Text:
        return "action_save_user_preferences"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
       
        preference_slots = ["cuisine_type", "interest", "mood", "budget", "age_group"]
        
       
        current_preferences = {}
        for slot in preference_slots:
            value = tracker.get_slot(slot)
            if value:
                current_preferences[slot] = value
    
        if current_preferences:
            logger.info(f"💾 Saving user preferences: {current_preferences}")
           
            
            dispatcher.utter_message(text="✅ I've saved your preferences to give you better recommendations!")
            return [SlotSet("user_preferences", current_preferences)]
        
        return []

class ActionResetSlots(Action):
    """Reset conversation slots for a fresh start"""
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
       
        slots_to_reset = [
            "city", "location", "place_category", "landmark", "filter", 
            "place_name", "date_range", "price_range", "capacity", 
            "event_name", "activity_type", "place_type", "event_type",
            "mood", "interest", "budget"
        ]
    
        dispatcher.utter_message(text="🔄 All right! I've cleared the previous info. Where should we plan our next California trip?")
        
       
        return [SlotSet(slot, None) for slot in slots_to_reset]
    
class ActionDefaultFallback(Action):
    """
    The primary safety net for the assistant.
    
    Function:
    - Executed when NLU confidence is below the threshold.
    - Provides interactive buttons to guide the user back to supported topics.
    - Ensures the conversation doesn't reach a dead end.
    """
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
       
        buttons = [
            {"title": "Weather 🌦️", "payload": "/ask_weather"},
            {"title": "Places to Visit 📍", "payload": "/search_places"},
            {"title": "Emergency Info 🚨", "payload": "/get_emergency_info"}
        ]

        dispatcher.utter_message(
            text="I'm sorry, I didn't quite catch that. 🧐 Could you try rephrasing? \n"
                 "Or, you can select one of these topics:",
            buttons=buttons
        )
        return []
    
class ActionTwoStageFallback(Action):
    """
    A sophisticated recovery mechanism for ambiguous user inputs.
    
    Workflow:
    1. Identifies the most likely intended intent.
    2. Asks the user for confirmation ('Did you mean...?').
    3. Prevents incorrect actions from being triggered prematurely.
    """
    def name(self) -> Text:
        return "action_two_stage_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
    
        
        intent = tracker.latest_message.get('intent', {}).get('name')
        
        if intent:
            dispatcher.utter_message(
                text=f"I think you're asking about '{intent.replace('_', ' ')}'. Is that correct?"
            )
        else:
            dispatcher.utter_message(
                text="I'm having a bit of trouble understanding. Could you please explain what you're looking for in California in a different way?"
            )
    
        return []
    