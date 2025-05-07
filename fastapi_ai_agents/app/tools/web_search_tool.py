import requests
import os
from pydantic import BaseModel, Field
from typing import Dict, Any
from app.models.schema import ToolCallRequest, ToolCallResponse

DUCKDUCKGO_API_URL = os.getenv("SEARCH_URL_DUCKDUCKGO", "https://api.duckduckgo.com/")

class SearchQuery(BaseModel):
    query: str = Field(..., description="The search query to look up on the web")

async def search_web(query: str) -> str:
    """Simple search tool using DuckDuckGo."""
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
        "skip_disambig": 1
    }

    try:
        response = requests.get(DUCKDUCKGO_API_URL, params=params)
        response.raise_for_status()
        result = response.json()
        return result.get("AbstractText") or "No relevant result found."
    except Exception as e:
        return f"Error performing web search: {str(e)}"

# Tool schema definition for OpenAI format
schema = {
    "type": "function",
    "function": {
        "name": "search_tool",
        "description": "Search the web for information on a specific topic using DuckDuckGo",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on the web"
                }
            },
            "required": ["query"]
        }
    }
}

# Direct API endpoint handler
async def handle_tool_call(request: ToolCallRequest) -> ToolCallResponse:
    try:
        if "query" not in request.parameters:
            return ToolCallResponse(
                result=None, 
                error="Missing required parameter: query"
            )
        
        result = await search_web(request.parameters["query"])
        return ToolCallResponse(result=result)
    except Exception as e:
        return ToolCallResponse(result=None, error=str(e))
