import numpy as np
from networkx.algorithms.structuralholes import constraint

import node
import connection
import networkx
import matplotlib.pyplot as plot
import random

log = []

class Graph:
    def __init__(self):
        self.nodes = {}
        self.connections = []

    def create(self, n, shape, randomness):
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
                        self.connections.append(connection.Connection(currentNode, right_node))

                    if i < n - 1: #create connection down
                        bottom_node = self.nodes[(i + 1, j)]
                        self.connections.append(connection.Connection(currentNode, bottom_node))

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
                        self.connections.append(connection.Connection(currentNode, rightNode))

                    # bottom-right neighbor
                    if i < n - 1 and j < n - 1:
                        bottomRightNode = self.nodes[(i + 1, j + (i % 2))]
                        self.connections.append(connection.Connection(currentNode, bottomRightNode))

                    # bottom-left neighbor
                    if i < n - 1 and j > 0:
                        bottomLeftNode = self.nodes[(i + 1, j - (1 - (i % 2)))]
                        self.connections.append(connection.Connection(currentNode, bottomLeftNode))

                     # top-right neighbor
                    if i > 0 and (j + (i % 2)) < n:
                        topRightNode = self.nodes[(i - 1, j + (i % 2))]
                        self.connections.append(connection.Connection(currentNode, topRightNode))

                    # top-left neighbor
                    if i > 0 and j > 0:
                        topRightNode = self.nodes[(i - 1, j -(1- (i % 2)))]
                        self.connections.append(
                        connection.Connection(currentNode, topRightNode))

        for connection1 in self.connections:
            for connection2 in self.connections:
                if connection1.node1 == connection2.node2 and connection1.node2 == connection2.node1:
                    self.connections.remove(connection1)

        # connection drawing - assign colour and positions
        # create colour map by taking max-min strength values and append to graphics
        for connectiona in self.connections:
            connectiona.weight -= random.randint(1,randomness)/10

        return self.nodes, self.connections

    def moveNodes(self, displace):
        count = 0
        length = int(np.sqrt(len(self.nodes)))
        constraintMove = []
        for node in self.nodes.values():
            if node.id < length:
                continue

            elif length < node.id < 2*length:
                y = list(node.position)
                y[0] += float(displace[count])
                y[1] += float(displace[count + 1])
                constraintMove.append(displace[count])
                constraintMove.append(displace[count + 1])
            else:
                y = list(node.position)
                y[0] += float(displace[count])
                y[1] += float(displace[count+1])
            node.position = tuple(y)
            count += 2

        for node in self.nodes.values():
            count = 0
            if node.id < length:
                y = list(node.position)
                y[0] += float(constraintMove[count])
                y[1] += float(constraintMove[count + 1])
                node.position = tuple(y)
            count += 2


    def weakenNodes(self, start, end):
        for i in range(len(self.connections)):
            i -= 1
            change = np.abs(start[i]-end[i])
            currentConnection = self.connections[i]
            currentConnection.weight -= np.abs(change)
            self.connections[i] = currentConnection

        for connection in self.connections:
            if connection.weight < 0:
                nodeA = str(connection.node1.id)
                nodeB = str(connection.node2.id)
                log.append(str("Edge Broken - " + nodeA + nodeB))
                self.connections.remove(connection)
        print(len(self.connections))

        # Open file to write log
        with open("log.txt", "w") as file:
            file.write("\n".join(log))


    # function to draw graph with connection weights
    def visualOutput(self):
        G = networkx.Graph()

        # Create a new matplotlib figure and axes
        fig, ax = plot.subplots()

        # Node drawing - take all node's positions to draw
        for node in self.nodes.values():

            G.add_node(node.id, pos=node.position)

        pos = networkx.get_node_attributes(G, 'pos')
        networkx.draw(G, pos, with_labels=True, node_size=150, node_color="green", font_size=10, ax=ax)

        # Edge drawing
        for connection in self.connections:

            G.add_edge(connection.node1.id, connection.node2.id)

            try:
                networkx.draw_networkx_edges(G, pos, edgelist=[(connection.node1.id, connection.node2.id)], alpha=connection.weight,width=2, ax=ax)
            except ValueError:
                networkx.draw_networkx_edges(G, pos, edgelist=[(connection.node1.id, connection.node2.id)], alpha=0,width=2, ax=ax)


        # Output arrows
        for node in self.nodes.values():
            if node.id > len(self.nodes) - (np.sqrt(len(self.nodes))) - 1:
                ax.arrow(node.position[0], node.position[1], 0, 0.4, head_width=0.1, head_length=0.1)

        # Instead of showing the plot, return the figure
        return fig