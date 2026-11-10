
PROBLEMS = [
    {
        "id": "sum-two",
        "title": "1. Sum of Two Numbers",
        "topic": "implementation",
        "difficulty": "Easy",
        "rating": 800,
        "description": (
            "Read two integers A and B. Print their sum."
        ),
        "input_format": "Two integers A and B separated by a space.",
        "output_format": "Print one integer: A + B.",
        "starter_code": (
            "#include <iostream>\n"
            "using namespace std;\n\n"
            "int main() {\n"
            "    int a, b;\n"
            "    cin >> a >> b;\n"
            "    // Print the sum of a and b\n"
            "    return 0;\n"
            "}\n"
        ),
        "examples": [
            {"input": "2 3\n", "output": "5\n"},
            {"input": "10 20\n", "output": "30\n"}
        ],
        "tests": [
            {"input": "2 3\n", "output": "5\n"},
            {"input": "10 20\n", "output": "30\n"},
            {"input": "-4 9\n", "output": "5\n"},
            {"input": "0 0\n", "output": "0\n"}
        ]
    },
    {
        "id": "even-odd",
        "title": "2. Even or Odd",
        "topic": "implementation",
        "difficulty": "Easy",
        "rating": 800,
        "description": (
            "Read an integer N. Print Even if it is even; otherwise print Odd."
        ),
        "input_format": "One integer N.",
        "output_format": "Print Even or Odd.",
        "starter_code": (
            "#include <iostream>\n"
            "using namespace std;\n\n"
            "int main() {\n"
            "    int n;\n"
            "    cin >> n;\n"
            "    // Check whether n is even or odd\n"
            "    return 0;\n"
            "}\n"
        ),
        "examples": [
            {"input": "4\n", "output": "Even\n"},
            {"input": "7\n", "output": "Odd\n"}
        ],
        "tests": [
            {"input": "4\n", "output": "Even\n"},
            {"input": "7\n", "output": "Odd\n"},
            {"input": "0\n", "output": "Even\n"},
            {"input": "-3\n", "output": "Odd\n"}
        ]
    },
    {
        "id": "largest-three",
        "title": "3. Largest of Three Numbers",
        "topic": "implementation",
        "difficulty": "Easy",
        "rating": 800,
        "description": (
            "Read three integers and print the largest number."
        ),
        "input_format": "Three integers A, B and C.",
        "output_format": "Print the largest integer.",
        "starter_code": (
            "#include <iostream>\n"
            "using namespace std;\n\n"
            "int main() {\n"
            "    int a, b, c;\n"
            "    cin >> a >> b >> c;\n"
            "    // Find and print the largest number\n"
            "    return 0;\n"
            "}\n"
        ),
        "examples": [
            {"input": "3 9 5\n", "output": "9\n"},
            {"input": "8 2 4\n", "output": "8\n"}
        ],
        "tests": [
            {"input": "3 9 5\n", "output": "9\n"},
            {"input": "8 2 4\n", "output": "8\n"},
            {"input": "-1 -2 -3\n", "output": "-1\n"},
            {"input": "5 5 2\n", "output": "5\n"}
        ]
    },
    {
        "id": "sum-array",
        "title": "4. Sum of Array Elements",
        "topic": "implementation",
        "difficulty": "Medium",
        "rating": 1200,
        "description": (
            "Read N followed by N integers. Print the sum of the integers."
        ),
        "input_format": "First N, then N integers.",
        "output_format": "Print the sum.",
        "starter_code": (
            "#include <iostream>\n"
            "using namespace std;\n\n"
            "int main() {\n"
            "    int n;\n"
            "    cin >> n;\n"
            "    int sum = 0;\n"
            "    for (int i = 0; i < n; i++) {\n"
            "        int x;\n"
            "        cin >> x;\n"
            "        // Add x to sum\n"
            "    }\n"
            "    cout << sum << endl;\n"
            "    return 0;\n"
            "}\n"
        ),
        "examples": [
            {"input": "4\n1 2 3 4\n", "output": "10\n"}
        ],
        "tests": [
            {"input": "4\n1 2 3 4\n", "output": "10\n"},
            {"input": "3\n-1 5 2\n", "output": "6\n"},
            {"input": "1\n9\n", "output": "9\n"}
        ]
    }
]


def get_problem_list():
    return [
        {
            "id": problem["id"],
            "title": problem["title"],
            "topic": problem["topic"],
            "difficulty": problem["difficulty"],
            "rating": problem["rating"]
        }
        for problem in PROBLEMS
    ]


def get_problem(problem_id):
    for problem in PROBLEMS:
        if problem["id"] == problem_id:
            return problem
    return None


def extract_problems(topic="implementation", difficulty="Easy"):
    topic = topic.strip().lower()

    return [
        {
            "title": problem["title"],
            "topic": problem["topic"],
            "rating": problem["rating"],
            "difficulty": problem["difficulty"],
            "url": "#practice",
            "id": problem["id"]
        }
        for problem in PROBLEMS
        if problem["topic"] == topic
        and problem["difficulty"] == difficulty
    ]


def get_daily_message(minutes):
    try:
        minutes = int(minutes)
    except (ValueError, TypeError):
        return "Please enter a valid practice time."

    if minutes <= 0:
        return "Choose a valid practice time."
    if minutes <= 15:
        return "Review one concept and attempt one coding problem."
    if minutes <= 30:
        return "Review a concept, solve 1-2 problems, and check mistakes."
    if minutes <= 60:
        return "Practise focused problem-solving and review your solutions."

    return (
        "Divide your time between revision, problem-solving, "
        "and reviewing mistakes. Take breaks too."
    )
