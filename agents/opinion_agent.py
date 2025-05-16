# agents/opinion_agent.py

import os
from openai_client import call_llm
from prompt_utils import load_prompt

PROMPT_PATH = os.path.join("prompts", "opinion_prompt.txt")
REBUTTAL_PATH = os.path.join("prompts", "rebuttal_prompt.txt")

class OpinionAgent:
    def __init__(self, agent_id, model="gpt-4.1"):
        self.agent_id = agent_id
        self.model = model
        self.original_opinion = ""
        self.rebuttal_opinion = ""

    def generate_opinion(self, topic):
        prompt = load_prompt(PROMPT_PATH, {
            "agent_id": self.agent_id,
            "topic": topic
        })
        self.original_opinion = call_llm(prompt, model=self.model)
        return self.original_opinion

    def generate_rebuttal(self, topic, other_opinions: dict):
        # 组装其他代理的观点为字符串段落
        others = "\n".join([f"{k}: {v}" for k, v in other_opinions.items() if k != self.agent_id])
        prompt = load_prompt(REBUTTAL_PATH, {
            "agent_id": self.agent_id,
            "topic": topic,
            "your_opinion": self.original_opinion,
            "other_opinions": others
        })
        self.rebuttal_opinion = call_llm(prompt, model=self.model)
        return self.rebuttal_opinion
