

import gen
import online


if __name__ == '__main__':
   """
      BRIEF  Main execution - filter the input data to 
   """
   for food in online.BipartiteGraph(gen.Read()).Filter():
      print(food)
      
      