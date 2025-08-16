# AWS AgentCore Production-Ready Implementation

This project provides a comprehensive, production-ready implementation of AWS AgentCore with real agents that can be deployed to AWS environments. Based on extensive research and testing, this repository demonstrates proper AgentCore integration following official specifications and best practices.

## 🌤️ What This Implementation Provides

### **Production-Ready Weather Agent**
A fully functional weather agent that demonstrates:
- ✅ **AgentCore Runtime Integration** - Proper deployment to AWS AgentCore Runtime
- ✅ **Specification Compliance** - Follows official AgentCore API standards
- ✅ **Local Development Support** - Environment-controlled testing mode
- ✅ **Error Handling** - Robust error management and logging
- ✅ **Session Management** - Proper session handling for conversations
- ✅ **Multiple Integration Options** - Supports both direct AgentCore and LangChain frameworks

### **Key Capabilities**
- **Current Weather Information** - Real-time weather data for any location
- **Weather Forecasts** - Multi-day weather predictions
- **Weather Alerts** - Severe weather warnings and notifications
- **Interactive Conversation** - Natural language weather queries
- **Production Deployment** - Ready for AWS AgentCore Runtime
- **Local Testing** - Comprehensive test scenarios for development

## 📦 Installation & Setup

### **Prerequisites**
- Python 3.10 or higher
- AWS CLI configured with appropriate permissions
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### **Required AWS Permissions**
Your AWS user/role needs the following policies:
- `BedrockAgentCoreFullAccess` (managed policy)
- `AmazonBedrockFullAccess` (managed policy)
- ECR, CloudWatch Logs, and CodeBuild permissions for container deployment

### **Installation Steps**

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd aws-agentcore
   
   # Install dependencies (includes bedrock-agentcore and starter toolkit)
   poetry install
   ```

2. **Configure AWS Environment**
   ```bash
   # Create environment configuration
   cat > .env << EOF
   AWS_PROFILE=your-aws-profile
   AWS_DEFAULT_REGION=us-east-1
   AWS_REGION=us-east-1
   EOF
   
   # Load environment variables
   export $(cat .env | xargs)
   ```

3. **Configure AgentCore**
   ```bash
   # Initialize AgentCore configuration
   poetry run agentcore configure --entrypoint examples/weather_agent.py --name weather_demo --region us-east-1
   ```

### **Dependency Verification**
```bash
# Verify all required packages are installed
poetry run python -c "
import bedrock_agentcore
import strands_agents
from bedrock_agentcore_starter_toolkit import AgentCoreApp
print('✅ All AgentCore dependencies successfully installed')
"
```

## 🎯 Usage

### **Production Agent Deployment**

1. **Test Locally**
   ```bash
   # Run local tests (important: use environment variable)
   WEATHER_AGENT_RUN_TESTS=true poetry run python examples/weather_agent.py
   ```

2. **Deploy to AWS AgentCore**
   ```bash
   # Ensure environment variables are loaded
   export $(cat .env | xargs)
   
   # Deploy the agent to AgentCore Runtime
   poetry run agentcore launch --agent weather_demo
   ```

3. **Test Production Agent**
   ```bash
   # Test with AgentCore specification compliant payload
   poetry run agentcore invoke --agent weather_demo '{"prompt":"What is the weather like in Tokyo?"}'
   ```

### **Development and Testing**

```bash
# Local testing mode (bypasses production behavior)
WEATHER_AGENT_RUN_TESTS=true poetry run python examples/weather_agent.py

# Production mode simulation (no tests, ready for requests)
poetry run python examples/weather_agent.py

# Check agent configuration
poetry run agentcore configure list

# Monitor agent status
poetry run agentcore status --agent weather_demo
```

### **Additional Testing**
```bash
# Test the weather agent with different queries
WEATHER_AGENT_RUN_TESTS=true poetry run python examples/weather_agent.py

# Test specific weather functions
poetry run python -c "
from examples.weather_agent import get_current_weather
print(get_current_weather('London'))
"
```

## 🛠️ Configuration

### **Environment Configuration**

Create a `.env` file for consistent environment setup:

```bash
# AWS Configuration (required)
AWS_PROFILE=your-aws-profile          # AWS profile name
AWS_DEFAULT_REGION=us-east-1          # Primary region
AWS_REGION=us-east-1                  # Ensure consistency

# Agent Testing Configuration
WEATHER_AGENT_RUN_TESTS=true          # Enable local testing mode
```

### **AWS Profile Setup**

Ensure your AWS profile has proper permissions:

```bash
# Check your AWS profile
aws configure list --profile your-aws-profile

# Verify credentials work
aws sts get-caller-identity --profile your-aws-profile

