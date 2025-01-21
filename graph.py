import numpy as np
import node
import connection
import matplotlib.pyplot as plt
import random

log = []

class Graph:
    def __init__(self):
        self.nodes = {}
        self.connections = []

    def create(self, n, randomness):
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
                    self.connections.append(connection.Connection(currentNode, topRightNode))

        for connection1 in self.connections:
            for connection2 in self.connections:
                if (connection1.node1 == connection2.node2 and connection1.node2 == connection2.node1):
                    self.connections.remove(connection1)

        # connection drawing - assign colour and positions
        # create colour map by taking max-min strength values and append to graphics
        for con in self.connections:
            con.weight -= random.randint(1,randomness)/10

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



    def weakenNodes(self, start, end):
        for i in range(len(self.connections)):
            i -= 1
            change = np.abs(start[i]-end[i])
            currentConnection = self.connections[i]
            currentConnection.weight -= np.abs(change)
            if currentConnection.weight < 0:
                currentConnection.weight = 0
            self.connections[i] = currentConnection

        for connection in self.connections:
            if connection.weight <= 0:
                nodeA = str(connection.node1.id)
                nodeB = str(connection.node2.id)
                log.append(str("Edge Broken - " + nodeA + nodeB))
                self.connections.remove(connection)
                
        print(len(self.connections))
        # File to write log
        with open("log.txt", "w") as file:
            file.write("\n".join(log))

    def visualise(self):
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot nodes
        for node in self.nodes.values():
            x, y = node.position
            ax.scatter(x, y, color="skyblue", s=300, zorder=2)
            ax.text(x, y, f"{node.id}", fontsize=12, ha="center", va="center", zorder=3)

        # Plot connections
        for con in self.connections:
            node1 = con.node1
            node2 = con.node2
            x1, y1 = node1.position
            x2, y2 = node2.position
            ax.plot([x1, x2], [y1, y2], color="gray", zorder=1, alpha=con.weight)

        # Set plot title and scaling
        ax.set_title("Triangular Lattice Graph")
        ax.axis("equal")

        return fig