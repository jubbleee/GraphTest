import matplotlib.pyplot as plt
import math
import numpy as np

# Your provided classes
class Connection:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.weight = 1
        self.decay = 100
        self.failed = False


class Node:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.count = 0


class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary of nodes, keyed by ID
        self.connections = []  # List of Connection objects

    def addNode(self, node):
        self.nodes[node.id] = node

    def addConnection(self, connection):
        self.connections.append(connection)

    def visualize(self):
        plt.figure(figsize=(10, 8))

        # Plot nodes
        for node in self.nodes.values():
            x, y = node.position
            plt.scatter(x, y, color="skyblue", s=300, zorder=2)
            plt.text(x, y, f"{node.id}", fontsize=12, ha="center", va="center", zorder=3)

        # Plot connections
        for con in self.connections:
            x1, y1 = self.nodes[con.node1].position
            x2, y2 = self.nodes[con.node2].position
            plt.plot([x1, x2], [y1, y2], color="gray", zorder=1)

        plt.title("Triangular Lattice Graph")
        plt.axis("equal")
        plt.show()


# Create the triangular lattice graph
def createLattice(graph, spacing=1):
    '''
            3       4
          /   \   /   \
         0______1______2
    '''

    node0 = Node(0,(0,0))
    node1 = Node(1, (1, 0))
    node2 = Node(2, (2, 0))
    node3 = Node(3, (0.5, math.sin(math.radians(60))))
    node4 = Node(4, (1.5, math.sin(math.radians(60))))

    graph.addNode(node0)
    graph.addNode(node1)
    graph.addNode(node2)
    graph.addNode(node3)
    graph.addNode(node4)

    # Create connections
    graph.addConnection(Connection(0, 1))
    graph.addConnection(Connection(0, 3))
    graph.addConnection(Connection(1, 2))
    graph.addConnection(Connection(1, 3))
    graph.addConnection(Connection(1, 4))
    graph.addConnection(Connection(2, 4))
    graph.addConnection(Connection(3, 4))

def createGlobalMatrix(graph):
    # Initialize the global stiffness matrix
    globalMatrix = np.zeros((2 * len(graph.nodes), 2 * len(graph.nodes)), dtype=float)

    # Loop connections and find element matrix
    for edge in graph.connections:
        deltaX = graph.nodes[edge.node1].position[0] - graph.nodes[edge.node2].position[0]
        deltaY = graph.nodes[edge.node1].position[1] - graph.nodes[edge.node2].position[1]
        length = np.sqrt(deltaX**2 + deltaY**2)
        angle = np.arctan2(deltaY, deltaX)
        c = np.cos(angle)
        s = np.sin(angle)

        # Create element stiffness matrix
        stiffness = 1 / length
        elementMatrix = stiffness * np.array([
            [ c**2,  c*s, -c**2, -c*s],
            [ c*s,  s**2, -c*s, -s**2],
            [-c**2, -c*s,  c**2,  c*s],
            [-c*s, -s**2,  c*s,  s**2]
        ])

        # Map the element matrix to the global matrix
        id1 = edge.node1 * 2
        id2 = edge.node2 * 2

        globalMatrix[id1:id1 + 2, id1:id1 + 2] += elementMatrix[0:2, 0:2]
        globalMatrix[id2:id2 + 2, id1:id1 + 2] += elementMatrix[2:4, 0:2]
        globalMatrix[id1:id1 + 2, id2:id2 + 2] += elementMatrix[0:2, 2:4]
        globalMatrix[id2:id2 + 2, id2:id2 + 2] += elementMatrix[2:4, 2:4]


    print(globalMatrix)

    globalMatrix = np.delete(globalMatrix, slice(0,6) , axis=0)
    globalMatrix = np.delete(globalMatrix, slice(0,6) , axis=1)
    #globalMatrix = np.delete(globalMatrix, 1, axis=0)
    #globalMatrix = np.delete(globalMatrix, 1, axis=1)

    return globalMatrix

def computeDisplacements(graph):
    globalMatrix = createGlobalMatrix(graph)

    print(globalMatrix)

    #forces = [0,0,0,0,0,1]
    forces = [0,1,0,1]
    displacements = np.linalg.solve(globalMatrix, forces)
    print(np.linalg.det(globalMatrix))

    displacements = np.insert(displacements, 0, [0,0,0,0,0,0])

    for node in graph.nodes:
        print(f"Node {node}: Displacement (u_x, u_y) = ({displacements[2 * node]:.4f}, {displacements[2 * node + 1]:.4f})")



# Main execution
np.set_printoptions(precision=3, suppress=True)

graph = Graph()
createLattice(graph, spacing=1)
graph.visualize()

computeDisplacements(graph)





