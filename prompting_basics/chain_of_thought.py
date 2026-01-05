import os
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


    OUTPUT FORMAT:
    { "step": "START" or "PLAN" or "OUTPUT", "content": "string" }
    EXAMPLES:
    Q: What is 12 multiplied by 15?
    PLAN: { "step": "START", "content": "User has asked for the multiplication of 12 and 15." }
    PLAN: { "step": "PLAN", "content": "To find the product of 12 and 15, I will multiply the two numbers together." }
    PLAN: { "step": "PLAN", "content": "12 multiplied by 15 equals 180." }
    PLAN: { "step": "OUTPUT", "content": "The product of 12 and 15 is 180." }
    
"""

message_history = []
user_query = input("=> ")


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={
        "type": "json_object"
    },
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hello! Check for odd and Even using js`"},
    ],
)

print(response.choices[0].message.content)