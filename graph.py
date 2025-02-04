import numpy as np
import node
import connection
import matplotlib.pyplot as plt
import random

class Graph:
    def __init__(self):
        self.nodes = []
        self.connections = []
        self.width = 0
        self.height = 0

    def create(self, n, m, randomness, switch):
        self.width = m
        self.height = n
        offsetCount = 0

        if switch == 1:

            for i in range(n):
                rowLength = m if i % 2 == 0 else m - 1  # Reduce columns every other row

                for j in range(rowLength):
                    nodeID = offsetCount  # Unique ID for each node
                    x = j + 0.5 * (i % 2)  # Offset odd rows
                    y = i

                    position = (x, y)  # Assign position
                    self.nodes.append(node.Node(nodeID, position))
                    offsetCount += 1

            # create connections
            for point in self.nodes:
                x,y = point.position

                for nodeObj in self.nodes:
                    nodePos = nodeObj.position

                    if (x-1,y) == nodePos: #Left
                        self.connections.append(connection.Connection(point.id,nodeObj.id))

                    if (x+1,y) == nodePos: #Right
                        self.connections.append(connection.Connection(point.id,nodeObj.id))

                    if (x+0.5,y+1) == nodePos: #TopRight
                        self.connections.append(connection.Connection(point.id,nodeObj.id))

                    if (x+0.5,y-1) == nodePos: #BottomRight
                        self.connections.append(connection.Connection(point.id,nodeObj.id))

                    if (x-0.5,y+1) == nodePos: #TopLeft
                        self.connections.append(connection.Connection(point.id,nodeObj.id))

                    if (x-0.5,y+1) == nodePos: #BottomLeft
                        self.connections.append(connection.Connection(point.id,nodeObj.id))

        else:
            for i in range(n):
                for j in range(m):
                    nodeID = offsetCount  # Unique ID for each node
                    x = j  # Offset odd rows
                    y = i + 0.5 * (j % 2)  # Keep natural ordering without vertical flip

                    position = (x, y)  # Assign position
                    self.nodes.append(node.Node(nodeID, position))
                    offsetCount += 1

            # Create connections to form triangles
            for point in self.nodes:
                x, y = point.position

                for nodeObj in self.nodes:
                    nodePos = nodeObj.position

                    if (x, y + 1) == nodePos:  # Up
                        self.connections.append(connection.Connection(point.id, nodeObj.id))
                    if (x, y - 1) == nodePos:  # Down
                        self.connections.append(connection.Connection(point.id, nodeObj.id))
                    if (x - 1, y - 0.5) == nodePos:  # Bottom Left
                        self.connections.append(connection.Connection(point.id, nodeObj.id))
                    if (x + 1, y - 0.5) == nodePos:  # Bottom Right
                        self.connections.append(connection.Connection(point.id, nodeObj.id))
                    if (x - 1, y + 0.5) == nodePos:  # Top Left
                        self.connections.append(connection.Connection(point.id, nodeObj.id))
                    if (x + 1, y + 0.5) == nodePos:  # Top Right
                        self.connections.append(connection.Connection(point.id, nodeObj.id))

        for connection1 in self.connections:
            for connection2 in self.connections:
                if (connection1.node1 == connection2.node2 and connection1.node2 == connection2.node1):
                    self.connections.remove(connection2)

        for con in self.connections:
            con.weight -= random.randint(1,randomness)/10

        return self.nodes, self.connections

    def createAlt(self, n, m, randomness):
        self.width = m
        self.height = n
        self.nodes = []
        self.connections = []
        offsetCount = 0

        for i in range(n):
            for j in range(m):
                nodeID = offsetCount  # Unique ID for each node
                x = j   # Offset odd rows
                y = i + 0.5 * (j % 2) # Keep natural ordering without vertical flip

                position = (x, y)  # Assign position
                self.nodes.append(node.Node(nodeID, position))
                offsetCount += 1

        # Create connections to form triangles
        for point in self.nodes:
            x, y = point.position

            for nodeObj in self.nodes:
                nodePos = nodeObj.position

                if (x , y + 1) == nodePos:  # Up
                    self.connections.append(connection.Connection(point.id, nodeObj.id))
                if (x , y - 1) == nodePos:  # Down
                    self.connections.append(connection.Connection(point.id, nodeObj.id))
                if (x - 1, y - 0.5) == nodePos:  # Bottom Left
                    self.connections.append(connection.Connection(point.id, nodeObj.id))
                if (x + 1, y - 0.5) == nodePos:  # Bottom Right
                    self.connections.append(connection.Connection(point.id, nodeObj.id))
                if (x - 1, y + 0.5) == nodePos:  # Top Left
                    self.connections.append(connection.Connection(point.id, nodeObj.id))
                if (x + 1, y + 0.5) == nodePos:  # Top Right
                    self.connections.append(connection.Connection(point.id, nodeObj.id))

        # Remove duplicate connections
        unique_connections = set()
        for con in self.connections:
            pair = tuple(sorted([con.node1, con.node2]))
            unique_connections.add(pair)

        self.connections = [connection.Connection(n1, n2) for n1, n2 in unique_connections]

        # Randomize connection weights
        for con in self.connections:
            con.weight -= random.randint(1, randomness) / 10

        return self.nodes, self.connections

    def moveNodes(self, displace):
        count = 0

        for node in self.nodes:
            x,y = node.position
            x += float(displace[count])
            y += float(displace[count+1])
            node.position = tuple((x,y))
            count += 2

    def weakenNodes(self, start, end):
        conToRemove = []
        for i in range(len(self.connections)):
            i -= 1
            change = np.abs(start[i]-end[i])
            currentConnection = self.connections[i]
            currentConnection.weight -= np.abs(change)*3

            if currentConnection.weight < 0:
                conToRemove.append(self.connections[i])

            self.connections[i] = currentConnection

        for con in conToRemove:
            self.connections.remove(con)


    def visualise(self):
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot nodes
        for point in self.nodes:
            if point.id < self.width:
                colour = "white"
            elif point.id > len(self.nodes) - 1 - self.width:
                colour = "red"
            else:
                colour = "skyblue"

            x, y = point.position
            ax.scatter(x, y, color=colour, s=300, zorder=2)
            ax.text(x, y, f"{point
                    .id}", fontsize=12, ha="center", va="center", zorder=3)

        # Plot connections
        for con in self.connections:

            for nodeObj in self.nodes:
                if con.node1 == nodeObj.id:
                    x1, y1 = nodeObj.position
                if con.node2 == nodeObj.id:
                    x2, y2 = nodeObj.position

            ax.plot([x1, x2], [y1, y2], color="gray", zorder=1, alpha=con.weight)

        # Set plot title and scaling
        ax.set_title("Triangular Lattice Graph")
        ax.axis("equal")

        return fig