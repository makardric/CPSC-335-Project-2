# Student Name: Richard Cam
# Titan Email: rccam@csu.fullerton.edu
# Project: CPSC 335 – Interactive Campus Navigation System
# Date: 10/25/2025

import tkinter as tk
from tkinter import ttk 
from tkinter import simpledialog
from tkinter import messagebox
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
        cur = parent.get(cur, None)
    if not rev_path or rev_path[-1] != start:
        return []
    return list(reversed(rev_path))


def dfs_path(graph, start, target):
    visited = set()
    parent = {}
    order = []
    found = False

    def dfs(u):
        nonlocal found
        if found:
            return
        visited.add(u)
        order.append(u)
        if u == target:
            found = True
            return
        for v in graph[u]:
            if v not in visited:
                parent[v] = u
                dfs(v)

    dfs(start)

    path = []
    if found:
        cur = target
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur, None)
        path.reverse()
    return path, order

# function for node selections
def select_node(node_name):
    global selected_nodes
    global node_items

    # checks if node is already selected, if so then unselect
    if node_name in selected_nodes:
        selected_nodes.remove(node_name)
        oval_id, _ = node_items[node_name]
        canvas.itemconfigure(oval_id, fill='white')
    
    # checks if node is not selected, and if 2 nodes already exist 
    elif len(selected_nodes) < 2:
        selected_nodes.append(node_name)
        oval_id, _ = node_items[node_name]
        canvas.itemconfigure(oval_id, fill='yellow') # Highlight color
    
    # Case 3: We try to select a 3rd node
    else:
        messagebox.showwarning("Selection Error", "You can only select two nodes at a time.")

    # Update the selection label
    if not selected_nodes:
        selection_label_var.set("Selected: None")
    else:
        selection_label_var.set(f"Selected: {', '.join(selected_nodes)}")


# function to insert a node when canvas clicked by user/select node
def insertNode(e):
    # check if we clicked an existing node first
    item = canvas.find_withtag("current") 
    if item:
        item_id = item[0]
        # check if this item_id is one of our nodes
        for name, (oval_id, text_id) in node_items.items():
            if item_id == oval_id or item_id == text_id:
                select_node(name)
                return 

    # get coordinates of where the user clicked and add a value of 30 for the radius of the circle
    x1, y1= (e.x-30), (e.y-30)
    x2, y2= (e.x+30), (e.y+30)

    # checks if user exits out of the window input
    try:
        building = simpledialog.askstring("Building creation", "What building would you like to add?").upper()
    except AttributeError:
        return
    
    # check if input is empty
    if building == "":
        return

    # checks if building exists already
    if building in nodes:
        messagebox.showwarning("Error", "Building already exists!")
        return
    
    # creates circle
    oval_id = canvas.create_oval(x1, y1, x2, y2, fill = 'white', outline = 'black') 
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    # creates text inside circle
    text_id = canvas.create_text( 
        center_x,
        center_y,
        text = building,
        font = ("Arial", 16, "bold"),
        fill = 'black'
    )

    # adds the building into the nodes list
    nodes.append(building)
    node_coords[building] = [e.x, e.y]
    node_items[building] = (oval_id, text_id) 
    # print(nodes)
    # print(f"Current coords: {str(e.x), str(e.y)}")

