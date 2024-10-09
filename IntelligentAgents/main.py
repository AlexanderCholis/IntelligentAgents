import heapq, random
import string
import copy
from collections import deque
from colorama import Fore, Style


# PriorityQueue class
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0


# A* Search function
def aStarSearch(node, heuristic=lambda state: 0):
    closed = set()
    Q = PriorityQueue()
    Q.push(node, node.pathCost())

    while not Q.isEmpty():
        node = Q.pop()

        if node.goalTest():
            return "Solution found"

        if str(node.state) not in closed:
            closed.add(str(node.state))
            for childNode in node.getSuccessors(heuristic):
                Q.push(childNode, childNode.pathCost())

    print(
        f"{Fore.RED}Solution is not possible, goal state is not achievable from the given problem state.{Style.RESET_ALL}")
    return "sol not found"


# Text menu in Python
def print_menu():
    print(30 * "-", f"{Fore.GREEN}MENU{Style.RESET_ALL}", 30 * "-")
    print(f"{Fore.BLUE}1. Blocks World Manual{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Blocks World Auto{Style.RESET_ALL}")
    print(f"{Fore.BLUE}3. Water Jug Manual{Style.RESET_ALL}")
    print(f"{Fore.BLUE}4. Water Jug Auto{Style.RESET_ALL}")
    print(f"{Fore.BLUE}5. Exit{Style.RESET_ALL}")
    print(67 * "-")


def get_user_blocks_world_data():
    stacks = int(input("Enter number of stacks: "))
    blocks = int(input("Enter number of blocks: "))

    initial_state = []
    print("Enter the initial state for each stack (e.g., A B C for stack 1, D E for stack 2):")
    for i in range(stacks):
        stack = input(f"Stack {i + 1}: ").strip().split()
        initial_state.append(stack)

    goal_state = []
    print("Enter the goal state for each stack (e.g., A B C for stack 1, D E for stack 2):")
    for i in range(stacks):
        stack = input(f"Goal Stack {i + 1}: ").strip().split()
        goal_state.append(stack)

    return stacks, blocks, initial_state, goal_state


def visualize_blocks_world(state):
    """
    Visualizes the state of the Blocks World problem as stacks of blocks.
    """
    max_height = max(len(stack) for stack in state)
    visualization = ""

    for level in reversed(range(max_height)):
        for stack in state:
            if level < len(stack):
                visualization += f"  {stack[level]}  "
            else:
                visualization += "  .  "
        visualization += "\n"
        visualization += "\n"

    visualization += "_____" * len(state) + "\n"
    for ib in range(len(state)):
        visualization += f"  {ib + 1}  "

    visualization += "\n"
    visualization += "\n"

    print(visualization)


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
                    visualization += " |   | "
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
def water_jug_bfs(initial_stateW, capacities, target_state):
    queue = deque([initial_stateW])
    visited = set([initial_stateW])
    parent = {initial_stateW: None}  # To keep track of the path

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
def generate_random_goal_state(initial_stateW, capacities):
    total_water = sum(initial_stateW)

    # Randomly distribute the total water across the jugs
    while True:
        goal_stateW = [random.randint(0, capacities[i]) for i in range(len(capacities))]
        if sum(goal_stateW) == total_water:
            return tuple(goal_stateW)


