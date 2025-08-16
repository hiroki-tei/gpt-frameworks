#!/usr/bin/env python3
"""
Sample Weather Agent using AWS AgentCore Toolkit

This is a complete, working example of an agent built with the
bedrock-agentcore-starter-toolkit that can be deployed to production.

Usage:
    # Deploy to AgentCore
    agentcore launch weather_agent.py --name weather-bot --memory

    # Test locally
    python weather_agent.py
"""

import json
import os
from typing import Dict, Any

# Try to import AgentCore toolkit - Multiple import attempts for reliability
TOOLKIT_AVAILABLE = False
AgentCoreApp = None

# Primary AgentCore import (correct specification)
try:
    from bedrock_agentcore import BedrockAgentCoreApp
    TOOLKIT_AVAILABLE = True
    print("✅ AgentCore loaded successfully")
except ImportError:
    print("⚠️ AgentCore not available")
    TOOLKIT_AVAILABLE = False

# Fallback for starter toolkit (if primary fails)
if not TOOLKIT_AVAILABLE:
    try:
        from bedrock_agentcore_starter_toolkit import AgentCoreApp as BedrockAgentCoreApp
        TOOLKIT_AVAILABLE = True
        print("✅ AgentCore starter toolkit loaded successfully")
    except ImportError:
        print("⚠️ AgentCore starter toolkit not available")

# Fallback: Create minimal AgentCore app for development
if not TOOLKIT_AVAILABLE:
    print("⚠️ All AgentCore packages unavailable - using fallback mode")
    
    class BedrockAgentCoreApp:
        def __init__(self):
            self.handlers = {}
        
        def entrypoint(self, func):
            self.handlers['main'] = func
            return func
        
        def run(self):
            # For fallback AgentCore app when toolkit is not available
            if should_run_local_tests():
                # Only run test when explicitly requested
                test_request = {
                    "input": "What's the weather like in Tokyo?",
                    "session_id": "test-session-123"
                }
                
                if 'main' in self.handlers:
                    result = self.handlers['main'](test_request)
                    print("🌤️ Weather Agent Response:")
                    print(json.dumps(result, indent=2))
                else:
                    print("No entrypoint handler registered")
            else:
                # In production mode, expose HTTP server on port 8080 as expected by AgentCore Runtime
                print("🌤️ Starting HTTP server on port 8080 for AgentCore Runtime...")
                try:
                    import http.server
                    import socketserver
                    import json as json_lib
                    from urllib.parse import parse_qs
                    
                    class AgentCoreHandler(http.server.BaseHTTPRequestHandler):
                        def do_POST(self):
                            try:
                                # AgentCore Runtime expects /invocations endpoint
                                if self.path == '/invocations':
                                    content_length = int(self.headers.get('Content-Length', 0))
                                    post_data = self.rfile.read(content_length)
                                    request_data = json_lib.loads(post_data.decode('utf-8'))
                                    
                                    # Call the registered handler
                                    if 'main' in self.server.agent_handlers:
                                        result = self.server.agent_handlers['main'](request_data)
                                        
                                        self.send_response(200)
                                        self.send_header('Content-Type', 'application/json')
                                        self.end_headers()
                                        self.wfile.write(json_lib.dumps(result).encode('utf-8'))
                                    else:
                                        self.send_error(500, "No handler registered")
                                else:
                                    self.send_error(404, "Not found")
                            except Exception as e:
                                print(f"Error processing request: {e}")
                                self.send_error(500, str(e))
                        
                        def do_GET(self):
                            # Health check endpoint expected by AgentCore Runtime
                            if self.path == '/ping':
                                self.send_response(200)
                                self.send_header('Content-Type', 'application/json')
                                self.end_headers()
                                response = {"status": "healthy", "agent": "weather_demo"}
                                self.wfile.write(json_lib.dumps(response).encode('utf-8'))
                            else:
                                self.send_error(404, "Not found")
                        
                        def log_message(self, format, *args):
                            print(f"[HTTP] {format % args}")
                    
                    with socketserver.TCPServer(("0.0.0.0", 8080), AgentCoreHandler) as httpd:
                        httpd.agent_handlers = self.handlers
                        print("✅ HTTP server ready on port 8080")
                        print("📡 Endpoints: /invocations (POST), /ping (GET)")
                        httpd.serve_forever()
                        
                except Exception as e:
                    print(f"❌ Failed to start HTTP server: {e}")
                    # Keep process alive as fallback
                    import time
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("Agent stopped")

# LangChain imports (optional, for advanced agent capabilities)
try:
    from langchain.agents import create_react_agent, AgentExecutor
    from langchain.tools import Tool
    from langchain_aws import ChatBedrock
    from langchain import hub
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("ℹ️ LangChain not available - using simple response generation")

