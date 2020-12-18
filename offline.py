

import data
import sklearn.cluster as sk
import random


def Avg(vals):
   """
      BRIEF  Get the average of the set of values
   """
   return sum(vals) / len(vals)
   
   
def StdDev(vals):
   """
      BRIEF  Get the standard deviation of the set of values
   """
   avg = Avg(vals)
   return (sum((val-avg)**2 for val in vals) / len(vals)) ** .5

   
EVAL_FCNS = [Avg, StdDev]


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
      
      
class Euclidean:
   def Distance(n1_vals, n2_vals):
      """
         BRIEF  Get the euclidean distance between the nodes w/ normalized values
                The maximum possible value returned here is 3
                  1.0 max distance per value, squared is still 1.0
                  9 values
                  sqrt(9) = 3
      """
      return sum((v1-v2)**2 for (v1,v2) in zip(n1_vals, n2_vals)) ** .5
      
   MAX_DISTANCE = Distance(Node([0.0]*len(data.ALL_COLS)), Node([1.0]*len(data.ALL_COLS)))
   
   
class Graph(object):
   """
      BRIEF  This graph will be used for clustering
   """
   
   def __init__(self, rows):
      """
         BRIEF  For now just create one node for each row
      """
      nodes = [Node(row) for row in rows]
      self.nodes    = {node.name:node for node in nodes}
      self.edges    = {}
      self.degrees  = {}
      self.adj_list = {}
      
      
   def SetEdges(self, distance_type, percent_threshold):
      """
         BRIEF  Create edges between similar nodes
         
         PARAM distance_type  Is a class with a Distance() method and a
                              MAX_DISTANCE value
         
         PARAM percent_threshold  A percent value [0.0, 1.0] of the maximum
                                  possible distance
      """
      self.edges.clear()
      
      # Iterate over all the nodes
      nodes = list(self.nodes.values())
      for i in range(len(nodes)):
         for j in range(i+1, len(nodes)):
            n1, n2 = nodes[i], nodes[j]
            
            # Calculate distances
            distance = distance_type.Distance(n1, n2)
            if distance < distance_type.MAX_DISTANCE * percent_threshold:
               
               # Create edges if the nodes are similar
               self.edges[frozenset((n1.name, n2.name))] = distance
               
      # Reset degrees for the new edges
      self.degrees = {name:0 for name in self.nodes}
      for (n1, n2) in self.edges:
         self.degrees[n1] += 1
         self.degrees[n2] += 1
         
      # Reset adjacency list for the new edges
      self.adj_list = {name:set() for name in self.nodes}
      for (n1, n2) in self.edges:
         self.adj_list[n1].add(n2)
         self.adj_list[n2].add(n1)
         
         
   def BFS(self, root, limit = 0):
      """
         BRIEF  Search using Breadth First Search, starting at 'node'
      """
      visited = set()
      unvisited = [root]
      
      while unvisited and (not limit or len(visited) < limit):
         
         # Access the next node
         node = unvisited.pop(0)
         yield self.nodes[node]
         visited.add(node)
         
         # Append its neighbors to the queue
         for neighbor in self.adj_list[node]:
            if not neighbor in visited:
               unvisited.append(neighbor)
               
               
   def Cluster(self, range_n_clusters, n_runs, cluster_fcn, *measure_fcns):
      """
         BRIEF  Average metrics across every run, for each number of clusters
      """
      min_n_clusters, max_n_clusters = range_n_clusters
      assert(max_n_clusters >= 2)
      assert(min_n_clusters <= max_n_clusters)
      assert(n_runs >= 1)
      
      yield ['n_clusters'] + [fcn.__name__ for fcn in measure_fcns]
      if min_n_clusters <= 1:
         min_n_clusters += 1
         yield [1] + [[fcn(list(self.nodes.values())), 0.0] for fcn in measure_fcns] # 1 cluster = the whole graph
         
      all_results = [[[] for _ in range(len(measure_fcns))] for __ in range(max_n_clusters-1)]
      for _ in range(n_runs):
         for n_clusters in range(min_n_clusters, max_n_clusters + 1):
            clusters = cluster_fcn(self, n_clusters)
            for i, fcn in enumerate(measure_fcns):
               all_results[n_clusters-min_n_clusters][i].append(fcn(*clusters))
               
      for i, per_clusters_n in enumerate(all_results):
         yield [i+min_n_clusters] + [[fcn(results) for fcn in EVAL_FCNS] for results in per_clusters_n]
         
         
def RandomClustering(graph, n_clusters):
   """
      BRIEF  This will randomly slice the graph into some number of clusters
             of mostly equal size. The last cluster(s) will be smaller if the
             nodes can't be divided evenly.
   """
   names = list(graph.nodes.keys())
   node_indices = list(range(len(names)))
   random.shuffle(node_indices)
   
   chunk_size = 1 + len(names) // n_clusters
   for i in range(n_clusters):
      yield [graph.nodes[names[i]] for i in node_indices[i*chunk_size:(i+1)*chunk_size]]
      
      
def KMeansClustering(graph, n_clusters):
   """
      BRIEF  Use the sklearn package to attempt KMeans clustering
   """
   clusters = [[] for _ in range(n_clusters)]
   kmeans = sk.KMeans(n_clusters).fit([node.vals for node in graph.nodes.values()])
   for node in graph.nodes.values():
      distances = [Euclidean.Distance(node.vals, center) for center in kmeans.cluster_centers_]
      clusters[distances.index(min(distances))].append(node)
   return clusters
   
   
def SpectralClustering(graph, n_clusters):
   """
      BRIEF  Use the sklearn package to attempt Spectral clustering
   """
   clusters = [[] for _ in range(n_clusters)]
   names = list(graph.nodes.keys())
   spectral = sk.SpectralClustering(n_clusters, assign_labels='discretize').fit([graph.nodes[name].vals for name in names])
   for i, cluster_i in enumerate(spectral.labels_):
      clusters[cluster_i].append(graph.nodes[names[i]])
   return clusters
   
   
def GraphClustering1(graph, *args):
   """
      BRIEF  A very simple approach: cherry-pick the nodes with high degrees
   """
   clusters = [[], []]
   for degree, name in sorted([(d,n) for n,d in graph.degrees.items()]):
      if len(clusters[0]) < len(graph.nodes) // 2:
         clusters[0].append(graph.nodes[name])
      else:
         clusters[1].append(graph.nodes[name])
   return clusters
   
   
def GraphClustering2(graph, *args):
   """
      BRIEF  Start with the node with highest degree and expand outwards with BFS
   """
   clusters = [[], []]
   maxdegree, name = sorted([(d,n) for n,d in graph.degrees.items()])[-1]
   clusters[0].extend(graph.BFS(name, len(graph.nodes) // 2))
   remaining = set(graph.nodes.keys()) - set([n.name for n in clusters[0]])
   clusters[1].extend([graph.nodes[n] for n in remaining])
   return clusters
   
   