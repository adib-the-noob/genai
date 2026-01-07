import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="gpt-4-turbo",
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
)

class State(TypedDict):
    message: Annotated[str, add_messages]


def chatbot(state: State):
    response = llm.invoke(
        state.get("message")
    )
    print("\n--- Chatbot Node ---\n")
    print(state)

    return {"message": [response]}


def sample_node(state: State):
    print("\n--- Sample Node ---\n")
    print(state)
    print("\n--- --- --- ---\n")

    return {"message": ["This is a sample node in the graph."]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample_node")
graph_builder.add_edge("sample_node", END)

graph = graph_builder.compile()
updated_state = graph.invoke(State({"message": "Hi, My name is ADIB"}))
print("updated_state:", updated_state)