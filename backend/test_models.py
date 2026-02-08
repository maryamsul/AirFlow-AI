import os
from google import genai

# Test script to list available models
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    print("ERROR: No API key found")
    exit(1)

client = genai.Client(api_key=GOOGLE_API_KEY)

print("Available models:")
print("-" * 50)

try:
    for model in client.models.list():
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"Error listing models: {e}")
