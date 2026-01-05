import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Few-shot prompting example
SYSTEM_PROMPT = """You are a Math assistant. You should only answer math-related questions. If the question is not related to math, politely inform the user that you can only assist with math-related queries.

Examples:
Q: What is 2 + 2?
A: 2 + 2 equals 4.

Q: Can you help me with my history homework?
A: I'm sorry, but I can only assist with math-related queries.

"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hello! I am Adib, Nice to meet you. Who are you?"},
    ],
)

print(response.choices[0].message.content)