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

    print(f"{Fore.RED}Solution is not possible, goal state is not achievable from the given problem state.{Style.RESET_ALL}")
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

    elif choice == 4:

        print("Water Jug Auto has been selected")

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
