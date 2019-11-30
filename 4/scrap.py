# # graph = {'A': set(['B', 'C']),
# #          'B': set(['A', 'D', 'E']),
# #          'C': set(['A', 'F']),
# #          'D': set(['B']),
# #          'E': set(['B', 'F']),
# #          'F': set(['C', 'E'])}

# maxX = 5
# maxY = 5
# minX = 0
# minY = 0

# def generateChildren(current):
#     n = (current[0], current[1] + 1)
#     e = (current[0] + 1, current[1])
#     s = (current[0], current[1] - 1)
#     w = (current[0] - 1, current[1])
#     children = [n, e, s, w]
#     validChildren = []
#     for i in range(len(children)):
#       inXBound = children[i][0] < maxX and children[i][0] > minX
#       inYBound = children[i][1] < maxY and children[i][1] > minY
#       if inXBound and inYBound:
#         validChildren.append(children[i])
#     return validChildren

# # current = (9, 1)

# # children = generateChildren(current)
# # graph = {current: set(children)}

# def findPath(current, target):
#   nextStates = generateChildren(current)
#   graph = {current: set(nextStates)}
#   return list(bfs(graph, current, target))

# def dfs(graph, start, goal):
#     stack = [(start, [start])]
#     # print "stack", stack
#     while stack:
#         popped = stack.pop()
#         # print "(vertex, path)", popped
#         (vertex, path) = popped

#         if vertex not in graph:
#           graph[vertex] = set(generateChildren(vertex))

#         for next in graph[vertex] - set(path):
#             # print "graph[vertex]", graph[vertex]
#             # print "set(path)", set(path)
#             # print "graph[vertex] - set(path)", graph[vertex] - set(path)
#             # print "next", next
#             # print "next == goal", next == goal
#             if next == goal:
#                 # print "****path + [next]", path + [next]
#                 yield path + [next]
#             else:
#                 stack.append((next, path + [next]))

# def bfs(graph, start, goal):
#     queue = [(start, [start])]
#     while queue:
#         (vertex, path) = queue.pop(0)
#         if vertex not in graph:
#           graph[vertex] = set(generateChildren(vertex))
#         for next in graph[vertex] - set(path):
#             if next == goal:
#                 yield path + [next]
#             else:
#                 queue.append((next, path + [next]))

# # list(dfs_paths(graph, 'A', 'F'))
# # print list(dfs(graph, (9, 1), (10, 1)))
# findPath((2, 2), (1, 1))
# # print generateChildren((1, 1))

a = (5, 6)
print sum(a)

for action in [1, 2]:
  print action