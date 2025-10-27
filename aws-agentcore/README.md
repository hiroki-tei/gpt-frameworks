# AWS AgentCore Comprehensive Demo Application

This project provides a comprehensive demonstration of AWS AgentCore capabilities through an interactive web interface and production-ready implementation. Built upon a proven weather agent foundation, it showcases all AgentCore features including Runtime, Memory, Gateway, Identity, Code Interpreter, Browser Tool, and Observability through practical, educational examples.

## 🚀 What This Demo Application Provides

### **Interactive Web Interface**
A comprehensive web application that demonstrates:
- 🌐 **React Frontend** - Clean, tabbed interface for exploring each AgentCore feature
- ⚡ **FastAPI Backend** - RESTful API with real-time WebSocket updates
- 📊 **Live Monitoring** - Real-time observability dashboard and metrics
- 🎯 **Educational Examples** - Pre-built scenarios with step-by-step explanations
- 🔧 **Configuration Management** - Advanced parameter tuning and profile switching
- 🧩 **Plugin System** - Extensible architecture for new AgentCore features

### **Complete AgentCore Feature Showcase**
- ✅ **Runtime** - Production-ready weather agent with educational enhancements
- 🧠 **Memory** - Session management and conversation context tracking
- 🌐 **Gateway** - External API integration with retry logic and monitoring
- 🔐 **Identity** - AWS authentication and permission validation
- 💻 **Code Interpreter** - Sandboxed Python execution with visualization
- 🌍 **Browser Tool** - Web content fetching and analysis
- 📈 **Observability** - Comprehensive logging, metrics, and monitoring
- 🔄 **Integrated Workflows** - Multi-feature scenarios showing real-world usage

### **Key Capabilities**
- **Production Foundation** - Built on proven weather agent implementation
- **Educational Focus** - Plain-language explanations and guided learning
- **Extensible Architecture** - Plugin system for future AgentCore features
- **Advanced Configuration** - Multiple profiles (beginner, intermediate, advanced)
- **Comprehensive Testing** - Full test suite with performance benchmarks
- **Real-time Interaction** - WebSocket-based live updates and progress tracking

## 📦 Installation & Setup

### **Prerequisites**
- Python 3.10 or higher
- AWS CLI configured with appropriate permissions
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Node.js 16+ (for frontend development, optional)

### **Required AWS Permissions**
Your AWS user/role needs the following policies:
- `BedrockAgentCoreFullAccess` (managed policy)
- `AmazonBedrockFullAccess` (managed policy)
- ECR, CloudWatch Logs, and CodeBuild permissions for container deployment

### **Quick Start (Web Interface)**

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd aws-agentcore
   
   # Install all dependencies (includes web interface and demo features)
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

3. **Start the Demo Application**
   ```bash
   # Start the web interface (includes all AgentCore features)
   poetry run python web/backend/main.py
   
   # Open your browser to http://localhost:8000
   # The web interface provides guided exploration of all features
   ```

### **Alternative: Production Agent Setup**

For production AgentCore deployment:

```bash
# Configure AgentCore for production deployment
poetry run agentcore configure --entrypoint examples/weather_agent.py --name weather_demo --region us-east-1

# Deploy to AWS AgentCore Runtime
poetry run agentcore launch --agent weather_demo
```

### **Dependency Verification**
```bash
# Verify all required packages are installed
poetry run python -c "
import bedrock_agentcore
import strands_agents
from bedrock_agentcore_starter_toolkit import AgentCoreApp
import fastapi
import uvicorn
print('✅ All AgentCore and web interface dependencies successfully installed')
"
```

## 🎯 Usage

### **Web Interface (Recommended)**

1. **Start the Demo Application**
   ```bash
   # Ensure AWS environment is configured
   export $(cat .env | xargs)
   
   # Start the web interface
   poetry run python web/backend/main.py
   ```

2. **Explore AgentCore Features**
   - Open http://localhost:8000 in your browser
   - Navigate through tabs to explore each AgentCore feature:
     - **Runtime** - Weather agent with educational explanations
     - **Memory** - Conversation context and session management
     - **Gateway** - External API integration demonstrations
     - **Identity** - AWS authentication and permissions
     - **Code Interpreter** - Python execution with visualizations
     - **Browser Tool** - Web content fetching and analysis
     - **Observability** - Real-time monitoring and metrics
     - **Workflows** - Integrated multi-feature scenarios

