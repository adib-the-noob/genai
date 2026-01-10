import os
import json
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

config = {
    "version": "0.1",
    "embedder": {
        "provider": "openai",
        "model": "text-embedding-3-small",
        "api_key": OPENAI_API_KEY,
    },
    "llm": {
        "provider": "openai",
        "config": {"model": "gpt-4-turbo", "api_key": OPENAI_API_KEY},
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://48efad12.databases.neo4j.io",
            "username": "neo4j",
            "password": "<>",
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        },
    },
}

mem_client = Memory.from_config(config)

while True:
    print("===============================")
    user_input = input("\nYou 👉: ")
    search_memory = mem_client.search(
        user_id="adib-the-noob",
        query=user_input,
    )

    memories = [
        f"ID: {mem.get('id')}\nContent: {mem.get('memory')}\n"
        for mem in search_memory.get("results", [])
    ]
    SYSTEM_PROMPT = f"""
    Here is the Context from your memory:
    {json.dumps(memories, indent=2)}
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
    )

    ai_response = response.choices[0].message.content
    print("===============================")
    print("\nRobo 🤖:", ai_response)
    mem_client.add(
        user_id="adib",
        messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": ai_response},
        ],
    )
