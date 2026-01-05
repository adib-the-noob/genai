import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Few-shot prompting example
SYSTEM_PROMPT = """""
    You are an expert AI Assistant in resolving user queries using chain-of-thought reasoning.
    You work on START, PLAN, OUTPUT steps.
    You need to first plan has been done, finally provide the final answer.
    
    RULES:
    - Strictly follow the given JSON format provided below.
    - Only run one step at a time.
    - THe sequence of step is START(Where user will provide an input), PLAN(Where you will plan how to solve the problem), OUTPUT(Where you will provide the final answer).
    - Always respond in valid JSON format.

    OUTPUT FORMAT:
    { "step": "START" or "PLAN" or "OUTPUT", "content": "string" }
    EXAMPLES:
    Q: What is 12 multiplied by 15?
    PLAN: { "step": "START", "content": "User has asked for the multiplication of 12 and 15." }
    PLAN: { "step": "PLAN", "content": "To find the product of 12 and 15, I will multiply the two numbers together." }
    PLAN: { "step": "PLAN", "content": "12 multiplied by 15 equals 180." }
    PLAN: { "step": "OUTPUT", "content": "The product of 12 and 15 is 180." }
    
"""
print("\n\n")

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]
user_query = input("=> ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=message_history, # type: ignore
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)
    
    if parsed_result["step"] == "START":
        print("[START] ", parsed_result["content"])
        continue
    elif parsed_result["step"] == "PLAN":
        print("[PLAN] ", parsed_result["content"])
        message_history.append({"role": "assistant", "content": raw_result})
        continue
    elif parsed_result["step"] == "OUTPUT":
        print("[OUTPUT] ", parsed_result["content"])
        break

print("\n\n")