3. **Try Example Scenarios**
   - Each feature includes pre-built examples
   - Modify inputs to see how different parameters affect results
   - Follow step-by-step explanations to understand AgentCore concepts

### **Advanced Configuration**

```bash
# Access configuration management
curl http://localhost:8000/api/config

# Switch to advanced configuration profile
curl -X PUT http://localhost:8000/api/config \
  -H "Content-Type: application/json" \
  -d '{"profile": "advanced"}'

# View available plugins
curl http://localhost:8000/api/plugins
```

### **Production Agent Deployment**

For production AWS AgentCore deployment:

1. **Test Locally**
   ```bash
   # Run local tests (important: use environment variable)
   WEATHER_AGENT_RUN_TESTS=true poetry run python examples/weather_agent.py
   ```

2. **Deploy to AWS AgentCore**
   ```bash
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
# Run comprehensive test suite
poetry run python run_tests.py --type all

# Run specific test categories
poetry run python run_tests.py --type web          # Web interface tests
poetry run python run_tests.py --type integration # Integration tests
poetry run python run_tests.py --type performance # Performance tests

# Test individual demo features
poetry run python demos/memory_demo.py
poetry run python demos/gateway_demo.py
poetry run python demos/observability_demo.py
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
│   └── weather_agent.py       # Production-ready weather agent (foundation)
├── demos/                     # AgentCore feature demonstrations
│   ├── memory_demo.py         # Memory service with session management
│   ├── gateway_demo.py        # Gateway service with API integration
│   ├── identity_demo.py       # Identity manager with AWS auth
│   ├── code_interpreter_demo.py # Code interpreter with sandboxed execution
│   ├── browser_tool_demo.py   # Browser tool with web content fetching
│   ├── observability_demo.py  # Observability with monitoring dashboard
│   └── workflow_demo.py       # Integrated multi-feature workflows
├── web/                       # Web interface application
│   ├── backend/               # FastAPI backend
│   │   ├── main.py           # Main application server
│   │   ├── routers/          # API endpoint routers
│   │   └── services/         # Business logic services
│   └── frontend/             # React frontend (optional)
│       ├── src/              # React components and services
│       └── package.json      # Frontend dependencies
├── plugins/                   # Plugin system for extensibility
│   ├── base.py               # Plugin base classes
│   ├── manager.py            # Plugin discovery and loading
│   └── examples/             # Example plugin implementations
├── config/                    # Configuration management
│   ├── manager.py            # Configuration manager
│   ├── models.py             # Configuration data models
│   └── profiles/             # Configuration profiles (beginner/advanced)
├── tests/                     # Comprehensive test suite
│   ├── test_performance.py   # Performance and load tests
│   ├── test_weather_agent_integration.py # Weather agent integration
│   └── test_system_integration.py # End-to-end system tests
├── run_tests.py              # Test runner script
├── conftest.py               # Shared test fixtures
├── pytest.ini               # Test configuration
├── pyproject.toml            # Project dependencies and configuration
├── Dockerfile               # Container configuration for deployment
└── README.md                # This comprehensive guide
```

### **Core Components Explained**

- **`examples/weather_agent.py`** - Production-ready weather agent following AgentCore specifications
- **`demos/`** - Individual feature demonstrations with educational examples
- **`web/backend/`** - FastAPI application providing REST API for all features
- **`web/frontend/`** - React interface for interactive feature exploration
- **`plugins/`** - Extensible plugin system for adding new AgentCore features
- **`config/`** - Advanced configuration management with multiple profiles
- **`tests/`** - Comprehensive test suite including performance and integration tests

## 🌐 Web Interface Features

### **Interactive Demo Dashboard**
- **Feature Navigation** - Clean tabbed interface for exploring each AgentCore capability
- **Real-time Updates** - WebSocket-based live progress tracking and results
- **Educational Examples** - Pre-built scenarios with step-by-step explanations
- **Parameter Tuning** - Interactive configuration management with immediate feedback
- **Monitoring Dashboard** - Live observability metrics and system health indicators

### **AgentCore Feature Demonstrations**

#### **🏃 Runtime**
- Production weather agent with educational enhancements
- Step-by-step execution visualization
- Parameter impact analysis
- Error handling demonstrations

#### **🧠 Memory**
- Session creation and management
- Conversation context tracking
- Memory limit demonstrations
- Context visualization and analysis

