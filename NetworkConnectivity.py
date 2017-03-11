import matplotlib.pyplot as plt
import networkx as nx
import random

class NetworkGraph(object):
	def __init__(self, networkGraph):
		self.nodes = list(networkGraph.nodes)
		self.edges = list(networkGraph.edges)
		self.adjMat = y = [[j for j in i] for i in x]
	def __init__(self):
		self.nodes = []
		self.edges = []
		self.adjMat = [[]]
	def randomGenerator(self, node_num, edge_num):
		self.nodes = list(range(node_num))
		i = edge_num
		self.edges = []
		self.adjMat = [[0]*node_num for i in range(node_num)]
		while i > 0:
			p = random.choice(self.nodes)
			q = random.choice(self.nodes)
			if p != q:
				self.edges.append((p, q))
				self.adjMat[p][q]+=1
				self.adjMat[q][p]+=1
				i-=1
	def addNodes(self, nodes):
		for i in nodes:
			self.nodes.append(i)
			#TODO: Modify the adjMat
	def removeNodes(self, nodes):
		for i in nodes:
			self.nodes.remove(i)
			#TODO: Modify the adjMat
	def addEdges(self, edges):
		for i in edges:
			self.edges.append(i)
			#TODO: Modify the adjMat
	def removeEdges(self, edges):
		for i in edges:
			self.edges.remove(i)
			#TODO: Modify the adjMat
	def draw(self):
		G = nx.Graph()
		G.add_nodes_from(self.nodes)
		G.add_edges_from(self.edges)
		nx.draw(G)
		plt.show()
	def connective(self):
		#TODO
		pass
	def connectiveBetween(self, nodeA, nodeB):
		#TODO
		pass


NG = NetworkGraph()
NG.randomGenerator(int(input()), int(input()))
NG.draw()


'''
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
'''