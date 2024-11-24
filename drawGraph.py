
import graph
import numpy
import stiffnessMatrix
from stiffnessMatrix import createGlobalMatrix

graph1 = graph.Graph()
graph1.create(2, 1)
print(f"Created {len(graph1.nodes)} nodes and {len(graph1.connections)} connections in a {10}x{10} lattice.")
graph1.visualOutput()

globalMatrix = createGlobalMatrix(graph1)
# create 2D array

# write 2D array to CSV
numpy.savetxt(
    "merry.csv",
    globalMatrix,
    delimiter=","
)