# function to create an edge
def createEdge():
    global edge_counter
    global selected_nodes 

    if len(selected_nodes) != 2:
        messagebox.showerror("Error", "Please click to select exactly two buildings on the canvas.")
        return
    
    building_A, building_B = selected_nodes
    connect_buildings = [building_A, building_B] 
    
    # checks if the user has inputted a valid input for the edge weights (distance and time)
    try:
        dist = int(addEdgeDistanceText.get())
        time = int(addEdgeTimeText.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for distance and time.")
        return
    
    # iterate over all the edges and see if the edge already exists or not
    for edge in graph_edges.values():
        edge_set = {edge['a'], edge['b']}
        if set(connect_buildings) == edge_set:
            edge['a'] = building_A
            edge['b'] = building_B
            edge['distance'] = dist
            edge['time'] = time
            edge['accessible'] = is_accessible.get()
            edge['user_closed'] = edgeClosureState.get()
            print(graph_edges)
            
            if edge['user_closed'] or edge['closed_random']:
                canvas.itemconfigure(edge['id'], fill = 'red', width = 4)
                canvas.itemconfigure(edge['text_id'], text = 'CLOSED', fill = 'black')
            elif edge['accessible']:
                canvas.itemconfigure(edge['id'], fill = 'black', width = 2)
                canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'CadetBlue1')
            else:
                canvas.itemconfigure(edge['id'], fill = 'orange', width = 2)
                canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'orange')
                
            oval_id_A, _ = node_items[building_A]
            oval_id_B, _ = node_items[building_B]
            canvas.itemconfigure(oval_id_A, fill='white')
            canvas.itemconfigure(oval_id_B, fill='white')
            selected_nodes.clear()
            selection_label_var.set("Selected: None")
            # messagebox.showerror("Error", "Edge already exists!")
            return

    # get centers of the two nodes on the canvas
    building_A_coords = node_coords[building_A]
    building_B_coords = node_coords[building_B]

    center_x = (building_A_coords[0] + building_B_coords[0])/2
    center_y = (building_A_coords[1] + building_B_coords[1])/2

    # checks if the user wants the edge be accessible and creates the line connecting the nodes, changing the color based on accessibility
    if edgeClosureState.get():
        edge = canvas.create_line(building_A_coords[0], building_A_coords[1],
                                building_B_coords[0], building_B_coords[1], 
                                fill = 'Red', width = 4)
        text = canvas.create_text(center_x,
                                center_y,
                                text = "CLOSED",
                                font = ("Arial", 12, "bold"),
                                fill = 'Black')

    elif is_accessible.get() == True:
        edge = canvas.create_line(building_A_coords[0], building_A_coords[1],
                                building_B_coords[0], building_B_coords[1], 
                                fill = 'Black', width = 2)
        text = canvas.create_text(center_x,
                                center_y,
                                text = f"{dist} feet\n {time} min(s)",
                                font = ("Arial", 12, "bold"),
                                fill = 'CadetBlue1')
    else:
        edge = canvas.create_line(building_A_coords[0], building_A_coords[1],
                                building_B_coords[0], building_B_coords[1],
                                fill = 'Orange', width = 2)
        text = canvas.create_text(center_x,
                                center_y,
                                text =  f"{dist} feet\n {time}min(s)",
                                font = ("Arial", 12, "bold"),
                                fill = 'orange',
                                )

    canvas.tag_lower(edge)
    canvas.tag_raise(text)

    # adding all attributes of the edge to a global variable to keep track
    edge_key = "edge" + str(edge_counter)
    graph_edges[edge_key] = {
        'a': building_A,
        'b': building_B,
        'distance': dist,
        'time': time,
        'accessible': is_accessible.get(),
        'user_closed': edgeClosureState.get(),
        'closed_random': False,
        'id': edge ,
        'text_id' : text
    }
    edge_counter += 1
    
    oval_id_A, _ = node_items[building_A]
    oval_id_B, _ = node_items[building_B]
    canvas.itemconfigure(oval_id_A, fill='white')
    canvas.itemconfigure(oval_id_B, fill='white')
    selected_nodes.clear()
    selection_label_var.set("Selected: None")
    
    print(graph_edges)

# function to randomize weights of the edges
def randomizeWeights():
    import random
    # iterates over all the edges that exist and randomizes the distance and the time (rate of 1 minute per 300 feet, rounded to the 2nd digit)
    for edge in graph_edges.values():
        edge['distance'] = random.randint(700,1500)
        edge['time'] = round(1 / 300 * edge['distance'], 2)
        if not edge['user_closed'] and not edge['closed_random']:
            canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)")
        # print(f"From {edge['a']} to {edge['b']}, the distance is {edge['distance']} feet and the time is now {edge['time']} minutes.")

