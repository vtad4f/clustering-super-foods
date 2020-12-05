

def AverageDeficiency(*clusters):
   """
      BRIEF  If a user picks a random food from each cluster,
             what is the average % daily value of nutrients they are missing?
   """
   deficiencies = list(_AverageDeficiencies(_Totals(clusters)))
   return sum(deficiencies) / len(deficiencies)
   
   
def _AverageDeficiencies(totals):
   """
      BRIEF  The average percent daily value missing
   """
   for total in totals:
      deficiency = 0.0
      for val in total:
         if val < 1.0:
            deficiency += 1.0 - val
      yield deficiency / len(total)
      
      
def _Totals(clusters):
   """
      BRIEF  1. Select one node from each cluster
             2. Yield the sum of values for the selected nodes
             3. Iterate over every possible combination
   """
   vals_per_node = len(clusters[0][0])
   iterator = MultiBaseNumber(*map(len, clusters))
   while iterator:
      total = [0.0]*vals_per_node
      for cluster, node in enumerate(iterator):
         for i, val in enumerate(clusters[cluster][node].vals):
            total[i] += val
      yield total
      iterator += 1
      
      
class MultiBaseNumber(object):
   """
      BRIEF  Every digit in this number has a different base
   """
   
   def __init__(self, *base):
      """
         BRIEF  Cache the bases for each digit and start with a value of 0
      """
      self.value = [0]*len(base)
      self.base = base
      
   def __iadd__(self, value):
      """
         BRIEF  Add the value, then adjust the digits until all values fall
                within acceptable ranges. If the value would completely roll
                over to all 0s, return None instead.
      """
      assert(value > 0) # Only meant to work with positive values
      self.value[-1] += value
      for i, base in reversed(list(enumerate(self.base))):
         while self.value[i] >= base:
            self.value[i] -= base
            if i > 0:
               self.value[i-1] += 1
            else:
               return None
      return self
      
      
   def __iter__(self):
      """
         BRIEF  Allow iteration over the digits
      """
      return iter(self.value)
      
      
   def __repr__(self):
      """
         BRIEF  The value is used as the string representation for the class
      """
      return str(self.value)
      
      
if __name__ == '__main__':
   """
      BRIEF  Test the multi-base number we'll use to iterate over clusters
   """
   import offline
   import gen
   import data
   
   x = MultiBaseNumber(2, 3, 4)
   # x += -1
   while x:
      print(x)
      x += 1
      
   graph = offline.Graph(gen.Read(gen.SUPERFOOD_FILE))
   
   # Do some measuring with the graph divided in half
   half = len(graph.nodes) // 2
   clusters = [graph.nodes[:half], graph.nodes[half:]]
   
   totals = list(_Totals(clusters))
   deficiencies = list(_AverageDeficiencies(totals))
   
   data.PrettyPrint(*totals)
   data.PrettyPrint(*deficiencies)
   data.PrettyPrint(sum(deficiencies) / len(deficiencies))
   data.PrettyPrint(AverageDeficiency(*clusters))
   
   # Do some measuring with the whole graph
   data.PrettyPrint(AverageDeficiency(graph.nodes))
   
   