# Initialize AgentCore app
app = BedrockAgentCoreApp()

# Create a WSGI-compatible application for AgentCore Runtime
def application(environ, start_response):
    """WSGI application for AgentCore Runtime compatibility."""
    try:
        # Get request method and path
        method = environ.get('REQUEST_METHOD', 'GET')
        path = environ.get('PATH_INFO', '/')
        
        if method == 'POST' and path == '/invoke':
            # Read request body
            content_length = int(environ.get('CONTENT_LENGTH', '0'))
            if content_length:
                request_body = environ['wsgi.input'].read(content_length)
                request_data = json.loads(request_body.decode('utf-8'))
                
                # Call the weather agent handler
                result = invoke(request_data)
                
                # Return JSON response
                response_data = json.dumps(result).encode('utf-8')
                status = '200 OK'
                headers = [
                    ('Content-Type', 'application/json'),
                    ('Content-Length', str(len(response_data)))
                ]
                start_response(status, headers)
                return [response_data]
        
        # Health check endpoint
        elif method == 'GET' and path == '/health':
            response_data = json.dumps({"status": "healthy", "agent": "weather_demo"}).encode('utf-8')
            status = '200 OK'
            headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_data)))
            ]
            start_response(status, headers)
            return [response_data]
        
        # Default response
        else:
            response_data = json.dumps({"error": "Not found", "path": path, "method": method}).encode('utf-8')
            status = '404 Not Found'
            headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_data)))
            ]
            start_response(status, headers)
            return [response_data]
            
    except Exception as e:
        error_data = json.dumps({"error": str(e), "type": type(e).__name__}).encode('utf-8')
        status = '500 Internal Server Error'
        headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(error_data)))
        ]
        start_response(status, headers)
        return [error_data]

def get_current_weather(location: str) -> str:
    """
    Get current weather information for a location.
    
    In a real implementation, this would call a weather API like OpenWeatherMap.
    """
    # Mock weather data for demonstration
    weather_data = {
        "location": location,
        "temperature": "22°C",
        "condition": "Partly cloudy",
        "humidity": "65%",
        "wind": "10 km/h NE",
        "feels_like": "24°C",
        "visibility": "10 km",
        "pressure": "1013 hPa"
    }
    
    return json.dumps(weather_data, indent=2)

def get_weather_forecast(location: str, days: int = 3) -> str:
    """
    Get weather forecast for a location.
    
    Args:
        location: City name or location
        days: Number of days for forecast (default: 3)
    """
    forecast = []
    conditions = ["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Clear"]
    
    for i in range(min(days, 7)):  # Max 7 days
        forecast.append({
            "day": f"Day {i+1}",
            "date": f"2024-01-{15+i:02d}",
            "high": f"{20+i*2}°C",
            "low": f"{15+i}°C", 
            "condition": conditions[i % len(conditions)],
            "chance_of_rain": f"{10 + i*5}%"
        })
    
    return json.dumps({
        "location": location,
        "forecast_days": days,
        "forecast": forecast
    }, indent=2)

def get_weather_alerts(location: str) -> str:
    """Get weather alerts and warnings for a location."""
    # Mock alert data
    alerts = [
        {
            "type": "High Temperature",
            "severity": "Minor",
            "description": f"Temperature in {location} expected to reach 35°C today",
            "valid_until": "2024-01-15 18:00"
        }
    ]
    
    return json.dumps({
        "location": location,
        "active_alerts": len(alerts),
        "alerts": alerts
    }, indent=2)

def create_weather_agent():
    """Create a weather agent with appropriate tools."""
    
    if LANGCHAIN_AVAILABLE:
        # Use LangChain for sophisticated agent behavior
        weather_tools = [
            Tool(
                name="get_current_weather",
                description="Get current weather conditions for a specific location. Use this for 'current', 'now', or 'today' weather requests.",
                func=get_current_weather
            ),
            Tool(
                name="get_weather_forecast",
                description="Get weather forecast for multiple days. Use this for 'forecast', 'upcoming', or 'next few days' requests.",
                func=lambda location: get_weather_forecast(location, 3)
            ),
            Tool(
                name="get_weather_alerts",
                description="Get weather alerts and warnings for a location. Use this for 'alerts', 'warnings', or 'severe weather' requests.",
                func=get_weather_alerts
            )
        ]
        
        try:
            # Try to use Bedrock Claude
            llm = ChatBedrock(
                model_id="anthropic.claude-3-sonnet-20240229-v1:0",
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
            
            prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, weather_tools, prompt)
            return AgentExecutor(agent=agent, tools=weather_tools, verbose=True)
            
        except Exception as e:
            print(f"⚠️ Could not initialize Bedrock LLM: {e}")
            # Fall back to simple implementation
            return None
    
    return None

