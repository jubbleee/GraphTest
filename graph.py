import node
import connection
import networkx
import matplotlib.pyplot as plot
import matplotlib.colors as col
import numpy
import random


class Graph:
    def __init__(self):
        self.nodes = {}
        self.connections = []

    def create(self, n, shape):
        if shape == 0: # create graph - square lattice

            # create nodes
            for i in range(n):
                for j in range(n):
                    node_id = j * n + i  #column no. + row
                    position = (i, j)
                    self.nodes[(i, j)] = node.Node(node_id, position)

            # create connections
            for i in range(n): #start 1st column
                for j in range(n): #start 1st row
                    currentNode = self.nodes[(i, j)]

                    if j < n - 1: #create connection right
                        right_node = self.nodes[(i, j + 1)]
                        self.connections.append(connection.Connection(currentNode, right_node, random.randint(1,50)))

                    if i < n - 1: #create connection down
                        bottom_node = self.nodes[(i + 1, j)]
                        self.connections.append(connection.Connection(currentNode, bottom_node, random.randint(1,50)))

        else: #create graph - triangular lattice

            # create nodes
            for i in range(n):
                for j in range(n):
                    node_id = i * n + j
                    position = (j + 0.5 * (i % 2), i ) # offset odd rows for triangular visual representation
                    self.nodes[(i, j)] = node.Node(node_id, position)

            # create connections
            for i in range(n):
                for j in range(n):
                    currentNode = self.nodes[(i, j)]

                    # right neighbor
                    if j < n - 1:
                        rightNode = self.nodes[(i, j + 1)]
                        self.connections.append(connection.Connection(currentNode, rightNode, random.randint(1,50)))

                    # bottom-right neighbor
                    if i < n - 1 and j < n - 1:
                        bottomRightNode = self.nodes[(i + 1, j + (i % 2))]
                        self.connections.append(connection.Connection(currentNode, bottomRightNode, random.randint(1,50)))

                    # bottom-left neighbor
                    if i < n - 1 and j > 0:
                        bottomLeftNode = self.nodes[(i + 1, j - (1 - (i % 2)))]
                        self.connections.append(connection.Connection(currentNode, bottomLeftNode, random.randint(1,50)))

                     # top-right neighbor
                    if i > 0 and (j + (i % 2)) < n:
                        topRightNode = self.nodes[(i - 1, j + (i % 2))]
                        self.connections.append(connection.Connection(currentNode, topRightNode, random.randint(1,50)))

                    # top-left neighbor
                    if i > 0 and j > 0:
                        topRightNode = self.nodes[(i - 1, j -(1- (i % 2)))]
                        self.connections.append(
                        connection.Connection(currentNode, topRightNode, random.randint(1, 50)))

        return self.nodes, self.connections

    def moveNodes(self, displace):
        count = 0
        length = int(numpy.sqrt(len(self.nodes)))
        for node in self.nodes.values():
            if node.id < length:
                continue
            else:
                y = list(node.position)
                y[0] += float(displace[count])
                y[1] += float(displace[count+1])
                node.position = tuple(y)
            count += 2
        for node in self.nodes.values():
            print(node.position)

    # function to draw graph with colour mapped connection weights
    def visualOutput(self):
        G = networkx.Graph()

        #node drawing - take all node's position to draw
        for node in self.nodes.values():
            #if node.id < int(numpy.sqrt(len(self.nodes))):
            #    continue
            G.add_node(node.id, pos=node.position)
        pos = networkx.get_node_attributes(G, 'pos')
        networkx.draw(G, pos, with_labels=True, node_size=150, node_color="gray", font_size=6)


        # connection drawing - assign colour and positions
        # create colour map by taking max-min strength values and append to graphics
        strengths = numpy.array([connection.weight for connection in self.connections])
        norm = col.Normalize(vmin=strengths.min(), vmax=strengths.max())
        cmap = plot.cm.viridis

        for connection in self.connections:
            G.add_edge(connection.node1.id, connection.node2.id, weight=connection.weight)

        # draw connections with respective colour map values
        for connection in self.connections:
            #if connection.node1.id < int(numpy.sqrt(len(self.nodes))) or connection.node2.id < int(numpy.sqrt(len(self.nodes))):
            #    continue
            connectColour = cmap(norm(connection.weight))
            networkx.draw_networkx_edges(G, pos, edgelist=[(connection.node1.id, connection.node2.id)],
                                   edge_color=[connectColour], width=2)

        # output graph

        for node in self.nodes.values():
            if  node.id < int(numpy.sqrt(len(self.nodes))):
            #if 2 * int(numpy.sqrt(len(self.nodes))) > node.id > int(numpy.sqrt(len(self.nodes))):
                plot.arrow(node.position[0], node.position[1], 0, -0.4, head_width=0.1, head_length=0.1)
            if node.id > len(self.nodes)-(numpy.sqrt(len(self.nodes))) - 1:
                plot.arrow(node.position[0], node.position[1], 0, 0.4, head_width=0.1, head_length=0.1)


        plot.show()
