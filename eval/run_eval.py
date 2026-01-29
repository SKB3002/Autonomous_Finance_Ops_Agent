import json
from api.app import run_agent

def run_tests():
    with open("eval/test_cases.json") as f:
        tests = json.load(f)

    results = []

    for test in tests:
        print(f"Running: {test['name']}")

        state = run_agent(
            user_query=test["input"].get("user_query"),
            uploaded_file=test["input"].get("uploaded_file")
        )

        passed = True
        for key, expected_value in test["expected"].items():
            if state.get(key) != expected_value:
                passed = False

        results.append({
            "test": test["name"],
            "passed": passed,
            "state": state
        })

    return results


if __name__ == "__main__":
    results = run_tests()
    for r in results:
        print(r["test"], "PASSED" if r["passed"] else "FAILED")
