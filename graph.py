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
        self.constraints = []
        self.forces = []

    def create(self, n, m, randomness, posRandom, switch):
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

                    if (x-0.5,y-1) == nodePos: #BottomLeft
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
                if connection1.node1 == connection2.node2 and connection1.node2 == connection2.node1:
                    self.connections.remove(connection1)

        for connection1 in self.connections:
            for connection2 in self.connections:
                if connection1.node1 == connection2.node2 and connection1.node2 == connection2.node1:
                    self.connections.remove(connection2)

        print(len(self.connections))

        for con in self.connections:
            con.weight -= random.uniform(0,0.05*(randomness-1))

        for nodeObj in self.nodes:
            (x,y) = nodeObj.position
            x = x + random.uniform(-0.05*(posRandom-1),0.05*(posRandom-1))
            y = y + random.uniform(-0.05*(posRandom-1),0.05*(posRandom-1))
            nodeObj.position = (x,y)

        self.constraints = list(range(self.width))
        self.forces = list(range(len(self.nodes)-self.width,len(self.nodes)))

        self.checkNodes()

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
        failureThreshold = 0
        for i in range(len(self.connections)):
            i -= 1
            change = np.abs(start[i]-end[i]) #calculate length change
            currentConnection = self.connections[i]
            currentConnection.weight -= np.abs(change) #weaken edge depending on change

            if currentConnection.weight < failureThreshold:
                conToRemove.append(self.connections[i]) #remove edge from

            self.connections[i] = currentConnection

        for con in conToRemove:
            self.connections.remove(con)

        self.checkNodes()

    def checkNodes(self):
        for node in self.nodes:
            var = False
            for con in self.connections: #check if connected to anything
                if con.node1 == node.id or con.node2 == node.id:
                    var = True
                    continue

            if var == False: #if not remove node - change length of forces and constraints
                if node.id in self.constraints:
                    self.constraints.remove(node.id)
                if node.id in self.forces:
                    self.forces.remove(node.id)

                for val in self.nodes: #change id's to compensate missing nodes
                    if val.id > node.id:
                        val.id -= 1
                for val in self.constraints: #reduce constraint points
                    if val == node.id:
                        self.constraints.remove(val)
                    if val > node.id:
                        val -= 1
                for val in self.forces: #reduce force points
                    if val == node.id:
                        self.forces.remove(val)
                    if val > node.id:
                        val -= 1
                for val in self.connections: #reduce connection ids
                    if val.node1 > node.id:
                        val.node1 -= 1
                    if val.node2 > node.id:
                        val.node2 -= 1
                self.nodes.remove(node)


    def visualise(self):
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot nodes
        for point in self.nodes:
            if point.id < len(self.constraints):
                colour = "white"
            elif point.id > len(self.nodes) - 1 - len(self.forces):
                colour = "red"
            else:
                colour = "skyblue"

            x, y = point.position
            ax.scatter(x, y, color=colour, s=50, zorder=2)
            ax.text(x, y, f"{point.id}", fontsize=8, ha="center", va="center", zorder=3)

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