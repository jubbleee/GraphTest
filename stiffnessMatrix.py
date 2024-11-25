import numpy as np
from networkx.classes import nodes
import graph


def createGlobalMatrix(graph):
    globalMatrix = np.zeros((2*len(graph.nodes), 2*len(graph.nodes)), dtype=float)
    size = int(np.sqrt(len(graph.nodes)))

    for edge in graph.connections:

        '''
        find length of connection and angle to the x-axis
        this is used to create the element stiffness matrix
        '''

        deltaX = edge.node1.position[0] - edge.node2.position[0]
        deltaY = edge.node1.position[1] - edge.node2.position[1]
        length = np.sqrt(deltaX**2 + deltaY**2)
        angle = np.arctan2(deltaY, deltaX)
        c = np.cos(angle)
        s = np.sin(angle)

        #create element matrix from angle
        elementMatrix = [[c**2, c*s,-c**2,-c*s],[c*s,s**2,-c*s,-s**2],[-c**2,-c*s,c**2,c*s],[-c*s,-s**2,c*s,s**2]]
        elementMatrix = np.dot(elementMatrix, 1/length)

        id1 = edge.node1.id
        id2 = edge.node2.id

        '''
        append each part of element matrix to respective nodes
        id*2 - 2 finds correct index for corresponding node
        the global matrix is size 2N*2N
        '''

        globalMatrix[id1 * 2:id1 * 2 + 2, id1 * 2:id1 * 2 + 2] += elementMatrix[0:2,0:2]
        globalMatrix[id2 * 2:id2 * 2 + 2, id1 * 2:id1 * 2 + 2] += elementMatrix[2:4,0:2]
        globalMatrix[id1 * 2:id1 * 2 + 2, id2 * 2:id2 * 2 + 2] += elementMatrix[0:2,2:4]
        globalMatrix[id2 * 2:id2 * 2 + 2, id2 * 2:id2 * 2 + 2] += elementMatrix[2:4,2:4]
        
        #globalMatrix[id1 * 2 - 2, id1 * 2 - 2] += elementMatrix[0, 0]
        #globalMatrix[id1 * 2 - 2, id1 * 2 - 1] += elementMatrix[0, 1]
        #globalMatrix[id1 * 2 - 1, id1 * 2 - 2] += elementMatrix[1, 0]
        #globalMatrix[id1 * 2 - 2, id1 * 2 - 2] += elementMatrix[1, 1]

        #globalMatrix[id1 * 2 - 2, id2 * 2 - 2] += elementMatrix[0, 2]
        #globalMatrix[id1 * 2 - 2, id2 * 2 - 1] += elementMatrix[0, 3]
        #globalMatrix[id1 * 2 - 1, id2 * 2 - 2] += elementMatrix[1, 2]
        #globalMatrix[id1 * 2 - 2, id2 * 2 - 2] += elementMatrix[1, 3]

        #globalMatrix[id2 * 2 - 2, id1 * 2 - 2] += elementMatrix[2, 0]
        #globalMatrix[id2 * 2 - 2, id1 * 2 - 1] += elementMatrix[2, 1]
        #globalMatrix[id2 * 2 - 1, id1 * 2 - 2] += elementMatrix[3, 0]
        #globalMatrix[id2 * 2 - 2, id1 * 2 - 2] += elementMatrix[3, 1]

        #globalMatrix[id2 * 2 - 2, id2 * 2 - 2] += elementMatrix[2, 2]
        #globalMatrix[id2 * 2 - 2, id2 * 2 - 1] += elementMatrix[2, 3]
        #globalMatrix[id2 * 2 - 1, id2 * 2 - 2] += elementMatrix[3, 2]
        #globalMatrix[id2 * 2 - 2, id2 * 2 - 2] += elementMatrix[3, 3]

    #add constraints on bottom nodes 
    for i in (0,1):
        globalMatrix = np.delete(globalMatrix,i*2,axis=0)
        globalMatrix = np.delete(globalMatrix,i*2,axis=1)
        globalMatrix = np.delete(globalMatrix,i*2+1,axis=0)
        globalMatrix = np.delete(globalMatrix,i*2+1,axis=1)
    #for i in range(size):
    #    globalMatrix[2 * i - 1, :] = 0
    #    globalMatrix[2 * i - 2, :] = 0
    #    globalMatrix[:, 2 * i - 1] = 0
    #    globalMatrix[:, 2 * i - 2] = 0

    #globalMatrix = np.tril(globalMatrix) #remove top diagonal to remove repeat values

    return globalMatrix

def findDisplacements(graph, stiffness):
    size = int((len(graph.nodes)))
    forces = np.zeros((2 * size,1), dtype=int) #create force vector

    for i in range(2*size): #fill force vector to apply pulling force on top nodes
        if i > 2 * size - 2 * np.sqrt(size) and i % 2 != 0:
            forces[i,0] = 1.
        if i < 4 and i % 2 != 0:
            forces[i,0] = -1.
    #remove forces on constrained nodes 
    for i in (0,1):
        forces = np.delete(forces,i*2,axis=0)
        forces = np.delete(forces,i*2+1,axis=0)

    np.savetxt(
        "forces.csv",
        forces,
        delimiter=","
    )

    displacements = np.linalg.solve(stiffness,forces)
    return displacements