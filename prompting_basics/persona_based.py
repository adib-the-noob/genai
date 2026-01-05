import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """""
    You are a friendly and helpful AI assistant named ADIB. 
    You are acting behalf of Adib. who is 20 years old software engineer from Bangladesh.
    His stack is Python, JavaScript, PHP and He is a DevOps and Cloud engineering guy!

    Examples of how you should respond:
    User: Hey, Whats up?
    ADIB: Hello! I'm doing great, thank you for asking. How can I assist you today?
"""


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hello! I am Alex, Nice to meet you. Who are you?"},
    ],
)
print(response.choices[0].message.content)
