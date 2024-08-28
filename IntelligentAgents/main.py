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

    def lenHeap(self):
        return len(self.heap)

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
    startNode = node
    Q.push(startNode, startNode.pathCost())
    visited = 0

    while True:
        if Q.isEmpty():
            print('Solution is not possible, goal state is not achievable from the given problem state.')
            return "sol not found"

        node = Q.pop()
        visited += 1

        if node.goalTest():
            return "Solution found"

        if str(node.state) not in closed:
            closed.add(str(node.state))
            for childNode in node.getSuccessors(heuristic):
                Q.push(childNode, childNode.pathCost())


# Text menu in Python
def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Blocks World")
    print("2. Water Jug")
    print("3. Exit")
    print(67 * "-")


loop = True

while loop:
    print_menu()
    choice = int(input("Enter your choice [1-3]: "))

    if choice == 1:
        print("Blocks World has been selected")

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

        print("Initial State:", startSt)
        print("Goal State:", finalSt)


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

            # def getSuccessors(self, heuristic):
            #     children = []
            #     for i, stack in enumerate(self.state):
            #         if not stack:
            #             continue
            #         for j in range(len(self.state)):
            #             if i != j:
            #                 new_state = copy.deepcopy(self.state)
            #                 block = new_state[i].pop()
            #                 new_state[j].append(block)
            #                 child = NodeBlocks(new_state, self.goal_state, parent=self)
            #                 children.append(child)
            #     return children

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
                for i in list(reversed(path_back)):
                    print(i)

            def pathCost(self):
                return self.heuristics() + self.cost


        aStarSearch(NodeBlocks(startSt, finalSt), lambda state: 0)

    elif choice == 2:
        print("Water Jug has been selected")

        data1 = int(input("Liters/Gallons in Jug 1: "))
        data2 = int(input("Liters/Gallons in Jug 2: "))
        while data1 < 0 or data2 < 0:
            print("Please enter positive numbers only.")
            data1 = int(input("Liters/Gallons in Jug 1: "))
            data2 = int(input("Liters/Gallons in Jug 2: "))
        t = (data1, data2)


        def getSuccessorsWater(J1, J2):
            successors = []
            (C1, C2) = t

            if J1 < C1:
                successors.append(((C1, J2), 'Fill Jug 1', 1))
            if J2 < C2:
                successors.append(((J1, C2), 'Fill Jug 2', 1))
            if J1 > 0:
                successors.append(((0, J2), 'Empty Jug 1', 1))
            if J2 > 0:
                successors.append(((J1, 0), 'Empty Jug 2', 1))

            if J1 + J2 <= C1:
                alpha = J1 + J2
                successors.append(((alpha, 0), 'Pour all from Jug 2 into Jug 1', 1))
            if J1 + J2 <= C2:
                alpha = J1 + J2
                successors.append(((0, alpha), 'Pour all from Jug 1 into Jug 2', 1))
            if J1 + J2 > C1:
                alpha = J1 + J2 - C1
                successors.append(((C1, alpha), 'Fill Jug 1 from Jug 2', 1))
            if J1 + J2 > C2:
                alpha = J1 + J2 - C2
                successors.append(((alpha, C2), 'Fill Jug 2 from Jug 1', 1))

            return successors


        def waterHeuristic(state):
            return abs(state[0] - 2)


        class NodeWater:
            def __init__(self, state, path, cost=0, heuristic=0):
                self.state = state
                self.path = path
                self.cost = cost
                self.heuristic = heuristic

            def getSuccessors(self, heuristicFunction=None):
                children = []
                for successor in getSuccessorsWater(self.state[0], self.state[1]):
                    state = successor[0]
                    path = list(self.path)
                    path.append(successor[1])
                    cost = self.cost + successor[2]
                    if heuristicFunction:
                        heuristic = heuristicFunction(self.state)
                    else:
                        heuristic = 0
                    node = NodeWater(state, path, cost, heuristic)
                    children.append(node)
                return children

            def pathCost(self):
                return self.cost + self.heuristic

            def goalTest(self):
                if self.state[0] == 2:
                    print(self.path)
                    return True
                else:
                    return False


        aStarSearch(NodeWater((0, 0), [], 0, 0), waterHeuristic)

    elif choice == 3:
        print("Exit has been selected")
        loop = False  # End the while loop

    else:
        input("Wrong option selection. Enter any key to try again..")
