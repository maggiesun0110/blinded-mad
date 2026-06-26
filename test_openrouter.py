from src.openrouter_client import call_model

response = call_model(
    model="openai/gpt-4o-mini",
    system_prompt="You are a helpful assistant.",
    user_prompt="What is the capital of France?",
)

print(response)