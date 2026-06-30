from src.agents import Agent
from src.debate import round1, round2_blinded

western_prompt = "You are reasoning from a Western cultural perspective. This perspective emphasizes individual freedom, personal autonomy, individual choice, equality in relationships, egalitarian social norms, self-expression, and self-reliance. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Prioritize this cultural perspective while remaining thoughtful, nuanced, and internally consistent."
east_asian_prompt = "You are reasoning from an East Asian cultural perspective. This perspective emphasizes long-term thinking, perseverance, self-discipline, social harmony, relational obligations, respect for social roles and responsibilities, pragmatism, and prudence. When evaluating social situations, consider how these values may shape judgements about what is appropriate or inappropriate and explain explicitly how they influence your judgement. Prioritize this cultural perspective while remaining thoughtful, nuanced, and internally consistent."

agent1 = Agent(
    name="agent1",
    model="openai/gpt-4o-mini",
    persona_name="Western",
    persona_prompt=western_prompt,)

agent2 = Agent(
    name="agent2",
    model="openai/gpt-4o-mini",
    persona_name="East Asian",
    persona_prompt=east_asian_prompt,
)

scenario = """

A student openly disagrees with a teacher during class discussion.

"""

round1_results = round1(agent1, agent2, scenario)

agent1_round2 = round2_blinded(agent1, scenario, round1_results["agent1"], round1_results["agent2"])
agent2_round2 = round2_blinded(agent2, scenario, round1_results["agent1"], round1_results["agent2"])

print("AGENT 1 BLINDED")
print(agent1_round2)
print("AGENT 2 BLINDED")
print(agent2_round2)

# print("AGENT 1")

# print(round1_results["agent1"])

# print("\nAGENT 2")

# print(round1_results["agent2"])
