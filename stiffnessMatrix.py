import numpy as np
import graph


def createGlobalMatrix(graph1):
    globalMatrix = np.zeros((2*len(graph1.nodes), 2*len(graph1.nodes)), dtype=int)

    for edge in graph1.connections:
        deltaX = abs(edge.node1.position[0]-edge.node2.position[0])
        deltaY = abs(edge.node1.position[1] - edge.node2.position[1])
        length = np.sqrt(deltaX**2 + deltaY**2)
        angle = np.arctan2(deltaY, deltaX)
        c = np.cos(angle)
        s = np.sin(angle)
        print(length)
        elementMatrix = [[c**2, c*s,-c**2,-c*s],[c*s,s**2,-c*s,-s**2],[-c**2,-c*s,c**2,c*s],[-c*s,-s**2,c*s,s**2]]
        elementMatrix = np.dot(elementMatrix, 1/length)

        id1 = edge.node1.id
        id2 = edge.node2.id

        globalMatrix[id1 * 2 - 2, id1 * 2 - 2] += elementMatrix[0, 0]
        globalMatrix[id1 * 2 - 2, id1 * 2 - 1] += elementMatrix[0, 1]
        globalMatrix[id1 * 2 - 1, id1 * 2 - 2] += elementMatrix[1, 0]
        globalMatrix[id1 * 2 - 2, id1 * 2 - 2] += elementMatrix[1, 1]

        globalMatrix[id1 * 2 - 2, id2 * 2 - 2] += elementMatrix[0, 2]
        globalMatrix[id1 * 2 - 2, id2 * 2 - 1] += elementMatrix[0, 3]
        globalMatrix[id1 * 2 - 1, id2 * 2 - 2] += elementMatrix[1, 2]
        globalMatrix[id1 * 2 - 2, id2 * 2 - 2] += elementMatrix[1, 3]

        globalMatrix[id2 * 2 - 2, id1 * 2 - 2] += elementMatrix[2, 0]
        globalMatrix[id2 * 2 - 2, id1 * 2 - 1] += elementMatrix[2, 1]
        globalMatrix[id2 * 2 - 1, id1 * 2 - 2] += elementMatrix[3, 0]
        globalMatrix[id2 * 2 - 2, id1 * 2 - 2] += elementMatrix[3, 1]

        globalMatrix[id2 * 2 - 2, id2 * 2 - 2] += elementMatrix[2, 2]
        globalMatrix[id2 * 2 - 2, id2 * 2 - 1] += elementMatrix[2, 3]
        globalMatrix[id2 * 2 - 1, id2 * 2 - 2] += elementMatrix[3, 2]
        globalMatrix[id2 * 2 - 2, id2 * 2 - 2] += elementMatrix[3, 3]

    return globalMatrix
