import numpy as np

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

    #add constraints on bottom nodes
    for i in range(size):
        globalMatrix = np.delete(globalMatrix,i*2,axis=0)
        globalMatrix = np.delete(globalMatrix,i*2,axis=1)
        globalMatrix = np.delete(globalMatrix,i*2+1,axis=0)
        globalMatrix = np.delete(globalMatrix,i*2+1,axis=1)

    return globalMatrix

def findDisplacements(graph, stiffness):
    size = int((len(graph.nodes)))
    forces = np.zeros((2 * size,1), dtype=float) #create force vector

    # remove forces on constrained nodes
    for i in range(int(np.sqrt(size)*2)):
        forces = np.delete(forces, i, axis=0)

    for i in range(len(forces)):
        if i % 2 != 0 and i >= (len(forces) - 2 * np.sqrt(size)): #top nodes
            forces[i, 0] = 1
        elif i % 2 != 0 and i <= 2 * np.sqrt(size): #bottom nodes
            forces[i,0] = -1

    displacements = np.linalg.solve(stiffness,forces)

    np.savetxt(
        "stiffness.csv",
        stiffness,
        delimiter=","
    )
    np.savetxt(
        "forces.csv",
        forces,
        delimiter=","
    )
    np.savetxt(
        "displacements.csv",
        displacements,
        delimiter=","
    )

    return displacements