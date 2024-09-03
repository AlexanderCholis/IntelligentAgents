import sys
import heapq, random
import string
import copy
import numpy as np


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

    print('Solution is not possible, goal state is not achievable from the given problem state.')
    return "sol not found"


# Text menu
def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Blocks World Manual")
    print("2. Blocks World Auto")
    print("3. Water Jug Manual")
    print("4. Water Jug Auto")
    print("5. Exit")
    print(67 * "-")


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
    for i in range(len(state)):
        visualization += f"  {i + 1}  "

    visualization += "\n"
    visualization += "\n"

    print(visualization)


def visualize_water_jugs(state, capacities):
    """
    Visualizes the state of the Water Jug problem using symbols to represent the water levels.
    """
    visualization = ""
    max_capacity = max(capacities)

    for level in reversed(range(max_capacity + 1)):
        for i in range(len(state)):
            if state[i] >= level:
                visualization += "  | ⊟ |  "
            elif level == 0:
                visualization += f" [{capacities[i]}] "
            else:
                visualization += "  |   |  "
        visualization += "\n"

    bottom_line = ""
    for i in range(len(state)):
        bottom_line += "  |___|  "
    visualization += bottom_line.rstrip() + "\n"

    state_line = ""
    for i, amount in enumerate(state):
        state_line += (f"    {amount}  "
                       f"  ")
    visualization += state_line.rstrip() + "\n"

    print(visualization)


while True:
    print_menu()
    choice = int(input("Enter your choice [1-5]: "))

    if choice == 2:

        print("Blocks World Auto has been selected")

        stacks = int(input("Stacks: "))
        blocks = int(input("Blocks: "))
        while stacks < 0 or blocks < 0:
            print("Please enter positive numbers only.")
            stacks = int(input("Stacks: "))
            blocks = int(input("Blocks: "))


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

                print('Number of MOVES required:', len(path_back) - 1)
                print('-------------------------------------------------')
                print("List of nodes forming the path from the root to the goal.")
                for state in reversed(path_back):
                    visualize_blocks_world(state)

            def pathCost(self):
                return self.heuristics() + self.cost


        aStarSearch(NodeBlocks(startSt, finalSt), lambda state: 0)


    elif choice == 3:

        print("Water Jug Manual has been selected")

        num_jugs = int(input("Enter number of jugs: "))
        capacities_list = []
        initial_state = []
        goal_state = []

        # Input capacities
        for i in range(num_jugs):
            capacity = int(input(f"Capacity of Jug {i + 1}: "))
            capacities_list.append(capacity)

        # Input initial amounts
        for i in range(num_jugs):
            amount = int(input(f"Initial amount in Jug {i + 1}: "))
            initial_state.append(amount)

        # Input goal amounts
        for i in range(num_jugs):
            amount = int(input(f"Goal amount in Jug {i + 1}: "))
            goal_state.append(amount)


        def getSuccessorsWater(state):
            successors = []
            capacities = capacities_list
            for i in range(len(state)):
                if state[i] < capacities[i]:
                    successors.append((state[:i] + (capacities[i],) + state[i + 1:], f'Fill Jug {i + 1}', 1))
                if state[i] > 0:
                    successors.append((state[:i] + (0,) + state[i + 1:], f'Empty Jug {i + 1}', 1))
                for j in range(len(state)):
                    if i != j:
                        transfer_amount = min(state[i], capacities[j] - state[j])
                        if transfer_amount > 0:
                            new_state = list(state)
                            new_state[i] -= transfer_amount
                            new_state[j] += transfer_amount
                            successors.append((tuple(new_state), f'Pour from Jug {i + 1} to Jug {j + 1}', 1))
            return successors


        def waterHeuristic(state):
            return sum(abs(state[i] - goal_state[i]) for i in range(len(state)))


        class NodeWater:
            def __init__(self, state, goal_state, path, cost=0, heuristic=0):
                self.state = state
                self.goal_state = goal_state
                self.path = path
                self.cost = cost
                self.heuristic = heuristic

            def getSuccessors(self, heuristicFunction=None):
                children = []
                for successor in getSuccessorsWater(self.state):
                    state = successor[0]
                    path = list(self.path)
                    path.append(successor[1])
                    cost = self.cost + successor[2]
                    heuristic = heuristicFunction(state) if heuristicFunction else 0
                    node = NodeWater(state, self.goal_state, path, cost, heuristic)
                    children.append(node)
                return children

            def pathCost(self):
                return self.cost + self.heuristic

            def goalTest(self):
                if self.state == self.goal_state:
                    print("Solution Found! Path to goal:", self.path)
                    return True
                return False


        print("Initial State:")
        visualize_water_jugs(initial_state, capacities_list)
        print("Goal State:")
        visualize_water_jugs(goal_state, capacities_list)

        aStarSearch(NodeWater(tuple(initial_state), tuple(goal_state), [], 0, 0), waterHeuristic)

    elif choice == 4:

        print("Water Jug Auto has been selected")


        def generate_random_water_jug_data():
            num_jugs = random.randint(2, 5)  # Random number of jugs between 2 and 5
            capacities_list = [random.randint(5, 20) for _ in range(num_jugs)]  # Random capacities between 5 and 20
            initial_state = [random.randint(0, cap) for cap in capacities_list]  # Random initial amounts
            goal_state = [random.randint(0, cap) for cap in capacities_list]  # Random goal amounts

            return num_jugs, capacities_list, initial_state, goal_state

        num_jugs, capacities_list, initial_state, goal_state = generate_random_water_jug_data()

        print(f"Generated Data: Jugs = {num_jugs}, Capacities = {capacities_list}")
        print("Initial State:", initial_state)
        print("Goal State:", goal_state)

        print("Visualized Initial State:")
        visualize_water_jugs(initial_state, capacities_list)
        print("Visualized Goal State:")
        visualize_water_jugs(goal_state, capacities_list)

        # aStarSearch(NodeWater(tuple(initial_state), tuple(goal_state), [], 0, 0), waterHeuristic)

    elif choice == 1:
        print("Blocks World Manual has been selected")


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

                print('Number of MOVES required:', len(path_back) - 1)
                print('-------------------------------------------------')
                print("List of nodes forming the path from the root to the goal.")
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
