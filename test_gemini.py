import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

client = genai.Client(api_key=api_key)

try:
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input="Reply with: Gemini connection successful!"
    )

    print("Gemini response:")
    print(response.output_text)

except Exception as error:
    print("Gemini API error:")
    print(type(error).__name__)
    print(error)