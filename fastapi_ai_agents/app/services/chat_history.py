import os
from supabase import create_client, Client

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

async def save_message(user_id, user_message, reply):
    supabase.table("chat_history").insert({
        "user_id": user_id,
        "message": user_message,
        "reply": reply
    }).execute()
