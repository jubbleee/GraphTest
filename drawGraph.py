import matplotlib.pyplot as plt
import numpy
import graph
from stiffnessMatrix import createGlobalMatrix, findDisplacements

def iterate():
    globalMatrix = createGlobalMatrix(graph1)
    displacements = findDisplacements(graph1, globalMatrix)
    graph1.moveNodes(displacements)
    graph1.visualOutput()


graph1 = graph.Graph()
graph1.create(5, 1)
print(f"Created {len(graph1.nodes)} nodes and {len(graph1.connections)} connections")

graph1.visualOutput()

iterate()





