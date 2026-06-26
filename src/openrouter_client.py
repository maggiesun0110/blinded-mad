import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("Put key in .env file")

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = API_KEY,
)

def call_model(
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 300,
) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content