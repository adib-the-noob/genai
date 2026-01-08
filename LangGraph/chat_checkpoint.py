import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

# MongoDB
from langgraph.checkpoint.mongodb import MongoDBSaver

DB_URI = os.getenv(
    "MONGODB_URI", "mongodb://admin:admin@localhost:27017/langgraph?authSource=admin"
)

load_dotenv()

llm = init_chat_model(
    model="gpt-4-turbo",
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
)


class State(TypedDict):
    message: Annotated[str, add_messages]


def chatbot(state: State):
    response = llm.invoke(state.get("message"))
    return {"message": [response]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


def compile_graph_with_checkpoint(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpoint = compile_graph_with_checkpoint(checkpointer)
    config = {"configurable": {"thread_id": "adib"}}

    for chunk in graph_with_checkpoint.stream(
        State(message="Now tell me how I can introduce myself to others?"), config=config,
        stream_mode="values"
    ):
        chunk["message"][-1].pretty_print()