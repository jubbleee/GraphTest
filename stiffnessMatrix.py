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
        elementMatrix = [[c**2, c*s,-c**2,-c*s]
                        ,[c*s,s**2,-c*s,-s**2],
                         [-c**2,-c*s,c**2,c*s],
                         [-c*s,-s**2,c*s,s**2]]

        elementMatrix = np.dot(elementMatrix, 1/length)

        id1 = edge.node1.id * 2
        id2 = edge.node2.id * 2

        globalMatrix[id1:id1 + 2, id1:id1 + 2] += elementMatrix[0:2,0:2]
        globalMatrix[id2:id2 + 2, id1:id1 + 2] += elementMatrix[2:4,0:2]
        globalMatrix[id1:id1 + 2, id2:id2 + 2] += elementMatrix[0:2,2:4]
        globalMatrix[id2:id2 + 2, id2:id2 + 2] += elementMatrix[2:4,2:4]

    #add constraints on bottom nodes
    for i in range(size):
        globalMatrix = np.delete(globalMatrix,slice(i*2,i*2+2),axis=0)
        globalMatrix = np.delete(globalMatrix,slice(i*2,i*2+2),axis=1)


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
        #elif i % 2 != 0 and i <= 2 * np.sqrt(size): #bottom nodes
        #   forces[i,0] = -1

    try:
        displacements = np.linalg.solve(stiffness,forces)
        displacements = np.multiply(displacements,0.01)

    except np.linalg.linalg.LinAlgError:
        displacements = []
        displacements.append("Stop")

    return displacements

''' debug file creator
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
'''

def findLength(graph):
    lengths = []
    for edge in graph.connections:

        '''
        find length of connection and angle to the x-axis
        this is used to create the element stiffness matrix
        '''

        deltaX = edge.node1.position[0] - edge.node2.position[0]
        deltaY = edge.node1.position[1] - edge.node2.position[1]
        length = np.sqrt(deltaX**2 + deltaY**2)
        lengths.append(length)

    return lengths