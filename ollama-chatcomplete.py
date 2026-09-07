import os
from dotenv import load_dotenv
from openai import OpenAI

OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')

# Get a fun fact

response = ollama.chat.completions.create(model="llama3.2", messages=[{"role": "user", "content": "Tell me a fun fact"}])

print(response.choices[0].message.content)

