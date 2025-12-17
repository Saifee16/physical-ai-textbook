import os
import requests
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_content(title: str, description: Optional[str] = None) -> str:
    """
    Generate chapter content using Gemini API.
    """
    prompt = f"Create a detailed textbook chapter on '{title}'."
    if description:
        prompt += f" Include the following description: {description}"

    url = "https://api.gemini.com/v1/generate"  # Replace with the actual Gemini endpoint
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()

    # Adjust according to Gemini API response
    return result.get("text", "")
