import customtkinter as CTk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# =========================================================
# Graph Logic
# =========================================================

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


# =========================================================
# Graph Visualization + Controls
# =========================================================

def makeGraph():
    ax.clear()
    for i in nodes:
        G.add_node(i)
    for edge in graph_edges.values():
        G.add_edge(edge['a'], edge['b'],
                   distance=edge['distance'],
                   time=edge['time'],
                   accessible=edge['accessible'])
    nx.draw(G, with_labels=True, node_color='lightblue',
            font_weight='bold', ax=ax)
    canvas.draw()


def updateGraph():
    input_text = addBuildingText.get("1.0", 'end-1c').upper()
    if not input_text:
        print("Invalid input.")
        return
    if input_text in nodes:
        print("Building already exists.")
        return
    nodes.append(input_text)
    makeGraph()


def createEdge():
    global edge_counter
    connect_buildings = [b.strip().upper()
                         for b in addEdgeBuildingsText.get("1.0", 'end-1c').split(',')]
    if len(connect_buildings) != 2:
        print("Please input 2 valid buildings")
        return

    a, b = connect_buildings
    try:
        edgeDistance = int(addEdgeDistanceText.get("1.0", 'end-1c'))
        edgeTime = int(addEdgeTimeText.get("1.0", 'end-1c'))
    except ValueError:
        print("Please input valid numbers for distance/time")
        return

    if edgeDistance <= 0 or edgeTime <= 0:
        print("Please enter positive non-zero numbers")
        return
    if a not in nodes or b not in nodes:
        print(f"One or both buildings ({a}, {b}) do not exist.")
        return

    for edges in graph_edges.values():
        if {a, b} == {edges['a'], edges['b']}:
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


# =========================================================
# CustomTkinter UI Setup
# =========================================================

CTk.set_appearance_mode("System")
CTk.set_default_color_theme("blue")

main_window = CTk.CTk()
main_window.geometry("1280x820")
main_window.title("CSUF Interactive Campus Navigation System")

# Data storage
nodes = []
graph_edges = {}
G = nx.Graph()
pos = {}
edge_counter = 0
is_accessible = CTk.BooleanVar(main_window, value=False)

# =========================================================
# Header
# =========================================================
header_frame = CTk.CTkFrame(main_window, fg_color="transparent")
header_label = CTk.CTkLabel(
    header_frame,
    text="🏫 Interactive Campus Navigation System",
    font=CTk.CTkFont(size=28, weight="bold")
)
header_label.pack(pady=10)
header_frame.pack(pady=(40, 20))

# =========================================================
# Main Layout Frames
# =========================================================
layout_frame = CTk.CTkFrame(main_window, corner_radius=20)
layout_frame.pack(fill="both", expand=True, padx=40, pady=20)

# Split layout: Graph on left, controls on right
layout_frame.grid_columnconfigure(0, weight=2)
layout_frame.grid_columnconfigure(1, weight=1)

# =========================================================
# Left Side - Graph Display
# =========================================================
canvas_frame = CTk.CTkFrame(layout_frame, corner_radius=15)
canvas_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

fig = Figure(figsize=(7, 6))
ax = fig.add_subplot(111)
ax.axis("off")
canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

# =========================================================
# Right Side - Controls
# =========================================================
control_frame = CTk.CTkFrame(layout_frame, corner_radius=15)
control_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

# Building creation section
CTk.CTkLabel(control_frame, text="🏗️ Add Building", font=CTk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))
addBuildingText = CTk.CTkTextbox(control_frame, height=25, width=200)
addBuildingText.pack(pady=5)
CTk.CTkButton(control_frame, text="Add Building", command=updateGraph).pack(pady=10)

ttk.Separator(control_frame, height=2).pack(fill="x", pady=10)

# Edge creation section
CTk.CTkLabel(control_frame, text="🔗 Create Edge", font=CTk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))
addEdgeBuildingsText = CTk.CTkTextbox(control_frame, height=25, width=200)
addEdgeDistanceText = CTk.CTkTextbox(control_frame, height=25, width=200)
addEdgeTimeText = CTk.CTkTextbox(control_frame, height=25, width=200)
addEdgeAccessible = CTk.CTkCheckBox(control_frame, text="Accessible Path", variable=is_accessible)

addEdgeBuildingsText.pack(pady=3)
addEdgeDistanceText.pack(pady=3)
addEdgeTimeText.pack(pady=3)
addEdgeAccessible.pack(pady=5)
CTk.CTkButton(control_frame, text="Create Edge", command=createEdge).pack(pady=10)

CTk.CTkSeparator(control_frame, height=2).pack(fill="x", pady=10)

# Traversal section
CTk.CTkLabel(control_frame, text="🧭 Path Traversal", font=CTk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))
buildingTraversalSelection = CTk.CTkTextbox(control_frame, height=25, width=200)
buildingTraversalSelection.pack(pady=5)
traversalSelection = ttk.Combobox(control_frame, values=["BFS", "DFS"], height=3, width=24)
traversalSelection.pack(pady=5)

CTk.CTkButton(control_frame, text="Randomize Weights").pack(pady=5)
CTk.CTkButton(control_frame, text="Simulate Closed Edges").pack(pady=5)
CTk.CTkButton(control_frame, text="Run Path Traversal").pack(pady=10)

# =========================================================
# Run App
# =========================================================
main_window.mainloop()