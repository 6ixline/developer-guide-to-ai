from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import Client, chat
from typing import Literal, List

from pydantic import BaseModel

from conversation_history import ConversationHistory

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

client = Client()

class ChatRequestMessage(BaseModel):
  role: Literal["user", "assistant"]
  content: str


class ChatRequest(BaseModel):
  history: List[ChatRequestMessage] = []
  question: str


def generate_stream(chatRequest: ChatRequest):
  conversation_history = ConversationHistory(system_message={
    "role": "system",
    "content": "You are a helpful assistant."
  })

  conversation_history.add_messages(chatRequest.history)

  conversation_history.add_message({
    "role": "user",
    "content": chatRequest.question
  })

  result = chat(
    stream=True, 
    model="llama3.2", 
    messages=conversation_history.get_messages()
  )

  for chunk in result:
    if chunk.message and chunk.message.content:
      yield chunk.message.content


@app.post("/")
def chat_request(chatRequest: ChatRequest):
  return StreamingResponse(
    generate_stream(chatRequest), media_type="text/plain")
