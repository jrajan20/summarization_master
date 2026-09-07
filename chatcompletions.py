import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

import requests

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

payload = {
    "model": "gpt-5-nano",
    "messages": [
        {"role": "user", "content": "Tell me a fun fact"}]
}

print(payload)
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=payload
)

print(response.json())

from openai import OpenAI
openai = OpenAI()

response = openai.chat.completions.create(model="gpt-5-nano", messages=[{"role": "user", "content": "Tell me a fun fact"}])

print(response.choices[0].message.content)