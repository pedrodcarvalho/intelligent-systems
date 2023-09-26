import heapq
import itertools

# Define the goal state of the 8-puzzle
GOAL_STATE = (4, 2, 1,
              7, 6, 3,
              0, 8, 5)

# Define the possible moves (up, down, left, right)
MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Function to calculate the Manhattan distance heuristic


def manhattan_distance(state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_row, goal_col = (state[i] - 1) // 3, (state[i] - 1) % 3
            current_row, current_col = i // 3, i % 3
            distance += abs(goal_row - current_row) + \
                abs(goal_col - current_col)
    return distance

# Function to check if a move is valid


def is_valid_move(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Function to generate the successor states


def generate_successors(state):
    successors = []
    blank_index = state.index(0)
    blank_row, blank_col = blank_index // 3, blank_index % 3

    for move in MOVES:
        new_row, new_col = blank_row + move[0], blank_col + move[1]
        if is_valid_move(new_row, new_col):
            new_state = list(state)
            new_blank_index = new_row * 3 + new_col
            new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]
            successors.append(tuple(new_state))

    return successors

# A* search algorithm


def astar_search(initial_state):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (manhattan_distance(
        initial_state), 0, initial_state))
    while open_list:
        _, cost, current_state = heapq.heappop(open_list)
        if current_state == GOAL_STATE:
            return cost
        if current_state in closed_set:
            continue
        closed_set.add(current_state)
        for successor in generate_successors(current_state):
            if successor not in closed_set:
                heapq.heappush(
                    open_list, (cost + 1 + manhattan_distance(successor), cost + 1, successor))
    return float("inf")

# Function to print the puzzle board


def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i], state[i + 1], state[i + 2])


# Main function
if __name__ == "__main__":
    initial_state = (1, 2, 3,
                     4, 0, 5,
                     7, 8, 6)  # Change this to the initial state you want to solve
    print("Initial State:")
    print_puzzle(initial_state)

    cost = astar_search(initial_state)

    if cost != float("inf"):
        print("\nSolution Found!")
        print(f"Total Cost: {cost} moves")
    else:
        print("\nNo solution found.")
