# agents/borda_aggregator.py

from collections import defaultdict

class BordaVotingAggregator:
    def __init__(self, candidates: list):
        self.candidates = candidates
        self.votes = []  # 每个智能体返回的候选项排名列表，例如 ["B", "C", "A"]

    def add_vote(self, ranked_list: list[str]):
        if set(ranked_list) != set(self.candidates):
            raise ValueError(f"投票无效：排名列表应包含所有候选项：{self.candidates}")
        self.votes.append(ranked_list)

    def compute_result(self):
        scores = defaultdict(int)
        n = len(self.candidates)

        for vote in self.votes:
            for rank, candidate in enumerate(reversed(vote)):  # 倒序打分：第一名得 n-1 分
                scores[candidate] += rank

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        winner = sorted_scores[0][0]
        return {
            "winner": winner,
            "scores": dict(sorted_scores),
            "raw_votes": self.votes
        }
