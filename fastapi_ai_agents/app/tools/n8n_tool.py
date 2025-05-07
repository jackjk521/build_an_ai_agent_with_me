import requests
import os
from pydantic import BaseModel, Field
from typing import Dict, Any
from app.models.schema import ToolCallRequest, ToolCallResponse

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

class N8NRequest(BaseModel):
    workflow: str = Field(..., description="The name of the workflow to trigger")
    data: str = Field(..., description="The data to send to the workflow")

async def send_to_n8n(workflow: str, data: str) -> str:
    """Send data to an n8n workflow."""
    if not N8N_WEBHOOK_URL:
        return "N8N_WEBHOOK_URL is not configured."
    
    payload = {
        "workflow": workflow,
        "data": data
    }
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return f"Successfully sent data to n8n workflow '{workflow}'"
    except Exception as e:
        return f"Error sending data to n8n: {str(e)}"

# Tool schema definition for OpenAI format
schema = {
    "type": "function",
    "function": {
        "name": "n8n_tool",
        "description": "Send data to an n8n workflow for automation tasks",
        "parameters": {
            "type": "object",
            "properties": {
                "workflow": {
                    "type": "string",
                    "description": "The name of the workflow to trigger"
                },
                "data": {
                    "type": "string",
                    "description": "The data to send to the workflow"
                }
            },
            "required": ["workflow", "data"]
        }
    }
}

# Direct API endpoint handler
async def handle_tool_call(request: ToolCallRequest) -> ToolCallResponse:
    try:
        params = request.parameters
        if "workflow" not in params or "data" not in params:
            return ToolCallResponse(
                result=None, 
                error="Missing required parameters: workflow and data are required"
            )
        
        result = await send_to_n8n(params["workflow"], params["data"])
        return ToolCallResponse(result=result)
    except Exception as e:
        return ToolCallResponse(result=None, error=str(e))
