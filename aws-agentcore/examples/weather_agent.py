"""
Weather Agent for AWS AgentCore Demo

This module provides a simple weather agent implementation for demonstration purposes.
"""

import json
import random
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


def get_mock_weather_data(location: str) -> Dict[str, Any]:
    """Generate mock weather data for demonstration purposes."""
    
    # Mock weather conditions
    conditions = ["Sunny", "Partly cloudy", "Cloudy", "Rainy", "Stormy", "Snowy"]
    
    # Generate realistic temperature based on location
    base_temp = 20  # Default base temperature
    if "tokyo" in location.lower():
        base_temp = 22
    elif "london" in location.lower():
        base_temp = 15
    elif "seattle" in location.lower():
        base_temp = 18
    elif "miami" in location.lower():
        base_temp = 28
    
    # Add some randomness
    temperature = base_temp + random.randint(-5, 10)
    
    return {
        "location": location,
        "temperature": f"{temperature}°C",
        "condition": random.choice(conditions),
        "humidity": f"{random.randint(40, 80)}%",
        "wind": f"{random.randint(5, 25)} km/h {random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])}",
        "feels_like": f"{temperature + random.randint(-2, 3)}°C",
        "visibility": f"{random.randint(8, 15)} km",
        "pressure": f"{random.randint(1000, 1020)} hPa"
    }


def get_mock_forecast_data(location: str, days: int = 3) -> Dict[str, Any]:
    """Generate mock forecast data for demonstration purposes."""
    
    forecast = []
    base_date = datetime.now()
    
    for i in range(min(days, 5)):  # Limit to 5 days
        date = base_date + timedelta(days=i)
        day_weather = get_mock_weather_data(location)
        
        forecast.append({
            "day": f"Day {i + 1}",
            "date": date.strftime("%Y-%m-%d"),
            "high": day_weather["temperature"],
            "low": f"{int(day_weather['temperature'].replace('°C', '')) - random.randint(3, 8)}°C",
            "condition": day_weather["condition"],
            "chance_of_rain": f"{random.randint(0, 30)}%"
        })
    
    return {
        "location": location,
        "forecast_days": len(forecast),
        "forecast": forecast
    }


def invoke(query: str) -> str:
    """
    Main invoke function for the weather agent.
    
    Args:
        query: User query about weather
        
    Returns:
        Weather information as a formatted string
    """
    
    try:
        # Simple query parsing
        query_lower = query.lower()
        
        # Extract location from query
        location = "Unknown Location"
        
        # Simple location extraction
        if "tokyo" in query_lower:
            location = "Tokyo"
        elif "london" in query_lower:
            location = "London"
        elif "seattle" in query_lower:
            location = "Seattle"
        elif "miami" in query_lower:
            location = "Miami"
        elif "new york" in query_lower or "nyc" in query_lower:
            location = "New York"
        elif "paris" in query_lower:
            location = "Paris"
        else:
            # Try to extract any capitalized word as location
            words = query.split()
            for word in words:
                if word and word[0].isupper() and len(word) > 2:
                    location = word
                    break
        
        # Determine if it's a forecast request
        if any(word in query_lower for word in ["forecast", "week", "days", "tomorrow", "future"]):
            # Forecast request
            days = 3
            if "5" in query or "five" in query_lower:
                days = 5
            elif "7" in query or "week" in query_lower:
                days = 7
            
            forecast_data = get_mock_forecast_data(location, days)
            
            return f"Here's the weather forecast for {location}:\n\n{json.dumps(forecast_data, indent=2)}"
        
        else:
            # Current weather request
            weather_data = get_mock_weather_data(location)
            
            return f"Here's the current weather for {location}:\n\n{json.dumps(weather_data, indent=2)}"
    
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your weather request: {str(e)}"


# For backward compatibility
def weather_agent_invoke(query: str) -> str:
    """Alias for invoke function."""
    return invoke(query)


def lambda_handler(event, context):
    """
    AWS Lambda handler function for the weather agent.
    
    Args:
        event: Lambda event containing the request data
        context: Lambda context object
        
    Returns:
        Response dictionary with weather information
    """
    try:
        # Extract input from event
        if isinstance(event, dict):
            # Handle different event formats
            if 'input' in event:
                query = event['input']
            elif 'prompt' in event:
                query = event['prompt']
            elif 'query' in event:
                query = event['query']
            elif 'body' in event:
                # Handle API Gateway format
                body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
                query = body.get('input', body.get('prompt', body.get('query', 'What is the weather?')))
            else:
                query = str(event)
        else:
            query = str(event)
        
        # Get weather response
        result = invoke(query)
        
        # Return response in expected format
        return {
            "result": result,
            "session_id": "default-session",
            "status": "success",
            "metadata": {
                "agent_type": "weather_assistant",
                "timestamp": datetime.now().isoformat(),
                "user_id": None,
                "toolkit_available": True,
                "langchain_available": False
            }
        }
        
    except Exception as e:
        return {
            "result": f"Error processing weather request: {str(e)}",
            "session_id": "default-session", 
            "status": "error",
            "error": str(e),
            "metadata": {
                "agent_type": "weather_assistant",
                "timestamp": datetime.now().isoformat(),
                "user_id": None,
                "toolkit_available": True,
                "langchain_available": False
            }
        }


if __name__ == "__main__":
    # Test the weather agent
    test_queries = [
        "What's the weather like in Tokyo?",
        "Show me the 5-day forecast for London",
        "How's the weather in Seattle today?",
        "What about tomorrow in Miami?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Response: {invoke(query)}")
        print("-" * 50)