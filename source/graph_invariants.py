# __author__ = 'ready4s'
#
# def make_link(G, node1, node2):
#     if node1 not in G:
#         G[node1] = {}
#     (G[node1])[node2] = 1
#     if node2 not in G:
#         G[node2] = {}
#     (G[node2])[node1] = 1
#     return G
#
# flights = [("ORD", "SEA"), ("ORD", "LAX"), ('ORD', 'DFW'), ('ORD', 'PIT'),
#            ('SEA', 'LAX'), ('LAX', 'DFW'), ('ATL', 'PIT'), ('ATL', 'RDU'),
#            ('RDU', 'PHL'), ('PIT', 'PHL'), ('PHL', 'PVD')]
#
# G = {}
# for (x,y) in flights: make_link(G,x,y)
#
# def clustering_coefficient(G,v):
#     neighbors = G[v].keys()
#     if len(neighbors) == 1: return -1.0
#     links = 0
#     for w in neighbors:
#         for u in neighbors:
#             if u in G[w]: links += 0.5
#     return 2.0*links/(len(neighbors)*(len(neighbors)-1))
#
# print clustering_coefficient(G,"ORD")
#
# total = 0
# for v in G.keys():
#     total += clustering_coefficient(G,v)
#
# print total/len(G)

def DFSvisit(G, v, visited, order, component):
    visited[v] = component
    for w in G[v]:
        if not visited[w]:
            DFSvisit(G, w, visited, order, component)
    order.append(v);

def DFS(G, sequence, visited, order):
    components = 0
    for v in sequence:
        if not visited[v]:
            components += 1
            DFSvisit(G, v, visited, order, components)

n, m = (int(i) for i in raw_input().strip().split())

G = [[] for i in xrange(n)]
Gt = [[] for i in xrange(n)]
for i in xrange(m):
    a, b = (int(i) for i in raw_input().strip().split())
    G[a-1].append(b-1)
    Gt[b-1].append(a-1)

order = []
components = [0]*n

DFS(G, xrange(n), [0]*n, order)
DFS(Gt, reversed(order), components, [])

print max(components)
print components
