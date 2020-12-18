

import offline
import gen
import matplotlib.pyplot as plt
import networkx as nx
import sys


def DrawDenseGraph(graph):
   """
      BRIEF  When the graph is dense, circular is the way to go
   """
   nx_graph = NetworkXGraph(graph)
   nx.draw_circular(nx_graph)
   plt.show()
   
   complement = nx.complement(nx_graph)
   nx.draw_circular(complement)
   plt.show()
   
   print('{0:<10} = {1}'.format('e(G)' , nx_graph.size()))
   print('{0:<10} = {1}'.format('e(~G)', complement.size()))
   sys.stdout.flush()
   
   
def DrawSparseGraph(graph):
   """
      BRIEF  Use spring for drawing a sparse graph
   """
   nx_graph = NetworkXGraph(graph)
   nx.draw_spring(nx_graph)
   plt.show()
   
   
def NetworkXGraph(graph):
   """
      BRIEF  We'll always use this code to create a NetworkX graph
   """
   nx_graph = nx.Graph()
   
   for name in graph.nodes:
      nx_graph.add_node(name)
      
   for edge in graph.edges:
      nx_graph.add_edge(*edge)
      
   return nx_graph
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution - draw the superfoods graph
   """
   graph = offline.Graph(gen.Read(gen.SUPERFOOD_FILE))
   
   graph.SetEdges(offline.Euclidean, .5)
   DrawDenseGraph(graph)
   
   graph.SetEdges(offline.Euclidean, .3)
   DrawSparseGraph(graph)
   
   