# Function for manual water jug problem
def solve_manual_water_jug_problem():
    # Get user input for number of jugs
    num_jugs = int(input("Enter the number of jugs (2 to 4): "))
    if num_jugs < 2 or num_jugs > 4:
        print(f"{Fore.RED}Number of jugs must be between 2 and 4.{Style.RESET_ALL}")
        return

    # Get user input for jug capacities
    capacities = []
    for i in range(num_jugs):
        capacity = int(input(f"Enter the capacity of jug {i + 1}: "))
        capacities.append(capacity)

    capacities = tuple(capacities)

    # Get user input for the initial state
    initial_stateW = []
    for i in range(num_jugs):
        initial_amount = int(input(f"Enter the initial amount of water in jug {i + 1} (0 to {capacities[i]}): "))
        if initial_amount > capacities[i]:
            print(f"{Fore.RED}Initial amount of water in jug {i + 1} cannot exceed its capacity.{Style.RESET_ALL}")
            return
        initial_stateW.append(initial_amount)

    initial_stateW = tuple(initial_stateW)

    # Get user input for the goal state
    goal_stateW = []
    for i in range(num_jugs):
        goal_amount = int(input(f"Enter the goal amount of water in jug {i + 1} (0 to {capacities[i]}): "))
        if goal_amount > capacities[i]:
            print(f"Goal amount of water in jug {i + 1} cannot exceed its capacity.")
            return
        goal_stateW.append(goal_amount)

    goal_stateW = tuple(goal_stateW)

    print(f"\nManual Initial State: {initial_stateW}")
    print(f"Manual Goal State: {goal_stateW}\n")

    # Visualize initial state
    print("Initial State Visualization:")
    visualize_water_jugs(initial_stateW, capacities)

    # Visualize goal state
    print("Goal State Visualization:")
    visualize_water_jugs(goal_stateW, capacities)

    # Solve the problem using BFS
    solution_path = water_jug_bfs(initial_stateW, capacities, goal_stateW)

    if solution_path:
        print(f"{Fore.GREEN}Solution found in {len(solution_path) - 1} steps:{Style.RESET_ALL}\n")
        for step_num, step in enumerate(solution_path):
            print(f"Step {step_num}: {step}")
            visualize_water_jugs(step, capacities)
    else:
        print(f"{Fore.RED}No solution found.{Style.RESET_ALL}")


# Function for automatic water jug problem
def solve_random_water_jug_problem():
    # Random number of jugs between 2 and 4
    num_jugs = random.randint(2, 4)

    # Set random capacities for each jug (between 1 and 10 liters)
    capacities = tuple(random.randint(1, 10) for _ in range(num_jugs))

    # Generate a random initial state
    initial_stateW = generate_random_state(capacities)

    # Generate a random goal state with the same total water
    goal_stateW = generate_random_goal_state(initial_stateW, capacities)

    print(f"Random Number of Jugs: {num_jugs}")
    print(f"Random Jug Capacities: {capacities}")
    print(f"Random Initial State: {initial_stateW}")
    print(f"Random Goal State: {goal_stateW}\n")

    # Visualize initial state
    print("Initial State Visualization:")
    visualize_water_jugs(initial_stateW, capacities)

    # Visualize goal state
    print("Goal State Visualization:")
    visualize_water_jugs(goal_stateW, capacities)

    # Find the solution using BFS
    solution_path = water_jug_bfs(initial_stateW, capacities, goal_stateW)

    if solution_path:
        print(f"{Fore.GREEN}Solution found in {len(solution_path) - 1} steps:{Style.RESET_ALL}\n")
        for step_num, step in enumerate(solution_path):
            print(f"Step {step_num}: {step}")
            visualize_water_jugs(step, capacities)
    else:
        print(f"{Fore.RED}No solution found.{Style.RESET_ALL}")


