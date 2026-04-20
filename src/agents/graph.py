"""
graph.py — Pipeline Orchestrator
Chains all 4 agents in order using plain function calls (no LangGraph).

Pipeline flow:
  difficulty_dict
      → run_analyzer_agent   → state["problems"]
      → run_retriever_agent  → state["principles"]
      → recommend_agent       → state["recommendations"]
      → generate_report      → markdown string  (returned, not written to state)
"""

from agents.analyzer  import run_analyzer_agent
from agents.retriever import run_retriever_agent
from agents.recommend import recommend_agent
from agents.reporter  import generate_report


def run_pipeline(difficulty_dict: dict, topic_analysis: dict = None) -> str:
    """
    Run the full 4-agent assessment pipeline.

    Args:
        difficulty_dict: e.g. {"Easy": 10, "Medium": 20, "Hard": 70, "total": 100}
        topic_analysis: Optional dict of topic-level performance data.

    Returns:
        A Markdown-formatted assessment quality report string.
    """
    # Build initial state
    state = {
        "difficulty": difficulty_dict,
        "topic_analysis": topic_analysis or {},
    }

    # Agent 1 — Analyze difficulty and identify problems
    state = run_analyzer_agent(state)

    # Agent 2 — Retrieve relevant pedagogical principles
    state = run_retriever_agent(state)

    # Agent 3 — Generate recommendations
    state = recommend_agent(state)

    # Agent 4 — Generate final report (returns markdown string, not written to state)
    report = generate_report(state)

    return report


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_difficulty = {
        "Easy":   10,
        "Medium": 20,
        "Hard":   70,
        "total":  100,
    }

    report = run_pipeline(test_difficulty)
