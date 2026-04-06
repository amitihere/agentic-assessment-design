import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.analyzer import run_analyzer_agent
from agents.retriever import run_retriever_agent

state = {
    "difficulty": {
        "Easy": 10,
        "Medium": 20,
        "Hard": 70,
        "total": 100
    }
}

# Agent 1 runs first
state = run_analyzer_agent(state)
print("Agent 1 Problems:", state["problems"])

# Agent 2 runs second
state = run_retriever_agent(state)
print("\nAgent 2 Principles:")
for p in state["principles"]:
    print(f"  • {p}")