# function to randomly close edges
def simulateClosedEdges():
    import random
    # checks if the user has it checked or not
    closedEdgesState = edgeClosureStateRandom.get()
    if closedEdgesState == True:
        # iterates over the edges and randomly decides if it is closed or not
        for edge in graph_edges.values():
            edge['closed_random'] = bool(random.getrandbits(1))
            if edge['closed_random'] or edge['user_closed']:
                canvas.itemconfigure(edge['id'], fill = 'red', width = 4)
                canvas.itemconfigure(edge['text_id'], text = 'CLOSED', fill = 'black')
            elif edge['accessible']:
                canvas.itemconfigure(edge['id'], fill = 'black', width = 2)
                canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'CadetBlue1')
            else:
                canvas.itemconfigure(edge['id'], fill = 'orange', width = 2)
                canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'orange')
    # when it is unchecked, reverts the previously closed edges to what they were before
    else:
        for edge in graph_edges.values():
            edge['closed_random'] = False
            if edge['user_closed']:
                canvas.itemconfigure(edge['id'], fill = 'red', width = 4)
                canvas.itemconfigure(edge['text_id'], text = 'CLOSED', fill = 'black')
            elif edge['accessible']:
                canvas.itemconfigure(edge['id'], fill = 'black', width = 2)
                canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'CadetBlue1')
            else:
                canvas.itemconfigure(edge['id'], fill = 'orange', width = 2)
                canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'orange')

# function to run BFS/DFS 
def runTraversal():
    # gets the user input
    node_selection = [b.strip().upper() for b in buildingTraversalSelection.get().split(',')]

    # checks if the user's input has two buildings
    if len(node_selection) != 2:
        messagebox.showerror("Error", "Please input 2 valid buildings")
        return
    
    starting_building, end_building = node_selection

    # checks if the buildings exist
    if starting_building not in nodes or end_building not in nodes:
        messagebox.showerror("Error", "One or more of the buildings do not exist.")
        return

    # sees if users wants to traverse only accessible edges, as well as which traversal (BFS/DFS) they want
    accessibility_state = accessibleOnly.get()
    traversalChoice = traversalSelection.get()
    
    # creates an adjacency list as well as a dictionary for edges to get their distance, time, and their edge id to later change the color
    adjacency_list = {node: [] for node in nodes}
    edge_info = {}

    # iterates over the edges
    for edge in graph_edges.values():
        # checks if the edge is closed, if so skip
        if edge['closed_random'] or edge['user_closed']:
            continue

        # checks if the user wants only accessible edges, if so then skip
        if accessibility_state and not edge['accessible']:
            continue

        # gets the current nodes the edge is connected to and appends it to the adjacency list, both ways as it is undirected
        a, b = edge['a'], edge['b']
        adjacency_list[a].append(b)
        adjacency_list[b].append(a)
        edge_info[(a, b)] = (edge['distance'], edge['time'], edge['id'])
        edge_info[(b, a)] = (edge['distance'], edge['time'], edge['id'])

    # performs traversal depending on user input
    if traversalChoice == "BFS":    
        dist, parent, order = bfs_shortest_paths(adjacency_list, starting_building)
        path = reconstruct_path(parent, starting_building, end_building)

    elif traversalChoice == "DFS":
        path, order = dfs_path(adjacency_list, starting_building, end_building)

    # checks if path doesn't exist
    if not path:
        messagebox.showinfo("Result", "Path not found.")
        return
    
    # iterates over path and colors the edges 
    total_distance = 0
    total_time = 0
    for i in range(len(path) - 1):
        a, b = path[i], path[i+1]
        dist, time, edge_id = edge_info[(a, b)]
        total_distance += dist
        total_time += time
        canvas.itemconfigure(edge_id, fill='green', width=6)

    path_length = len(path) - 1
    messagebox.showinfo(
        "Traversal Result",
        f"Traversal Type: {traversalSelection.get()}\n"
        f"Traversal Order: {' → '.join(order)}\n"
        f"Path Found: {' → '.join(path)}\n"
        f"Path Length: {path_length} edge(s)\n"
        f"Total Distance: {total_distance} feet\n"
        f"Total Time: {total_time:.2f} min(s)"
    )

    # after the message box is closed, change back the colors/texts of the lines to what they were
    for edge in graph_edges.values():
        if edge['user_closed'] or edge['closed_random']:
            canvas.itemconfigure(edge['id'], fill = 'red', width = 4)
            canvas.itemconfigure(edge['text_id'], text = 'CLOSED', fill = 'black')
        elif edge['accessible']:
            canvas.itemconfigure(edge['id'], fill = 'black', width = 2)
            canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'CadetBlue1')
        else:
            canvas.itemconfigure(edge['id'], fill = 'orange', width = 2)
            canvas.itemconfigure(edge['text_id'], text = f"{edge['distance']} feet\n {edge['time']} min(s)", fill = 'orange')

