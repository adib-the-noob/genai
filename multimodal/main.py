import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful AI assistant that helps people find information.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": "https://images.pexels.com/photos/2102416/pexels-photo-2102416.jpeg"},
                },
            ],
        },
    ],
)


print("AI Assistant Response:")
print(response.choices[0].message.content)