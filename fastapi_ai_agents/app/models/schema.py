from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="The message sent by the user")
    agent: str = Field(..., description="The AI agent to use (e.g., 'deepseek', 'gemini', 'openai')")
    conversation_id: Optional[str] = Field(None, description="ID of an existing conversation, if continuing one")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the request")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="The agent's response to the user")
    tools_used: Optional[List[str]] = Field(None, description="List of tools used in generating the response")
    conversation_id: Optional[str] = Field(None, description="ID of the conversation")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata about the response")

class ToolCallRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the tool to call")
    parameters: Dict[str, Any] = Field(..., description="Parameters for the tool")

class ToolCallResponse(BaseModel):
    result: Any = Field(..., description="Result returned by the tool")
    error: Optional[str] = Field(None, description="Error message if the tool call failed")

class AgentListResponse(BaseModel):
    available_agents: List[Dict[str, Any]] = Field(..., description="List of available agents and their capabilities")