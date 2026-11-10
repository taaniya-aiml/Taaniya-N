
from tools import extract_problems, get_daily_message


def suggest_next_level(solved, attempted, difficulty):
    if attempted == 0:
        return "Start with a few problems to track your progress."

    if solved / attempted >= 0.8:
        if difficulty == "Easy":
            return "You're making progress! Try Medium problems next."
        if difficulty == "Medium":
            return "Great work! Consider trying Hard problems."
        return "Excellent effort! Keep challenging yourself."

    return "Keep practising and review mistakes at your own pace."


def achievement_summary(solved, attempted, topics=None):
    rate = solved / attempted * 100 if attempted else 0

    message = (
        f"You solved {solved} out of {attempted} problems "
        f"({rate:.0f}% success rate). "
    )

    if solved >= 10:
        message += "Amazing milestone! You've solved 10 or more problems."
    elif solved:
        message += "Every solved problem is progress. Keep going!"
    else:
        message += "Let's work towards solving your first problem!"

    if topics:
        message += " Topics selected: " + ", ".join(topics) + "."

    return message


def run_agent(
    topic="implementation",
    difficulty="Easy",
    minutes=30,
    solved=0,
    attempted=0,
    topics=None
):
    if difficulty not in ("Easy", "Medium", "Hard"):
        problems = []
        message = "Please select a valid difficulty."
    elif minutes <= 0 or solved < 0 or attempted < 0 or solved > attempted:
        problems = []
        message = "Please enter valid time and progress values."
    else:
        problems = extract_problems(topic, difficulty)
        message = (
            f"Found {len(problems)} practice problems."
            if problems else
            "No matching problems found. Try another topic or difficulty."
        )

    return {
        "problems": problems,
        "message": message,
        "summary": achievement_summary(solved, attempted, topics),
        "daily_plan": get_daily_message(minutes),
        "next_level": suggest_next_level(solved, attempted, difficulty)
        if difficulty in ("Easy", "Medium", "Hard") else ""
    }
