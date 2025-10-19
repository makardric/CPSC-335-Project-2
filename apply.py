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
    for i in test_data:
        g.add_node(i)

    for edges in test_edges.values():
        g.add_edge(edges[0], edges[1])

    edges = g.edges()
    
    # colors = [g[u][v]['color'] for u,v in edges]
    # weights = [g[u][v]['weight'] for u,v in edges]
    nx.draw(g, with_labels=True, node_color='lightblue', font_weight='bold', ax = ax)

    canvas.draw()
    canvas.get_tk_widget().pack()

    # plt.show()

def updateGraph():
    pass

def createEdge():
    pass


test_data = ["CS", "Library", "Cafe"]
test_edges = {"edge1" : ["CS", "Library"], "edge2" : ["Library", "Cafe"]}


# initialize main window
main_window = tk.Tk()

    



# window size and title of window
main_window.geometry("1200x800")
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
addEdgeWeightText = tk.Text(edge_button_left_frame, height = 1, width = 20)
addEdgeAccessible = tk.Checkbutton(edge_button_left_frame, text = "Accessible", height = 1, width = 20)

addEdgeBuildingsText.pack(side = tk.TOP)
addEdgeWeightText.pack(side = tk.TOP)
addEdgeAccessible.pack(side = tk.TOP)


# frame for edge create button on the right
edge_button_right_frame = tk.Frame(edge_outer_frame, pady= 5)
edge_button_right_frame.pack(side="left", padx=5, pady=5)

# button to create edge
addEdgeBuildingButton = tk.Button(edge_button_right_frame, text = "Create Edge", command = createEdge, height = 3, width = 20)
addEdgeBuildingButton.pack()



generateGraphButton = tk.Button(main_window, text = "Make Graph", command = makeGraph)


generateGraphButton.pack(pady=5)

main_frame.pack()

g = nx.Graph()

fig = Figure(figsize = (5,5))
ax = fig.add_subplot(111)
ax.axis('off')
canvas = FigureCanvasTkAgg(fig, master=main_window)
canvas.get_tk_widget().pack(pady=20)


# main window loop
main_window.mainloop()