def simple_weather_response(user_input: str) -> str:
    """Simple weather response when LangChain is not available."""
    user_input_lower = user_input.lower()
    
    # Extract location (simple heuristic)
    location = "Unknown Location"
    words = user_input.split()
    for i, word in enumerate(words):
        if word.lower() in ["in", "for", "at"] and i + 1 < len(words):
            location = words[i + 1].title()
            break
    
    # Determine response type based on keywords
    if any(keyword in user_input_lower for keyword in ["forecast", "tomorrow", "next", "upcoming", "days"]):
        return f"Here's the weather forecast for {location}:\n\n{get_weather_forecast(location)}"
    elif any(keyword in user_input_lower for keyword in ["alert", "warning", "severe"]):
        return f"Here are the weather alerts for {location}:\n\n{get_weather_alerts(location)}"
    else:
        return f"Here's the current weather for {location}:\n\n{get_current_weather(location)}"

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main agent entry point.
    
    This function is called by AgentCore Runtime for each request.
    
    Args:
        request: Dictionary containing:
            - input: User's message/question
            - session_id: Unique session identifier
            - user_id: User identifier (optional)
            - metadata: Additional request metadata (optional)
    
    Returns:
        Dictionary containing:
            - response: Agent's response message
            - session_id: Session identifier  
            - status: "success" or "error"
            - metadata: Additional response metadata (optional)
    """
    
    try:
        # Extract payload data (AgentCore standard)
        user_input = payload.get("prompt", "")
        
        # Also support "input" for backward compatibility
        if not user_input:
            user_input = payload.get("input", "")
            
        session_id = payload.get("session_id", "default-session")
        user_id = payload.get("user_id")
        
        # Validate input
        if not user_input.strip():
            return {
                "result": "Hello! I'm your weather assistant. Please ask me about the weather in any location. For example: 'What's the weather like in Tokyo?' or 'Show me the forecast for London'.",
                "session_id": session_id,
                "status": "success",
                "metadata": {"type": "welcome_message"}
            }
        
        # Try to use advanced agent first
        agent_executor = create_weather_agent()
        
        if agent_executor:
            # Use LangChain agent for sophisticated responses
            response = agent_executor.invoke({
                "input": user_input,
                "session_id": session_id
            })
            
            agent_response = response.get("output", "I couldn't process that weather request.")
        else:
            # Use simple weather response
            agent_response = simple_weather_response(user_input)
        
        # Log the interaction (in production, this would go to CloudWatch)
        print(f"[{session_id}] User: {user_input}")
        print(f"[{session_id}] Agent: {agent_response[:100]}...")
        
        return {
            "result": agent_response,
            "session_id": session_id,
            "status": "success",
            "metadata": {
                "agent_type": "weather_assistant",
                "timestamp": "2024-01-15T10:30:00Z",
                "user_id": user_id,
                "toolkit_available": TOOLKIT_AVAILABLE,
                "langchain_available": LANGCHAIN_AVAILABLE
            }
        }
        
    except Exception as e:
        error_message = f"I apologize, but I encountered an error while processing your weather request: {str(e)}"
        
        # Log the error (in production, this would go to CloudWatch)
        print(f"[ERROR] {session_id}: {str(e)}")
        
        return {
            "result": error_message,
            "session_id": session_id,
            "status": "error",
            "metadata": {
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        }

def run_local_tests():
    """
    Run local test scenarios for development and testing.
    This function is separated to avoid automatic execution in runtime environments.
    """
    print("🌤️ Weather Agent - Local Test Mode")
    print("=" * 50)
    
    # Test scenarios
    test_scenarios = [
        {
            "input": "What's the weather like in Tokyo?",
            "session_id": "test-session-1"
        },
        {
            "input": "Show me the forecast for London", 
            "session_id": "test-session-2"
        },
        {
            "input": "Are there any weather alerts for New York?",
            "session_id": "test-session-3"
        },
        {
            "input": "",  # Empty input test
            "session_id": "test-session-4"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🧪 Test Scenario {i}:")
        print(f"Input: '{scenario['input']}'")
        
        result = invoke(scenario)
        
        print(f"Status: {result['status']}")
        print(f"Response: {result['result'][:200]}{'...' if len(result['result']) > 200 else ''}")
        
        if result.get('metadata'):
            print(f"Metadata: {json.dumps(result['metadata'], indent=2)}")
    
    print(f"\n🚀 Agent ready for deployment!")
    
    if TOOLKIT_AVAILABLE:
        print("To deploy this agent to AWS AgentCore:")
        print("  agentcore launch weather_agent.py --name weather-bot --memory")
        print("  agentcore invoke weather-bot --input 'What is the weather in Paris?'")
    else:
        print("Install AgentCore toolkit to deploy:")
        print("  pip install bedrock-agentcore-starter-toolkit")
        print("  agentcore configure")

# Check if we should run in test mode or runtime mode
def should_run_tests():
    """
    Determine if we should run test scenarios.
    Return False if running in AgentCore Runtime environment.
    """
    import os
    import sys
    
    # Check for AgentCore Runtime specific environment variables
    agentcore_env_vars = [
        'BEDROCK_AGENTCORE_RUNTIME',
        'AWS_LAMBDA_FUNCTION_NAME',
        'AWS_EXECUTION_ENV',
        '_HANDLER'
    ]
    
    for env_var in agentcore_env_vars:
        if os.environ.get(env_var):
            return False
    
    # Check if running in container (Docker environment)
    if os.path.exists('/.dockerenv'):
        return False
        
    # Check command line arguments for toolkit availability
    # If toolkit is available but we're not running locally, don't run tests
    if TOOLKIT_AVAILABLE and 'python' not in sys.argv[0]:
        return False
    
    return True

# Check if this is being run as a direct script execution
def is_direct_execution():
    """Check if this script is being executed directly via 'python weather_agent.py'"""
    import sys
    import os
    
    # Check if we're being run directly via python command
    if len(sys.argv) > 0 and 'weather_agent.py' in sys.argv[0]:
        return True
    
    # Check if we're in an interactive environment 
    if hasattr(sys, 'ps1'):
        return True
        
    return False

# Environment-based control: Only run tests when explicitly requested
def should_run_local_tests():
    """
    Only run local tests when explicitly enabled via environment variable.
    This ensures tests never run in production/container environments.
    """
    import os
    return os.environ.get('WEATHER_AGENT_RUN_TESTS', '').lower() in ('true', '1', 'yes')

if __name__ == "__main__":
    """
    Weather Agent entry point.
    
    For local testing: WEATHER_AGENT_RUN_TESTS=true python weather_agent.py
    For deployment: agentcore launch weather_agent.py --name weather-bot
    """
    
    # Only run tests when explicitly enabled via environment variable
    if should_run_local_tests():
        print("🧪 Running in LOCAL TEST mode (WEATHER_AGENT_RUN_TESTS=true)")
        run_local_tests()
        
        # Run the app for local testing when toolkit is available
        if TOOLKIT_AVAILABLE:
            print("\n⚡ Starting AgentCore app for local testing...")
            app.run()
        else:
            print("\n⚠️ AgentCore toolkit not available. Install it for full functionality.")
    else:
        # Production/runtime mode - just register handler and wait for requests
        print("🌤️ Weather Agent - Production Mode")
        print("Handler registered via @app.entrypoint decorator")
        print("Ready to receive requests from AgentCore Runtime")
        
        if TOOLKIT_AVAILABLE:
            print("✅ AgentCore toolkit available")
            # Keep the app running to handle requests
            app.run()
        else:
            print("⚠️ AgentCore toolkit not available - running in fallback mode")
            print("💡 For local testing: WEATHER_AGENT_RUN_TESTS=true python weather_agent.py")
            # Start the fallback HTTP server for AgentCore Runtime
            app.run()

# Important: The agent handler is always registered via the @app.entrypoint decorator
# regardless of how the script is executed. This ensures AgentCore Runtime can
# always find and invoke the invoke function.

# Standard AgentCore Runtime entry points
def handler(event, context=None):
    """
    AWS Lambda-style handler for AgentCore Runtime.
    This is a common entry point that AgentCore Runtime might expect.
    """
    try:
        return invoke(event)
    except Exception as e:
        return {
            "result": f"Error: {str(e)}",
            "session_id": event.get("session_id", "unknown"),
            "status": "error",
            "metadata": {"error_type": type(e).__name__}
        }

def main(event=None, context=None):
    """
    Alternative entry point for AgentCore Runtime.
    """
    if event:
        return handler(event, context)
    else:
        # If called without event, it's probably a direct invocation
        return {
            "message": "Weather Agent is ready",
            "status": "ready",
            "handler": "invoke"
        }

# Export the handler function at module level for AgentCore Runtime
__all__ = ['invoke', 'handler', 'main', 'application']

# For AgentCore Runtime environments, the agent should be ready to handle requests
# without running the test scenarios automatically.
# The @app.entrypoint decorator ensures the invoke function 
# is properly registered for incoming requests.