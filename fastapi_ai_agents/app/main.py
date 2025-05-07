from fastapi import FastAPI, Request
from app.agents.agent_switcher import get_agent
# from app.services.chat_history import save_message
from app.models.schema import ChatRequest, ChatResponse

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    agent = get_agent(request.agent)
    reply = await agent.chat(request)

    # Save to Supabase history
    # await save_message(request.user_id, request.message, reply)

    return ChatResponse(reply=reply)
