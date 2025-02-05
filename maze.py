import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):    
        self.frontier.append(node)



    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop(0)
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename=None):
    
    # Read the maze from a file
        with open(filename) as f:
            contents = f.read()

        # Validate start goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal point")
        
        # Determine height and width of the Maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        # Keep track of walls, start, and goal
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col: 
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        
    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)), 
            ("down", (row, col - 1)), 
            ("left",(row + 1, col)), 
            ("right", (row, col + 1))
        ]
        
        results = []
        for action, (next_row, next_col) in candidates:
            if 0 <= next_row < self.height and 0 <= next_col < self.width and not self.walls[next_row][next_col]:
                results.append((action, (next_row, next_col)))
        return results

    def solve(self):
        """"Finds a solution to maze, if one exists. """
    
        # Keep track of number os states explored
        self.num_explored = 0
        
        # Initialize frontier to the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no solution
            if frontier.empty():
                raise Exception("No solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If the node is the goal, then we're done!
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return actions

            # Add the node to the explored set
            self.explored.add(node.state)

            # Add neighbors to the frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state, node, action)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2
        no_of_cells_x = self.width
        no_of_cells_y = self.height

        # Create a blank canvas
        img = Image.new(
            'RGBA', (cell_size * no_of_cells_x, cell_size * no_of_cells_y), 'black')
        

        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if show_solution else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col: 
                    fill = (40,40,40)
                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (240, 235, 113)

                # Explored
                elif show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    [(j * cell_size + cell_border, i * cell_size + cell_border),
                     ((j+1 )* cell_size  - cell_border,
                      (i+1) * cell_size  - cell_border)],
                    fill=fill)
            
            img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving:...")
m.solve()
print("States explored",m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)