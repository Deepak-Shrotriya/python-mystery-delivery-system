import json

from main import simulate_delivery


def test_all_packages_are_delivered():
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    report, assignments = simulate_delivery(data)

    assert len(assignments) == len(data["packages"])


def test_package_count_matches():
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    report, assignments = simulate_delivery(data)

    total_delivered = sum(
        report[agent_id]["packages_delivered"]
        for agent_id in data["agents"]
    )

    assert total_delivered == len(data["packages"])


if __name__ == "__main__":
    test_all_packages_are_delivered()
    test_package_count_matches()

    print("All tests passed.")