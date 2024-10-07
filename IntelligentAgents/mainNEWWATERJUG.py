import random
from collections import deque
from colorama import Fore, Style, init

init()


# Function to visualize the current state of the Water Jug problem
def visualize_water_jugs(state, capacities):
    """
    Visualizes the state of the Water Jug problem using symbols to represent the water levels.
    The filled boxes (⊟) and empty boxes are consistently aligned.
    """
    visualization = ""
    max_capacity = max(capacities)

    for level in reversed(range(max_capacity + 1)):
        for i in range(len(state)):
            if state[i] >= level:
                # visualization += " | ⊟ | "
                visualization += f" | {Fore.CYAN}⊟{Style.RESET_ALL} | "
            else:
                if level == 0:
                    # visualization += f" [{capacities[i]:2}] "  # Capacity of each jug displayed on the bottom
                    visualization += f" [{Fore.YELLOW}{capacities[i]:2}{Style.RESET_ALL}] "
                else:
                    visualization += " |     | "
        visualization += "\n"

    bottom_line = ""
    for _ in range(len(state)):
        bottom_line += " |___| "
    visualization += bottom_line.rstrip() + "\n"

    state_line = ""
    for amount in state:
        # state_line += f"  {amount:2}  "  # Show the current amount in each jug
        state_line += f"  {Fore.YELLOW}{amount:2}  {Style.RESET_ALL}  "
    visualization += state_line.rstrip() + "\n"

    print(visualization)


# Function to check if the current state is the goal state
def is_goal_state(state, target):
    return state == target


# Function to pour water from one jug to another
def pour_water(state, from_jug, to_jug, capacities):
    new_state = list(state)
    transfer_amount = min(state[from_jug], capacities[to_jug] - state[to_jug])
    new_state[from_jug] -= transfer_amount
    new_state[to_jug] += transfer_amount
    return tuple(new_state)


# Function to get all possible next states from the current state
def get_next_states(state, capacities):
    next_states = []
    jug_count = len(capacities)
    # Generate all combinations of pouring between the jugs
    for i in range(jug_count):
        for j in range(jug_count):
            if i != j:
                next_states.append(pour_water(state, i, j, capacities))
    return next_states


# BFS function to solve the water jug problem
def water_jug_bfs(initial_state, capacities, target_state):
    queue = deque([initial_state])
    visited = set([initial_state])
    parent = {initial_state: None}  # To keep track of the path

    while queue:
        current_state = queue.popleft()

        # Check if we reached the goal state
        if is_goal_state(current_state, target_state):
            # Reconstruct the path
            path = []
            while current_state is not None:
                path.append(current_state)
                current_state = parent[current_state]
            return path[::-1]  # Return reversed path (from start to goal)

        # Get all possible next states and explore them
        for next_state in get_next_states(current_state, capacities):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = current_state
                queue.append(next_state)

    # If no solution is found
    return None


# Function to generate a random initial state
def generate_random_state(capacities):
    return tuple(random.randint(0, capacity) for capacity in capacities)


# Function to generate a random goal state with the same total water
def generate_random_goal_state(initial_state, capacities):
    total_water = sum(initial_state)

    # Randomly distribute the total water across the jugs
    while True:
        goal_state = [random.randint(0, capacities[i]) for i in range(len(capacities))]
        if sum(goal_state) == total_water:
            return tuple(goal_state)


# Menu function
def print_menu():
    print(30 * "-", f"{Fore.GREEN}MENU{Style.RESET_ALL}", 30 * "-")
    print(f"{Fore.BLUE}1. Water Jug Manual{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Water Jug Auto{Style.RESET_ALL}")
    print(f"{Fore.BLUE}3. Exit{Style.RESET_ALL}")
    print(67 * "-")


# Function for manual water jug problem
def solve_manual_water_jug_problem():
    # Get user input for number of jugs
    num_jugs = int(input("Enter the number of jugs (2 to 4): "))
    if num_jugs < 2 or num_jugs > 4:
        print("Number of jugs must be between 2 and 4.")
        return

    # Get user input for jug capacities
    capacities = []
    for i in range(num_jugs):
        capacity = int(input(f"Enter the capacity of jug {i + 1}: "))
        capacities.append(capacity)

    capacities = tuple(capacities)

    # Get user input for the initial state
    initial_state = []
    for i in range(num_jugs):
        initial_amount = int(input(f"Enter the initial amount of water in jug {i + 1} (0 to {capacities[i]}): "))
        if initial_amount > capacities[i]:
            print(f"Initial amount of water in jug {i + 1} cannot exceed its capacity.")
            return
        initial_state.append(initial_amount)

    initial_state = tuple(initial_state)

    # Get user input for the goal state
    goal_state = []
    for i in range(num_jugs):
        goal_amount = int(input(f"Enter the goal amount of water in jug {i + 1} (0 to {capacities[i]}): "))
        if goal_amount > capacities[i]:
            print(f"Goal amount of water in jug {i + 1} cannot exceed its capacity.")
            return
        goal_state.append(goal_amount)

    goal_state = tuple(goal_state)

    print(f"\nManual Initial State: {initial_state}")
    print(f"Manual Goal State: {goal_state}\n")

    # Visualize initial state
    print("Initial State Visualization:")
    visualize_water_jugs(initial_state, capacities)

    # Visualize goal state
    print("Goal State Visualization:")
    visualize_water_jugs(goal_state, capacities)

    # Solve the problem using BFS
    solution_path = water_jug_bfs(initial_state, capacities, goal_state)

    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} steps:\n")
        for step_num, step in enumerate(solution_path):
            print(f"Step {step_num}: {step}")
            visualize_water_jugs(step, capacities)
    else:
        print("No solution found.")


# Function for automatic water jug problem
def solve_random_water_jug_problem():
    # Random number of jugs between 2 and 4
    num_jugs = random.randint(2, 4)

    # Set random capacities for each jug (between 1 and 10 liters)
    capacities = tuple(random.randint(1, 10) for _ in range(num_jugs))

    # Generate a random initial state
    initial_state = generate_random_state(capacities)

    # Generate a random goal state with the same total water
    goal_state = generate_random_goal_state(initial_state, capacities)

    print(f"Random Number of Jugs: {num_jugs}")
    print(f"Random Jug Capacities: {capacities}")
    print(f"Random Initial State: {initial_state}")
    print(f"Random Goal State: {goal_state}\n")

    # Visualize initial state
    print("Initial State Visualization:")
    visualize_water_jugs(initial_state, capacities)

    # Visualize goal state
    print("Goal State Visualization:")
    visualize_water_jugs(goal_state, capacities)

    # Find the solution using BFS
    solution_path = water_jug_bfs(initial_state, capacities, goal_state)

    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} steps:\n")
        for step_num, step in enumerate(solution_path):
            print(f"Step {step_num}: {step}")
            visualize_water_jugs(step, capacities)
    else:
        print("No solution found.")


# Main function to run the program
def main():
    while True:
        print_menu()  # Display menu
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            solve_manual_water_jug_problem()
        elif choice == '2':
            solve_random_water_jug_problem()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")


# Run the program
main()
