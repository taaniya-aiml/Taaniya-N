
import os
import time
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request

from agent import run_agent
from tools import get_problem, get_problem_list

BASE_DIR = Path(__file__).resolve().parent

JUDGE0_URL = os.environ.get(
    "JUDGE0_URL", "https://ce.judge0.com"
).rstrip("/")

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)


LANGUAGE_IDS = {
    "cpp": 54  # C++ (GCC 9.2.0)
}


@app.route("/", methods=["GET", "POST"])
def home():
    profile = {
        "name": "",
        "domain": "C++",
        "level": "Beginner",
        "companies": "",
        "hours": 5
    }

    topic = "implementation"
    difficulty = "Easy"
    result = None

    if request.method == "POST":
        profile["name"] = request.form.get("name", "").strip()
        profile["domain"] = request.form.get("domain", "C++")
        profile["level"] = request.form.get("level", "Beginner")
        profile["companies"] = request.form.get("companies", "").strip()

        try:
            profile["hours"] = int(request.form.get("hours", 5))
        except (ValueError, TypeError):
            profile["hours"] = 5

        profile["hours"] = max(1, min(profile["hours"], 80))
        topic = request.form.get("topic", "implementation")
        difficulty = request.form.get("difficulty", "Easy")

        result = run_agent(
            topic=topic,
            difficulty=difficulty,
            minutes=profile["hours"] * 60,
            solved=0,
            attempted=0,
            topics=[topic]
        )

    return render_template(
        "index.html",
        profile=profile,
        topic=topic,
        difficulty=difficulty,
        result=result,
        problem_list=get_problem_list()
    )


@app.route("/api/problem/<problem_id>", methods=["GET"])
def problem_details(problem_id):
    problem = get_problem(problem_id)

    if not problem:
        return jsonify({"error": "Problem not found."}), 404

    return jsonify({
        "id": problem["id"],
        "title": problem["title"],
        "description": problem["description"],
        "input_format": problem["input_format"],
        "output_format": problem["output_format"],
        "examples": problem["examples"],
        "starter_code": problem["starter_code"]
    })


@app.route("/api/run-code", methods=["POST"])
def run_code():
    data = request.get_json(silent=True) or {}

    problem_id = str(data.get("problem_id", ""))
    source_code = data.get("source_code", "")
    action = data.get("action", "run")

    problem = get_problem(problem_id)

    if not problem:
        return jsonify({"error": "Please select a valid problem."}), 400

    if not isinstance(source_code, str) or not source_code.strip():
        return jsonify({"error": "Please write some C++ code first."}), 400

    if len(source_code) > 20000:
        return jsonify({"error": "Code must be under 20,000 characters."}), 400

    if action not in ("run", "submit"):
        return jsonify({"error": "Invalid action."}), 400

    test_cases = problem["examples"] if action == "run" else problem["tests"]
    results = []

    try:
        for case in test_cases:
            payload = {
                "source_code": source_code,
                "language_id": LANGUAGE_IDS["cpp"],
                "stdin": case["input"],
                "expected_output": case["output"],
                "cpu_time_limit": 2,
                "cpu_extra_time": 1,
                "wall_time_limit": 5,
                "memory_limit": 128000
            }

            response = requests.post(
                f"{JUDGE0_URL}/submissions",
                params={"base64_encoded": "false", "wait": "false"},
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            token = response.json().get("token")

            if not token:
                return jsonify({
                    "error": "The code runner did not return a submission token."
                }), 502

            result = None

            for _ in range(20):
                time.sleep(1)

                poll = requests.get(
                    f"{JUDGE0_URL}/submissions/{token}",
                    params={"base64_encoded": "false"},
                    timeout=10
                )
                poll.raise_for_status()
                result = poll.json()

                status_id = result.get("status", {}).get("id")

                if status_id not in (1, 2):
                    break

            if not result or result.get("status", {}).get("id") in (1, 2):
                return jsonify({
                    "error": "Execution is taking too long. Please try again."
                }), 504

            status = result.get("status", {}).get("description", "Unknown")
            stdout = result.get("stdout") or ""
            stderr = result.get("stderr") or ""
            compile_output = result.get("compile_output") or ""
            message = result.get("message") or ""

            passed = status == "Accepted"

            results.append({
                "input": case["input"],
                "expected": case["output"],
                "output": stdout,
                "status": status,
                "passed": passed,
                "error": compile_output or stderr or message
            })

            if status not in ("Accepted", "Wrong Answer"):
                break

            if action == "run":
                # Running uses sample tests only.
                continue

    except requests.RequestException:
        return jsonify({
            "error": (
                "Could not connect to the code runner. "
                "Check your internet connection or try again later."
            )
        }), 502

    passed_count = sum(1 for item in results if item["passed"])
    all_passed = len(results) == len(test_cases) and passed_count == len(test_cases)

    return jsonify({
        "results": results,
        "passed": passed_count,
        "total": len(results),
        "all_passed": all_passed,
        "message": (
            "All tested cases passed!"
            if all_passed
            else f"{passed_count} of {len(results)} tested cases passed."
        )
    })


@app.route("/api/mentor", methods=["POST"])
def mentor():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question first."}), 400

    return jsonify({
        "answer": (
            "The AI Mentor service is not connected yet. "
            "You can use the inbuilt C++ editor to practise."
        )
    })


if __name__ == "__main__":
    app.run(debug=True)
