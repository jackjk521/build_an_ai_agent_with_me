import os
import requests
import json
from app.agents.base import BaseAgent
from app.tools.tool_registry import tool_registry

class DeepSeekAgent(BaseAgent):
    async def chat(self, request):
        # Step 1: Call DeepSeek with tool options
        tools_schema = tool_registry.get_openai_schema()
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": request.message}],
                "tools": tools_schema,
                "tool_choice": "auto"
            }
        )
        data = resp.json()
        tool_calls = data["choices"][0]["message"].get("tool_calls")

        if tool_calls:
            for call in tool_calls:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                tool_func = tool_registry.get_tool(name)
                tool_result = await tool_func(**args)

                # 2nd round: send tool result back to LLM
                return f"(Tool used: {name}) Result: {tool_result}"
        else:
            return data["choices"][0]["message"]["content"]
