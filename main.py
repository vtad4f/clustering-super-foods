

import gen
import csv


def Read(filepath):
   """
      BRIEF  
   """
   with open(filepath, 'r') as f:
      reader = csv.Reader(f)
      for row in reader:
         yield list(row)
         
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
      self.partition1 = gen.NUTRIENTS + [PROPERTY]
      self.partition2 = []
      
      self.e12 = {}
      for nutrient in gen.NUTRIENTS:
         self.e12[nutrient] = []
      self.e12[PROPERTY] = {}
      
      for row in rows:
         name = row[0]
         
         # Create a node for the food item
         self.partition2.append(name)
         
         # Create an edge if the food provides at least .5 the daily %
         for i, nutrient in enumerate(gen.NUTRIENTS):
            n = float(row[i+1])
            if n >= EDGE_THRESHOLD:
               self.e12[nutrient].append((name, max(0, 1 - n)))
               
         # Always create an edge for the desired property node
         self.e12[PROPERTY][name] = float(row[-1])
         
   def ShortestPath(self, nutrient):
      """
         BRIEF  Calculate the shortest path from the nutrient to the property
      """
      shortest_d = 2 # max distance 1.0 + 1.0
      best_food = None
      
      for food, weight in self.e12[nutrient]:
         distance = weight + self.e12[PROPERTY][food]
         
         if distance < shortest_d:
            shortest_d = distance
            best_food = food
            
      return best_food
      
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   graph = BipartiteGraph(Read(gen.INPUT_FILE))
   shortest_paths = [graph.ShortestPath(nutrient) for nutrient in gen.NUTRIENTS]
   
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
         
   for food in super_food:
      print(food)
      