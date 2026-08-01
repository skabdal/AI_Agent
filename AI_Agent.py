from google import genai
from google.genai import types
import os

client = genai.Client(
    api_key=os.getenv("API_Key")
)

def sum_numbers(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b

def check_prime(n: int) -> bool:
    """Checks whether a number is prime."""
    if n <= 1:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True

config = types.GenerateContentConfig(
    system_instruction=(
        "You are an AI Agent. "
        "You have access to two tools: "
        "sum_numbers and check_prime. "
        "Use these tools whenever they are needed. "
        "If the user asks a general question, answer directly."
    ),
    tools=[
        sum_numbers,
        check_prime
    ]
)

history = []

def get_response(user_input):
    history.append(
        types.Content(
            role="user",
            parts=[
                types.Part(text=user_input)
            ]
        )
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=history,
        config=config
    )

    history.append(response.candidates[0].content)

    return response.text

while True:
    user_input = input("\nEnter your prompt: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    try:
        response = get_response(user_input)
        print("\nAgent:", response)

    except Exception as e:
        print("\nError:", e)

