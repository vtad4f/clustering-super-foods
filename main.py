

import measure
import offline
import online
import gen
import data
import itertools


NUM_FILTERS = 5


def ReadInChunks():
   """
      BRIEF  Potentially parse the data in chunks. Ideally this would be
             parallelized, but the following code is a proof of concept.
   """
   food = gen.Read(gen.INPUT_FILE)
   if NUM_FILTERS > 1:
      food = list(food)
      chunk_size = len(food) // NUM_FILTERS
      for i in range(NUM_FILTERS):
         yield food[i*chunk_size:(i+1)*chunk_size]
   else:
      yield food
      
      
def WriteFilteredOutput(superfood):
   """
      BRIEF  Record the superfood as its own file
   """
   names = set(superfood)
   rows = []
   for row in gen.Read(gen.INPUT_FILE):
      if row[data.NAME_COL_INDEX] in names:
         rows.append({col:row[i] for i, col in enumerate(data.ALL_COLS)})
   gen.Write(rows, gen.SUPERFOOD_FILE)
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution - filter the input data to 
   """
   superfood = itertools.chain.from_iterable(online.BipartiteGraph(food).Filter() for food in ReadInChunks())
   WriteFilteredOutput(superfood)
   data.PrintBanner('-', "High-nutrient [super]foods filtered from {0}".format(gen.INPUT_FILE))
   gen.PrettyPrint(gen.SUPERFOOD_FILE)
   
   graph = offline.Graph(gen.Read(gen.SUPERFOOD_FILE), offline.EuclideanDistance)
   max_n_clusters = 5
   n_runs = 5
   
   for cluster_fcn, measure_fcns in [
      [offline.Random, [measure.Deficiency]]
   ]:
      data.PrintBanner('-', 'Clustering - {0} {1}'.format(cluster_fcn.__name__, data.PrettyString([func.__name__ for func in offline.FCNS])))
      data.PrettyPrint(*graph.Cluster(max_n_clusters, n_runs, cluster_fcn, *measure_fcns))
      
      