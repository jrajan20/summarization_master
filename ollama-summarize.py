# imports

import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI


# Initialize Ollama client using OpenAI-compatible API

OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')

# Test the connection

message = "Hello! This is my first message to you via Ollama!"

messages = [{"role": "user", "content": message}]

print(messages)

response = ollama.chat.completions.create(model="llama3.2", messages=messages)
print(response.choices[0].message.content)

# Let's try out the scraper utility

ed = fetch_website_contents("https://edwarddonner.com")
print(ed)

# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""
# Define our user prompt

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""
# See how this function creates exactly the format above

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]

print(messages_for(ed))

# Define the function to summarize the website contents using Ollama

def summarize(url):
    website = fetch_website_contents(url)
    response = ollama.chat.completions.create(
        model = "llama3.2",  # Using local Ollama model instead of GPT
        messages = messages_for(website)
    )
    return response.choices[0].message.content

print(summarize("https://edwarddonner.com"))

# A function to display this nicely in the output, using markdown

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

display_summary("https://edwarddonner.com")

# A function to display the summary of a list of websites

def display_summaries(urls):
    for url in urls:
        display_summary(url)

display_summaries(["https://edwarddonner.com", "https://www.google.com","https://www.openai.com"])
