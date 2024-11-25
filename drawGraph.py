
import graph
import numpy
from stiffnessMatrix import createGlobalMatrix, findDisplacements

graph1 = graph.Graph()
graph1.create(2, 1)
print(f"Created {len(graph1.nodes)} nodes and {len(graph1.connections)} connections")
graph1.visualOutput()

globalMatrix = createGlobalMatrix(graph1)

print(numpy.linalg.det(globalMatrix))

# write 2D array to CSV
numpy.savetxt(
    "stiffness.csv",
    globalMatrix,
    delimiter=","
)


displacements = findDisplacements(graph1, globalMatrix)
numpy.savetxt(
    "displacements.csv",
    displacements,
    delimiter=","
)
