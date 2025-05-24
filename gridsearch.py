"""
Grid Search Algorithms (DFS, BFS, A*, Dijkstra)

Copyright (c) 2020 Gabriele Gilardi


Notes
-----
- Written and tested in Python 3.8.5.
- Two-dimensional grid search implementation using Depth First Search, Breath
  First Search, A* algorithm, and Dijkstra's algorithm.
- DFS uses a stack as data structure.
- BFS uses a queue as data structure.
- A* uses a priority queue as data structure and f-values as priority.
- Dijkstra uses a binary heap as data structure and g-values as priority.
- Any offset can be defined but only 1-step motion is allowed.
- Start and goal positions can be changed dynamically.
- Obstacles can be added/removed dynamically.
- Examples of usage are in <test_GridSearch.py>.
- Reference: "Problem Solving with Algorithms and Data Structures", by Miller
  and Ranum.


GridSearch Class
----------------
layout              List of lists with the grid layout.
bound               List of lists with the grid boundaries.
start               Tuple with the start position.
goal                Tuple with the goal position.
offset              List with the offset in each allowed direction.
prob                List with the probabilities of each direction.
__init__()          Initializes the grid object.
show()              Shows the grid layout.
is_valid()          Checks if a position is inside the grid.
set_start()         Sets the start position.
set_goal()          Sets the goal position.
add_obstacle()      Adds an obstacle to the grid.
del_obstacle()      Deletes an obstacle from the grid.
set_motion()        Sets the offset and the corresponding probabilities.
order_dir()         Defines the order in the direction of motion.
get_path()          Returns the path between the start and the goal position.
dfs()               Find the path using depth first search.
bfs()               Find the path using breath first search.
A_star()            Find the path using A* algorithm.
Dijkstra()          Find the path using Dijkstra's algorithm.
"""

import numpy as np
from links import *
from settings import *

