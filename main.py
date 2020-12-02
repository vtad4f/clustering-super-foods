

import gen
import online


NUM_FILTERS = 10


def Read():
   """
      BRIEF  Potentially parse the data in chunks. Ideally this would be
             parallelized, but the following code is a proof of concept.
   """
   food_data = gen.Read()
   if NUM_FILTERS > 1:
      food_data = list(food_data)
      chunk_size = len(food_data) // NUM_FILTERS
      for i in range(NUM_FILTERS):
         yield food_data[i*chunk_size:(i+1)*chunk_size]
   else:
      yield food_data
      
      
if __name__ == '__main__':
   """
      BRIEF  Main execution - filter the input data to 
   """
   for food_data in Read():
      print()
      for food in online.BipartiteGraph(food_data).Filter():
         print(food)
         
         