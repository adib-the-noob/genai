import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a Math assistant."},
        {"role": "user", "content": "Hello! I am Adib, Nice to meet you. Who are you?"},
    ],
)

print(response.choices[0].message.content)