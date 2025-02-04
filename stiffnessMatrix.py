import numpy as np
from debugpy.adapter.servers import connections


def createGlobalMatrix(graph):
    np.set_printoptions(precision=3, suppress=True)
    globalMatrix = np.zeros((2*len(graph.nodes), 2*len(graph.nodes)), dtype=float)

    for edge in graph.connections:
        if edge.weight <= 0:
            continue

        deltaX = graph.nodes[edge.node1].position[0] - graph.nodes[edge.node2].position[0]
        deltaY = graph.nodes[edge.node1].position[1] - graph.nodes[edge.node2].position[1]
        length = np.sqrt(deltaX**2 + deltaY**2)
        angle = np.arctan2(deltaY, deltaX)
        c = np.cos(angle)
        s = np.sin(angle)

        #create element matrix from angle
        elementMatrix = [[c**2, c*s,-c**2,-c*s]
                        ,[c*s,s**2,-c*s,-s**2],
                         [-c**2,-c*s,c**2,c*s],
                         [-c*s,-s**2,c*s,s**2]]

        elementMatrix = np.dot(elementMatrix, 1/length)

        id1 = edge.node1 * 2
        id2 = edge.node2 * 2

        globalMatrix[id1:id1 + 2, id1:id1 + 2] += elementMatrix[0:2,0:2]
        globalMatrix[id2:id2 + 2, id1:id1 + 2] += elementMatrix[2:4,0:2]
        globalMatrix[id1:id1 + 2, id2:id2 + 2] += elementMatrix[0:2,2:4]
        globalMatrix[id2:id2 + 2, id2:id2 + 2] += elementMatrix[2:4,2:4]

    #add constraints on bottom nodes
    for i in range(graph.width):
        globalMatrix = np.delete(globalMatrix,slice(0,2),axis=0)
        globalMatrix = np.delete(globalMatrix,slice(0,2),axis=1)
    return globalMatrix

def findDisplacements(graph, stiffness):
    size = int(len(graph.nodes))
    forces = np.zeros((2 * size,1), dtype=float) #create force vector

    # remove forces on constrained nodes
    for i in range(graph.width*2):
        forces = np.delete(forces, i, axis=0)

    for i in range(len(forces)):
        if i % 2 != 0 and i > (len(forces) - 2 * graph.width): #top nodes
            forces[i, 0] = 1

    try:
        displacements = np.linalg.solve(stiffness,forces)
        displacements = np.multiply(displacements,0.001)

        for i in range(graph.width*2):
            displacements = np.insert(displacements, 0, 0)

    except np.linalg.linalg.LinAlgError:
        displacements = []
        displacements.append("Stop")

    return displacements


def findLength(graph): #used to find the change in lengths for each connection to modify connection weighting
    lengths = []
    for edge in graph.connections:
        deltaX = graph.nodes[edge.node1].position[0] - graph.nodes[edge.node2].position[0]
        deltaY = graph.nodes[edge.node1].position[1] - graph.nodes[edge.node2].position[1]
        length = np.sqrt(deltaX**2 + deltaY**2)
        lengths.append(length)

    return lengths
