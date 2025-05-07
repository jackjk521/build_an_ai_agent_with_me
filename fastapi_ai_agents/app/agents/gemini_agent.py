# agents/gemini_agent.py
import os
import requests
import json
from app.agents.base import BaseAgent
from app.tools.tool_registry import tool_registry

class GeminiAgent(BaseAgent):
    async def chat(self, request):
        # Step 1: Call Gemini with tool options
        tools_schema = tool_registry.get_openai_schema()
        
        # Format the prompt to include instructions about tools
        # Gemini doesn't have native tool calling, so we'll use a workaround
        tool_instructions = "You have access to the following tools:\n"
        for tool in tools_schema:
            tool_instructions += f"- {tool['function']['name']}: {tool['function']['description']}\n"
        
        tool_instructions += "\nTo use a tool, respond with JSON in this format: {\"tool\":\"tool_name\",\"parameters\":{...}}"
        
        full_prompt = f"{tool_instructions}\n\nUser query: {request.message}"
        
        # Call Gemini API
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": os.getenv("GEMINI_API_KEY")
        }
        body = {
            "contents": [
                {"parts": [{"text": full_prompt}]}
            ]
        }

        response = requests.post(
            os.getenv("GEMINI_API_URL"),
            headers=headers, 
            params=params, 
            json=body
        )
        response.raise_for_status()
        result = response.json()
        response_text = result['candidates'][0]['content']['parts'][0]['text']
        
        # Check if the response contains a tool call
        try:
            # Extract the JSON part of the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                tool_data = json.loads(json_str)
                
                if 'tool' in tool_data and 'parameters' in tool_data:
                    name = tool_data['tool']
                    args = tool_data['parameters']
                    tool_func = tool_registry.get_tool(name)
                    tool_result = await tool_func(**args)
                    
                    # 2nd round: Generate a response with the tool result
                    followup_prompt = (
                        f"User query: {request.message}\n\n"
                        f"You used the tool '{name}' and got this result: {tool_result}\n\n"
                        "Please provide a helpful response based on this information."
                    )
                    
                    followup_body = {
                        "contents": [
                            {"parts": [{"text": followup_prompt}]}
                        ]
                    }
                    
                    followup_response = requests.post(
                        os.getenv("GEMINI_API_URL"),
                        headers=headers, 
                        params=params, 
                        json=followup_body
                    )
                    followup_response.raise_for_status()
                    followup_result = followup_response.json()
                    final_response = followup_result['candidates'][0]['content']['parts'][0]['text']
                    
                    return f"(Tool used: {name}) {final_response}"
        except (json.JSONDecodeError, KeyError):
            pass
            
        # If no tool was called or there was an error parsing the tool call
        return response_text