# Test AgentCore access
aws bedrock list-foundation-models --region us-east-1 --profile your-aws-profile
```

### **AgentCore Architecture Compliance**

This implementation follows official AgentCore specifications:

- **Entry Point**: Uses `@app.entrypoint def invoke(payload)` as required
- **Payload Structure**: Accepts `{"prompt": "user message"}` format
- **Response Format**: Returns `{"result": "agent response"}` structure
- **Dependencies**: Includes all required packages (`bedrock-agentcore`, `strands-agents`, `bedrock-agentcore-starter-toolkit`)
- **Runtime Integration**: Proper HTTP server on port 8080 with `/invocations` and `/ping` endpoints

## 📖 Project Structure

```
aws-agentcore/
├── examples/
│   └── weather_agent.py       # Production-ready weather agent
├── pyproject.toml             # Project dependencies and configuration
├── poetry.toml               # Poetry configuration
├── poetry.lock               # Locked dependency versions
├── Dockerfile                # Container configuration for deployment
├── .dockerignore            # Docker build optimization
├── .gitignore               # Git ignore patterns
└── README.md                # This comprehensive guide
```

### **Core Files Explained**

- **`examples/weather_agent.py`** - The main weather agent implementation following AgentCore specifications
- **`pyproject.toml`** - Contains all required dependencies including `bedrock-agentcore`, `strands-agents`, and `bedrock-agentcore-starter-toolkit`
- **`Dockerfile`** - Configured for AgentCore Runtime deployment with proper Python environment
- **Configuration files** - Optimized for both local development and production deployment

## 🔍 Weather Agent Capabilities

### **Weather Information Features**
- **Current Weather** - Real-time weather conditions including temperature, humidity, wind speed, and visibility
- **Weather Forecasts** - Multi-day weather predictions with high/low temperatures and conditions
- **Weather Alerts** - Severe weather warnings and emergency notifications
- **Location Support** - Works with city names, coordinates, and natural language location descriptions

### **Technical Features**
- **Natural Language Processing** - Understands conversational weather queries
- **Session Management** - Maintains conversation context across multiple requests
- **Error Handling** - Graceful handling of invalid locations or service errors
- **Framework Integration** - Optional LangChain integration for enhanced capabilities
- **Logging and Monitoring** - Comprehensive logging for debugging and monitoring

## 🚦 Quick Start Guide

### **Complete Deployment Walkthrough**

1. **Setup Environment**
   ```bash
   # Clone and install
   git clone <repository-url> && cd aws-agentcore
   poetry install
   
   # Configure AWS environment
   echo "AWS_PROFILE=your-profile\nAWS_DEFAULT_REGION=us-east-1\nAWS_REGION=us-east-1" > .env
   export $(cat .env | xargs)
   ```

2. **Test Agent Locally**
   ```bash
   # Test with environment variable (crucial for proper testing)
   WEATHER_AGENT_RUN_TESTS=true poetry run python examples/weather_agent.py
   ```

3. **Configure and Deploy**
   ```bash
   # Configure agent for deployment
   poetry run agentcore configure --entrypoint examples/weather_agent.py --name weather_demo --region us-east-1
   
   # Deploy to AWS AgentCore Runtime
   poetry run agentcore launch --agent weather_demo
   ```

4. **Verify Production Deployment**
   ```bash
   # Test deployed agent with proper payload format
   poetry run agentcore invoke --agent weather_demo '{"prompt":"Weather in Tokyo"}'
   ```

### **Expected Success Output**
```json
{
  "result": "Here's the current weather for Tokyo...",
  "session_id": "session-id",
  "status": "success",
  "statusCode": 200
}
```

### **Troubleshooting**

**Common Issues and Solutions:**

1. **"AgentCore toolkit not available"**
   - Ensure `bedrock-agentcore` and `strands-agents` are installed
   - Run `poetry install` to update dependencies

2. **"Access denied" errors**
   - Verify AWS permissions (need `BedrockAgentCoreFullAccess` and `AmazonBedrockFullAccess`)
   - Check your AWS profile: `aws sts get-caller-identity --profile your-profile`

3. **Runtime startup errors**
   - Review CloudWatch logs: `aws logs tail /aws/bedrock-agentcore/runtimes/weather_demo-*/runtime-logs --region us-east-1`
   - Ensure environment variables are properly set

4. **Local testing not working**
   - Always use `WEATHER_AGENT_RUN_TESTS=true` for local testing
   - Without this environment variable, the agent runs in production mode

## 🏗️ Agent Development Best Practices

### **AgentCore Specification Compliance**

This implementation strictly follows official AgentCore specifications discovered through extensive testing:

```python
# ✅ Correct agent structure
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Extract input (supports both 'prompt' and 'input' for compatibility)
    user_input = payload.get("prompt", "") or payload.get("input", "")
    
    # Process request
    response = process_request(user_input)
    
    # Return in correct format
    return {
        "result": response,                    # Use 'result', not 'response'
        "session_id": payload.get("session_id", "default"),
        "status": "success",
        "metadata": {...}
    }

