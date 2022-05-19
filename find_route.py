# Author: Lucia Saldana Barco

from platform import node
import sys
import math

# Checks that the program was called properly (correct files and order of arguments)
if len(sys.argv) != 4:
    print("usage: find_route.py input_filename.txt origin_city destination_city")
    exit(-1)

# Command-line arguments
input_filename = sys.argv[1]
origin_city = sys.argv[2]
destination_city = sys.argv[3]

# Dictionary representation of tree
tree = {}
# Input File
input_file = None



# PARSER: 
# Takes in a graph (input file)
def parser():
    input_file = open(input_filename, 'r')
    has_more_lines = True
    
    while has_more_lines == True:
        road = input_file.readline()
        if road == "END OF INPUT\n" or road == "END OF INPUT":
            has_more_lines = False
        else:
            # Splits each road/edge into components
            # Format of road (input line): origin destination distance
            origin = road.split(" ")[0]
            destination = road.split(" ")[1]
            if "\n" in road:
                distance = road.split(" ")[2][:road.split(" ")[2].index("\n")] # Removes "\n" at the end
            else:
                distance = road.split(" ")[2]
            tree_generator(origin, destination, distance) # Passes the processed edge so that it can be added to the tree



# TREE GENERATOR: adds road to the tree dictionary
def tree_generator(origin, destination, distance):
    # Include direction: origin -> destination
    if origin in tree:
        tree[origin].append([destination, int(distance)])
    else: # This road is the first one that goes through origin
        tree[origin] = [[destination, int(distance)]]

    # Include direction: destination -> origin
    if destination in tree:
        tree[destination].append([origin, int(distance)])
    else: # This road is the first one that goes through destination
        tree[destination] = [[origin, int(distance)]]



# NODE CLASS:
# Objects of this class are the data structures that represent a tree node
# A node keeps track of pointers to its parent and children nodes
class Node:
    def __init__(self, name, parent, distance_from_parent, depth):
        self.name = name
        self.parent = parent
        self.distance_from_parent = distance_from_parent
        self.depth = depth
        self.total_distance = 0
        self.children = []

    def update_total_distance(self, distance):
        self.total_distance = distance

    def add_child(self, Node):
        self.children.append(Node)



# HEURISTIC FUNCTION:
# Gets called to determine how many cities the algorithm should explore 
# before determining that there is no solution
def heuristic_function():
    return math.ceil(152.955 * math.log(0.00131804 * len(tree.keys()) + 1.87754) - 91.0284)



# UNIFORM COST SEARCH ALGORITHM:
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
def uniform_cost_search():
    current_node = Node(origin_city, None, 0, 0) # current node
    children = tree[current_node.name].copy() # children of current node (taken from tree dictionary)
    ancestors = [] # names of current node's ancestors

    queue = [] # Queue
    queue.append(current_node)

    # Flow control variables
    minimum_distance = float('inf') # current smallest distance found between origin and destination
    solution = None # current destination node with smallest distance
    stop = False # True if heuristic function says algorithm should stop
    
    
    if origin_city == destination_city: # default: is origin the same as destination?
        solution = "equal"
        stop = True

    # Executes while heuristic function says to keep exploring cities
    while len(queue) != 0 and stop == False:
        
        # Get current_node's ancestors
        ancestors.clear()
        current_ancestor = current_node.parent
        while current_ancestor != None:
            ancestors.append(current_ancestor.name)
            current_ancestor = current_ancestor.parent

        # Stop if we have explored the number of cities that the heuristic allows
        if len(ancestors) >= heuristic_function():
            stop = True

        # If we have reached the destination, check if this path was better than the one previously found
        if (current_node.name == destination_city) and (current_node.total_distance < minimum_distance):
            minimum_distance = current_node.total_distance # If it is better -> update
            solution = current_node

        # Create child nodes avoiding repeats
        for child in children:
            if child[0] not in ancestors:
                new_child = Node(child[0], current_node, child[1], current_node.depth + 1)
                new_child.update_total_distance(current_node.total_distance + child[1])
                current_node.add_child(new_child)

        # Push children onto the queue in ascending order
        # This is where the uniform cost search part comes in (explore those with smallest cost first)
        child_list_copy = current_node.children.copy()
        while len(child_list_copy) != 0:
            min_node = min(child_list_copy, key=lambda child: child.total_distance)
            queue.append(min_node)
            child_list_copy.remove(min_node)

        # Update variables for next element in the queue
        queue.pop(0)
        if len(queue) != 0:
            current_node = queue[0]
        children = tree[current_node.name].copy()

    return solution
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~



# PRINT ROUTE:
# Prints the total distance and route between origin_city and destination_city
def print_route(solution):
    if solution == None: # No route exists between the two input cities
        print("distance: infinity")
        print("route:")
        print("none")
    elif solution == "equal": # origin_city and destination_city are the same
        print("distance: 0 km")
        print("route:")
        print(origin_city + " to " + destination_city + ", 0 km")
    else: # At least one route exists
        print("distance: " + str(solution.total_distance) + " km")
        print("route:")
        node = solution
        # The code below back-tracks through the nodes to get steps of route
        road_list = []
        while node.name != origin_city:
            road_list.insert(0, node.parent.name + " to " + node.name + ", " + str(node.distance_from_parent) + " km")
            node = node.parent
        # Prints route in order
        for step in road_list:
            print(step)



##########################################
# RUNNER / FUNCTION CALLS:
parser()
solution = uniform_cost_search()
print_route(solution)
# The End :)
##########################################