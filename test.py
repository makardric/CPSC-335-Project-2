
# while True:
#     new_building = input("What building would you like to add?: ")
#     if new_building not in campus:
#         campus[new_building] = []
#     if len(campus) > 1:
#         print("What buildings would you like to connect?")
#         buildingOne = input("First building: ")
#         buildingTwo = input("Second building: ")
#         # connected_buildings = connected_buildings.split(",")  # e.g., "Library, Gym" -> ["Library", "Gym"]

    
#         if buildingOne and buildingTwo in campus:
#             if buildingOne not in campus[buildingTwo]:
#                 campus[buildingTwo].append(buildingOne)

#             if buildingTwo not in campus[buildingOne]:
#                 campus[buildingOne].append(buildingTwo)
#         else:
#             campus[buildingOne] = []
#             campus[buildingTwo] = [] 

#     print(campus)

#     exit_loop = input("Exit loop? (Yes/No): \n")
#     if exit_loop.lower() == "yes":
#         break
    
# #Demo BFS Function

# campus = {
#     "CS": ["LIB", "GYM"],
#     "LIB": ["CS", "CAFE"],
#     "GYM": ["CS", "CAFE"],
#     "CAFE": ["LIB", "GYM"],
# }

# dist, parent, order = bfs_shortest_paths(campus, "CS")
# print("BFS order from CS:", order)
# path = reconstruct_path(parent, "CS", "CAFE")
# print("Shortest (fewer hops) path CS -> CAFE:", path)



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
