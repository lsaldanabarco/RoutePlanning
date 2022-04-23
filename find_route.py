# Author: Lucia Saldana Barco

from platform import node
import sys
import math

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


# Parser
def parser():
    input_file = open(input_filename, 'r')
    has_more_lines = True
    
    while has_more_lines == True:
        road = input_file.readline()
        if road == "END OF INPUT\n":
            has_more_lines = False
        else:
            # Format of road (input line): origin destination distance
            origin = road.split(" ")[0]
            destination = road.split(" ")[1]
            distance = road.split(" ")[2][:road.split(" ")[2].index("\n")] # Removes "\n" at the end
            tree_generator(origin, destination, distance)



# Tree Generator: adds a road to the tree
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



def breadth_first_search(origin_city, destination_city):
    # CURRENT CITY AND CHILDREN VARIABLES
    current_city = origin_city
    children = tree[origin_city].copy()
    # QUEUE VARIABLES
    path_cost = 0
    depth = 0
    # For reference: 
    # queue[*] is a node where * is an index
    # queue[*][0] = city name
    # queue[*][1] = path_cost to get to this city from origin_city
    # queue[*][2] = depth of node
    # queue[*][3] = route to get to this city from origin_city
    queue = [[origin_city, path_cost, depth]] # initialized to origin_city node (no route)
    # SOLUCTION VARAIABLE
    solution = [float('inf'), []] # stores [path_cost, route] where route = [[step1], [step2], ..., [stepN]]
    
    # The two input cities are the SAME
    if origin_city == destination_city:
        solution = [0, [[origin_city + " to " + destination_city, 0]]]
        return solution
    # The two input cities are DIFFERENT
    heuristic_result = heuristic()
    print(tree)
    while queue[0][2] <= 9: # While depth of current city is less than heuristic result
        if len(children) != 0: # If current_city has children
            # Add children to queue
            for node in children:
                queue.append(node.copy())
                queue[-1][1] = path_cost + queue[-1][1]  # child's TOTAL path cost = (parent's path_cost) + (distance between parent and child)
                queue[-1].append(queue[0][2] + 1) # child's depth = parent's depth + 1
                if len(queue[0]) != 4: # If current_city is origin_city (i.e. does not have a fourth element/route)
                    queue[-1].append([[current_city + " to " + queue[-1][0], queue[-1][1]]]) # append first step in route
                else:
                    queue[-1].append([])
                    for step in queue[0][3]: # append all previous steps in route
                        queue[-1][3].append(step)
                    queue[-1][3].append([current_city + " to " + queue[-1][0], queue[-1][1] - queue[0][1]]) # append new step in route
            # Update variables for next element in the queue
            queue.pop(0)
            current_city = queue[0][0]
            children = tree[queue[0][0]].copy()
            path_cost = queue[0][1]
            # If the new queue[0] is the destination city, update solution
            if(current_city == destination_city):
                print(queue[0])
                if path_cost < solution[0]:
                    print("\n")
                    solution[0] = path_cost
                    solution[1] = queue[0][3]
    return solution



# Heuristic function to put a limit on the depth of the tree
def heuristic():
    #7.785112595\cdot\log\left(x\right)-4.29362608478
    count = 0
    for key in tree:
        count = count + len(tree[key])
    average = count / len(tree.keys()) # Average number of children per parent
    result = math.ceil(len(tree.keys()) / average) # Heuristic
    print(result)
    return result



# Prints Output (distance and route between origin_city and destination_city)
def print_route(solution):
    if solution[0] == float('inf'): # No route exists between the two input cities
        print("distance: infinity")
        print("route:")
        print("none")
    else:
        print("distance: " + str(solution[0]) + " km")
        print("route:")
        for step in solution[1]:
            #print(solution[1])
            #print(step)
            #print(step[0])
            #print(step[1])
            print(step[0] + ", " + str(step[1]) + " km")



# Code Runner
parser()
solution = breadth_first_search(origin_city, destination_city)
print_route(solution)
# The End :)