# Student Name: Richard Cam
# Titan Email: rccam@csu.fullerton.edu
# Project: CPSC 335 – Interactive Campus Navigation System
# Date: 10/25/2025

import customtkinter as CTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        cur = parent.get(cur, None)
    if not rev_path or rev_path[-1] != start:
        return []
    return list(reversed(rev_path))


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


def makeGraph():
    ax.clear()
    for i in nodes:
        G.add_node(i)
    for edge in graph_edges.values():
        G.add_edge(edge['a'], edge['b'], 
                   distance=edge['distance'], 
                   time=edge['time'], 
                   accessible=edge['accessible'], 
                   closed=edge['closed'])
    
    pos = nx.spring_layout(G, seed = 5)

    # Separate accessible vs non-accessible edges
    closed_edges = []
    accessible_edges = []
    nonaccessible_edges = []
    for u, v, d in G.edges(data=True):
        if d['closed']:
            closed_edges.append((u, v))
        elif d['accessible']:
            accessible_edges.append((u, v))
        else:
            nonaccessible_edges.append((u, v))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size = 700, node_color='lightblue', ax=ax)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_weight='bold', ax=ax)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist = accessible_edges, edge_color='black', width=2, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist = nonaccessible_edges, edge_color='orange', style='dashed', width=2, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist = closed_edges, edge_color = 'red', width = 5, ax = ax)

    # Draw edge labels for distance/time
    edge_labels = { (u,v): f"{d['distance']}ft, {d['time']}min" for u,v,d in G.edges(data=True) }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', ax=ax)

    ax.axis('off')
    canvas.draw()


def updateGraph():
    input_text = addBuildingText.get().upper()
    if not input_text:
        messagebox.showerror("Error!", "Invalid input.")
        print("Invalid input.")
        return
    if input_text in nodes:
        messagebox.showerror("Error!", "Building already exists.")
        print("Building already exists.")
        return
    nodes.append(input_text)
    print(nodes)
    makeGraph()


def createEdge():
    global edge_counter
    connect_buildings = [b.strip().upper() for b in addEdgeBuildingsText.get().split(',')]
    if len(connect_buildings) != 2:
        messagebox.showerror("Error!", "Please input 2 valid buildings that are comma seperated. \n(e. g.) Building 1, Building 2")
        print("Please input 2 valid buildings")
        return

    a, b = connect_buildings
    try:
        edgeDistance = int(addEdgeDistanceText.get())
        edgeTime = int(addEdgeTimeText.get())
    except ValueError:
        messagebox.showerror("Error!", "Please input valid numbers for distance and or time.")
        print("Please input valid numbers for distance and or time")
        return

    if edgeDistance <= 0 or edgeTime <= 0:
        messagebox.showerror("Error!", "Please enter positive non-zero numbers for distance and time.")
        print("Please enter positive non-zero numbers for distance and time")
        return
    
    if a not in nodes or b not in nodes:
        messagebox.showerror("Error!", f"One or both buildings ({a}, {b}) do not exist.")
        print(f"One or both buildings ({a}, {b}) do not exist.")
        return
    for edges in graph_edges.values():
        if {a, b} == {edges['a'], edges['b']}:
            messagebox.showerror("Error!", "This edge already exists.")
            print("This edge already exists.")
            return

    graph_edges["edge" + str(edge_counter)] = {
        'a': a,
        'b': b,
        'distance': edgeDistance,
        'time': edgeTime,
        'accessible': is_accessible.get(),
        'closed': False
    }
    makeGraph()
    edge_counter += 1
    print(graph_edges)
    return

def randomizeWeights():
    for edge in graph_edges.values():
        import random
        edge['distance'] = random.randint(500, 1500)
        edge['time'] = round(edge['distance'] * 1/300, 3)
    makeGraph()

def simulateClosedEdges():
    import random
    if edgeClosureState.get() == False:
        for edge in graph_edges.values():
            edge['closed'] = False
        print("Re-opened edges") 
    else:
        for edge in graph_edges.values():
            edge['closed'] = random.choice([True, False])
        print("Closed edges")
    makeGraph()

def runTraversal():
    buildingChoice = [b.strip().upper() for b in buildingTraversalSelection.get().split(',')]
    traversalChoice = traversalSelection.get()

    if not traversalChoice:
        messagebox.showerror("Error!", "Please choose a searching algorithm.")
        print("Please choose a searching algorithm")
        return
    if len(buildingChoice) != 2:
        messagebox.showerror("Error!", "Please input 2 valid buildings.")
        print("Please input 2 valid buildings")
        return
    
    a, b = buildingChoice

    if a not in nodes or b not in nodes:
        print("Buildings do not exist")
        return
    print(buildingChoice)
    print(traversalChoice)


nodes = []
graph_edges = {}

CTk.set_appearance_mode("System")
CTk.set_default_color_theme("blue")

main_window = CTk.CTk()
is_accessible = CTk.BooleanVar(main_window, value=False)

main_window.geometry("1200x800")
main_window.title("Graph Visualization")

