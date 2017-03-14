import matplotlib.pyplot as plt
import networkx as nx
import random
from copy import copy


class NetworkGraph(object):
    def __init__(self, node_num=0):
        self.nodes = []  # list(range(node_num))
        self.edges = []
        self.adjMat = [[0] * node_num for _ in range(node_num)]

    def __copy__(self):
        result = NetworkGraph()
        result.nodes = list(self.nodes)
        result.edges = list(self.edges)
        result.adjMat = [[j for j in i] for i in self.adjMat]
        return result

    def random_generator(self, node_num, edge_num):
        self.nodes = list(range(node_num))
        i = edge_num
        self.edges = []
        self.adjMat = [[0] * node_num for i in range(node_num)]
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
            # k = self.nodes.index(i)
            for j in range(len(self.nodes)):
                self.adjMat[j][i] = self.adjMat[i][j] = 0
                # TODO: check
            self.nodes.remove(i)

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
        nx.draw(g, with_labels=True)
        plt.show()

    def connective(self):
        x = self.nodes[0]
        l = [x]
        i = 0
        while i < len(l):
            for j in range(len(self.adjMat)):
                if (self.adjMat[l[i]][j] > 0) and (j not in l):
                    l.append(j)
            i += 1
        if len(l) == len(self.nodes):
            return True
        else:
            return False

    def connective_between(self, node_a, node_b):
        x = node_a
        l = [x]
        i = 0
        while i < len(l):
            for j in range(len(self.adjMat)):
                if (self.adjMat[l[i]][j] > 0) and (j not in l):
                    l.append(j)
            i += 1
        if node_b in l:
            return True
        else:
            return False

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
        t_g = copy(self)
        result = True
        for x in self.edges:
            t_g.remove_edges([x])
            if not t_g.connective():
                k_edges.append(x)
                result = False
            t_g.add_edges([x])
        return result, k_edges

    def key_node(self):
        k_node = []
        for x in self.nodes:
            t_g = copy(self)
            # t_g.draw()  # del
            t_g.remove_nodes([x])
            # t_g.draw()  # del
            if not t_g.connective():
                k_node.append(x)
        return k_node

'''
ng = NetworkGraph()
ng.random_generator(10, 20)
ng.draw()
ng.key_node()


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
