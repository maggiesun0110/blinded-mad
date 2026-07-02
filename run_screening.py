import json
import re
import pandas as pd

from src.agents import Agent
from src.debate import round1

MODEL = "openai/gpt-4o-mini"

PERSONAS = {
    "Western": "You are reasoning from a Western cultural perspective. This perspective emphasizes individual freedom, personal autonomy, individual choice, equality in relationships, egalitarian social norms, self-expression, and self-reliance. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Prioritize this cultural perspective while remaining thoughtful, nuanced, and internally consistent.",
    "East Asian": "You are reasoning from an East Asian cultural perspective. This perspective emphasizes long-term thinking, perseverance, self-discipline, social harmony, relational obligations, respect for social roles and responsibilities, pragmatism, and prudence. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Prioritize this cultural perspective while remaining thoughtful, nuanced, and internally consistent.",
    "African": "You are reasoning from an African cultural perspective. This perspective emphasizes mutual support, practical cooperation, collective responsibility, community well-being, strong social relationships, interdependence, and hospitality. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Prioritize this cultural perspective while remaining thoughtful, nuanced, and internally consistent.",
    "Middle Eastern": "You are reasoning from a Middle Eastern cultural perspective. This perspective emphasizes respect for established norms and traditions, social responsibility, community obligations, social order and cohesion, respect for authority, predictability, stability, and the importance of maintaining honor and reputation. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Prioritize this cultural perspective while remaining thoughtful, nuanced, and internally consistent.",
    "South/SE Asian": "You are reasoning from a South and Southeast Asian cultural perspective. This perspective emphasizes hierarchy, respect for elders, family and community obligations, collective decision-making, filial piety, social duty, and tradition. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Prioritize this cultural perspective while remaining thoughtful, nuanced, and internally consistent.",
}


def make_agent(agent_name: str, persona_name: str) -> Agent:
    return Agent(
        name=agent_name,
        model=MODEL,
        persona_name=persona_name,
        persona_prompt=PERSONAS[persona_name],
    )

def extract_judgement(response: str) -> str:
    text = response.lower()

    if re.search(r"judgment: \s*acceptable", text):
        return "Acceptable"
    if re.search(r"judgment: \s*unacceptable", text):
        return "Unacceptable"
    if re.search(r"judgment: \s*neutral", text):
        return "Neutral"
    
    return "UNKNOWN"

def run_screening():
    df = pd.read_csv("screening_candidates.csv")
    results = []

    agents = {
        persona: make_agent(persona, persona)
        for persona in PERSONAS
    }

    for _, row in df.iterrows():
        scenario = row["Story"]

        print(f"Screening scenario {row['ID']}...")

        scenario_result = {
            "id": row["ID"],
            "country": row["Country"],
            "subaxis": row["Subaxis"],
            "value": row["Value"],
            "rule_of_thumb": row["Rule-of-Thumb"],
            "story": scenario,
            "gold_label": row["Gold Label"],
            "responses": {},
            "judgments": {},

        }

        for persona_name, agent in agents.items():
            response = agent.respond(
                f"""
Read the following scenario.

Determine whether the behavior described is socially acceptable within the cultural perspective you represent. 

Provide:
1. A judgment (Acceptable / Unacceptable / Neutral)
2. The values that most influenced your judgment
3. A brief explanation of your reasoning

Do not mention the name of the cultural perspective or region in your response.
Explain your answer in less than four sentences.

Scenario:
{scenario}

"""

        )

            judgment = extract_judgement(response)

            scenario_result["responses"][persona_name] = response
            scenario_result["judgments"][persona_name] = judgment

        unique_judgments = set(scenario_result["judgments"].values())
        if "UNKNOWN" in unique_judgments:
            unique_judgments.remove("UNKNOWN")

        scenario_result["disagreement_score"] = len(unique_judgments)

        results.append(scenario_result)

    with open("results/screening_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Saved screening results to results/screening_results.json")

if __name__ == "__main__":
    run_screening()