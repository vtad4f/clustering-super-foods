

import csv
import os
import random

NUTRIENTS = ['A', 'B', 'C', 'D', 'E', 'K', 'calcium', 'iodine', 'iron']
PRECISION = 100

def Write(fpath, n_rows):
   """
      BRIEF  Write a csv file with random data
   """
   os.makedirs(os.path.dirname(fpath), exist_ok=True)
   with open(fpath, 'w', newline='') as f:
      writer = csv.DictWriter(f, ['name'] + NUTRIENTS)
      writer.writeheader()
      n_digits = len(str(n_rows-1))
      for i in range(n_rows):
         row = { 'name' : 'food' + str(i).zfill(n_digits) }
         for nutrient in NUTRIENTS:
            row[nutrient] = random.randint(0,PRECISION)/PRECISION
         writer.writerow(row)
         
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   tempfile = 'output/temp.csv'
   Write(tempfile, 500)
   os.remove(tempfile)
   
   