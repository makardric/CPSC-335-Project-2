# Student Name: Richard Cam
# Titan Email: rccam@csu.fullerton.edu
# Project: CPSC 335 – Interactive Campus Navigation System
# Date:

# Map the CSUF buildings as nodes in a graph, be able to use BFS and DFS
# to demonstrate paths between certain buildings

# Figure out how to map nodes onto screen
# Make the adjacency table, probably
# Get user input on their starting building and where they want to go 


import tkinter as tk
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



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


def foo():
    print("yay")


def makeGraph():
    ax.clear()

    # Add new nodes and edges
    for i in nodes:
        G.add_node(i)
    for edge in graph_edges.values():
        G.add_edge(edge[0], edge[1])

    # if len(G.nodes) > 0:
    #     # If pos is empty (first time), generate positions for all nodes
    #     if not pos:
    #         pos.update(nx.spring_layout(G))
    #     else:
    #         # Only compute positions for new nodes, keep old nodes fixed
    #         new_nodes = [n for n in G.nodes() if n not in pos]
    #         if new_nodes:
    #             new_pos = nx.spring_layout(G, pos=pos, fixed=pos.keys())
    #             pos.update(new_pos)

    nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold', ax=ax)

    canvas.draw()


def updateGraph():
    input = addBuildingText.get("1.0", 'end-1c').upper()
    if not input:
        return
    if input in nodes:
        print("Building already exists.")
        return

    nodes.append(input)
    print(nodes)
    makeGraph()

def createEdge():
    global edge_counter
    connect_buildings = [b.strip().upper() for b in addEdgeBuildingsText.get("1.0", 'end-1c').split(',')] 
    
    if len(connect_buildings) != 2:
        print("Please input 2 valid buildings")
        return
    
    a, b = connect_buildings
    
    try:
        edgeDistance = int(addEdgeDistanceText.get("1.0", 'end-1c'))
        edgeTime = int(addEdgeTimeText.get("1.0", 'end-1c'))
    except ValueError:
        print("Please input a valid number for distances and or time")

    if a not in nodes or b not in nodes:
        print(f"One or both buildings ({a}, {b}) do not exist.")
    
    for edges in graph_edges.values():
        if set(edges) == {a, b}:
            print("This edge already exists.")
            return
        
    graph_edges["edge" + str(edge_counter)] = [a, b]
    makeGraph()
    edge_counter += 1
    print(graph_edges)
    print(f"Current edge weight: {edgeDistance}")
    print(f"Current edge time: {edgeTime}")



nodes = []
graph_edges = {}


# initialize main window
main_window = tk.Tk()

    



# window size and title of window
main_window.geometry("1200x1000")
main_window.title("Graph Visualization")
# main_window.configure(bg = "AntiqueWhite2")


# frame initilization
header_frame = tk.Frame(main_window, pady= 20)
header_frame.pack()

header_text = tk.Label(header_frame, text = "Interactive Campus Visualization", font = ("Arial", 24))
header_text.pack()

main_frame = tk.Frame(main_window, pady= 5)

# main frame for buttons/inputs
building_frame = tk.Frame(main_frame, pady = 5)
building_frame.pack()


# frame for creating a button / node
building_button_left_frame = tk.Frame(building_frame, pady= 5)
building_button_left_frame.pack(side="left", padx=5, pady=5)


# addBuildingInput = tk.Text(main_window, text = "What building would you like to insert?")
addBuildingText = tk.Text(building_button_left_frame, height = 1, width = 20)
addBuildingText.pack(side=tk.TOP)




building_button_right_frame = tk.Frame(building_frame, pady= 5)
building_button_right_frame.pack(side="left", padx=5, pady=5)



addBuildingButton = tk.Button(building_button_right_frame, text = "Add Building", command = updateGraph, height = 1, width = 20)
addBuildingButton.pack()




# frame for creating an edge
edge_outer_frame = tk.Frame(main_frame)
edge_outer_frame.pack()

# frame for text boxes on left for edge buildings/weight/accessibility
edge_button_left_frame = tk.Frame(edge_outer_frame, pady= 5)
edge_button_left_frame.pack(side="left", padx=5, pady=5)

# buttons to customize edges
addEdgeBuildingsText = tk.Text(edge_button_left_frame, height = 1, width = 20)
addEdgeDistanceText = tk.Text(edge_button_left_frame, height = 1, width = 20)
addEdgeTimeText = tk.Text(edge_button_left_frame, height = 1, width = 20)
addEdgeAccessible = tk.Checkbutton(edge_button_left_frame, text = "Accessible", height = 1, width = 20)

addEdgeBuildingsText.pack(side = tk.TOP)
addEdgeDistanceText.pack(side = tk.TOP)
addEdgeTimeText.pack(side = tk.TOP)
addEdgeAccessible.pack(side = tk.TOP)


# frame for edge create button on the right
edge_button_right_frame = tk.Frame(edge_outer_frame, pady= 5)
edge_button_right_frame.pack(side="left", padx=5, pady=5)

# button to create edge
addEdgeBuildingButton = tk.Button(edge_button_right_frame, text = "Create Edge", command = createEdge, height = 3, width = 20)
addEdgeBuildingButton.pack()

main_frame.pack()

generateGraphButton = tk.Button(main_window, text = "Make Graph", command = makeGraph)


generateGraphButton.pack(pady=5)



G = nx.Graph()
pos = {}
edge_counter = 0

fig = Figure(figsize = (5,5))
ax = fig.add_subplot(111)
ax.axis('off')
canvas = FigureCanvasTkAgg(fig, master=main_window)
canvas.get_tk_widget().pack(pady=20)







# main window loop
main_window.mainloop()