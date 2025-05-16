# agents/coordinator.py

from agents.opinion_agent import OpinionAgent
from agents.voting_agent import VotingAgent
from openai_client import call_llm
from prompt_utils import load_prompt
import os

VOTING_PROMPT = os.path.join("prompts", "voting_prompt.txt")

class DebateCoordinator:
    def __init__(self, topic, opinion_agents, voting_agents):
        self.topic = topic
        self.opinion_agents = opinion_agents
        self.voting_agents = voting_agents

        self.opinions = {}
        self.rebuttals = {}
        self.votes = {}

    def run_debate(self):
        print(f"\n🧠 正在讨论议题：{self.topic}")

        # 1️⃣ 初始观点生成
        print("\n📌 初始观点：")
        for agent in self.opinion_agents:
            opinion = agent.generate_opinion(self.topic)
            self.opinions[agent.agent_id] = opinion
            print(f"[{agent.agent_id}]: {opinion}\n")

        # 2️⃣ 观点交换 + 修正
        print("\n🔁 观点交换与修正：")
        for agent in self.opinion_agents:
            rebuttal = agent.generate_rebuttal(self.topic, self.opinions)
            self.rebuttals[agent.agent_id] = rebuttal
            print(f"[{agent.agent_id}]: {rebuttal}\n")

        # 3️⃣ 投票与立场判断
        print("\n🗳️ 投票阶段：")
        for agent in self.voting_agents:
            full_dialogue = "\n".join([f"{k}: {v}" for k, v in self.rebuttals.items()])
            prompt = load_prompt(VOTING_PROMPT, {
                "topic": self.topic,
                "agent_id": agent.agent_id,
                "all_opinions": full_dialogue
            })
            vote_result = call_llm(prompt, model=agent.model)
            self.votes[agent.agent_id] = "YES" if "YES" in vote_result.upper() else "NO"
            print(f"[{agent.agent_id} 投票] {self.votes[agent.agent_id]} | {vote_result.strip()}\n")

        # 4️⃣ 汇总结果
        self._print_result()

    def _print_result(self):
        tally = {"YES": 0, "NO": 0}
        for v in self.votes.values():
            tally[v] += 1
        print(f"\n✅ 最终共识：{'YES' if tally['YES'] > tally['NO'] else 'NO'}")
        print(f"📊 投票分布：{tally}")
