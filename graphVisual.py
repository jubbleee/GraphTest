import tkinter as tk
from tkinter import ttk
from math import sqrt


class graph1Editor:
    def __init__(self, root, graph1):
        self.root = root
        self.graph1 = graph1
        self.nodePos = {}
        self.edgeLines = {}
        self.scaleFactor = None
        self.draggingNode = None  # Track the node being dragged

        # Create a frame for controls (left panel)
        self.controlFrame = tk.Frame(root)
        self.controlFrame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a canvas for drawing the graph
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.RIGHT)

        self.drawgraph1()

        # Event bindings
        self.canvas.bind("<Button-1>", self.onClick)  # Left-click: remove connection
        self.canvas.bind("<Button-3>", self.onRightClick)  # Right-click: select node for dragging
        self.canvas.bind("<B3-Motion>", self.onDrag)  # Dragging event
        self.canvas.bind("<ButtonRelease-3>", self.onRelease)  # Stop dragging

    def calculateScale(self):
        """Calculate the scale factor based on graph dimensions."""
        maxX = max(node.position[0] for node in self.graph1.nodes)
        maxY = max(node.position[1] for node in self.graph1.nodes)
        self.scaleFactor = min((600 - 100) / (maxX + 1), (600 - 100) / (maxY + 1))


    def drawgraph1(self):
        """Draw all nodes and edges with scaling applied."""
        self.canvas.delete("all")
        self.nodePos.clear()
        self.edgeLines.clear()
        self.calculateScale()

        # Map logical node positions to screen coordinates
        for node in self.graph1.nodes:
            x, y = node.position
            x = x * self.scaleFactor + 50
            y = -y * self.scaleFactor + 550  # Flip Y for GUI
            self.nodePos[node.id] = (x, y)

        # Draw edges (connections)
        for connection in self.graph1.connections:
            n1, n2 = connection.node1, connection.node2
            x1, y1 = self.nodePos[n1]
            x2, y2 = self.nodePos[n2]
            connectID = self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            self.edgeLines[connection] = connectID

        # Draw nodes
        for nodeID, (x, y) in self.nodePos.items():
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="skyblue", outline="black", width=2,
                                    tags=f"node_{nodeID}")

    def onClick(self, event):
        """Handle left-click to remove a connection."""
        clicked = self.conFind(event.x, event.y)
        if clicked:
            self.conRemove(clicked)

    def conFind(self, x, y):
        """Find the connection closest to the click point."""
        for connection, connectID in self.edgeLines.items():
            coords = self.canvas.coords(connectID)  # [x1, y1, x2, y2]
            if nearLine(x, y, *coords):
                return connection
        return None

    def conRemove(self, connection):
        """Remove a connection and update the graph."""
        self.graph1.connections.remove(connection)
        self.canvas.delete(self.edgeLines[connection])
        del self.edgeLines[connection]
        self.graph1.checkNodes()

    def onRightClick(self, event):
        """Detect if a node is right-clicked to start dragging."""
        for nodeID, (x, y) in self.nodePos.items():
            if (x - 10 <= event.x <= x + 10) and (y - 10 <= event.y <= y + 10):
                self.draggingNode = nodeID
                return

    def onDrag(self, event):
        """Move the selected node and update edges dynamically."""
        if self.draggingNode is not None:
            graphX = (event.x - 50) / self.scaleFactor
            graphY = -(event.y - 550) / self.scaleFactor
            self.graph1.nodes[self.draggingNode].position = (graphX, graphY)
            self.updateNode(self.draggingNode)

    def onRelease(self, event):
        """Stop dragging."""
        self.draggingNode = None

    def changeNode(self, nodeID):

        self.updateNode(nodeID)

    def updateNode(self, nodeID):
        """Redraw only the moved node and its edges."""
        x, y = self.nodePos[nodeID] = (
            self.graph1.nodes[nodeID].position[0] * self.scaleFactor + 50,
            -self.graph1.nodes[nodeID].position[1] * self.scaleFactor + 550
        )

        # Clear old node and redraw it
        self.canvas.delete(f"node_{nodeID}")
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="skyblue", outline="black", width=2, tags=f"node_{nodeID}")

        # Redraw only affected edges
        for connection in self.graph1.connections:
            if connection.node1 == nodeID or connection.node2 == nodeID:
                x1, y1 = self.nodePos[connection.node1]
                x2, y2 = self.nodePos[connection.node2]
                self.canvas.delete(self.edgeLines[connection])
                self.edgeLines[connection] = self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)


def nearLine(px, py, x1, y1, x2, y2, tolerance=3):
    # Calculate the squared length of the line segment
    lineLengthSquared = (x2 - x1) ** 2 + (y2 - y1) ** 2

    # Handle the case where the segment is a single point
    if lineLengthSquared == 0:
        distance = sqrt((px - x1) ** 2 + (py - y1) ** 2)
        return distance <= tolerance

    # Calculate the projection scalar 't'
    t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / lineLengthSquared

    # Clamp t to the range [0, 1] to restrict to the segment
    t = max(0, min(1, t))

    # Find the projected point on the segment
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)

    # Calculate the distance from the point to the projected point
    distance = sqrt((px - proj_x) ** 2 + (py - proj_y) ** 2)

    # Check if the distance is within the tolerance
    return distance <= tolerance





