import tkinter as tk
import random
from math import sqrt


class GraphEditor:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()
        self.nodePos = {}  # {node_id: (x, y)}
        self.edgeLines = {}  # {connection: connectID}
        self.scaleFactor = None
        self.drawGraph()
        self.canvas.bind("<Button-1>", self.onClick)

    def calculateScale(self):
        """Calculate the scaling factor to fit the graph within the canvas."""
        maxX = max(node.position[0] for node in self.graph.nodes.values())
        maxY = max(node.position[1] for node in self.graph.nodes.values())
        # Calculate scaling factors for both dimensions and take the smaller one
        scaleX = (600 - 100) / (maxX + 1)  # Leave padding
        scaleY = (600 - 100) / (maxY + 1)  # Leave padding
        self.scaleFactor = min(scaleX, scaleY)

    def drawGraph(self):
        #Draw the nodes and connections.
        self.canvas.delete("all")
        self.nodePos.clear()
        self.edgeLines.clear()

        self.calculateScale()

        # Map node positions for visualization
        for node in self.graph.nodes.values():
            x, y = node.position
            x = x * self.scaleFactor + 50  # Apply scaling and offset for padding
            y = y * self.scaleFactor + 50
            self.nodePos[node.id] = (x, y)

        # Draw connections (edges)
        for connection in self.graph.connections:
            x1, y1 = self.nodePos[connection.node1.id]
            x2, y2 = self.nodePos[connection.node2.id]
            connectID = self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            self.edgeLines[connection] = connectID

        # Draw nodes
        for node_id, (x, y) in self.nodePos.items():
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="skyblue", outline="black", width=2)
            self.canvas.create_text(x, y, text=str(node_id), font=("Arial", 10))

    def onClick(self, event):
        #Handle mouse clicks to detect and remove connections.
        clicked = self.conFind(event.x, event.y)
        if clicked:
            self.conRemove(clicked)

    def conFind(self, x, y):
        #Find the connection closest to the click coordinates.
        for connection, connectID in self.edgeLines.items():
            coords = self.canvas.coords(connectID)  # [x1, y1, x2, y2]
            if nearLine(x, y, *coords):
                return connection
        return None

    def conRemove(self, connection):
        # Remove the connection and update the graph.
        self.graph.connections.remove(connection)  # Remove from data
        self.canvas.delete(self.edgeLines[connection])  # Remove from canvas
        del self.edgeLines[connection]  # Remove from internal mapping

def nearLine(px, py, x1, y1, x2, y2, tolerance=3):
    """
    Check if a click (px, py) is near a finite line segment (x1, y1, x2, y2)
    within a given tolerance.
    """
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





