from rag.retriever import retrieve_relevant_principles

def run_retriever_agent(state: dict) -> dict:
    """
    Agent 2: Takes problems from Agent 1, retrieves
    relevant teaching principles from the knowledge base.
    
    Expects state to have: state["problems"] (list of strings)
    Returns: state updated with state["principles"]
    """
    problems = state.get("problems", [])
    
    if not problems:
        state["principles"] = ["No problems identified — exam appears well-balanced."]
        return state
    
    principles = retrieve_relevant_principles(problems, top_k=3)
    state["principles"] = principles
    
    print("Agent 2 — Retrieved Principles:")
    for p in principles:
        print(f"  → {p}")
    
    return state
