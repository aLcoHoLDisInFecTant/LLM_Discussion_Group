# agents/voting_agent.py

import os
from openai_client import call_llm
from prompt_utils import load_prompt

VOTING_PROMPT_PATH = os.path.join("prompts", "voting_prompt.txt")


class VotingAgent:
    def __init__(self, agent_id, model="gpt-4.1"):
        self.agent_id = agent_id
        self.model = model
        self.vote = None
        self.reasoning = None

    def cast_vote(self, topic, all_opinions: dict) -> str:
        # 合并所有观点（已反驳的）为字符串
        opinion_text = "\n".join([f"{agent}: {text}" for agent, text in all_opinions.items()])

        # 填充 voting_prompt.txt
        prompt = load_prompt(VOTING_PROMPT_PATH, {
            "agent_id": self.agent_id,
            "topic": topic,
            "all_opinions": opinion_text
        })

        # 请求 LLM 得到投票内容
        result = call_llm(prompt, model=self.model)
        self.reasoning = result.strip()
        self.vote = "YES" if "YES" in result.upper() else "NO"
        return self.vote
