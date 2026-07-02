import json
import pandas as pd

from src.agents import Agent
from src.debate import round1, round2_blinded, round2_unblinded

MODEL = "openai/gpt-4o-mini"

PERSONAS = {
    "Western": "You are reasoning from a Western cultural perspective. This perspective emphasizes individual freedom, personal autonomy, individual choice, equality in relationships, egalitarian social norms, self-expression, and self-reliance. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Consider this cultural perspective as your primary lens while remaining thoughtful, nuanced, and internally consistent.",
    "East Asian": "You are reasoning from an East Asian cultural perspective. This perspective emphasizes long-term thinking, perseverance, self-discipline, social harmony, relational obligations, respect for social roles and responsibilities, pragmatism, and prudence. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Consider this cultural perspective as your primary lens while remaining thoughtful, nuanced, and internally consistent.",
    "African": "You are reasoning from an African cultural perspective. This perspective emphasizes mutual support, practical cooperation, collective responsibility, community well-being, strong social relationships, interdependence, and hospitality. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Consider this cultural perspective as your primary lens while remaining thoughtful, nuanced, and internally consistent.",
    "Middle Eastern": "You are reasoning from a Middle Eastern cultural perspective. This perspective emphasizes respect for established norms and traditions, social responsibility, community obligations, social order and cohesion, respect for authority, predictability, stability, and the importance of maintaining honor and reputation. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Consider this cultural perspective as your primary lens while remaining thoughtful, nuanced, and internally consistent.",
    "South/SE Asian": "You are reasoning from a South and Southeast Asian cultural perspective. This perspective emphasizes hierarchy, respect for elders, family and community obligations, collective decision-making, filial piety, social duty, and tradition. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Consider this cultural perspective as your primary lens while remaining thoughtful, nuanced, and internally consistent.",
}

def comparison_persona(region: str) -> str:
    if region == "Western":
        return "East Asian"
    return region

def make_agent(agent_name: str, persona_name: str) -> Agent:
    return Agent(
        name=agent_name,
        model=MODEL,
        persona_name=persona_name,
        persona_prompt=PERSONAS[persona_name],
    )

def run_one_scenario(row):
    scenario = row["scenario"]
    target_persona = comparison_persona(row["region"])

    agent1 = make_agent("agent1", "Western")
    agent2 = make_agent("agent2", target_persona)

    print(f"Running scenario: {row['scenario_id']} : Western vs {target_persona}")

    r1 = round1(agent1, agent2, scenario)

    agent1_blinded = round2_blinded(
        agent1,
        scenario,
        agent1.persona_name,
        r1["agent1"],
        agent2.persona_name,
        r1["agent2"],
    )

    agent2_blinded = round2_blinded(
        agent2,
        scenario,
        agent1.persona_name,
        r1["agent1"],
        agent2.persona_name,
        r1["agent2"],
    )

    agent1_unblinded = round2_unblinded(
        agent1,
        scenario,
        agent1.persona_name,
        r1["agent1"],
        agent2.persona_name,
        r1["agent2"],
    )

    agent2_unblinded = round2_unblinded(
        agent2,
        scenario,
        agent1.persona_name,
        r1["agent1"],
        agent2.persona_name,
        r1["agent2"],
    )

    return {
        "scenario_id": row["scenario_id"],
        "country": row["country"],
        "region": row["region"],
        "scenario": scenario,

        "agent1_persona": agent1.persona_name,
        "agent2_persona": agent2.persona_name,

        "round1_agent1": r1["agent1"],
        "round1_agent2": r1["agent2"],

        "round2_blinded_agent1": agent1_blinded,
        "round2_blinded_agent2": agent2_blinded,

        "round2_unblinded_agent1": agent1_unblinded,
        "round2_unblinded_agent2": agent2_unblinded,
    }

def main():
    df = pd.read_csv("benchmarks/pilot_2.csv")

    results = []

    for _, row in df.iterrows():
        result = run_one_scenario(row)
        results.append(result)
    
    with open("results/pilot_results_2.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Pilot complete. Results in results/pilot_results_2.json")

if __name__ == "__main__":
    main()