class GridSearch:
    """
    Class for grid search algorithms.
    """
    def __init__(self, type, board):
        """
        Initialize the grid object.
        """
        self.board = board
        self.type = type
        self.bound = []
        self.layout = []
        self.path = []
        self.new_path = []
        self.visited = 0
        
        self.open = []
        
        self.i = 0
        self.j = 10
        
        self.runs = 0
        
        for i in range(ROWS):
            sub_list = []
            for j in range(COLS):

                if self.board[i][j].color == BRDR_COLOR:
                    sub_list.append('#')
                else:
                    sub_list.append(' ')
                
                if self.board[i][j].color == START_COLOR:
                    self.start = (i+1, j+1)
                if self.board[i][j].color == STOP_COLOR:
                    self.goal = (i+1, j+1)

            sub_list.insert(0, '*')
            sub_list.append('*')
            self.layout.append(sub_list)

        self.layout.insert(0, ['*' for _ in range(COLS+2)])
        self.layout.append(['*' for _ in range(COLS+2)])

        for i, row in enumerate(self.layout):
            self.bound.append([i for i, x in enumerate(row) if x == "*"])
            if (len(self.bound[i]) <= 1):
                raise SystemExit("\nThe grid bounds are not consistent.")

        self.offset = None
        self.prob = None
        
        self.not_yet_done = True

        # Init
        self.set_motion([(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)])
        self.set_start(self.start[0], self.start[1])
        self.set_goal(self.goal[0], self.goal[1])
    
    def decide(self, type):
        if type == "DFS":
            self.new_path, self.open_size = self.dfs()
        elif type == "AStar":
            self.new_path, self.open_size = self.A_star()
        elif type == "Dijkstra":
            self.new_path, self.open_size = self.Dijkstra()
        elif type == "BFS":
            self.new_path, self.open_size = self.bfs()

    def solve(self):
        if self.not_yet_done:
            self.decide(self.type)

            self.not_yet_done = False
        else:
            self.mark_path(self.new_path)
            
        return (self.visited, self.open_size, len(self.new_path), (str(round(self.runs / FPS * 10) / 10)) + "s")
    
    def mark_path(self, path):
        for i,j in path:
            self.path.append(self.board[i-1][j-1])
        
        if self.path:
            self.path[self.i].color = PATH_COLOR
            self.path[self.j].color = PATH_RUN_COLOR
            
            self.i = self.i + 1
            self.j = self.j + 1
            
            if self.i >= len(self.path):
                self.i = 0
            if self.j >= len(self.path):
                self.j = 0
        
        self.board[self.start[0]-1][self.start[1]-1].color = START_COLOR
        self.board[self.goal[0]-1][self.goal[1]-1].color = STOP_COLOR

    def is_valid(self, row, col):
        """
        Returns <True> if (row, col) is inside the grid. Returns <False> if not.
        """
        max_rows = len(self.bound)

        # Check if <row> is a valid row
        if (row >= max_rows or row <= 0):
            return False

        # Check if <col> is correctly bounded by walls
        if (col > max(self.bound[row]) or col < min(self.bound[row])):
            return False

        # Build the column corresponding to <col> and check if it is valid
        column = []
        for i, k in enumerate(self.bound):
            if (col in k):
                column.append(i)
        if (len(column) <= 1):
            raise SystemExit("\nThe grid bounds are not consistent.")

        # Check if <row> is correctly bounded by walls
        if (row > max(column) or row < min(column)):
            return False

        # Check if the position is a wall
        if (self.layout[row][col] == '*'):
            return False

        return True

    def set_start(self, row, col):
        """
        Sets the start position.
        """
        # Check if it is inside
        if (self.is_valid(row, col)):

            # If present remove the current start position
            if (self.start is not None):
                self.layout[self.start[0]][self.start[1]] = ' '

            # Set the new start position
            self.start = (row, col)
            self.layout[row][col] = 'S'

        # Raise an error if it is outside
        else:
            raise SystemExit("\nThe start position is not valid.")

    def set_goal(self, row, col):
        """
        Sets the goal position.
        """
        # Check if it is inside
        if (self.is_valid(row, col)):

            # If present remove the current goal position
            if (self.goal is not None):
                self.layout[self.goal[0]][self.goal[1]] = ' '

            # Set the new goal position
            self.goal = (row, col)
            self.layout[row][col] = 'G'

        # Raise an error if it is outside
        else:
            raise SystemExit("\nThe goal position is not valid.")

    def add_obstacle(self, row, col):
        """
        Adds an obstacle to the grid.
        """
        # Check if it is inside and add the obstacle
        if (self.is_valid(row, col)):
            self.layout[row][col] = '#'

        # Raise an error if it is outside
        else:
            raise SystemExit("\nThe obstacle position is not valid.")

    def del_obstacle(self, row, col):
        """
        Deletes an obstacle from the grid.
        """
        # Check if it is inside and remove the obstacle
        if (self.is_valid(row, col)):
            self.layout[row][col] = ' '

        # Raise an error if it is outside
        else:
            raise SystemExit("\nthe obstacle position is not valid.")

    def set_motion(self, offset, prob=None):
        """
        Sets the offset and the corresponding probabilities.
        """
        self.offset = offset
        self.prob = prob

    def order_dir(self):
        """
        Returns the direction order using the given probabilities. If no
        probabilities, uses the same order specified as in <self.offset>.
        """
        n = len(self.offset)
        idx = np.arange(n)

        if (self.prob is not None):
            idx = np.random.choice(idx, size=n, replace=False, p=self.prob)

        return idx

    def get_path(self, previous):
        """
        Returns the path between the start and the goal position.
        """
        current = self.goal
        path = []

        # Loop until the start (its predecessor is <None>)
        while (current is not None):
            path.append(current)
            current = previous[current]

        # Reverse the order
        # path.reverse()

        return path

    def dfs(self):
        """
        Returns the path from the start position to the goal position using
        depth first search (DFS). Returns <None> if no solution is found.
        """
        # Initialize the stack
        self.stack = Stack()

        # Add the start point to the stack
        self.stack.push(self.start)
        previous = {self.start: None}
        self.added = 1

        # Loop until the stack is empty
        while (not self.stack.is_empty()):
            
            self.runs += 1
            
            for i,j in self.stack.items:
                self.board[i-1][j-1].color = EDGE_COLOR

            # Get the last position from the stack
            current = self.stack.pop()
            self.board[current[0]-1][current[1]-1].color = CLOSED_COLOR
            self.visited += 1

            # Stop if it is the goal and return the path
            if (current == self.goal):
                path = self.get_path(previous)
                return path, self.stack.size

            # Define the order in the directions
            idx = self.order_dir()

            # Add to the stack the neighbours of the current position
            for direction in idx:

                # Offset values
                row_offset, col_offset = self.offset[direction]

                # Neighbour position
                row_neigh = current[0] + row_offset
                col_neigh = current[1] + col_offset
                neighbour = (row_neigh, col_neigh)

                # If neighbour position is valid and not in the dictionary
                if (self.layout[row_neigh][col_neigh] != '#' and
                    self.layout[row_neigh][col_neigh] != '*' and
                    neighbour not in previous):

                    # Add it to the queue
                    self.stack.push(neighbour)
                    previous[neighbour] = current
                    self.added += 1

        return None

    def bfs(self):
        """
        Returns the path from the start position to the goal position using
        breath first search (BFS). Returns <None> if no solution is found.
        """
        # Initialize the queue
        self.queue = Queue()

        # Add the start point to the queue
        self.queue.enqueue(self.start)
        previous = {self.start: None}
        self.added = 1

        # Loop until the queue is empty
        while (not self.queue.is_empty()):

            self.runs += 1
            
            for i,j in self.queue.items:
                self.board[i-1][j-1].color = EDGE_COLOR

            # Get the last item from the queue
            current = self.queue.dequeue()
            self.board[current[0]-1][current[1]-1].color = CLOSED_COLOR
            self.visited += 1

            # Stop if it is the goal and return the path
            if (current == self.goal):
                path = self.get_path(previous)
                return path, self.queue.size

            # Define the order in the directions
            idx = self.order_dir()

            # Add to the queue the neighbours of the current position
            for direction in idx:

                # Offset values
                row_offset, col_offset = self.offset[direction]

                # Neighbour position
                row_neigh = current[0] + row_offset
                col_neigh = current[1] + col_offset
                neighbour = (row_neigh, col_neigh)

                # If neighbour position is valid and not in the dictionary
                if (self.layout[row_neigh][col_neigh] != '#' and
                    self.layout[row_neigh][col_neigh] != '*' and
                    neighbour not in previous):

                    # Add it to the queue
                    self.queue.enqueue(neighbour)
                    previous[neighbour] = current
                    self.added += 1

        return None

    def A_star(self):
        """
        Returns the path from the start position to the goal position using the
        A-star (A*) algorithm. Returns <None> if no solution is found.
        """

        # Heuristic distance between two positions
        def heuristic(a, b):
            """
            Calculates the Manhattan distance between two positions.
            """
            x1, y1 = a
            x2, y2 = b
            dist = abs(x1 - x2) + abs(y1 - y2)

            return dist

        # Initialize the priority queue
        self.pq = PriorityQueue(queue_type='min')

        # Values for the start point
        g = 0
        h = heuristic(self.goal, self.start)
        f = g + h

        # Add the start point to the priority queue.
        self.pq.put(f, self.start)
        g_values = {self.start: g}
        previous = {self.start: None}
        self.added = 1

        # Loop until the priority queue is empty
        while (not self.pq.is_empty()):
            
            self.runs += 1
            
            for _, cords in self.pq.items:
                if cords != "dummy":
                    self.board[cords[0]-1][cords[1]-1].color = EDGE_COLOR

            # Get the highest priority position from the priority queue
            f, current = self.pq.get()
            self.board[current[0]-1][current[1]-1].color = CLOSED_COLOR
            self.visited += 1

            # Stop if it is the goal and return the path
            if (current == self.goal):
                path = self.get_path(previous)
                return path, self.pq.size

            # Define the order in the directions
            idx = self.order_dir()

            # Add to the priority queue the neighbours of the current position
            for direction in idx:

                # Offset values
                row_offset, col_offset = self.offset[direction]

                # Neighbour position
                row_neigh = current[0] + row_offset
                col_neigh = current[1] + col_offset
                neighbour = (row_neigh, col_neigh)

                # If neighbour position is valid and not in the dictionary
                if (self.layout[row_neigh][col_neigh] != '#' and
                    self.layout[row_neigh][col_neigh] != '*' and
                    neighbour not in previous):

                    # Values (the g-value of all neighbour positions differ
                    # from the g-value of the current position by 1)
                    g = g_values[current] + 1
                    h = heuristic(self.goal, neighbour)
                    f = g + h

                    # Add it to the priority queue
                    self.pq.put(f, neighbour)
                    g_values[neighbour] = g
                    previous[neighbour] = current
                    self.added += 1

        return None

    def Dijkstra(self):
        """
        Returns the path from the start position to the goal position using
        Dijkstra's algorithm (DA). Returns <None> if no solution is found.
        """

        # Initialize the binary heap
        self.bh = BinaryHeap(heap_type='min')

        # Add the start point to the binary heap.
        g = 0
        self.bh.put((g, self.start))
        g_values = {self.start: g}
        previous = {self.start: None}
        self.added = 1

        # Loop until the priority queue is empty
        while (not self.bh.is_empty()):
            
            self.runs += 1

            for value in self.bh.items:
                if value != 0:
                    self.board[value[1][0]-1][value[1][1]-1].color = EDGE_COLOR
                
            # Get the highest priority position from the priority queue
            (g, current) = self.bh.get()
            self.board[current[0]-1][current[1]-1].color = CLOSED_COLOR
            self.visited += 1

            # Stop if it is the goal and return the path
            if (current == self.goal):
                path = self.get_path(previous)
                return path, self.bh.size

            # Define the order in the directions
            idx = self.order_dir()

            # Add to the binary heap the neighbours of the current position
            for direction in idx:

                # Offset values
                row_offset, col_offset = self.offset[direction]

                # Neighbour position
                row_neigh = current[0] + row_offset
                col_neigh = current[1] + col_offset
                neighbour = (row_neigh, col_neigh)

                # If neighbour position is valid and not in the dictionary
                if (self.layout[row_neigh][col_neigh] != '#' and
                    self.layout[row_neigh][col_neigh] != '*' and
                    neighbour not in previous):

                    # Values (the g-value of all neighbour positions differ
                    # from the g-value of the current position by 1)
                    g = g_values[current] + 1

                    # Add it to the priority queue
                    self.bh.put((g, neighbour))
                    g_values[neighbour] = g
                    previous[neighbour] = current
                    self.added += 1

        return None
