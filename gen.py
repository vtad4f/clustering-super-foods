

import csv
import os
import random

INPUT_FILE = 'input/food.csv'
N_ROWS = 500

NAME = 'name'
NUTRIENTS = ['A', 'B', 'C', 'D', 'E', 'K', 'calcium', 'iodine', 'iron']
PROPERTY = 'calories'
PRECISION = 100


def Write(fpath, n_rows):
   """
      BRIEF  Write a csv file with random data
   """
   os.makedirs(os.path.dirname(fpath), exist_ok=True)
   with open(fpath, 'w', newline='') as f:
      writer = csv.DictWriter(f, [NAME] + NUTRIENTS + [PROPERTY])
      writer.writeheader()
      n_digits = len(str(n_rows-1))
      for i in range(n_rows):
         row = { NAME : 'food' + str(i).zfill(n_digits) }
         for nutrient in NUTRIENTS:
            row[nutrient] = random.randint(0,PRECISION)/PRECISION
         writer.writerow(row)
         
if __name__ == '__main__':
   """
      BRIEF  Main execution
   """
   gen.Write(INPUT_FILE, N_ROWS)
   
   