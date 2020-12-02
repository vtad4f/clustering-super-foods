

import offline
import online
import gen
import data
import itertools


SUPERFOOD_FILE = 'output/superfood.csv'
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
   gen.Write(rows, SUPERFOOD_FILE)
   
   
if __name__ == '__main__':
   """
      BRIEF  Main execution - filter the input data to 
   """
   superfood = itertools.chain.from_iterable(online.BipartiteGraph(food).Filter() for food in ReadInChunks())
   WriteFilteredOutput(superfood)
   gen.PrettyPrint(SUPERFOOD_FILE, "Behold the super-foods! These high-nutrient foods have been selected from {0} for your convenience.".format(gen.INPUT_FILE))
   
   offline.Graph(gen.Read(SUPERFOOD_FILE))