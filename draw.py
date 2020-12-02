

import main
import offline
import gen
import matplotlib.pyplot as plt
import networkx as nx


if __name__ == '__main__':
   """
      BRIEF  Main execution - draw the superfoods graph
   """
   my_g = offline.Graph(gen.Read(main.SUPERFOOD_FILE))
   nx_g = nx.Graph()
   
   for node in my_g.nodes:
      nx_g.add_node(node.name)
      
   for edge in my_g.edges:
      nx_g.add_edge(*edge)
      
   nx.draw_circular(nx_g)
   plt.show()
   
   nx.draw_circular(nx.complement(nx_g))
   plt.show()
   
   