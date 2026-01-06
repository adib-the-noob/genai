import os
from dotenv import load_dotenv

from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY"),
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="sys-design",
    embedding=embedding_model,
)

user_query = input(">>> Ask Anything: ")
search_results = vector_db.similarity_search(user_query, k=3)

context = "\n\n\n".join(
    [
        f"Page Content: {result.page_content}\nPage Numbers: {result.metadata['page_label']}\n File Location: {result.metadata['source']}"
        for result in search_results
    ]
)

SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant that who answers user queries based on the available context retrieved from a vector database along with `page_content` and `page_numbers`

    you should only answer the user based on the following context and navigate the user to open the right page number to know more.

    Context:
    {context}
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ],
)

print("AI Assistant Response:")
print(response.choices[0].message.content)
