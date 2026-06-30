from src.agents import Agent

ROUND1_TASK_PROMPT = """
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

ROUND2_BLINDED_PROMPT = """
Scenario:
{scenario}

Based on the following opinions from agents:
Agent Opinion 1:
{opinion1}

Agent Opinion 2:
{opinion2}

Consider these agents’ opinions to provide an updated response to the question. 

Briefly explain your reasoning while limiting your response to less than 4 sentences, then state your final judgment clearly. 

Make sure to state your final answer in curly brackets at the very end of your response, using exactly one of the following formats:

{{final answer: Acceptable}}
{{final answer: Unacceptable}}
{{final answer: Neutral}}

"""

def round1(agent1: Agent, agent2: Agent, scenario: str):
    user_prompt =ROUND1_TASK_PROMPT.format(scenario=scenario)
    response1 = agent1.respond(user_prompt)
    response2 = agent2.respond(user_prompt)

    return {
        "agent1": response1,
        "agent2": response2,
        # "round1_prompt": user_prompt,
    }

def round2_blinded(agent, scenario, opinion1, opinion2):
    prompt = ROUND2_BLINDED_PROMPT.format(
        scenario=scenario,
        opinion1=opinion1,
        opinion2=opinion2,
    )

    return agent.respond(prompt)