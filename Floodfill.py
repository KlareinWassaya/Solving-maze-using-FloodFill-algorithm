from Algorithm import *
import API

# Floodfill algorithm for solving mazes, by imagining the maze as a grid of cells. 
# Each cell is given a number that shows how far it is from the goal, 
# as defined in the MAZE_SETTINGS , the goal is given 0. 
# Starting from the robot's position, look for the cell with the smallest number next to it, 
# move to that cell and repeat until the goal is reached. 
# Floodfill helps in finding the shortest path by following numbers towards the goal.
class FloodFill(Algorithm):

    def execute(self):

        API.log("FLOODFILL RUNNING...")

        #  0 > up, 1 > right,  2 > down, 3 > left
        orientation = 0
        current_position = [0, 0]  # start point

        nodes_since_last_decision = []  # stack
        last_decision_node = []

        # As long as the goal is not reached, keep moving
        while MAZE_SETTINGS[current_position[0]][current_position[1]] != 0:

            # Give values for each cell in the maze
            self.update_maze_values()

            # Colour the path, that the mouse move in, in blue
            API.setColor(current_position[1], current_position[0], 'B')

            row, col = current_position
            front_wall = API.wallFront()
            right_wall = API.wallRight()
            left_wall = API.wallLeft()

            # The neighbouring cells (Forward, Right, Left)
            neighbouring_nodes = [(), (), ()]
            neighbouring_values = [float("inf"), float("inf"), float("inf")]  # Around blocks that can be visited

            # Check for the walls around
            self.check_walls_around(front_wall, left_wall, right_wall, col, neighbouring_nodes, orientation, row,
                                    neighbouring_values)

            # If this node has been visited before, update the nodes visited since the last decision
            is_visited_node = last_decision_node and (row, col) in last_decision_node
            if is_visited_node:  # visited
                self.update_previously_visited_nodes(col, nodes_since_last_decision, row)

            # If a dead end is reached, return to your original spot
            dead_end = left_wall and right_wall and front_wall
            if dead_end:
                orientation = self.turn_back(col, current_position, nodes_since_last_decision, orientation, row)
                continue

            # Find the neighbour with the least value to move to it
            lowest_neighbor = min(neighbouring_values)
            orientation = self.choose_lowest_neigbour(col, current_position, lowest_neighbor, nodes_since_last_decision,
                                                      orientation, row, neighbouring_values)

            cross_road = (not left_wall and not right_wall) or (not left_wall and not front_wall) or (
                    not front_wall and not right_wall)

            if cross_road:
                # Mouse is making a new decision, so we update our arrays to reflect that
                self.update_decision_nodes(col, last_decision_node, nodes_since_last_decision, row)

        # If the gol is reached
        API.log("FINISHED!!")

    # Take a decision to where to move
    def update_decision_nodes(self, col, last_decision_node, nodes_since_last_decision, row):
        nodes_since_last_decision.append([])
        if (row, col) not in last_decision_node:  # If this node has never been visited before
            last_decision_node.append((row, col))
            
    # Update the values for visited nodes
    def update_previously_visited_nodes(self, col, nodes_since_last_decision, row):
        previous_node = (row, col)
        for node in nodes_since_last_decision[-2]:  # top of stack
            MAZE_SETTINGS[node[0]][node[1]] = MAZE_SETTINGS[previous_node[0]][previous_node[1]] + 1  # cost + 1
            previous_node = (node[0], node[1])

    # Choose the neighbour with the least value
    def choose_lowest_neigbour(self, col, current_position, lower_neighbor, nodes_since_last_decision, orientation, row,
                               neighbouring_nodes):
        if lower_neighbor == neighbouring_nodes[0]:
            # If the neighbour in front of the mouse has the least value, move forward
            API.moveForward()
            for nodesSince in nodes_since_last_decision:
                nodesSince.append((row, col))

            # Updating position based on orientation
            if orientation == 0:
                current_position[0] += 1
            elif orientation == 1:
                current_position[1] += 1
            elif orientation == 2:
                current_position[0] -= 1
            elif orientation == 3:
                current_position[1] -= 1


        elif lower_neighbor == neighbouring_nodes[1]:  # if least value is Right of mouse
            # If the neighbour to the right of the mouse has the least value, turn right and move forward
            API.turnRight()
            API.moveForward()
            for nodesSince in nodes_since_last_decision:
                nodesSince.append((row, col))

            # Updating position and orientation based on orientation
            if orientation == 0:
                current_position[1] += 1
                orientation = 1

            elif orientation == 1:
                current_position[0] -= 1
                orientation = 2

            elif orientation == 2:
                current_position[1] -= 1
                orientation = 3

            elif orientation == 3:
                current_position[0] += 1
                orientation = 0

        elif lower_neighbor == neighbouring_nodes[2]:
            # If the neighbour to the left of the mouse has the least value, turn right and move forward
            API.turnLeft()
            API.moveForward()
            for nodesSince in nodes_since_last_decision:
                nodesSince.append((row, col))

            # Updating position and orientation based on orientation
            if orientation == 0:
                current_position[1] -= 1
                orientation = 3

            elif orientation == 1:
                current_position[0] += 1
                orientation = 0

            elif orientation == 2:
                current_position[1] += 1
                orientation = 1

            elif orientation == 3:
                current_position[0] -= 1
                orientation = 2
        return orientation

    # Function to move backward when reaching a dead end
    def turn_back(self, col, current_position, nodes_since_last_decision, orientation, row):
        API.turnRight()
        API.turnRight()
        API.moveForward()
        for nodesSince in nodes_since_last_decision:  # push move to stack
            nodesSince.append((row, col))
        # Updating position and orientation based on orientation
        if orientation == 0:
            current_position[0] -= 1
            orientation = 2
        elif orientation == 1:
            current_position[1] -= 1
            orientation = 3
        elif orientation == 2:
            current_position[0] += 1
            orientation = 0
        elif orientation == 3:
            current_position[1] += 1
            orientation = 1
        return orientation

    # Function to spot the walls
    def check_walls_around(self, front_wall, left_wall, right_wall, col, neighbouring_nodes, orientation, row, neighbouring_values):

        # The wall is not in the front
        if not front_wall:
            if orientation == 0:
                front_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[0] = (row + 1, col)
            elif orientation == 1:
                front_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[0] = (row, col + 1)
            elif orientation == 2:
                front_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[0] = (row - 1, col)
            elif orientation == 3:
                front_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[0] = (row, col - 1)
            neighbouring_values[0] = front_val
        # The wall is not to the right
        if not right_wall:
            if orientation == 0:
                right_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[1] = (row, col + 1)
            elif orientation == 1:
                right_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[1] = (row - 1, col)
            elif orientation == 2:
                right_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[1] = (row, col - 1)
            elif orientation == 3:
                right_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[1] = (row + 1, col)
            neighbouring_values[1] = right_val
        # The wall is not to the left
        if not left_wall:
            if orientation == 0:
                left_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[2] = (row, col - 1)
            if orientation == 1:
                left_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[2] = (row + 1, col)
            if orientation == 2:
                left_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[2] = (row, col + 1)
            if orientation == 3:
                left_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[2] = (row - 1, col)
            neighbouring_values[2] = left_val