# function to clear canvas
def clearCanvas():
    global nodes
    global node_coords
    global graph_edges
    global edge_counter
    global selected_nodes 
    global node_items 

    nodes = []
    node_coords = {}
    graph_edges = {}
    edge_counter = 0
    selected_nodes = [] 
    node_items = {} 
    selection_label_var.set("Selected: None") 
    canvas.delete('all')


# global variables to store needed information
nodes = []
node_coords = {}
graph_edges = {}
edge_counter = 0
selected_nodes = [] 
node_items = {} 

# make main window
# determine window size
# make title of window
main_window = tk.Tk()  
main_window.geometry("1600x800")
main_window.title("Interactive Campus Visualization")

# make the grid the frames will fall into
main_window.grid_columnconfigure(0, weight=3)
main_window.grid_columnconfigure(1, weight=1)
main_window.grid_rowconfigure(1, weight=1)

# variables for the checkboxes
is_accessible = tk.BooleanVar(main_window, value=False)
accessibleOnly = tk.BooleanVar(main_window, value=False)
edgeClosureState = tk.BooleanVar(main_window, value=False)
edgeClosureStateRandom = tk.BooleanVar(main_window, value=False)
selection_label_var = tk.StringVar(main_window, value="Selected: None") 

# frame for the header
header_frame = ttk.Frame(main_window)
header_frame.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="ew")

# header text
header_text = ttk.Label(header_frame, text="Interactive Campus Visualization", font=("Trebuchet MS", 32, "bold"))
header_text.pack()

# frame for the canvas
canvas_frame = ttk.Frame(main_window, relief="groove", borderwidth=1)
canvas_frame.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)

# canvas creation
canvas = tk.Canvas(canvas_frame, width = 800,  height = 600, bg = 'white')
canvas.bind('<Button-1>', insertNode)

canvas.pack(anchor=tk.CENTER, expand=True)

# main panel for the other frames to go into
control_panel_frame = ttk.Frame(main_window)
control_panel_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)
control_panel_frame.grid_columnconfigure(0, weight=1)

# legend
control_panel_frame.grid_rowconfigure(0, weight=0)
# edge buttons/input
control_panel_frame.grid_rowconfigure(1, weight=0) 
# traversal buttons
control_panel_frame.grid_rowconfigure(2, weight=0) 



# frame for the legend
key_group = ttk.LabelFrame(control_panel_frame, text="Legend")
key_group.grid(row=0, column=0, sticky="new", padx=10, pady=10)
key_group.grid_columnconfigure(0, weight=1)

