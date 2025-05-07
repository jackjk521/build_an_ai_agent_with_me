from app.agents.deepseek_agent import DeepSeekAgent
from app.agents.gemini_agent import GeminiAgent

def get_agent(agent_name: str):
    if agent_name == "deepseek":
        return DeepSeekAgent()
    elif agent_name == "gemini":
        return GeminiAgent()
    else:
        raise ValueError("Unknown agent")
