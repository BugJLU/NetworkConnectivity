import matplotlib.pyplot as plt
import networkx as nx
import random


class NetworkGraph(object):
    def __init__(self, network_graph):
        self.nodes = list(network_graph.nodes)
        self.edges = list(network_graph.edges)
        self.adjMat = [[j for j in i] for i in network_graph.adjMat]

    def __init__(self, node_num):
        self.adjMat = [[0]*node_num for i in range(node_num)]

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.adjMat = [[]]

    def random_generator(self, node_num, edge_num):
        self.nodes = list(range(node_num))
        i = edge_num
        self.edges = []
        self.adjMat = [[0]*node_num for i in range(node_num)]
        while i > 0:
            p = random.choice(self.nodes)
            q = random.choice(self.nodes)
            if p != q:
                self.edges.append((p, q))
                self.adjMat[p][q] += 1
                self.adjMat[q][p] += 1
                i -= 1

    def add_nodes(self, nodes):
        for i in nodes:
            self.nodes.append(i)
            # TODO: Modify the adjMat

    def remove_nodes(self, nodes):
        for i in nodes:
            k = self.nodes.index(i)
            self.nodes.remove(i)
            for j in range(len(self.nodes)):
                self.adjMat[j][k] = self.adjMat[k][j] = 0
            # TODO: check

    def add_edges(self, edges):
        for i in edges:
            self.edges.append(i)
            self.adjMat[i[0]][i[1]] += 1
            self.adjMat[i[1]][i[0]] += 1
            # TODO: check

    def remove_edges(self, edges):
        for i in edges:
            self.edges.remove(i)
            self.adjMat[i[0]][i[1]] -= 1
            self.adjMat[i[1]][i[0]] -= 1
            # TODO: check

    def draw(self):
        g = nx.Graph()
        g.add_nodes_from(self.nodes)
        g.add_edges_from(self.edges)
        nx.draw(g)
        plt.show()

    def connective(self):
        x = self.nodes[0]
        l = [x]
        i = 0
        while i < len(l):
            for j in range(len(self.nodes)):
                if (self.adjMat[l[i]][j] > 0) and (j not in l):
                    l.append(j)
            i += 1
        if len(l) == len(self.nodes):
            return True
        else:
            return False
        pass

    def connective_between(self, node_a, node_b):
        # TODO
        pass

    def check_redundancy(self):
        r_edges = []
        t_g = NetworkGraph(len(self.nodes))
        t_g.add_nodes(self.nodes)
        for x in self.edges:
            if t_g.connective_between(x[0], x[1]):
                r_edges.append(x)
            else:
                t_g.add_edges([x])
        return t_g, r_edges

    def check_reliability(self):
        k_edges = []
        t_g = NetworkGraph(self)
        result = False
        for x in self.edges:
            t_g.remove_edges([x])
            if not t_g.connective():
                k_edges.append(x)
                result = True
            t_g.add_edges([x])
        return result, k_edges

    def key_node(self):
        k_node = []
        for x in self.nodes:
            t_g = NetworkGraph(self)
            t_g.remove_nodes([x])
            if not t_g.connective():
                k_node.append(x)
        return k_node

'''
NG = NetworkGraph()
NG.random_generator(int(input()), int(input()))
NG.draw()



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