key_text = (
    "Yellow → Selected Node\n" 
    "Green → Current BFS/DFS path\n"
    "Red → Closed or blocked path\n"
    "Orange → Non-accessible path\n"
    "Gray/Black → Open regular path"
)
key_label = ttk.Label(key_group, text=key_text, font=("Arial", 12, "bold"), justify="left")
key_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)


# frame for buttons/inputs to create an edge
edge_group = ttk.LabelFrame(control_panel_frame, text="Create/Update Edge")
edge_group.grid(row=1, column=0, sticky="new", padx=10, pady=10)
edge_group.grid_columnconfigure(0, weight=1)
edge_group.grid_columnconfigure(1, weight=1)

# label for user selection
selection_label = ttk.Label(edge_group, textvariable=selection_label_var, font=("Arial", 10, "bold"))
selection_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5,5))

# labels for clarity
ttk.Label(edge_group, text="Distance (feet):").grid(row=2, column=0, sticky="w", padx=(10,5), pady=(5,0))
addEdgeDistanceText = ttk.Entry(edge_group)
addEdgeDistanceText.grid(row=3, column=0, sticky="ew", padx=(10,5), pady=(0,5)) 

ttk.Label(edge_group, text="Time (mins):").grid(row=2, column=1, sticky="w", padx=(5,10), pady=(5,0)) 
addEdgeTimeText = ttk.Entry(edge_group)
addEdgeTimeText.grid(row=3, column=1, sticky="ew", padx=(5,10), pady=(0,5)) 

addEdgeAccessible = ttk.Checkbutton(edge_group, text="Accessible Path", variable=is_accessible)
addEdgeAccessible.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=5) 

addEdgeClosed = ttk.Checkbutton(edge_group, text = "Closed Path", variable = edgeClosureState)
addEdgeClosed.grid(row=7, column = 0, columnspan=2, sticky="w", padx= 10, pady=5) 

addEdgeBuildingButton = ttk.Button(edge_group, text="Create/Update Edge", command=createEdge)
addEdgeBuildingButton.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10)) 


# frame for traversal buttons/inputs
traversal_group = ttk.LabelFrame(control_panel_frame, text="Run Analysis")
traversal_group.grid(row=2, column=0, sticky="new", padx=10, pady=10)
traversal_group.grid_columnconfigure(0, weight=1)

# label for clarity
ttk.Label(traversal_group, text="Path (e.g., Start, End):").grid(row=0, column=0, sticky="w", padx=10, pady=(5,0))
buildingTraversalSelection = ttk.Entry(traversal_group)
buildingTraversalSelection.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,5))

# dropdown for bfs/dfs
traversalSelection = ttk.Combobox(traversal_group, state='readonly', values=["BFS", "DFS"])
traversalSelection.set("BFS")
traversalSelection.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

randomizeWeightsButton = ttk.Button(traversal_group, text="Randomize Weights", command=randomizeWeights)
randomizeWeightsButton.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

simulateClosedEdgesButton = ttk.Checkbutton(traversal_group, text="Toggle Random Edge Closures", command=simulateClosedEdges, variable=edgeClosureStateRandom)
simulateClosedEdgesButton.grid(row=4, column=0, sticky="w", padx=10, pady=5)

accessibleOnlyCheckbox = ttk.Checkbutton(traversal_group, text="Find Accessible Path Only?", variable=accessibleOnly)
accessibleOnlyCheckbox.grid(row=5, column=0, sticky="w", padx=10, pady=5)

traversalButton = ttk.Button(traversal_group, text="Run Path Traversal", command=runTraversal)
traversalButton.grid(row=6, column=0, sticky="ew", padx=10, pady=(10, 10))

clearButton = ttk.Button(traversal_group, text = "Clear Canvas", command = clearCanvas)
clearButton.grid(row = 7, column = 0, sticky = "ew", padx=10, pady=(0,10))

ttk.Frame(control_panel_frame).grid(row=3, column=0, sticky="nsew")


# run window
main_window.mainloop()