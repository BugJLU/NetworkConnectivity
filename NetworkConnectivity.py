import matplotlib.pyplot as plt
import networkx as nx
import random
n = int(input())
m = int(input())
nodes = list(range(0, n))
edges = []
for x in range(m):
	edges.append((random.choice(nodes), random.choice(nodes)))
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.draw(G)
plt.show()