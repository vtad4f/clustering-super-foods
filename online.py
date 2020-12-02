

import data


class BipartiteGraph(object):
   """
      BRIEF  This graph will be used as a filter
   """
   EDGE_THRESHOLD = .5
   
   def __init__(self, rows):
      """
         BRIEF  Cache nodes and edges for each row
      """
      
      # Create nodes for the nutrients and the desired property
      self.partition1 = data.NUTRIENTS + [data.PROPERTY]
      self.partition2 = []
      
      self.e12 = {}
      for nutrient in data.NUTRIENTS:
         self.e12[nutrient] = []
      self.e12[data.PROPERTY] = {}
      
      for row in rows:
         name = row[data.NAME_COL_INDEX]
         
         # Create a node for the food item
         self.partition2.append(name)
         
         # Create an edge if the food provides at least .5 the daily %
         for i, nutrient in enumerate(data.NUTRIENTS):
            n = float(row[i+1])
            if n >= BipartiteGraph.EDGE_THRESHOLD:
               self.e12[nutrient].append((name, max(0, 1 - n)))
               
         # Always create an edge for the desired property node
         self.e12[data.PROPERTY][name] = float(row[data.PROP_COL_INDEX])
         
         
   def Filter(self):
      """
         BRIEF  Use shortest path and betweenness centrality calculations to
                find the super foods in the data
      """
      shortest_paths = [self.ShortestPath(nutrient) for nutrient in data.NUTRIENTS]
      
      betweenness_centrality = {}
      for food in shortest_paths:
         if not food is None:
            if not food in betweenness_centrality:
               betweenness_centrality[food] = 0
            betweenness_centrality[food] += 1
            
      max_bc = 0
      super_food = []
      for food, bc in betweenness_centrality.items():
         if bc > max_bc:
            max_bc = bc
            super_food = [food]
         elif bc == max_bc:
            super_food.append(food)
            
      for food in sorted(super_food):
         yield food
         
         
   def ShortestPath(self, nutrient):
      """
         BRIEF  Calculate the shortest path from the nutrient to the property
      """
      shortest_d = 2 # max distance 1.0 + 1.0
      best_food = None
      
      for food, weight in self.e12[nutrient]:
         distance = weight + self.e12[data.PROPERTY][food]
         
         if distance < shortest_d:
            shortest_d = distance
            best_food = food
            
      return best_food
      
      