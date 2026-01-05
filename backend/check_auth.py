from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load env from current directory (which should be Desktop/Agent)
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")

print(f"--- Auth Check ---")
print(f"Key loaded: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")
print(f"Model: {model}")

if not api_key:
    print("ERROR: No API Key found.")
    sys.exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "Local Orchestrator Agent",
    }
)

try:
    print("Sending test request...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "Hi"}
        ],
    )
    print("SUCCESS!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("FAILURE!")
    print(e)
