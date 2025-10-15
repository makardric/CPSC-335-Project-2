# Student Name: Richard Cam
# Titan Email: rccam@csu.fullerton.edu
# Project: CPSC 335 – Interactive Campus Navigation System
# Date:

# Map the CSUF buildings as nodes in a graph, be able to use BFS and DFS
# to demonstrate paths between certain buildings

# Figure out how to map nodes onto screen
# Make the adjacency table, probably
# Get user input on their starting building and where they want to go 


from tkinter import *
import matplotlib
from collections import deque



def bfs_shortest_paths(graph, start):
    dist = {v: float('inf') for v in graph}
    parent = {v: None for v in graph}
    visited = set()
    q = deque([start])
    visited.add(start)
    dist[start] = 0
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:

            if v not in visited:
                visited.add(v)
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
        
    return dist, parent, order

def reconstruct_path(parent, start, target):
    rev_path = []
    cur = target
    while cur is not None:
        rev_path.append(cur)
        if cur == start:
            break
        cur = parent.get(cur,None)
    if not rev_path or rev_path[-1] != start:
        return []
    return list(reversed(rev_path))


#Directed Acyclic Graph (DAG)
def dfs_cycle_and_topo(graph):
    color = {v: 0 for v in graph}
    postorder = []
    has_cycle = False

    def visit(u):
        nonlocal has_cycle
        color[u] = 1
        for v in graph[u]:
            if color[v] == 0:
                visit(v)
            elif color[v] == 1:
                has_cycle = True
            color[u] = 2
            postorder.append(u)

    for node in graph:
        if color[node] == 0:
            visit(node)
    if has_cycle:
        return True, []
    
    topo = list(reversed(postorder))

    return False, topo

campus = {}
while True:
    new_building = input("What building would you like to add?: ")
    if new_building not in campus:
        campus[new_building] = []
    if len(campus) > 1:
        print("What buildings would you like to connect?")
        buildingOne = input("First building: ")
        buildingTwo = input("Second building: ")
        # connected_buildings = connected_buildings.split(",")  # e.g., "Library, Gym" -> ["Library", "Gym"]

    
        if buildingOne and buildingTwo in campus:
            if buildingOne not in campus[buildingTwo]:
                campus[buildingTwo].append(buildingOne)

            if buildingTwo not in campus[buildingOne]:
                campus[buildingOne].append(buildingTwo)
        else:
            campus[buildingOne] = []
            campus[buildingTwo] = [] 

    print(campus)

    exit_loop = input("Exit loop? (Yes/No): \n")
    if exit_loop.lower() == "yes":
        break
    


# #Demo BFS Function

# campus = {
#     "CS": ["LIB", "GYM"],
#     "LIB": ["CS", "CAFE"],
#     "GYM": ["CS", "CAFE"],
#     "CAFE": ["LIB", "GYM"],
# }
dist, parent, order = bfs_shortest_paths(campus, "CS")
print("BFS order from CS:", order)
path = reconstruct_path(parent, "CS", "CAFE")
print("Shortest (fewer hops) path CS -> CAFE:", path)



# #Demonstration of DFS
# prereq_dag = {
#     "CS1": ["CS2"],
#     "CS2": ["ALGO"],
#     "MATH": ["ALGO"],
#     "ALGO": [],
# }
# has_cycle, topo = dfs_cycle_and_topo(prereq_dag)
# print("Cycle in prereque_dag?", has_cycle)
# print("One Valid couse order:", topo)

# cyclic = {
#     "A": ["B"],
#     "B": ["C"],
#     "C": ["A"],
# }

# cyc, topo2 = dfs_cycle_and_topo(cyclic)
# print("Cycle in Cyclic?", cyc)
# print("Topo for Cyclic (should be empty):", topo2)