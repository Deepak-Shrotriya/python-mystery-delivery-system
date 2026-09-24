import json
import math


def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    """

    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return distance


def find_nearest_agent(agents, warehouse_location):
    """
    Find the agent closest to the warehouse.
    """

    nearest_agent = min(
        agents,
        key=lambda agent_id:
        calculate_distance(
            agents[agent_id],
            warehouse_location
        )
    )

    return nearest_agent


def simulate_delivery(data):
    """
    Assign packages to agents and simulate delivery.
    """

    warehouses = data["warehouses"]
    agents = data["agents"]
    packages = data["packages"]

    # Create initial report for every agent
    report = {}

    for agent_id in agents:

        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "efficiency": 0.0
        }

    # Store detailed package assignments
    assignments = []

    # Process every package
    for package in packages:

        package_id = package["id"]
        warehouse_id = package["warehouse"]
        destination = package["destination"]

        # Get warehouse coordinates
        warehouse_location = warehouses[warehouse_id]

        # Find nearest agent
        agent_id = find_nearest_agent(
            agents,
            warehouse_location
        )

        # Get agent coordinates
        agent_location = agents[agent_id]

        # Agent -> Warehouse distance
        agent_to_warehouse = calculate_distance(
            agent_location,
            warehouse_location
        )

        # Warehouse -> Destination distance
        warehouse_to_destination = calculate_distance(
            warehouse_location,
            destination
        )

        # Total distance for this package
        package_distance = (
            agent_to_warehouse +
            warehouse_to_destination
        )

        # Update agent statistics
        report[agent_id]["packages_delivered"] += 1

        report[agent_id]["total_distance"] += package_distance

        # Store assignment details
        assignments.append({
            "package_id": package_id,
            "warehouse": warehouse_id,
            "assigned_agent": agent_id,
            "agent_to_warehouse_distance":
                round(agent_to_warehouse, 2),
            "warehouse_to_destination_distance":
                round(warehouse_to_destination, 2),
            "total_package_distance":
                round(package_distance, 2)
        })

    # Calculate efficiency
    for agent_id in report:

        packages_delivered = \
            report[agent_id]["packages_delivered"]

        total_distance = \
            report[agent_id]["total_distance"]

        if packages_delivered > 0:

            efficiency = (
                total_distance /
                packages_delivered
            )

            report[agent_id]["total_distance"] = \
                round(total_distance, 2)

            report[agent_id]["efficiency"] = \
                round(efficiency, 2)

        else:

            report[agent_id]["total_distance"] = 0.0

            report[agent_id]["efficiency"] = 0.0

    # Find agents that actually delivered packages
    active_agents = []

    for agent_id in agents:

        if report[agent_id]["packages_delivered"] > 0:
            active_agents.append(agent_id)

    # Find best agent
    if active_agents:

        best_agent = min(
            active_agents,
            key=lambda agent_id:
            report[agent_id]["efficiency"]
        )

    else:

        best_agent = None

    report["best_agent"] = best_agent

    return report, assignments


def main():

    # Read input JSON file
    with open(
        "data.json",
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    # Run delivery simulation
    report, assignments = simulate_delivery(data)

    # Save final report
    with open(
        "report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    # Display assignments
    print("Delivery Assignments")
    print("--------------------")

    for assignment in assignments:

        print(
            f'{assignment["package_id"]} -> '
            f'{assignment["assigned_agent"]} '
            f'({assignment["total_package_distance"]:.2f})'
        )

    # Display final report
    print("\nFinal Report")
    print("------------")

    print(
        json.dumps(
            report,
            indent=4
        )
    )

    print("\nReport saved to report.json")


if __name__ == "__main__":
    main()