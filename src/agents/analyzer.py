"""analyzer.py — Agent 1 (Analyzer)

Rule-based difficulty analysis agent.
Detects imbalance problems in exam difficulty distribution
and returns a list of human-readable issue strings.
"""


def analyze_difficulty(difficulty_json: dict) -> list:
    """
    Analyze difficulty distribution and return a list of identified problems.

    Args:
        difficulty_json: dict with keys Easy, Medium, Hard, total (counts)

    Returns:
        List of problem description strings. Empty list means exam is balanced.
    """
    problems = []
    easy   = difficulty_json.get("Easy", 0)
    medium = difficulty_json.get("Medium", 0)
    hard   = difficulty_json.get("Hard", 0)
    total  = max(difficulty_json.get("total", 1), 1)  # prevent division by zero

    easy_pct   = (easy   / total) * 100
    medium_pct = (medium / total) * 100
    hard_pct   = (hard   / total) * 100

    # Check hard question ratio
    if hard_pct > 45:
        problems.append(f"{hard_pct:.1f}% questions are Hard — exam is too difficult")
    elif hard_pct < 20:
        problems.append(f"{hard_pct:.1f}% questions are Hard — lacks high-level challenge")

    # Check easy question ratio
    if easy_pct < 15:
        problems.append("Very few Easy questions — students may lack confidence building")
    elif easy_pct > 50:
        problems.append("Too many Easy questions — exam may not challenge students enough")

    # Check overall balance against 30-40-30 ideal
    if abs(easy_pct - 30) > 15 or abs(medium_pct - 40) > 15 or abs(hard_pct - 30) > 15:
        problems.append("Difficulty distribution is imbalanced (deviates significantly from 30-40-30)")
    else:
        if medium_pct < 35:
            problems.append(f"Medium questions only {medium_pct:.0f}% — slightly low")

    # Check for missing difficulty levels
    if easy == 0 or medium == 0 or hard == 0:
        problems.append("One or more difficulty levels missing — poor exam structure")

    return problems


def run_analyzer_agent(state: dict) -> dict:
    difficulty_json = state.get("difficulty", {})
    problems = analyze_difficulty(difficulty_json)
    state["problems"] = problems
    return state
