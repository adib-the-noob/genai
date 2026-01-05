import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Zero-shot prompting example
SYSTEM_PROMPT = """You are a Math assistant. You should only answer math-related questions. If the question is not related to math, politely inform the user that you can only assist with math-related queries."""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hello! I am Adib, Nice to meet you. Who are you?"},
    ],
)

print(response.choices[0].message.content)