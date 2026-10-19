from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ollama import Client


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


client  = Client();


class ChatRequest(BaseModel):
    question: str


def get_ollama_response(question: str):
    result = client.generate(
        model="llama3.2",
        prompt=question,
        options = {
            "num_predict": 1,
            "temperature": 0
        }
    )

    return result.response


@app.post("/")
def chat(chatRequest: ChatRequest):
  return get_ollama_response(chatRequest.question)
