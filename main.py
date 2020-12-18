

import measure
import offline
import online
import preprocess
import gen
import data
import itertools
import os


NUM_FILTERS = 5


def ReadInChunks(fpath):
   """
      BRIEF  Potentially parse the data in chunks. Ideally this would be
             parallelized, but the following code is a proof of concept.
   """
   food = list(gen.Read(fpath))
   chunk_size = 1 + len(food) // NUM_FILTERS
   for i in range(NUM_FILTERS):
      yield food[i*chunk_size:(i+1)*chunk_size]
      
      
def WriteFilteredOutput(superfood, all_rows):
   """
      BRIEF  Record the superfood as its own file
   """
   names = set(superfood)
   rows = []
   for row in all_rows:
      if row[data.NAME_COL_INDEX] in names:
         rows.append({col:row[i] for i, col in enumerate(data.ALL_COLS)})
   gen.Write(rows, gen.SUPERFOOD_FILE)
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution - filter the input data to 
   """
   import argparse
   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group(required=True)
   group.add_argument("-r", "--random", action="store_true", help="Use random data")
   group.add_argument("-m", "--male"  , action="store_true", help="Use adult male data")
   group.add_argument("-f", "--female", action="store_true", help="Use adult male data")
   args = parser.parse_args()
   
   # Generate random data if not 
   if args.random:
      if not os.path.isfile(gen.INPUT_FILE):
         gen.Main()
      fpath = gen.INPUT_FILE
      
   if args.male:
      if not os.path.isfile(preprocess.AdultMale.FILE):
         preprocess.Main()
      fpath = preprocess.AdultMale.FILE
      
   if args.female:
      if not os.path.isfile(preprocess.AdultFemale.FILE):
         preprocess.Main()
      fpath = preprocess.AdultFemale.FILE
      
   # Run the online (filtering) algorithm
   superfood = itertools.chain.from_iterable(online.BipartiteGraph(food).Filter() for food in ReadInChunks(fpath))
   WriteFilteredOutput(superfood, gen.Read(fpath))
   data.PrintBanner('-', "High-nutrient [super]foods filtered from {0}".format(gen.INPUT_FILE))
   gen.PrettyPrint(gen.SUPERFOOD_FILE)
   
   # Run the offline (clustering) algorithms
   graph = offline.Graph(gen.Read(gen.SUPERFOOD_FILE))
   graph.SetEdges(offline.Euclidean, .3)
   
   for cluster_fcn, range_n_clusters, n_runs in [
      (offline.RandomClustering,  (1, 5), 5),
      (offline.KMeansClustering,  (2, 5), 5),
      (offline.SpectralClustering,(2, 5), 5),
      (offline.GraphClustering1,  (2, 2), 5),
      (offline.GraphClustering2,  (2, 2), 5)
   ]:
      data.PrintBanner('-', '{0}, {1} run(s) {2}'.format(*map(data.PrettyString, [cluster_fcn, n_runs, offline.EVAL_FCNS])))
      data.PrettyPrint(*graph.Cluster(range_n_clusters, n_runs, cluster_fcn, measure.Deficiency))
      
      