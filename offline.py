

import data
import random


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
      
      
   def __getitem__(self, i):
      """
         BRIEF  Provide access to the values
      """
      return self.vals[i]
      
      
   def __len__(self):
      """
         BRIEF  Provide access to the number of values
      """
      return len(self.vals)
      
      
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
            pair_id = frozenset((new.name, existing.name))
            if distance < Graph.EDGE_THRESHOLD:
               self.edges.add(pair_id)
            self.distance[pair_id] = new.Distance(existing)
         self.nodes.append(new)
         
         
   def Cluster(self, max_n_clusters, n_runs, cluster_fcn, *measure_fcns):
      """
         BRIEF  Average metrics across every run, for each number of clusters
      """
      assert(max_n_clusters >= 2)
      assert(n_runs >= 1)
      
      all_results = [[[] for _ in range(len(measure_fcns))] for __ in range(max_n_clusters-1)]
      for _ in range(n_runs):
         for n_clusters in range(2, max_n_clusters + 1):
            clusters = cluster_fcn(self, n_clusters)
            for i, fcn in enumerate(measure_fcns):
               all_results[n_clusters-2][i].append(fcn(*clusters))
               
      yield ['n_clusters'] + [fcn.__name__ for fcn in measure_fcns]
      yield [1] + [fcn(self.nodes) for fcn in measure_fcns] # 1 cluster = the whole graph
      for i, results_for_n_clusters in enumerate(all_results):
         yield [i+2] + [(sum(results) / len(results)) for results in results_for_n_clusters] # Average over all the runs
         
         
def Random(graph, n_clusters):
   """
      BRIEF  This will randomly slice the graph into some number of clusters
             of mostly equal size. The last cluster(s) will be smaller if the
             nodes can't be divided evenly.
   """
   assert(n_clusters > 0)
   
   node_indices = list(range(len(graph.nodes)))
   random.shuffle(node_indices)
   
   chunk_size = 1 + len(graph.nodes) // n_clusters
   for i in range(n_clusters):
      yield [graph.nodes[i] for i in node_indices[i*chunk_size:(i+1)*chunk_size]]
      
      