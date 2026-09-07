import os
from dotenv import load_dotenv
from openai import OpenAI

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

load_dotenv(override=True)

google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    print("No API key was found - please be sure to add your key to the .env file, and save the file! Or you can skip the next 2 cells if you don't want to use Gemini")
elif not google_api_key.startswith(("AIz", "AQ.")):
    print("An API key was found, but it doesn't start with AIz or AQ.")
else:
    print("API key found and looks good so far!")

gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)

response = gemini.chat.completions.create(model="gemini-3.1-flash-lite", messages=[{"role": "user", "content": "Tell me a fun fact"}])

print(response.choices[0].message.content)