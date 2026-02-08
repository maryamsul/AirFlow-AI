
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("AIzaSyCIjKrL__KZADF0gN9VHBUyXxxLDCfLiCs"))

model = genai.GenerativeModel("gemini-3-pro")

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hackathon mode
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    text: str

@app.post("/generate")
def generate(prompt: Prompt):
    response = model.generate_content(prompt.text)
    return {"result": response.text}