#### **🌐 Gateway**
- External API integration examples
- Retry logic and error handling
- API call monitoring and metrics
- Response caching demonstrations

#### **🔐 Identity**
- AWS credential validation
- Permission checking and verification
- Identity information display
- Authentication troubleshooting

#### **💻 Code Interpreter**
- Sandboxed Python execution
- Data analysis with pandas/numpy
- Matplotlib visualization generation
- Security restriction demonstrations

#### **🌍 Browser Tool**
- Web content fetching and parsing
- Text extraction and summarization
- Content analysis and display
- Error handling for web requests

#### **📈 Observability**
- Real-time metrics collection
- Performance monitoring dashboard
- Error tracking and reporting
- System health indicators

#### **🔄 Integrated Workflows**
- Multi-feature collaboration scenarios
- Data flow visualization
- Step-by-step workflow execution
- Performance analysis across features

### **Advanced Features**
- **Plugin System** - Hot-reload capability for new AgentCore features
- **Configuration Profiles** - Beginner, intermediate, and advanced settings
- **Performance Testing** - Built-in load testing and benchmarking
- **Comprehensive Logging** - Detailed operation tracking and debugging

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

**Web Interface Issues:**

1. **"Web interface won't start"**
   ```bash
   # Check if all dependencies are installed
   poetry install
   
   # Verify FastAPI and uvicorn are available
   poetry run python -c "import fastapi, uvicorn; print('✅ Web dependencies OK')"
   
   # Start with debug mode
   poetry run uvicorn web.backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **"Features not working in web interface"**
   - Ensure AWS credentials are configured: `aws sts get-caller-identity`
   - Check browser console for JavaScript errors
   - Verify API endpoints: `curl http://localhost:8000/api/runtime/status`

3. **"Memory/Observability services not responding"**
   ```bash
   # Reset services and restart
   poetry run python -c "
   from demos.memory_service import reset_memory_service
   from demos.observability_service import reset_observability_service
   reset_memory_service()
   reset_observability_service()
   print('✅ Services reset')
   "
   ```

**AgentCore Production Issues:**

1. **"AgentCore toolkit not available"**
   - Ensure `bedrock-agentcore` and `strands-agents` are installed
   - Run `poetry install` to update dependencies

2. **"Access denied" errors**
   - Verify AWS permissions (need `BedrockAgentCoreFullAccess` and `AmazonBedrockFullAccess`)
   - Check your AWS profile: `aws sts get-caller-identity --profile your-profile`

3. **"Runtime startup errors"**
   - Review CloudWatch logs: `aws logs tail /aws/bedrock-agentcore/runtimes/weather_demo-*/runtime-logs --region us-east-1`
   - Ensure environment variables are properly set

4. **"Local testing not working"**
   - Always use `WEATHER_AGENT_RUN_TESTS=true` for local testing
   - Without this environment variable, the agent runs in production mode

**Testing Issues:**

1. **"Tests failing"**
   ```bash
   # Run test environment check
   poetry run python run_tests.py --check-env
   
   # Run specific test categories
   poetry run python run_tests.py --type unit
   poetry run python run_tests.py --type integration
   ```

2. **"Performance tests timing out"**
   ```bash
   # Run performance tests with extended timeout
   poetry run python run_tests.py --type performance
   
   # Check system resources
   poetry run python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
   ```

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

## 📚 Documentation and Resources

### **Application Documentation**
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Complete installation and configuration instructions
- **[User Guide](docs/USER_GUIDE.md)** - Comprehensive guide to using all features
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation with examples
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Testing strategies and performance benchmarks

### **Quick Reference**
- **Web Interface**: http://localhost:8000 (interactive feature exploration)
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Test Runner**: `poetry run python run_tests.py --type all`
- **Configuration**: `curl http://localhost:8000/api/config`

### **Official AWS Documentation**
- [AWS AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AgentCore Starter Toolkit](https://aws.github.io/bedrock-agentcore-starter-toolkit/)
- [AgentCore Quickstart Guide](https://aws.github.io/bedrock-agentcore-starter-toolkit/user-guide/runtime/quickstart.html)

### **This Implementation**
- **Comprehensive Demo**: Interactive web interface showcasing all AgentCore features
- **Production Foundation**: Built on proven weather agent implementation
- **Educational Focus**: Step-by-step explanations and guided learning
- **Extensible Architecture**: Plugin system for future AgentCore features
- **Testing Excellence**: Comprehensive test suite with performance benchmarks

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