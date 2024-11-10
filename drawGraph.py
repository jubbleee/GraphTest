
import graph

graph1 = graph.Graph()
graph1.create(15, 0)
print(f"Created {len(graph1.nodes)} nodes and {len(graph1.connections)} connections in a {10}x{10} lattice.")
graph1.visualOutput()

graph2 = graph.Graph()
graph2.create(15, 1)
print(f"Created {len(graph2.nodes)} nodes and {len(graph2.connections)} connections in a {10}x{10} lattice.")
graph2.visualOutput()