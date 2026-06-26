from dataclasses import dataclass
from src.openrouter_client import call_model

@dataclass
class Agent:
    name: str
    model: str
    persona_name: str
    persona_prompt: str
    temperature: float = 0.7
    max_tokens: int = 300

    def respond(self, user_prompt: str) -> str:
        return call_model(
            model=self.model,
            system_prompt=self.persona_prompt,
            user_prompt=user_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )