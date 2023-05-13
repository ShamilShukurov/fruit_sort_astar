from queue import PriorityQueue


def find_nearest_goal_state(state: list) -> list:
    """
    Finds the nearest goal state to the given state out of 6 
    possible goal state according to Manhattan distance. 6 possible states are:
        1.Apples in ascending order, followed by oranges and then bananas
        2.Bananas in ascending order, followed by apples and then oranges
        3.Bananas in ascending order, followed by oranges and then apples
        4.Oranges in ascending order, followed by apples and then bananas
        5.Oranges in ascending order, followed by bananas and then apples
    Args:
        state (list): A list representing the current state of the fruit grid, where each element is a string
                      representing a fruit ("a1" to "a10" for apples, "b1" to "b10" for bananas, and "c1" to "c10"
                      for oranges).
        
    Returns:
        list: The nearest goal state to the given state.
    """
    # Create all the possible goal states

    a = [f"a{i}" for i in range(1, 11)]
    b = [f"b{i}" for i in range(1, 11)]
    c = [f"c{i}" for i in range(1, 11)]
    possible_goal_states = [
        a + b + c, b + a + c, b + c + a, c + b + a, c + a + b, a + c + b
    ]

    # Calculate the Manhattan distance from the current state to each possible goal state
    distances = []
    for goal_state in possible_goal_states:
        distance = 0
        for i, fruit in enumerate(state):
            row = i // 10
            col = i % 10
            goal_row = goal_state.index(fruit) // 10
            goal_col = goal_state.index(fruit) % 10
            distance += abs(row - goal_row) + abs(col - goal_col)
        distances.append(distance)
    # Find the nearest goal state and return it
    nearest_index = distances.index(min(distances))
    return possible_goal_states[nearest_index]


def heuristic(state, goal_state):
    """
    Calculates an estimate of the distance between the given state and the target state.
    This heuristic function uses the Manhattan distance between each fruit in the state and its position
    in the target state as the estimate of the distance.

    Args:
        state (list): A list representing the current state of the fruit grid, where each element is a string
                      representing a fruit ("a1" to "a10" for apples, "b1" to "b10" for bananas, and "c1" to "c10"
                      for oranges).
        goal_state (list): A list representing the target/goal state of the fruit grid, where each element is a
                             string representing a fruit in the same format as the state list.

    Returns:
        int: An estimate of the distance between the given state and the target state, based on the Manhattan distance
             between each fruit in the state and its position in the target state.
    """
    h = 0
    for i, fruit in enumerate(state):
        row = i // 10
        col = i % 10
        goal_row = goal_state.index(fruit) // 10
        goal_col = goal_state.index(fruit) % 10
        h += abs(row - goal_row) + abs(col - goal_col)
    return h


# define A* algorithm
def astar(initial_state):
    """
    A* algorithm to solve the fruit sorting problem.
    Args:
        initial_state: a list representing the initial state of the problem
    Returns:
        A tuple containing the goal state and the cost to reach it.
    """
    # Find the nearest goal state to the initial state
    goal_state = find_nearest_goal_state(initial_state)

    # Initialize the visited set and the priority queue
    visited = []
    queue = PriorityQueue()

    # Put the initial state into the priority queue with its estimated cost and actual cost both equal to 0
    queue.put((heuristic(initial_state, goal_state), 0, initial_state))

    while not queue.empty():
        # Get the state with the lowest estimated cost from the priority queue
        _, cost, state = queue.get()

        # If the state is the goal state, return the goal state and the cost
        if state == goal_state:
            return state, cost

        # If the state has already been visited, skip it
        if state in visited:
            continue

        # Mark the state as visited
        visited.append(state)

        # Generate all possible neighbors by swapping adjacent fruits, and add them to the priority queue if they haven't been visited
        for i in range(30):
            if i % 10 < 9:
                # swap with neighbor to the right
                neighbor = state[:]
                neighbor[i], neighbor[i + 1] = neighbor[i + 1], neighbor[i]
                if neighbor not in visited:
                    queue.put((heuristic(neighbor, goal_state) + cost + 1,
                               cost + 1, neighbor))
            if i < 20:
                # swap with neighbor below
                neighbor = state[:]
                neighbor[i], neighbor[i + 10] = neighbor[i + 10], neighbor[i]
                if neighbor not in visited:
                    queue.put((heuristic(neighbor, goal_state) + cost + 1,
                               cost + 1, neighbor))


# example input 3x10 array
#(I represented it as list but further improvements can be done to make it work with other formats like np.array or list of lists)
initial_state = [
    'a9', 'a2', 'c4', 'c5', 'b3', 'a1', 'a6', 'c8', 'a10', 'a7', 'b5', 'c1',
    'c2', 'a3', 'a4', 'a8', 'b6', 'b7', 'b9', 'c10', 'c3', 'b2', 'b1', 'b4',
    'a5', 'c6', 'c7', 'b8', 'b10', 'c9'
]

# solve using A* algorithm
solution, repl = astar(initial_state)

#Print results
for i in range(10):
    print(solution[i], solution[i + 10], solution[i + 20])
print("=================")
print("Moves made: {}".format(repl))
