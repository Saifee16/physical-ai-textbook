# app/services/gemini_service.py
import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure this is in your .env

def generate_content(prompt: str) -> str:
    """
    Send prompt to Gemini API and return the generated content.
    """
    url = "https://api.gemini.example/v1/generate"  # Replace with actual Gemini API endpoint
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("text", "No content returned.")
    else:
        return f"Error {response.status_code}: {response.text}"
