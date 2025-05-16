# main.py

from agents.opinion_agent import OpinionAgent
from agents.voting_agent import VotingAgent
from agents.coordinator import DebateCoordinator

def main():
    print("🎯 欢迎使用多模型多智能体协商系统")
    topic = input("请输入一个议题（如：是否应禁止AI生成艺术？）\n> ").strip()

    # 为每个Agent分配不同的模型
    agent_configs = {
        "Agent_A": "gpt-4.1",
        "Agent_B": "gemini-2.0-flash-thinking-exp",
        "Agent_C": "Pro/deepseek-ai/DeepSeek-R1"
    }

    # 初始化智能体（opinion和voting可共用模型）
    opinion_agents = [OpinionAgent(agent_id, model=model) for agent_id, model in agent_configs.items()]
    voting_agents = [VotingAgent(agent_id, model=model) for agent_id, model in agent_configs.items()]

    # 协调讨论过程
    coordinator = DebateCoordinator(topic, opinion_agents, voting_agents)
    coordinator.run_debate()

if __name__ == "__main__":
    main()