# frame for headers
header_frame = CTk.CTkFrame(main_window, fg_color="transparent")
header_text = CTk.CTkLabel(header_frame, text="Interactive Campus Visualization", font=CTk.CTkFont(family = "Trebuchet MS", size=50, weight="bold"))
header_text.pack()
header_frame.pack(pady=(100, 0))

# frame for all the buttons and canvas
main_frame = CTk.CTkFrame(main_window)
canvas_frame = CTk.CTkFrame(main_window)

# frame for the building/nodes creation
building_frame = CTk.CTkFrame(main_frame, fg_color="transparent")
building_frame.pack(side='top', pady=5)

# left frame for the text inputs
building_button_left_frame = CTk.CTkFrame(building_frame, fg_color="transparent")
building_button_left_frame.pack(side="left", padx=5)

addBuildingText = CTk.CTkEntry(building_button_left_frame, height=25, width=200, placeholder_text="Enter Building Name")
addBuildingText.pack(side="top")

# right frame for the button
building_button_right_frame = CTk.CTkFrame(building_frame, fg_color="transparent")
building_button_right_frame.pack(side="left", padx=5)

addBuildingButton = CTk.CTkButton(building_button_right_frame, text="Add Building", command=updateGraph)
addBuildingButton.pack()

# frame for the edge creation
edge_outer_frame = CTk.CTkFrame(main_frame, fg_color="transparent")
edge_outer_frame.pack(side="top", pady=5)

# frame for the text inputs/checkboxes for user input
edge_button_left_frame = CTk.CTkFrame(edge_outer_frame, fg_color="transparent")
edge_button_left_frame.pack(side="left", padx=5)

addEdgeBuildingsText = CTk.CTkEntry(edge_button_left_frame, height=25, width=200, placeholder_text="Buildings comma separated (A, B)")
addEdgeDistanceText = CTk.CTkEntry(edge_button_left_frame, height=25, width=200, placeholder_text="Enter Distance (in feet)")
addEdgeTimeText = CTk.CTkEntry(edge_button_left_frame, height=25, width=200, placeholder_text="Enter Time (in minutes)")
addEdgeAccessible = CTk.CTkCheckBox(edge_button_left_frame, text="Accessible", variable=is_accessible)

addEdgeBuildingsText.pack(pady=2)
addEdgeDistanceText.pack(pady=2)
addEdgeTimeText.pack(pady=2)
addEdgeAccessible.pack(pady=2)

# frame for the edge creation button on the right
edge_button_right_frame = CTk.CTkFrame(edge_outer_frame, fg_color="transparent")
edge_button_right_frame.pack(side="left", padx=5)

addEdgeBuildingButton = CTk.CTkButton(edge_button_right_frame, text="Create Edge", command=createEdge)
addEdgeBuildingButton.pack(pady=5)

# frame for the traversal selection and buttons
traversal_button_frame = CTk.CTkFrame(main_frame, fg_color="transparent")
traversal_button_frame.pack(side="bottom")

# left frame for the buttons/selections
traversal_button_left_frame = CTk.CTkFrame(traversal_button_frame, fg_color="transparent")
traversal_button_left_frame.pack(side="left", padx=5)

# right frame for the button to start traversal
traversal_button_right_frame = CTk.CTkFrame(traversal_button_frame, fg_color="transparent")
traversal_button_right_frame.pack(side="left", padx=5)

accessibleOnly = tk.BooleanVar(main_window, value = False)
edgeClosureState = tk.BooleanVar(main_window, value = False)

buildingTraversalSelection = CTk.CTkEntry(traversal_button_left_frame, height=25, width=200, placeholder_text="Enter Buildings for Traversal")
traversalSelection = ttk.Combobox(traversal_button_left_frame, state= 'readonly', values=["BFS", "DFS"], height=3, width=24)
randomizeWeightsButton = CTk.CTkButton(traversal_button_left_frame, text="Randomize Weights", command=randomizeWeights)
simulateClosedEdgesButton = CTk.CTkCheckBox(traversal_button_left_frame, text="Toggle Edge Closures", command=simulateClosedEdges, variable = edgeClosureState)
accessibleOnlyCheckbox = CTk.CTkCheckBox(traversal_button_left_frame, text = "Accessible Only?", variable = accessibleOnly)
traversalButton = CTk.CTkButton(traversal_button_right_frame, text="Run Path Traversal", command=runTraversal)

buildingTraversalSelection.pack(pady=2)
traversalSelection.pack(pady=2)
randomizeWeightsButton.pack(pady=2)
simulateClosedEdgesButton.pack(pady=2)
accessibleOnlyCheckbox.pack(pady=2)
traversalButton.pack(pady=2)

main_frame.pack(side='right', padx=(10, 100))
canvas_frame.pack(side='left', padx=(100, 10))

# graph drawing
G = nx.Graph()
pos = {}
edge_counter = 0
fig = Figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.axis('off')
fig.tight_layout(pad=2)
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(fill = "both", expand= True)

# run window
main_window.mainloop()
