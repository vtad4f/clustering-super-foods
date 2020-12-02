

import data


class Node(object):
   """
      BRIEF  A data container, used to represent a single food item
   """
   
   def __init__(self, row):
      """
         BRIEF  Cache the data
      """
      self.name = row[data.NAME_COL_INDEX]
      self.vals = list(map(float, row[data.NAME_COL_INDEX+1:data.PROP_COL_INDEX]))
      self.prop = float(row[data.PROP_COL_INDEX])
      
      
   def Distance(self, other):
      """
         BRIEF  Get the euclidean distance between the nodes w/ normalized values
                The maximum possible value returned here is 3
                  1.0 max distance per value, squared is still 1.0
                  9 values
                  sqrt(9) = 3
      """
      return sum((v1-v2)**2 for (v1,v2) in zip(self.vals, other.vals)) ** .5
      
      
   def __hash__(self):
      """
         BRIEF  Used as a 'unique' ID when storing an instance of this class
      """
      return hash(self.name)
      
      
class Graph(object):
   """
      BRIEF  This graph will be used for clustering
   """
   EDGE_THRESHOLD = 1.5
   
   def __init__(self, rows):
      """
         BRIEF  Cache nodes and edges for each row
      """
      self.nodes = []
      self.edges = set()
      self.distance = {}
      for row in rows:
         new = Node(row)
         for existing in self.nodes:
            distance = new.Distance(existing)
            pair_id = frozenset((new, existing))
            if distance < Graph.EDGE_THRESHOLD:
               self.edges.add(pair_id)
            self.distance[pair_id] = new.Distance(existing)
         self.nodes.append(new)
         