if __name__ == "__main__":
    app.run()
```

### **Environment-Based Testing Strategy**

```python
# Development: Enable testing mode
WEATHER_AGENT_RUN_TESTS=true python examples/weather_agent.py

# Production: Run without tests (default)
python examples/weather_agent.py
```

### **Required Dependencies**

```toml
# pyproject.toml
[tool.poetry.dependencies]
bedrock-agentcore-starter-toolkit = "^0.1.6"
bedrock-agentcore = "*"
strands-agents = "*"
```

## 📚 Resources and Documentation

### **Official Documentation**
- [AWS AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AgentCore Starter Toolkit](https://aws.github.io/bedrock-agentcore-starter-toolkit/)
- [AgentCore Quickstart Guide](https://aws.github.io/bedrock-agentcore-starter-toolkit/user-guide/runtime/quickstart.html)

### **This Implementation**
- **Specification Compliant**: Follows official AgentCore runtime expectations
- **Production Ready**: Successfully tested in AWS AgentCore Runtime environment
- **Best Practices**: Incorporates lessons learned from extensive debugging and testing
- **Dual Mode**: Supports both local development and production deployment

## 🔬 Research & Implementation Journey

This implementation is the result of comprehensive research, debugging, and testing to achieve successful AWS AgentCore Runtime deployment. Here are the key discoveries:

### **Critical Findings**

1. **Correct AgentCore Imports**
   ```python
   # ✅ Primary import (works in production)
   from bedrock_agentcore import BedrockAgentCoreApp
   
   # ✅ Fallback import (for compatibility)
   from bedrock_agentcore_starter_toolkit import AgentCoreApp as BedrockAgentCoreApp
   ```

2. **Essential Dependencies**
   - `bedrock-agentcore`: Core runtime functionality
   - `strands-agents`: Agent framework integration
   - `bedrock-agentcore-starter-toolkit`: CLI and deployment tools

3. **AgentCore Runtime Expectations**
   - **Entry Point**: `@app.entrypoint def invoke(payload)`
   - **Payload Format**: `{"prompt": "user message"}`
   - **Response Format**: `{"result": "agent response"}`
   - **HTTP Endpoints**: `/invocations` (POST) and `/ping` (GET) on port 8080

4. **Environment Control Strategy**
   ```python
   # Development/Testing
   WEATHER_AGENT_RUN_TESTS=true python agent.py
   
   # Production (no automatic tests)
   python agent.py
   ```

### **Common Pitfalls Avoided**

1. **❌ Wrong Entry Point Name**
   ```python
   # Wrong
   @app.entrypoint
   def weather_agent_handler(request):
   
   # ✅ Correct
   @app.entrypoint
   def invoke(payload):
   ```

2. **❌ Incorrect Response Structure**
   ```python
   # Wrong
   return {"response": "..."}
   
   # ✅ Correct
   return {"result": "..."}
   ```

3. **❌ Missing Dependencies**
   ```toml
   # Insufficient
   bedrock-agentcore-starter-toolkit = "^0.1.6"
   
   # ✅ Complete
   bedrock-agentcore-starter-toolkit = "^0.1.6"
   bedrock-agentcore = "*"
   strands-agents = "*"
   ```

4. **❌ Automatic Test Execution in Production**
   ```python
   # Problematic - tests run in container
   if __name__ == "__main__":
       run_tests()
   
   # ✅ Controlled execution
   if __name__ == "__main__":
       if should_run_local_tests():
           run_tests()
       else:
           app.run()
   ```

### **Debugging Process Insights**

Our implementation journey involved:

1. **Specification Research**: Studying official AgentCore documentation
2. **Dependency Analysis**: Identifying required vs. optional packages
3. **Runtime Environment Testing**: Understanding container behavior
4. **CloudWatch Log Analysis**: Debugging deployment issues
5. **IAM Permission Optimization**: Configuring proper AWS access
6. **Payload Format Validation**: Ensuring specification compliance

### **Production Validation**

Final verification confirmed:
- ✅ HTTP Status Code: 200
- ✅ Proper JSON response structure
- ✅ Session management functionality
- ✅ AgentCore toolkit recognition (`toolkit_available: true`)
- ✅ Error-free CloudWatch logs
- ✅ Successful agent invocation

## 🤝 Contributing

This project represents a production-ready implementation based on comprehensive research and testing. Contributions should maintain:

1. **AgentCore Specification Compliance**
2. **Production Deployment Capability** 
3. **Comprehensive Testing Strategy**
4. **Clear Documentation**

### **Validation Process**

Before contributing, ensure your changes pass:

```bash
# Local testing
WEATHER_AGENT_RUN_TESTS=true poetry run python examples/weather_agent.py

# Production deployment
poetry run agentcore launch --agent your_agent

# Production verification
poetry run agentcore invoke --agent your_agent '{"prompt":"test message"}'
```