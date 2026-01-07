from dotenv import load_dotenv

load_dotenv()

import os
from typing import Annotated, Optional, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def evalute_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("Evaluating response...", state)
    if True:
        return "endnode"
    return "chatbot_gemini"`
    

def chatbot(state: State):
    print("Invoking chatbot...", state)
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": state.get("user_query")}]
    )
    state["llm_output"] = response.choices[0].message.content
    return state


def chatbot_gemini(state: State):
    print("Invoking chatbot_gemini...", state)
    response = client.chat.completions.create(
        model="gpt-5", messages=[{"role": "user", "content": state.get("user_query")}]
    )
    state["llm_output"] = response.choices[0].message.content
    return state

def endnode(state: State):
    print("End node reached. Final state:", state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evalute_response)
graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_state = graph.invoke({
    "user_query": "what is 2+2?"
})
print(updated_state)


# Output: If evalute_response > returns "endnode"
# uv run ./LangGraph/chat_2.py
# Invoking chatbot... {'user_query': 'what is 2+2?'}
# Evaluating response... {'user_query': 'what is 2+2?', 'llm_output': '2 + 2 equals 4.'}
# End node reached. Final state: {'user_query': 'what is 2+2?', 'llm_output': '2 + 2 equals 4.'}
# {'user_query': 'what is 2+2?', 'llm_output': '2 + 2 equals 4.'}