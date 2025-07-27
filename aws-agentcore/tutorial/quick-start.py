from bedrock_agentcore.runtime import BedrockAgentCoreApp
from langgraph.prebuilt import create_react_agent
import os


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


from langchain_anthropic import ChatAnthropic

# Initialize the model with API key
model = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

agent = create_react_agent(
    model=model,
    tools=[get_weather],
    prompt="You are a helpful assistant",
)

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    location = payload.get("prompt")
    result = agent.invoke(
        {"messages": [{"role": "user", "content": f"what is the weather in {location}"}]}
    )
    return {"result": result["messages"][-1].content}


if __name__ == "__main__":
    app.run()