while True:
    print_menu()
    choice = int(input("Enter your choice [1-5]: "))

    if choice == 2:

        print("Blocks World Auto has been selected")

        # Generate random number of stacks and blocks
        stacks = random.randint(3, 5)  # Random number of stacks between 3 and 5
        blocks = random.randint(5, 10)  # Random number of blocks between 5 and 10

        print(f"Randomly generated {stacks} stacks and {blocks} blocks.")


        # Function to generate a random state
        def generate_random_state(stacks, blocks):
            all_blocks = list(string.ascii_uppercase[:blocks])
            random.shuffle(all_blocks)
            state = [[] for _ in range(stacks)]
            for block in all_blocks:
                stack_choice = random.choice(state)
                stack_choice.append(block)
            return state


        # Generate a random initial and goal state
        startSt = generate_random_state(stacks, blocks)
        finalSt = generate_random_state(stacks, blocks)

        print("Initial State:")
        visualize_blocks_world(startSt)
        print("Goal State:")
        visualize_blocks_world(finalSt)


        class NodeBlocks:
            def __init__(self, elements, goal_state, parent=None):
                self.state = elements
                self.goal_state = goal_state
                self.parent = parent
                self.cost = 0
                if parent:
                    self.cost = parent.cost + 1

            def goalTest(self):
                if self.state == self.goal_state:
                    print("Solution Found!")
                    self.traceback()
                    return True
                else:
                    return False

            def heuristics(self):
                return sum(1 for i, stack in enumerate(self.state) if stack != self.goal_state[i])

            def getSuccessors(self, heuristic):
                children = []
                for i, stack in enumerate(self.state):
                    for j, stack1 in enumerate(self.state):
                        if i != j and len(stack1):
                            temp = copy.deepcopy(stack)
                            child = copy.deepcopy(self)
                            temp1 = copy.deepcopy(stack1)
                            temp.append(temp1[-1])
                            del temp1[-1]
                            child.state[i] = temp
                            child.state[j] = temp1
                            child.parent = copy.deepcopy(self)
                            children.append(child)
                return children

            def traceback(self):
                s, path_back = self, []
                while s:
                    path_back.append(s.state)
                    s = s.parent

                print(f"{Fore.GREEN}Number of MOVES required:{Style.RESET_ALL}", len(path_back) - 1)
                print(f"{Fore.GREEN}-------------------------------------------------{Style.RESET_ALL}")
                print(f"{Fore.GREEN}List of nodes forming the path from the root to the goal.{Style.RESET_ALL}")
                for state in reversed(path_back):
                    visualize_blocks_world(state)

            def pathCost(self):
                return self.heuristics() + self.cost


        # Run the A* algorithm
        aStarSearch(NodeBlocks(startSt, finalSt), lambda state: 0)

    elif choice == 3:

        print("Water Jug Manual has been selected")
        solve_manual_water_jug_problem()

    elif choice == 4:

        print("Water Jug Auto has been selected")
        solve_random_water_jug_problem()

    elif choice == 1:

        print("Blocks World Manual has been selected")

        stacks, blocks, initial_state, goal_state = get_user_blocks_world_data()

        print("Initial State:")
        visualize_blocks_world(initial_state)
        print("Goal State:")
        visualize_blocks_world(goal_state)


        class NodeBlocks:
            def __init__(self, elements, goal_state, parent=None):
                self.state = elements
                self.goal_state = goal_state
                self.parent = parent
                self.cost = 0
                if parent:
                    self.cost = parent.cost + 1

            def goalTest(self):
                if self.state == self.goal_state:
                    print("Solution Found!")
                    self.traceback()
                    return True
                return False

            def heuristics(self):
                return sum(1 for i, stack in enumerate(self.state) if stack != self.goal_state[i])

            def getSuccessors(self, heuristic):
                children = []
                for i, stack in enumerate(self.state):
                    for j, stack1 in enumerate(self.state):
                        if i != j and len(stack1):
                            temp = copy.deepcopy(stack)
                            child = copy.deepcopy(self)
                            temp1 = copy.deepcopy(stack1)
                            temp.append(temp1[-1])
                            del temp1[-1]
                            child.state[i] = temp
                            child.state[j] = temp1
                            child.parent = copy.deepcopy(self)
                            children.append(child)
                return children

            def traceback(self):
                s, path_back = self, []
                while s:
                    path_back.append(s.state)
                    s = s.parent

                print(f"{Fore.GREEN}Number of MOVES required:{Style.RESET_ALL}", len(path_back) - 1)
                print(f"{Fore.GREEN}-------------------------------------------------{Style.RESET_ALL}")
                print(f"{Fore.GREEN}List of nodes forming the path from the root to the goal.{Style.RESET_ALL}")
                for state in reversed(path_back):
                    visualize_blocks_world(state)

            def pathCost(self):
                return self.heuristics() + self.cost


        aStarSearch(NodeBlocks(initial_state, goal_state), lambda state: 0)

    elif choice == 5:
        print("Exit has been selected")
        break

    else:
        input("Wrong option selection. Enter any key to try again..")
