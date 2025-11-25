# openai.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from MainLLMApp import MainLLMApp as LLM
from Models.User import User
import uvicorn
import re
import uuid


app = FastAPI()
LLM_Agent = LLM()

# OpenWebUI maintains a unique header for each user
# We map that to your User() memory
User.DB = {}   # { webui_user_id : User() }


# ---------- Request/Response Schemas ----------
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "PortableTA"
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 0.0
    stream: Optional[bool] = False


class ApiKeyRequest(BaseModel):
    username: Optional[str] = None
    key: Optional[str] = None


# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Cleaning Utilities ----------
def replace_double_dolor(text):
    return text.replace('$$', '$')

def replace_dollar_math(text):
    return re.sub(r'\$(.+?)\$', r'\\[\1\\]', text)

def replace_double_backslashes(text):
    return text.replace('\\\\', '\\')

def remove_zwnj(text):
    return text.replace('\u200c', '')

def clean_text(text):
    text = replace_double_dolor(text)
    #text = replace_dollar_math(text)
    text = replace_double_backslashes(text)
    text = remove_zwnj(text)
    return text


# ---------- Root /v1 endpoint ----------
@app.get("/v1")
async def v1_root():
    return {
        "message": "OpenAI-compatible API running",
        "endpoints": ["/v1/models", "/v1/chat/completions"]
    }


@app.post("/v1/give_apikey")
async def give_api_key(body: ApiKeyRequest):
    """
    Issue new API key or validate an existing one.
    """

    # 1) User already has a key → validate it
    if body.key and body.key in User.DB.keys():
        return {
            "status": "valid",
            "api_key": body.key,
        }

    # 2) Create new key for a new user
    new_key = "PT-" + uuid.uuid4().hex
    u = User(new_key)
    return {
        "status": "created",
        "api_key": new_key,
    }


# ---------- Required by OpenWebUI ----------
@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "PortableTA",
                "object": "model",
                "owned_by": "server",
                "permission": [],
                "root": "PortableTA"
            }
        ]
    }


# ---------- Optional but sometimes needed ----------
@app.get("/v1/engines")
async def list_engines():
    return {
        "data": [
            {
                "id": "PortableTA",
                "object": "engine",
            }
        ]
    }


# ---------- Main Chat Completion Endpoint ----------
@app.post("/v1/chat/completions")
async def chat_completion(request: Request, body: ChatCompletionRequest):

    # 1) OpenWebUI unique user ID
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return {"error": "Missing API key"}, 401

    api_key = auth.replace("Bearer ", "").strip()

    if api_key not in User.DB.keys():
        return {"error": "Invalid API key"}, 403

    u = User.DB[api_key]
    #print(u.session_number, len(body.messages))

   # print(body.messages)
    # detect new session when messages length == 1
    if len(body.messages) == 1 and body.messages[0].role == "user":
        u.session_number += 1
        u.history[f"S{u.session_number}"] = {}
        u.prev_conv_summery = ""

    # 3) Take latest user message
    user_message = body.messages[-1].content

    # 4) Run your agent
    try:
        llm_result = LLM_Agent(u, user_message)
        llm_result = clean_text(llm_result)
    except Exception as e:
        llm_result = "LLM Server Error: " + str(e)

    # 5) Send in OpenAI format
    return {
        "id": "chatcmpl-local-001",
        "object": "chat.completion",
        "model": body.model,
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": llm_result
                }
            }
        ]
    }


# ---------- Run ----------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
