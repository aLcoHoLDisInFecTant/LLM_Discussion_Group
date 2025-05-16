# agents/refiner_agent.py

from openai_client import call_llm


class RefinerAgent:
    def __init__(self, model="gpt-4.1"):
        self.model = model

    def refine_opinion(self, agent_id: str, topic: str, raw_text: str) -> str:
        prompt = f"""
Agent {agent_id} was asked to take a clear position on the following topic:

"{topic}"

But the response was vague or neutral:
---
{raw_text}
---

Please rewrite the response to clearly support or oppose the topic.
Avoid saying "it depends", "both sides", or remaining neutral.
Make the position firm but preserve the original reasoning where appropriate.
Length ≤ 100 words.
"""
        return call_llm(prompt, model=self.model)
